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
        "dataset_revision": None,
        "fetch_stack_v2_content": False,
        "files_per_language": None,
        "input_jsonl": None,
        "content_prefetch_workers": 1,
        "content_prefetch_buffer_size": 1,
        "language_field": None,
        "max_records_per_language": 10_000,
        "max_content_chars": 1_000_000,
        "max_line_comment_chars": 12_000,
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
        "4D",
        "ABAP",
        "Adobe_Font_Metrics",
        "ASN.1",
        "ASP.NET",
        "C-Sharp",
        "Cap-n_Proto",
        "ColdFusion",
        "ColdFusion_CFC",
        "F-Star",
        "F-Sharp",
        "Graphviz_(DOT)",
        "HOCON",
        "HTML+ECR",
        "HTML+EEX",
        "HTML+ERB",
        "HTML+PHP",
        "HTML+Razor",
        "JSON_with_Comments",
        "MiniYAML",
        "Objective-C",
        "C++",
        "Pascal",
        "Q-Sharp",
        "robots.txt",
        "Slim",
        "Visual_Basic_.NET",
    )
    args = _args()

    assert GENERATOR._dataset_config_for(args, "python", {}, available_configs) == "Python"
    assert (
        GENERATOR._dataset_config_for(args, "coffeescript", {}, available_configs) == "CoffeeScript"
    )
    assert GENERATOR._dataset_config_for(args, "abap", {}, available_configs) == "ABAP"
    assert (
        GENERATOR._dataset_config_for(args, "adobe_font_metrics", {}, available_configs)
        == "Adobe_Font_Metrics"
    )
    assert GENERATOR._dataset_config_for(args, "four_d", {}, available_configs) == "4D"
    assert GENERATOR._dataset_config_for(args, "asn1", {}, available_configs) == "ASN.1"
    assert GENERATOR._dataset_config_for(args, "aspnet", {}, available_configs) == "ASP.NET"
    assert GENERATOR._dataset_config_for(args, "c#", {}, available_configs) == "C-Sharp"
    assert GENERATOR._dataset_config_for(args, "capn_proto", {}, available_configs) == "Cap-n_Proto"
    assert GENERATOR._dataset_config_for(args, "coldfusion", {}, available_configs) == "ColdFusion"
    assert (
        GENERATOR._dataset_config_for(args, "coldfusion_cfc", {}, available_configs)
        == "ColdFusion_CFC"
    )
    assert GENERATOR._dataset_config_for(args, "f_star", {}, available_configs) == "F-Star"
    assert GENERATOR._dataset_config_for(args, "f#", {}, available_configs) == "F-Sharp"
    assert (
        GENERATOR._dataset_config_for(args, "graphviz_dot", {}, available_configs)
        == "Graphviz_(DOT)"
    )
    assert GENERATOR._dataset_config_for(args, "hocon", {}, available_configs) == "HOCON"
    assert GENERATOR._dataset_config_for(args, "html_ecr", {}, available_configs) == "HTML+ECR"
    assert GENERATOR._dataset_config_for(args, "html_eex", {}, available_configs) == "HTML+EEX"
    assert GENERATOR._dataset_config_for(args, "html_erb", {}, available_configs) == "HTML+ERB"
    assert GENERATOR._dataset_config_for(args, "html_php", {}, available_configs) == "HTML+PHP"
    assert GENERATOR._dataset_config_for(args, "html_razor", {}, available_configs) == "HTML+Razor"
    assert (
        GENERATOR._dataset_config_for(args, "jsonc", {}, available_configs) == "JSON_with_Comments"
    )
    assert GENERATOR._dataset_config_for(args, "mini_yaml", {}, available_configs) == "MiniYAML"
    assert (
        GENERATOR._dataset_config_for(args, "objective-c", {}, available_configs) == "Objective-C"
    )
    assert GENERATOR._dataset_config_for(args, "c++", {}, available_configs) == "C++"
    assert GENERATOR._dataset_config_for(args, "pascal", {}, available_configs) == "Pascal"
    assert GENERATOR._dataset_config_for(args, "qsharp", {}, available_configs) == "Q-Sharp"
    assert GENERATOR._dataset_config_for(args, "robots_txt", {}, available_configs) == "robots.txt"
    assert GENERATOR._dataset_config_for(args, "slim", {}, available_configs) == "Slim"
    assert (
        GENERATOR._dataset_config_for(args, "visual_basic_net", {}, available_configs)
        == "Visual_Basic_.NET"
    )


@pytest.mark.parametrize(
    ("language", "row_language"),
    [
        ("asn1", "ASN.1"),
        ("aspnet", "ASP.NET"),
        ("capn_proto", "Cap'n Proto"),
        ("coldfusion", "ColdFusion"),
        ("coldfusion_cfc", "ColdFusion CFC"),
        ("f_star", "F*"),
        ("four_d", "4D"),
        ("graphviz_dot", "Graphviz (DOT)"),
        ("hocon", "HOCON"),
        ("html_ecr", "HTML+ECR"),
        ("html_eex", "HTML+EEX"),
        ("html_erb", "HTML+ERB"),
        ("html_php", "HTML+PHP"),
        ("html_razor", "HTML+Razor"),
        ("jsonc", "JSON with Comments"),
        ("mini_yaml", "MiniYAML"),
        ("pascal", "Pascal"),
        ("qsharp", "Q#"),
        ("robots_txt", "robots.txt"),
        ("slim", "Slim"),
        ("visual_basic_net", "Visual Basic .NET"),
    ],
)
def test_record_language_matching_accepts_stack_v2_punctuation_labels(
    language: str, row_language: str
) -> None:
    args = _args()
    dataset_language = GENERATOR._dataset_language_for(language, {})

    assert GENERATOR._record_matches_language(
        {"language": row_language},
        args,
        language,
        dataset_language,
    )


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


def test_source_identity_distinguishes_same_path_in_different_repositories() -> None:
    first = {"repo": "owner/one", "path": "src/main.java"}
    second = {"repo": "owner/two", "path": "src/main.java"}

    assert GENERATOR._source_identity(first, 1) != GENERATOR._source_identity(second, 2)


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
        GENERATOR._record_content({"content": "# note\nprint(1)\n"}, args) == "# note\nprint(1)\n"
    )


@pytest.mark.parametrize(
    ("record", "language", "content"),
    [
        pytest.param(
            {"path": "assets/model.bin"},
            "python",
            (
                "version https://git-lfs.github.com/spec/v1\r\n"
                f"oid sha256:{'aB' * 32}\r\n"
                "size 123\r\n"
            ),
            id="exact-git-lfs-pointer-is-language-and-suffix-independent",
        ),
        pytest.param(
            {"path": "legacy.php"},
            "hack",
            "<?php\n// PHP is not Hack\n",
            id="legacy-hack-php-requires-hack-header",
        ),
        pytest.param(
            {"path": "legacy.PHP"},
            "Hack",
            "<html><!-- not Hack --></html>",
            id="legacy-hack-extension-is-case-insensitive",
        ),
        pytest.param(
            {"path": "screen.ccp"},
            "cobol",
            '<Page Name="Screen"><Components /></Page>',
            id="codecharge-page-document-is-not-cobol",
        ),
        pytest.param(
            {"path": "screen.CCP"},
            "COBOL",
            '\ufeff <?xml version="1.0"?>\n<Page>\n</Page>',
            id="codecharge-page-after-xml-declaration",
        ),
        pytest.param(
            {"path": "sample.las"},
            "lasso",
            "~Version Information\nVERS. 2.0\n",
            id="las-version-section-is-a-well-log",
        ),
        pytest.param(
            {"path": "sample.las"},
            "lasso",
            "metadata\n  ~Well Information\nSTRT.M 1000\n",
            id="las-well-section-is-a-well-log",
        ),
        pytest.param(
            {"path": "sample.las"},
            "lasso",
            "~CURVE: curve definitions\nDEPT.M\n",
            id="las-curve-section-is-a-well-log",
        ),
        pytest.param(
            {"path": "sample.las"},
            "lasso",
            "~ASCII Log Data\n1000 2.4\n",
            id="las-ascii-section-is-a-well-log",
        ),
        pytest.param(
            {"path": "/amaze-your-friends/macros/goodies/c.ik"},
            "ioke",
            ("map! \x16\x01 ()\x1bi\nmap! \x16\x0b /* */\x19\x16\r\n\x16\x12\x16\x17\x16\x06\n"),
            id="ioke-line-858dc617545e99f2",
        ),
        pytest.param(
            {"path": "/marc/seca_034.mrc"},
            "mirc_script",
            "00045cpcaa2200037Ii 4500001000700000\x1evalue?\x1e\x1d",
            id="mirc_script-line-112a24da87b41074",
        ),
        pytest.param(
            {"path": "/cypress/fixtures/marcBibFileForC388505.mrc"},
            "mIRC Script",
            "00045cam a2200037Ii 41y0001000700000\x1evalue?\x1e\x1d",
            id="mirc_script-line-f1d67ed1511082e4",
        ),
        pytest.param(
            {"path": "/data/minute_data_unverified/20180904/CERC.pb"},
            "purebasic",
            "\n\x04CERC\x10\xa8\x9f\xcf\t\x18\x01\x1a\x08\x04\x15;noise",
            id="purebasic-line-3c75577cc9cf362e",
        ),
        pytest.param(
            {"path": "/data/minute_data/20190116/JTD.pb"},
            "PureBasic",
            "\n\x03JTD\x10\xa4\x87\x90\t\x18\x01\x1a\x08\x04\x15;noise",
            id="purebasic-line-dc70ea784b65525e",
        ),
        pytest.param(
            {"path": "/data/minute_data/20180523/NZF.pb"},
            "purebasic",
            "\n\x03NZF\x10\x82\x83\x84\t\x18\x01\x1a\x08\x04\x15;noise",
            id="purebasic-line-e0ea3f025bb42d83",
        ),
        pytest.param(
            {"path": "/data/minute_data/20180920/BOTZ.pb"},
            "purebasic",
            "\n\x04BOTZ\x10\x8a\x8b\x8c\t\x18\x01\x1a\x08\x04\x15;noise",
            id="purebasic-line-e3d3f4e5e741e046",
        ),
        pytest.param(
            {"path": "/vip_run/verifyEncoderWithDecoderResult/q13.Y"},
            "yacc",
            "\x85\x8a\x8c\x8c\x88\x84\x7f\x80\x81\x81\x84\x88//-/./2149;@A?",
            id="yacc-line-4fcf0508f0dcbcea",
        ),
    ],
)
def test_record_eligibility_rejects_exact_non_source_signatures(
    record: dict[str, str],
    language: str,
    content: str,
) -> None:
    assert not GENERATOR._record_is_eligible_source(record, language, content)


@pytest.mark.parametrize(
    ("record", "language", "content"),
    [
        pytest.param(
            {"path": "pointer.txt"},
            "python",
            (
                "version https://git-lfs.github.com/spec/v1\n"
                f"oid sha256:{'a' * 64}\n"
                "size 123\n"
                "# trailing source\n"
            ),
            id="git-lfs-pointer-with-extra-source",
        ),
        pytest.param(
            {"path": "pointer.txt"},
            "python",
            (f"version https://git-lfs.github.com/spec/v1\noid sha256:{'a' * 63}\nsize 123\n"),
            id="git-lfs-pointer-with-short-object-id",
        ),
        pytest.param(
            {"path": "source.hack"},
            "hack",
            "// Native .hack files need no opening tag\n",
            id="native-hack-extension",
        ),
        pytest.param(
            {"path": "legacy.php"},
            "hack",
            "\ufeff \n\t<?hh // strict\n// Hack source\n",
            id="legacy-hack-php-with-header",
        ),
        pytest.param(
            {"path": "legacy.php"},
            "hack",
            " \t#!/usr/bin/env hhvm\r\n \t<?hh\n// Hack source\n",
            id="legacy-hack-php-with-shebang-and-header",
        ),
        pytest.param(
            {"path": "program.cob"},
            "cobol",
            "<Page> is valid COBOL data here\n",
            id="codecharge-gate-is-extension-scoped",
        ),
        pytest.param(
            {"path": "program.ccp"},
            "cobol",
            "<Pageant> is not the CodeCharge root element\n",
            id="codecharge-root-near-miss",
        ),
        pytest.param(
            {"path": "source.las"},
            "lasso",
            "[no_square_brackets]\n// genuine legacy Lasso source\n",
            id="genuine-legacy-lasso-extension",
        ),
        pytest.param(
            {"path": "source.lasso"},
            "lasso",
            "~Version is application content\n",
            id="well-log-gate-is-extension-scoped",
        ),
        pytest.param(
            {"path": "source.ik"},
            "ioke",
            "map! is a documented command\nmap! can appear in prose\n",
            id="ioke-vi-map-text-without-controls",
        ),
        pytest.param(
            {"path": "source.ik"},
            "ioke",
            "\x16\x01\x1b\x16\x0b\x19\x16\x12\x17\n; embedded controls without vi maps\n",
            id="ioke-controls-without-vi-map-structure",
        ),
        pytest.param(
            {"path": "source.ik"},
            "ioke",
            (
                "map! \x16\x01 ()\x1bi\n"
                "\x16\x0b\x19\x16\x12\x17\x06\n"
                "; one map command is insufficient evidence\n"
            ),
            id="ioke-single-vi-map-line",
        ),
        pytest.param(
            {"path": "source.ioke"},
            "ioke",
            ("map! \x16\x01 ()\x1bi\nmap! \x16\x0b /* */\x19\x16\r\n\x16\x12\x16\x17\x16\x06\n"),
            id="ioke-vi-map-gate-is-ik-extension-scoped",
        ),
        pytest.param(
            {"path": "source.ik"},
            "python",
            ("map! \x16\x01 ()\x1bi\nmap! \x16\x0b /* */\x19\x16\r\n\x16\x12\x16\x17\x16\x06\n"),
            id="ioke-vi-map-gate-is-language-scoped",
        ),
        pytest.param(
            {"path": "script.mrc"},
            "mirc_script",
            "00045cam a2200037Ii 4500\nalias announce { echo -a 001000700000 }\n",
            id="marc-looking-leader-without-directory-terminators",
        ),
        pytest.param(
            {"path": "colors.mrc"},
            "mirc_script",
            "\x03" * 20 + "\n; mIRC formatting controls are source data\n",
            id="mirc-control-codes-are-not-a-binary-gate",
        ),
        pytest.param(
            {"path": "source.pb"},
            "purebasic",
            'EnableExplicit\n; genuine PureBasic comment\nPrintN("ready")\n',
            id="genuine-purebasic-source",
        ),
        pytest.param(
            {"path": "boundary.pb"},
            "purebasic",
            "\x01" * 7 + "\n; below the binary-control count threshold\n",
            id="purebasic-control-count-near-miss",
        ),
        pytest.param(
            {"path": "grammar.y"},
            "yacc",
            "%token VALUE\n%%\ninput: VALUE ;\n// genuine grammar comment\n",
            id="genuine-yacc-source",
        ),
        pytest.param(
            {"path": "binary-looking.py"},
            "python",
            "\x01" * 20 + "\n# gate is limited to collision-prone languages\n",
            id="binary-control-gate-is-language-scoped",
        ),
    ],
)
def test_record_eligibility_preserves_near_misses_and_genuine_source(
    record: dict[str, str],
    language: str,
    content: str,
) -> None:
    assert GENERATOR._record_is_eligible_source(record, language, content)


def test_source_eligibility_runs_after_fetch_and_before_extraction(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pointer = f"version https://git-lfs.github.com/spec/v1\noid sha256:{'a' * 64}\nsize 123\n"
    sample = tmp_path / "sample.jsonl"
    sample.write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "id": "pointer",
                        "language": "Python",
                        "path": "pointer.py",
                        "content": pointer,
                    }
                ),
                json.dumps(
                    {
                        "id": "source",
                        "language": "Python",
                        "path": "source.py",
                        "content": "# actual comment\nvalue = 1\n",
                    }
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    real_query = GENERATOR.CommentQuery
    extracted_contents = []

    class RecordingQuery:
        def __init__(self, language: str) -> None:
            self.delegate = real_query(language)

        def iter_ranges(self, content: str) -> Any:
            extracted_contents.append(content)
            return self.delegate.iter_ranges(content)

    monkeypatch.setattr(GENERATOR, "CommentQuery", RecordingQuery)
    source_root = tmp_path / "files"
    source_root.mkdir()

    result = GENERATOR._collect_language_cases(
        args=_args(
            input_jsonl=sample,
            max_records_per_language=2,
            per_kind=1,
        ),
        language="python",
        syntax=GENERATOR.get_comment_syntax("python"),
        target_kinds=("line",),
        language_map={},
        source_root=source_root,
    )

    assert extracted_contents == ["# actual comment\nvalue = 1\n"]
    assert [case.raw_comment for case in result.cases] == ["# actual comment"]


def test_overlong_line_candidate_is_skipped_and_replaced_for_file_quota(
    tmp_path: Path,
) -> None:
    overlong = "# " + ("x" * 40)
    sample = tmp_path / "sample.jsonl"
    sample.write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "id": "overcaptured",
                        "language": "Python",
                        "path": "overcaptured.py",
                        "content": overlong + "\n",
                    }
                ),
                json.dumps(
                    {
                        "id": "replacement",
                        "language": "Python",
                        "path": "replacement.py",
                        "content": "# replacement\n",
                    }
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    source_root = tmp_path / "files"
    source_root.mkdir()

    result = GENERATOR._collect_language_cases(
        args=_args(
            input_jsonl=sample,
            files_per_language=1,
            max_records_per_language=2,
            max_line_comment_chars=20,
        ),
        language="python",
        syntax=GENERATOR.get_comment_syntax("python"),
        target_kinds=("line",),
        language_map={},
        source_root=source_root,
    )

    assert result.scanned_records == 2
    assert [case.source_id for case in result.cases] == ["replacement"]
    assert [case.raw_comment for case in result.cases] == ["# replacement"]
    written_sources = list(source_root.iterdir())
    assert len(written_sources) == 1
    assert written_sources[0].read_text(encoding="utf-8") == "# replacement\n"


def test_line_limit_does_not_cap_delimited_block_comments(tmp_path: Path) -> None:
    block_comment = "/* " + ("x" * 40) + " */"
    sample = tmp_path / "sample.jsonl"
    sample.write_text(
        json.dumps(
            {
                "id": "long-block",
                "language": "Java",
                "path": "LongBlock.java",
                "content": block_comment + "\n",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    source_root = tmp_path / "files"
    source_root.mkdir()

    result = GENERATOR._collect_language_cases(
        args=_args(
            input_jsonl=sample,
            files_per_language=1,
            max_records_per_language=1,
            max_line_comment_chars=20,
        ),
        language="java",
        syntax=GENERATOR.get_comment_syntax("java"),
        target_kinds=("block",),
        language_map={},
        source_root=source_root,
    )

    assert [case.comment_kind for case in result.cases] == ["block"]
    assert [case.raw_comment for case in result.cases] == [block_comment]


def test_zero_disables_line_comment_limit() -> None:
    assert not GENERATOR._line_comment_exceeds_judge_limit(
        _args(max_line_comment_chars=0),
        "line",
        "#" + ("x" * 100_000),
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


@pytest.mark.parametrize(
    ("dataset_revision", "expected_kwargs"),
    [
        (None, {"split": "train", "streaming": True}),
        (
            "0123456789abcdef",
            {
                "split": "train",
                "streaming": True,
                "revision": "0123456789abcdef",
            },
        ),
    ],
)
def test_load_streaming_dataset_passes_config_split_and_optional_revision(
    dataset_revision: str | None,
    expected_kwargs: dict[str, Any],
) -> None:
    calls = []

    def fake_load_dataset(*args: Any, **kwargs: Any) -> str:
        calls.append((args, kwargs))
        return "dataset"

    result = GENERATOR._load_streaming_dataset(
        load_dataset=fake_load_dataset,
        dataset="bigcode/the-stack-v2",
        dataset_config="Python",
        split="train",
        dataset_revision=dataset_revision,
    )

    assert result == "dataset"
    assert calls == [(("bigcode/the-stack-v2", "Python"), expected_kwargs)]


@pytest.mark.parametrize(
    ("dataset_revision", "expected_kwargs"),
    [
        (None, {}),
        ("fedcba9876543210", {"revision": "fedcba9876543210"}),
    ],
)
def test_dataset_config_discovery_passes_optional_revision(
    monkeypatch: pytest.MonkeyPatch,
    dataset_revision: str | None,
    expected_kwargs: dict[str, str],
) -> None:
    datasets_module = types.ModuleType("datasets")
    calls = []

    def fake_get_dataset_config_names(*args: Any, **kwargs: Any) -> list[str]:
        calls.append((args, kwargs))
        return ["Python"]

    datasets_module.get_dataset_config_names = fake_get_dataset_config_names
    monkeypatch.setitem(sys.modules, "datasets", datasets_module)
    GENERATOR._dataset_config_names.cache_clear()

    assert GENERATOR._dataset_config_names(
        "example/revision-test",
        dataset_revision,
    ) == ("Python",)
    assert calls == [
        (
            ("example/revision-test",),
            expected_kwargs,
        )
    ]


def test_parse_args_accepts_dataset_revision(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build_stack_v2_comment_judge_cases.py",
            "--dataset-revision",
            "0123456789abcdef",
        ],
    )

    assert GENERATOR.parse_args().dataset_revision == "0123456789abcdef"


def test_main_rejects_empty_dataset_revision(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build_stack_v2_comment_judge_cases.py",
            "--dataset-revision",
            "",
            "--no-progress",
        ],
    )

    with pytest.raises(SystemExit, match="--dataset-revision"):
        GENERATOR.main()


def test_iter_records_wraps_streaming_dataset_open_errors(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    datasets_module = types.ModuleType("datasets")

    def fake_load_dataset(*args: Any, **kwargs: Any) -> Any:
        raise RuntimeError("hub unavailable")

    datasets_module.load_dataset = fake_load_dataset
    monkeypatch.setitem(sys.modules, "datasets", datasets_module)
    monkeypatch.setattr(
        GENERATOR,
        "_safe_dataset_config_names",
        lambda dataset, revision: None,
    )
    args = _args(
        dataset="example/dataset",
        dataset_revision="0123456789abcdef",
        input_jsonl=None,
    )

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


def test_sampling_limit_uses_total_file_quota_when_configured() -> None:
    args = _args(
        files_per_language=50,
        per_kind=20,
        max_records_per_language=None,
    )

    GENERATOR._normalize_sampling_limits(args)

    assert args.max_records_per_language == 50 * DEFAULT_SCAN_MULTIPLIER


def test_sampling_limit_preserves_explicit_max_records() -> None:
    args = _args(per_kind=20, max_records_per_language=123)

    GENERATOR._normalize_sampling_limits(args)

    assert args.max_records_per_language == 123


def test_sampling_limits_must_be_positive() -> None:
    with pytest.raises(SystemExit, match="--per-kind"):
        GENERATOR._normalize_sampling_limits(_args(per_kind=0))

    with pytest.raises(SystemExit, match="--files-per-language"):
        GENERATOR._normalize_sampling_limits(_args(files_per_language=0))

    with pytest.raises(SystemExit, match="--max-records-per-language"):
        GENERATOR._normalize_sampling_limits(_args(per_kind=20, max_records_per_language=0))

    with pytest.raises(SystemExit, match="--max-line-comment-chars"):
        GENERATOR._normalize_sampling_limits(_args(max_line_comment_chars=-1))


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

        def submit(
            self, function: Any, record: dict[str, Any], args: Any, *extra_args: Any
        ) -> FakeFuture:
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


def test_nested_capable_single_level_comments_can_fill_block_bucket() -> None:
    pascal = GENERATOR.get_comment_syntax("pascal")
    coldfusion = GENERATOR.get_comment_syntax("coldfusion")

    assert GENERATOR._classify_comment(pascal, "{ block }") == ("block", "{...}")
    assert GENERATOR._classify_comment(pascal, "{ outer { inner } outer }") == ("nested", "{...}")
    assert GENERATOR._classify_comment(coldfusion, "<!--- note --->") == (
        "block",
        "<!---...--->",
    )
    assert GENERATOR._classify_comment(coldfusion, "<!--- outer <!--- inner ---> outer --->") == (
        "nested",
        "<!---...--->",
    )


def test_line_like_block_openers_classify_before_shorter_line_openers() -> None:
    syntax = GENERATOR.get_comment_syntax("slim")

    assert GENERATOR._classify_comment(syntax, "  /! note") == ("block", "/!")
    assert GENERATOR._classify_comment(syntax, "  / note") == ("line", "/")


def test_hocon_manifest_sampling_targets_line_comments_only() -> None:
    syntax = GENERATOR.get_comment_syntax("hocon")

    assert GENERATOR._supported_comment_kinds(syntax, "hocon") == ("line",)
    assert GENERATOR.CommentQuery("hocon").parse("a = 1\n/* not hocon */\n") == []


def test_figlet_manifest_sampling_targets_contextual_comments() -> None:
    syntax = GENERATOR.get_comment_syntax("figlet_font")

    assert GENERATOR._supported_comment_kinds(syntax, "figlet_font") == ("contextual",)
    assert GENERATOR._syntax_examples_for_kind(syntax, "contextual") == [
        "FIGlet font attribution\n  leading space is content"
    ]
    assert GENERATOR._classify_comment(syntax, "font attribution\n  leading space is content") == (
        "contextual",
        "contextual",
    )


def test_genshi_manifest_sampling_excludes_reviewed_xml_block_bucket() -> None:
    syntax = GENERATOR.get_comment_syntax("genshi")

    assert GENERATOR._supported_comment_kinds(syntax, "genshi") == ()
    assert GENERATOR.CommentQuery("genshi").parse("<div><!-- note --><span>${value}</span></div>")
    assert GENERATOR.CommentQuery("genshi").parse("{# text template #}\n") == []
    assert GENERATOR.CommentQuery("genshi").parse("## legacy text template\n") == []


def test_total_file_quota_reports_zero_target_registry_language(
    tmp_path: Path,
) -> None:
    source_root = tmp_path / "files"
    source_root.mkdir()

    result = GENERATOR._collect_requested_language(
        args=_args(files_per_language=50),
        language_index=1,
        language_count=1,
        language="genshi",
        language_map={},
        source_root=source_root,
    )

    assert result.cases == []
    assert len(result.failures) == 1
    failure = result.failures[0].to_json()
    assert failure["comment_kind"] == "source_files"
    assert failure["expected_count"] == 50
    assert failure["observed_count"] == 0
    assert "No eligible Stack v2 comment kinds remain" in failure["reason"]
    assert "does not mark zero-target registry languages as complete" in failure["recommendation"]


def test_stack_v2_manifest_excludes_reviewed_sparse_corpus_buckets() -> None:
    excluded_buckets = {
        ("berry", "block"),
        ("cmake", "block"),
        ("genshi", "block"),
        ("html_ecr", "block"),
        ("liquid", "line"),
        ("openqasm", "block"),
        ("sieve", "block"),
    }

    for language, comment_kind in excluded_buckets:
        syntax = GENERATOR.get_comment_syntax(language)
        assert comment_kind not in GENERATOR._supported_comment_kinds(syntax, language)


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
    assert "does not by itself prove a parser or registry bug" in failure["recommendation"]


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


def test_local_jsonl_manifest_requires_n_cases_per_kind_within_m_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    sample = tmp_path / "sample.jsonl"
    records = [
        {
            "id": f"java-{index}",
            "language": "Java",
            "content": f"// java line {index}\nclass Demo {{ /* java block {index} */ }}\n",
        }
        for index in range(2)
    ]
    records.extend(
        {
            "id": f"haskell-{index}",
            "language": "Haskell",
            "content": f"-- haskell line {index}\nvalue = {index}\n"
            "{- outer {- inner -} outer -}\n",
        }
        for index in range(2)
    )
    with sample.open("w", encoding="utf-8") as outfile:
        for record in records:
            outfile.write(json.dumps(record) + "\n")

    expected_counts = {
        ("java", "line"): 2,
        ("java", "block"): 2,
        ("haskell", "line"): 2,
        ("haskell", "nested"): 2,
    }

    for language in ("java", "haskell"):
        output_root = tmp_path / f"out-{language}"
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "build_stack_v2_comment_judge_cases.py",
                "--input-jsonl",
                str(sample),
                "--languages",
                language,
                "--per-kind",
                "2",
                "--max-records-per-language",
                "4",
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
        actual_counts = {
            (language, kind): sum(
                1
                for row in manifest_rows
                if row["language"] == language and row["comment_kind"] == kind
            )
            for kind in {"line", "block", "nested"}
        }

        for bucket, expected_count in expected_counts.items():
            if bucket[0] == language:
                assert actual_counts[bucket] == expected_count
        assert not (output_root / "failures.jsonl").exists()


def test_local_jsonl_total_file_quota_uses_one_case_per_distinct_source(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    sample = tmp_path / "sample.jsonl"
    with sample.open("w", encoding="utf-8") as outfile:
        for index in range(4):
            outfile.write(
                json.dumps(
                    {
                        "id": f"java-{index}",
                        "language": "Java",
                        "content": (
                            f"// java line {index}\nclass Demo {{ /* java block {index} */ }}\n"
                        ),
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
            "java",
            "--files-per-language",
            "3",
            "--max-records-per-language",
            "4",
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
    assert len(manifest_rows) == 3
    assert {row["source_id"] for row in manifest_rows} == {
        "java-0",
        "java-1",
        "java-2",
    }
    assert len({row["source_file"] for row in manifest_rows}) == 3
    assert sorted(row["comment_kind"] for row in manifest_rows) == [
        "block",
        "line",
        "line",
    ]
    assert not (output_root / "failures.jsonl").exists()


def test_total_file_quota_stops_fetching_when_quota_is_full(tmp_path: Path) -> None:
    sample = tmp_path / "sample.jsonl"
    with sample.open("w", encoding="utf-8") as outfile:
        for index in range(100):
            outfile.write(
                json.dumps(
                    {
                        "id": f"java-{index}",
                        "language": "Java",
                        "content": f"// java line {index}\n",
                    }
                )
                + "\n"
            )
    source_root = tmp_path / "files"
    source_root.mkdir()
    args = _args(
        input_jsonl=sample,
        files_per_language=2,
        max_records_per_language=100,
    )

    result = GENERATOR._collect_language_cases(
        args=args,
        language="java",
        syntax=GENERATOR.get_comment_syntax("java"),
        target_kinds=("line", "block"),
        language_map={},
        source_root=source_root,
    )

    assert result.scanned_records == 2
    assert len(result.cases) == 2
    assert {case.comment_kind for case in result.cases} == {"line"}


def test_local_jsonl_total_file_quota_reports_incomplete_language(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    sample = tmp_path / "sample.jsonl"
    with sample.open("w", encoding="utf-8") as outfile:
        for index in range(2):
            outfile.write(
                json.dumps(
                    {
                        "id": f"java-{index}",
                        "language": "Java",
                        "content": (
                            f"// java line {index}\nclass Demo {{ /* java block {index} */ }}\n"
                        ),
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
            "java",
            "--files-per-language",
            "3",
            "--max-records-per-language",
            "4",
            "--output-root",
            str(output_root),
            "--no-progress",
        ],
    )

    assert GENERATOR.main() == 0

    failures = [
        json.loads(line)
        for line in (output_root / "failures.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert len(failures) == 1
    assert failures[0]["comment_kind"] == "source_files"
    assert failures[0]["expected_count"] == 3
    assert failures[0]["observed_count"] == 2
    assert failures[0]["observed_kinds"] == {"block": 1, "line": 1}


def test_local_jsonl_manifest_reports_missing_kinds_when_file_limit_is_too_low(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    sample = tmp_path / "sample.jsonl"
    with sample.open("w", encoding="utf-8") as outfile:
        for index in range(2):
            outfile.write(
                json.dumps(
                    {
                        "id": f"java-{index}",
                        "language": "Java",
                        "content": (
                            f"// java line {index}\nclass Demo {{ /* java block {index} */ }}\n"
                        ),
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
            "java",
            "--per-kind",
            "2",
            "--max-records-per-language",
            "1",
            "--output-root",
            str(output_root),
            "--no-progress",
        ],
    )

    assert GENERATOR.main() == 0

    failures = [
        json.loads(line)
        for line in (output_root / "failures.jsonl").read_text(encoding="utf-8").splitlines()
    ]

    assert {
        (failure["comment_kind"], failure["observed_count"], failure["expected_count"])
        for failure in failures
    } == {("line", 1, 2), ("block", 1, 2)}
    assert {failure["max_records_per_language"] for failure in failures} == {1}


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

    def fake_iter_records(args: Any, language: str, language_map: dict[str, Any]) -> Any:
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


def test_prefetch_content_errors_skip_record_and_continue(
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

    def fake_iter_records(args: Any, language: str, language_map: dict[str, Any]) -> Any:
        yield {
            "id": "java-1",
            "language": "Java",
            "blob_id": "abc",
            "src_encoding": "utf-8",
        }
        yield {
            "id": "java-2",
            "language": "Java",
            "content": "// java line\nclass Demo { /* java block */ }\n",
        }

    def fake_record_content(record: dict[str, Any], args: Any) -> str:
        if record["id"] == "java-2":
            return record["content"]
        raise GENERATOR._CorpusCollectionError("content endpoint unavailable")

    monkeypatch.setattr(GENERATOR, "_iter_records", fake_iter_records)
    monkeypatch.setattr(GENERATOR, "_record_content", fake_record_content)
    source_root = tmp_path / "files"
    source_root.mkdir()

    result = GENERATOR._collect_requested_language(
        args=args,
        language_index=1,
        language_count=1,
        language="java",
        language_map={},
        source_root=source_root,
    )

    assert [case.comment_kind for case in result.cases] == ["line", "block"]
    assert result.failures == []
