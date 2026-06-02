from __future__ import annotations

import importlib.util
import json
import sys
import types
from argparse import Namespace
from pathlib import Path
from typing import Any

import pytest


def _load_generator_module() -> Any:
    script_path = (
        Path(__file__).resolve().parents[1] / "scripts" / "build_stack_v2_comment_judge_cases.py"
    )
    spec = importlib.util.spec_from_file_location("stack_v2_comment_judge_cases", script_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


GENERATOR = _load_generator_module()
DEFAULT_DATASET = GENERATOR.DEFAULT_DATASET
DEFAULT_SCAN_MULTIPLIER = GENERATOR.DEFAULT_SCAN_MULTIPLIER


def _args(**overrides: Any) -> Namespace:
    values = {
        "content_field": None,
        "context_chars": 1200,
        "dataset": DEFAULT_DATASET,
        "dataset_config": None,
        "dataset_config_template": "{stack_label}",
        "fetch_stack_v2_content": False,
        "input_jsonl": None,
        "content_prefetch_workers": 1,
        "content_prefetch_buffer_size": 1,
        "language_field": None,
        "max_records_per_language": 10_000,
        "max_content_chars": 1_000_000,
        "no_progress": True,
        "num_workers": 1,
        "per_kind": 1,
        "progress_every": 0,
        "s3_content_prefix": "s3://softwareheritage/content",
        "s3_sign_requests": False,
        "split": "train",
    }
    values.update(overrides)
    return Namespace(**values)


def test_stack_v2_dataset_config_resolves_current_config_names() -> None:
    available_configs = (
        "Python",
        "CoffeeScript",
        "ABAP",
        "Adobe_Font_Metrics",
        "ASN.1",
        "C-Sharp",
        "F-Sharp",
        "Objective-C",
        "C++",
    )
    args = _args()

    assert GENERATOR._dataset_config_for(args, "python", {}, available_configs) == "Python"
    assert (
        GENERATOR._dataset_config_for(args, "coffeescript", {}, available_configs)
        == "CoffeeScript"
    )
    assert GENERATOR._dataset_config_for(args, "abap", {}, available_configs) == "ABAP"
    assert (
        GENERATOR._dataset_config_for(args, "adobe_font_metrics", {}, available_configs)
        == "Adobe_Font_Metrics"
    )
    assert GENERATOR._dataset_config_for(args, "asn1", {}, available_configs) == "ASN.1"
    assert GENERATOR._dataset_config_for(args, "c#", {}, available_configs) == "C-Sharp"
    assert GENERATOR._dataset_config_for(args, "f#", {}, available_configs) == "F-Sharp"
    assert (
        GENERATOR._dataset_config_for(args, "objective-c", {}, available_configs)
        == "Objective-C"
    )
    assert GENERATOR._dataset_config_for(args, "c++", {}, available_configs) == "C++"


def test_selected_languages_accepts_common_stack_v2_aliases() -> None:
    assert GENERATOR._selected_languages("c_plus_plus,c_sharp,f_sharp") == [
        "c++",
        "c#",
        "f#",
    ]


def test_selected_languages_can_take_first_n_supported_languages() -> None:
    supported = GENERATOR.get_supported_comment_languages()

    assert GENERATOR._selected_languages(None, 3) == supported[:3]


def test_selected_languages_can_limit_explicit_language_list() -> None:
    assert GENERATOR._selected_languages("python,java,coffeescript", 2) == [
        "python",
        "java",
    ]


def test_selected_languages_count_must_be_positive() -> None:
    with pytest.raises(SystemExit, match="--language-count"):
        GENERATOR._selected_languages(None, 0)


def test_validate_selected_languages_fails_before_streaming() -> None:
    with pytest.raises(SystemExit, match="Unsupported comment language"):
        GENERATOR._validate_selected_languages(["definitely_missing_language"])


def test_official_stack_v2_requires_content_source() -> None:
    args = _args()

    assert GENERATOR._needs_stack_v2_content_source(args)
    with pytest.raises(SystemExit, match="file IDs, not source text"):
        GENERATOR._record_content({"blob_id": "abc", "src_encoding": "utf-8"}, args)


def test_local_jsonl_content_is_used_without_stack_v2_fetch() -> None:
    args = _args(dataset="local-jsonl")

    assert not GENERATOR._needs_stack_v2_content_source(args)
    assert (
        GENERATOR._record_content({"content": "# note\nprint(1)\n"}, args)
        == "# note\nprint(1)\n"
    )


def test_oversized_local_content_is_skipped() -> None:
    args = _args(dataset="local-jsonl", max_content_chars=10)

    assert GENERATOR._record_content({"content": "#" * 10}, args) == "#" * 10
    assert GENERATOR._record_content({"content": "#" * 11}, args) == ""


def test_content_size_cap_can_be_disabled() -> None:
    args = _args(dataset="local-jsonl", max_content_chars=0)

    assert GENERATOR._record_content({"content": "#" * 11}, args) == "#" * 11


def test_stack_v2_download_reads_only_size_cap_plus_one(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    read_sizes = []

    class FakeStream:
        def __enter__(self) -> "FakeStream":
            return self

        def __exit__(self, *args: Any) -> None:
            return None

        def read(self, size: int) -> bytes:
            read_sizes.append(size)
            return b"#" * size

    def fake_open(*args: Any, **kwargs: Any) -> FakeStream:
        return FakeStream()

    monkeypatch.setitem(sys.modules, "smart_open", types.SimpleNamespace(open=fake_open))
    monkeypatch.setattr(
        GENERATOR,
        "_stack_v2_s3_client",
        lambda *, sign_requests: object(),
    )

    content = GENERATOR._download_stack_v2_content(
        {"blob_id": "abc", "src_encoding": "utf-8"},
        "s3://example",
        sign_requests=False,
        max_content_chars=10,
    )

    assert read_sizes == [11]
    assert content == ""


def test_stack_v2_download_runtime_errors_are_collection_errors(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_open(*args: Any, **kwargs: Any) -> Any:
        raise RuntimeError("endpoint unavailable")

    monkeypatch.setitem(sys.modules, "smart_open", types.SimpleNamespace(open=fake_open))
    monkeypatch.setattr(
        GENERATOR,
        "_stack_v2_s3_client",
        lambda *, sign_requests: object(),
    )

    with pytest.raises(
        GENERATOR._CorpusCollectionError,
        match="Could not fetch Stack v2 content for abc",
    ):
        GENERATOR._download_stack_v2_content(
            {"blob_id": "abc", "src_encoding": "utf-8"},
            "s3://example",
            sign_requests=False,
            max_content_chars=10,
        )


def test_stack_v2_s3_client_uses_unsigned_requests_by_default() -> None:
    boto3 = pytest.importorskip("boto3")
    botocore = pytest.importorskip("botocore")

    client = GENERATOR._stack_v2_s3_client(sign_requests=False)

    assert client.meta.service_model.service_name == "s3"
    assert client.meta.config.signature_version == botocore.UNSIGNED
    assert boto3 is not None


def test_load_streaming_dataset_passes_config_and_split() -> None:
    calls = []

    def fake_load_dataset(*args: Any, **kwargs: Any) -> str:
        calls.append((args, kwargs))
        return "dataset"

    result = GENERATOR._load_streaming_dataset(
        load_dataset=fake_load_dataset,
        dataset="bigcode/the-stack-v2",
        dataset_config="Python",
        split="train",
    )

    assert result == "dataset"
    assert calls == [
        (
            ("bigcode/the-stack-v2", "Python"),
            {"split": "train", "streaming": True},
        )
    ]


def test_iter_records_wraps_streaming_dataset_open_errors(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    datasets_module = types.ModuleType("datasets")

    def fake_load_dataset(*args: Any, **kwargs: Any) -> Any:
        raise RuntimeError("hub unavailable")

    datasets_module.load_dataset = fake_load_dataset
    monkeypatch.setitem(sys.modules, "datasets", datasets_module)
    monkeypatch.setattr(GENERATOR, "_safe_dataset_config_names", lambda dataset: None)
    args = _args(dataset="example/dataset", input_jsonl=None)

    with pytest.raises(GENERATOR._CorpusCollectionError, match="hub unavailable"):
        list(GENERATOR._iter_records(args, "python", {}))


def test_manifest_progress_interval_and_counts() -> None:
    args = _args(progress_every=10)

    assert not GENERATOR._should_emit_record_progress(args, 9)
    assert GENERATOR._should_emit_record_progress(args, 10)
    assert GENERATOR._format_progress_counts({"line": 2}, ("line", "block"), 10) == (
        "line=2/10 block=0/10"
    )


def test_num_workers_must_be_positive(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build_stack_v2_comment_judge_cases.py",
            "--num-workers",
            "0",
            "--no-progress",
        ],
    )

    with pytest.raises(SystemExit, match="--num-workers must be at least 1"):
        GENERATOR.main()


def test_sampling_limit_defaults_to_per_kind_scan_multiplier() -> None:
    args = _args(per_kind=20, max_records_per_language=None)

    GENERATOR._normalize_sampling_limits(args)

    assert args.max_records_per_language == 20 * DEFAULT_SCAN_MULTIPLIER


def test_sampling_limit_preserves_explicit_max_records() -> None:
    args = _args(per_kind=20, max_records_per_language=123)

    GENERATOR._normalize_sampling_limits(args)

    assert args.max_records_per_language == 123


def test_sampling_limits_must_be_positive() -> None:
    with pytest.raises(SystemExit, match="--per-kind"):
        GENERATOR._normalize_sampling_limits(_args(per_kind=0))

    with pytest.raises(SystemExit, match="--max-records-per-language"):
        GENERATOR._normalize_sampling_limits(
            _args(per_kind=20, max_records_per_language=0)
        )


def test_content_prefetch_workers_must_be_positive(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build_stack_v2_comment_judge_cases.py",
            "--content-prefetch-workers",
            "0",
            "--no-progress",
        ],
    )

    with pytest.raises(SystemExit, match="--content-prefetch-workers"):
        GENERATOR.main()


def test_content_prefetch_buffer_size_must_be_positive(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build_stack_v2_comment_judge_cases.py",
            "--content-prefetch-buffer-size",
            "0",
            "--no-progress",
        ],
    )

    with pytest.raises(SystemExit, match="--content-prefetch-buffer-size"):
        GENERATOR.main()


def test_prefetched_records_preserve_order_and_fetch_only_matching_language(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    args = _args(
        dataset="local-jsonl",
        content_prefetch_workers=2,
        content_prefetch_buffer_size=2,
        language_field="language",
    )
    records = iter(
        [
            {"id": "python-1", "language": "Python", "content": "# first"},
            {"id": "java-1", "language": "Java", "content": "// skipped"},
            {"id": "python-2", "language": "Python", "content": "# second"},
        ]
    )
    fetched_ids = []

    def fake_record_content(record: dict[str, Any], args: Any) -> str:
        fetched_ids.append(record["id"])
        return f"fetched:{record['id']}"

    monkeypatch.setattr(GENERATOR, "_record_content", fake_record_content)

    prefetched = list(
        GENERATOR._iter_prefetched_records(
            records=records,
            args=args,
            language="python",
            dataset_language="Python",
        )
    )

    assert [item.record_index for item in prefetched] == [1, 2, 3]
    assert [item.content for item in prefetched] == [
        "fetched:python-1",
        "",
        "fetched:python-2",
    ]
    assert fetched_ids == ["python-1", "python-2"]


def test_next_record_uses_iteration_lock_for_huggingface_stream(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class RecordingLock:
        def __init__(self) -> None:
            self.entered = False

        def __enter__(self) -> "RecordingLock":
            self.entered = True
            return self

        def __exit__(self, *args: Any) -> None:
            return None

    lock = RecordingLock()
    monkeypatch.setattr(GENERATOR, "_HUGGINGFACE_DATASET_ITERATION_LOCK", lock)
    record_iterator = iter([(1, {"id": "python-1"})])

    assert GENERATOR._next_record(record_iterator, _args(input_jsonl=None)) == (
        1,
        {"id": "python-1"},
    )
    assert lock.entered


def test_next_record_does_not_lock_local_jsonl(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    class FailingLock:
        def __enter__(self) -> "FailingLock":
            raise AssertionError("local JSONL should not use Hugging Face lock")

        def __exit__(self, *args: Any) -> None:
            return None

    monkeypatch.setattr(GENERATOR, "_HUGGINGFACE_DATASET_ITERATION_LOCK", FailingLock())
    record_iterator = iter([(1, {"id": "local-1"})])

    assert GENERATOR._next_record(
        record_iterator, _args(input_jsonl=tmp_path / "sample.jsonl")
    ) == (1, {"id": "local-1"})


def test_prefetched_records_buffer_can_exceed_worker_count(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    args = _args(
        dataset="local-jsonl",
        content_prefetch_workers=2,
        content_prefetch_buffer_size=4,
        language_field="language",
        max_records_per_language=10,
    )
    records = iter(
        [
            {"id": f"python-{index}", "language": "Python", "content": f"# {index}"}
            for index in range(5)
        ]
    )
    submitted_ids = []
    submitted_counts_at_result = []

    class FakeFuture:
        def __init__(self, record: dict[str, Any]) -> None:
            self.record = record

        def result(self) -> str:
            submitted_counts_at_result.append(len(submitted_ids))
            return f"fetched:{self.record['id']}"

        def cancel(self) -> None:
            return None

    class FakeExecutor:
        def __init__(self, max_workers: int) -> None:
            self.max_workers = max_workers

        def submit(self, function: Any, record: dict[str, Any], args: Any) -> FakeFuture:
            submitted_ids.append(record["id"])
            return FakeFuture(record)

        def shutdown(self, *, wait: bool, cancel_futures: bool) -> None:
            return None

    monkeypatch.setattr(GENERATOR, "ThreadPoolExecutor", FakeExecutor)
    iterator = GENERATOR._iter_prefetched_records(
        records=records,
        args=args,
        language="python",
        dataset_language="Python",
    )

    first = next(iterator)

    assert first.record_index == 1
    assert first.content == "fetched:python-0"
    assert submitted_counts_at_result[0] == 4
    assert [item.record_index for item in iterator] == [2, 3, 4, 5]


def test_prefetched_records_do_not_fetch_beyond_record_limit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    args = _args(
        dataset="local-jsonl",
        content_prefetch_workers=3,
        content_prefetch_buffer_size=6,
        language_field="language",
        max_records_per_language=1,
    )
    records = iter(
        [
            {"id": "python-1", "language": "Python", "content": "# first"},
            {"id": "python-2", "language": "Python", "content": "# second"},
            {"id": "python-3", "language": "Python", "content": "# third"},
        ]
    )
    fetched_ids = []

    def fake_record_content(record: dict[str, Any], args: Any) -> str:
        fetched_ids.append(record["id"])
        return f"fetched:{record['id']}"

    monkeypatch.setattr(GENERATOR, "_record_content", fake_record_content)

    prefetched = list(
        GENERATOR._iter_prefetched_records(
            records=records,
            args=args,
            language="python",
            dataset_language="Python",
        )
    )

    assert [item.record_index for item in prefetched] == [1, 2]
    assert [item.content for item in prefetched] == ["fetched:python-1", ""]
    assert fetched_ids == ["python-1"]


def test_coffeescript_block_example_classifies_before_hash_line_opener() -> None:
    syntax = GENERATOR.get_comment_syntax("coffeescript")
    raw_comment = "###\nnote\n###"

    assert GENERATOR._syntax_examples_for_kind(syntax, "block") == [raw_comment]
    assert GENERATOR._classify_comment(syntax, raw_comment) == ("block", "###...###")


def test_incomplete_comment_kind_becomes_failure_row() -> None:
    args = _args(per_kind=10, max_records_per_language=1000)
    syntax = GENERATOR.get_comment_syntax("coffeescript")
    result = GENERATOR.StackCollectionResult(
        cases=[],
        scanned_records=1000,
        dataset_config="CoffeeScript",
        dataset_language="CoffeeScript",
    )

    failures = GENERATOR._build_failures(
        args=args,
        language="coffeescript",
        syntax=syntax,
        target_kinds=("line", "block"),
        counts={"line": 10},
        result=result,
    )

    assert len(failures) == 1
    failure = failures[0].to_json()
    assert failure["language"] == "coffeescript"
    assert failure["comment_kind"] == "block"
    assert failure["observed_count"] == 0
    assert failure["expected_count"] == 10
    assert failure["scanned_records"] == 1000
    assert failure["dataset_config"] == "CoffeeScript"
    assert "###" in "\n".join(failure["syntax_examples"])
    assert "corpus-backed syntax failure" in failure["recommendation"]


def test_incomplete_nested_comment_kind_is_rarity_review_signal() -> None:
    args = _args(per_kind=20, max_records_per_language=10_000)
    syntax = GENERATOR.get_comment_syntax("agda")
    result = GENERATOR.StackCollectionResult(
        cases=[],
        scanned_records=10_000,
        dataset_config="Agda",
        dataset_language="Agda",
    )

    failures = GENERATOR._build_failures(
        args=args,
        language="agda",
        syntax=syntax,
        target_kinds=("nested",),
        counts={},
        result=result,
    )

    assert len(failures) == 1
    failure = failures[0].to_json()
    assert failure["comment_kind"] == "nested"
    assert failure["expected_count"] == 20
    assert "nested comment examples can be rare" in failure["recommendation"]
    assert "does not by itself prove a parser or registry bug" in failure[
        "recommendation"
    ]


def test_write_failures_creates_jsonl_and_removes_stale_file(tmp_path: Path) -> None:
    failure_path = tmp_path / "failures.jsonl"
    failure = GENERATOR.StackFailure(
        language="coffeescript",
        comment_kind="block",
        expected_count=10,
        observed_count=0,
        scanned_records=1000,
        max_records_per_language=1000,
        dataset="bigcode/the-stack-v2",
        dataset_config="CoffeeScript",
        dataset_language="CoffeeScript",
        syntax_examples=["###\nnote\n###"],
        observed_kinds={"line": 10},
        reason="missing",
        recommendation="review",
    )

    GENERATOR._write_failures(failure_path, [failure])
    assert failure_path.exists()
    assert '"comment_kind": "block"' in failure_path.read_text(encoding="utf-8")

    GENERATOR._write_failures(failure_path, [])
    assert not failure_path.exists()


def test_incomplete_buckets_do_not_fail_generation_by_default(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    sample = tmp_path / "sample.jsonl"
    sample.write_text(
        json.dumps({"language": "CoffeeScript", "content": "# note\nx = 1\n"}) + "\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build_stack_v2_comment_judge_cases.py",
            "--input-jsonl",
            str(sample),
            "--languages",
            "coffeescript",
            "--per-kind",
            "1",
            "--max-records-per-language",
            "1",
            "--output-root",
            str(tmp_path / "out"),
            "--no-progress",
        ],
    )

    assert GENERATOR.main() == 0
    assert (tmp_path / "out" / "manifest.jsonl").exists()
    assert (tmp_path / "out" / "failures.jsonl").exists()


def test_fail_on_incomplete_restores_strict_generation_exit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    sample = tmp_path / "sample.jsonl"
    sample.write_text(
        json.dumps({"language": "CoffeeScript", "content": "# note\nx = 1\n"}) + "\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build_stack_v2_comment_judge_cases.py",
            "--input-jsonl",
            str(sample),
            "--languages",
            "coffeescript",
            "--per-kind",
            "1",
            "--max-records-per-language",
            "1",
            "--output-root",
            str(tmp_path / "out"),
            "--no-progress",
            "--fail-on-incomplete",
        ],
    )

    assert GENERATOR.main() == 1
    assert (tmp_path / "out" / "failures.jsonl").exists()


def test_local_jsonl_manifest_collects_coffeescript_block_comments(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    sample = tmp_path / "sample.jsonl"
    with sample.open("w", encoding="utf-8") as outfile:
        for index in range(10):
            outfile.write(
                json.dumps(
                    {
                        "id": f"coffee-{index}",
                        "language": "CoffeeScript",
                        "content": f"# line {index}\nvalue = {index}\n###\nnote\n###\n",
                    }
                )
                + "\n"
            )
    output_root = tmp_path / "out"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build_stack_v2_comment_judge_cases.py",
            "--input-jsonl",
            str(sample),
            "--languages",
            "coffeescript",
            "--per-kind",
            "10",
            "--max-records-per-language",
            "100",
            "--output-root",
            str(output_root),
            "--no-progress",
        ],
    )

    assert GENERATOR.main() == 0

    manifest_rows = [
        json.loads(line)
        for line in (output_root / "manifest.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    block_rows = [row for row in manifest_rows if row["comment_kind"] == "block"]

    assert len(block_rows) == 10
    assert {row["raw_comment"] for row in block_rows} == {"###\nnote\n###"}
    assert {row["syntax_label"] for row in block_rows} == {"###...###"}
    assert not (output_root / "failures.jsonl").exists()


def test_local_jsonl_manifest_can_collect_languages_in_parallel(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    sample = tmp_path / "sample.jsonl"
    records = [
        {
            "id": "coffee-1",
            "language": "CoffeeScript",
            "content": "# coffee line\nvalue = 1\n###\ncoffee block\n###\n",
        },
        {
            "id": "java-1",
            "language": "Java",
            "content": "// java line\nclass Demo { /* java block */ }\n",
        },
    ]
    with sample.open("w", encoding="utf-8") as outfile:
        for record in records:
            outfile.write(json.dumps(record) + "\n")
    output_root = tmp_path / "out"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build_stack_v2_comment_judge_cases.py",
            "--input-jsonl",
            str(sample),
            "--languages",
            "coffeescript,java",
            "--per-kind",
            "1",
            "--max-records-per-language",
            "10",
            "--output-root",
            str(output_root),
            "--num-workers",
            "2",
            "--no-progress",
        ],
    )

    assert GENERATOR.main() == 0

    manifest_rows = [
        json.loads(line)
        for line in (output_root / "manifest.jsonl").read_text(encoding="utf-8").splitlines()
    ]

    assert [row["language"] for row in manifest_rows] == [
        "coffeescript",
        "coffeescript",
        "java",
        "java",
    ]
    assert [row["comment_kind"] for row in manifest_rows] == [
        "line",
        "block",
        "line",
        "block",
    ]
    assert not (output_root / "failures.jsonl").exists()


def test_parallel_language_collection_reports_streaming_errors_as_failures(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    args = _args(
        dataset="local-jsonl",
        input_jsonl=tmp_path / "unused.jsonl",
        language_field="language",
        max_records_per_language=10,
        num_workers=2,
        per_kind=1,
    )

    def fake_iter_records(
        args: Any, language: str, language_map: dict[str, Any]
    ) -> Any:
        if language == "java":
            raise GENERATOR._CorpusCollectionError("hub read failed")
        yield {
            "id": "coffee-1",
            "language": "CoffeeScript",
            "content": "# coffee line\nvalue = 1\n###\ncoffee block\n###\n",
        }

    monkeypatch.setattr(GENERATOR, "_iter_records", fake_iter_records)
    source_root = tmp_path / "files"
    source_root.mkdir()

    results = GENERATOR._collect_requested_languages(
        args=args,
        languages=["coffeescript", "java"],
        language_map={},
        source_root=source_root,
    )

    coffeescript_result, java_result = results

    assert [case.comment_kind for case in coffeescript_result.cases] == [
        "line",
        "block",
    ]
    assert coffeescript_result.failures == []
    assert java_result.cases == []
    assert {failure.comment_kind for failure in java_result.failures} == {
        "line",
        "block",
    }
    assert all("hub read failed" in failure.reason for failure in java_result.failures)
    assert all(
        "corpus access or streaming error" in failure.recommendation
        for failure in java_result.failures
    )


def test_prefetch_content_errors_become_language_failures(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    args = _args(
        dataset="local-jsonl",
        input_jsonl=tmp_path / "unused.jsonl",
        content_prefetch_workers=2,
        content_prefetch_buffer_size=2,
        language_field="language",
        max_records_per_language=10,
        per_kind=1,
    )

    def fake_iter_records(
        args: Any, language: str, language_map: dict[str, Any]
    ) -> Any:
        yield {
            "id": "java-1",
            "language": "Java",
            "blob_id": "abc",
            "src_encoding": "utf-8",
        }

    def fake_record_content(record: dict[str, Any], args: Any) -> str:
        raise GENERATOR._CorpusCollectionError("content endpoint unavailable")

    monkeypatch.setattr(GENERATOR, "_iter_records", fake_iter_records)
    monkeypatch.setattr(GENERATOR, "_record_content", fake_record_content)

    result = GENERATOR._collect_requested_language(
        args=args,
        language_index=1,
        language_count=1,
        language="java",
        language_map={},
        source_root=tmp_path / "files",
    )

    assert result.cases == []
    assert {failure.comment_kind for failure in result.failures} == {"line", "block"}
    assert all(
        "content endpoint unavailable" in failure.reason for failure in result.failures
    )
