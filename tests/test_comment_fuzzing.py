import importlib.util
import random
import sys
import warnings
from pathlib import Path

import pytest

from ml4setk import CommentQuery, CommentSanitizer
from ml4setk.Parsing.Comments import iter_comment_syntaxes

_BODY_PLACEHOLDERS = (
    "Remember the bull.",
    "Visible content",
    "block note",
    "inline note",
    "+ 100",
    "note",
)
_NON_ENGLISH_PAYLOAD = (
    "\u6ce8\u91c8"
    "\u041f\u0440\u0438\u043c\u0435\u0447\u0430\u043d\u0438\u0435"
    "\u0645\u0644\u0627\u062d\u0638\u0629"
    "\U0001f9ea"
    "e\u0301"
)


def _load_fuzzer():
    script_path = (
        Path(__file__).resolve().parents[1] / "scripts" / "fuzz_comment_parsers.py"
    )
    spec = importlib.util.spec_from_file_location("comment_parser_fuzzer", script_path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_seeded_unicode_parser_and_sanitizer_fuzz_contracts_hold_across_registry():
    fuzzer = _load_fuzzer()
    run = fuzzer.run_fuzz(
        seed=fuzzer.DEFAULT_SEED,
        cases_per_language=8,
        max_length=64,
        max_failures=1,
        sanitizer_payloads_per_example=2,
    )

    assert run.cases == run.languages * 8
    assert run.parser_cases == run.languages * 8
    assert run.sanitizer_random_cases == run.languages * 8
    assert run.sanitizer_structured_cases > 2_000
    assert run.failures == ()


def test_non_english_payload_mutations_survive_extraction_and_sanitization():
    cases = 0
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for syntax in iter_comment_syntaxes():
            for language in syntax.language_names:
                examples = [
                    *syntax.shared_regex_examples,
                    *syntax.shared_nested_examples,
                    *syntax.shared_contextual_examples,
                ]
                if language == syntax.canonical_name:
                    examples.extend(syntax.canonical_regex_examples)
                    examples.extend(syntax.canonical_nested_examples)
                    examples.extend(syntax.canonical_contextual_examples)

                for example in examples:
                    placeholder = next(
                        (
                            candidate
                            for candidate in _BODY_PLACEHOLDERS
                            if candidate in example.expected_match
                        ),
                        None,
                    )
                    if placeholder is None:
                        continue

                    expected = example.expected_match.replace(
                        placeholder, _NON_ENGLISH_PAYLOAD, 1
                    )
                    sample = example.sample.replace(
                        example.expected_match, expected, 1
                    )
                    matches = CommentQuery(language).parse(sample)
                    exact_matches = [
                        match for match in matches if match.match == expected
                    ]

                    assert exact_matches, (language, expected, matches)
                    assert _NON_ENGLISH_PAYLOAD in CommentSanitizer(
                        language
                    ).sanitize(exact_matches[0])
                    cases += 1

    assert cases > 900


@pytest.mark.parametrize(
    ("campaign", "runs_parser", "runs_sanitizer"),
    (
        ("all", True, True),
        ("parser", True, False),
        ("sanitizer", False, True),
    ),
)
def test_fuzz_campaigns_report_separate_case_counters(
    campaign,
    runs_parser,
    runs_sanitizer,
):
    fuzzer = _load_fuzzer()
    run = fuzzer.run_fuzz(
        languages=("figlet_font", "java"),
        seed=1234,
        cases_per_language=3,
        max_length=32,
        max_failures=1,
        campaign=campaign,
        sanitizer_payloads_per_example=0,
    )

    assert run.campaign == campaign
    assert run.cases == 6
    assert run.parser_cases == (6 if runs_parser else 0)
    assert run.sanitizer_random_cases == (6 if runs_sanitizer else 0)
    assert run.sanitizer_structured_cases == (2 if runs_sanitizer else 0)
    assert run.failures == ()


def test_parser_and_sanitizer_fuzz_streams_are_stable_and_independent():
    fuzzer = _load_fuzzer()

    parser_seed = fuzzer._stable_campaign_seed(1234, "java", "parser")
    sanitizer_seed = fuzzer._stable_campaign_seed(
        1234,
        "java",
        "sanitizer_random",
    )
    structured_seed = fuzzer._stable_campaign_seed(
        1234,
        "java",
        "sanitizer_structured",
    )

    assert parser_seed == fuzzer._stable_language_seed(1234, "java")
    assert len({parser_seed, sanitizer_seed, structured_seed}) == 3
    assert sanitizer_seed == fuzzer._stable_campaign_seed(
        1234,
        "java",
        "sanitizer_random",
    )


def test_structured_sanitizer_fuzzing_includes_safe_wrapper_and_newline_mutations():
    fuzzer = _load_fuzzer()

    mutation_names = set()
    for language in ("autoit", "beef", "pogoscript"):
        cases = fuzzer._iter_structured_sanitizer_cases(
            CommentSanitizer(language),
            random.Random(1234),
            0,
        )
        mutation_names.update(mutation for mutation, _, _ in cases)

    assert any(name.startswith("nested_wrapper:") for name in mutation_names)
    assert any(name.startswith("unclosed_wrapper:") for name in mutation_names)
    assert any(name.startswith("newline_crlf:") for name in mutation_names)
    assert any(name.startswith("newline_cr:") for name in mutation_names)


def test_sanitizer_fuzz_contract_does_not_assume_idempotence_or_delimiter_absence():
    fuzzer = _load_fuzzer()
    sanitizer = CommentSanitizer("java")

    fuzzer._check_sanitizer_case("java", sanitizer, "// // note")
    fuzzer._check_sanitizer_case(
        "java",
        sanitizer,
        "// visit https://example.test/a//b",
    )

    cleaned_once = sanitizer.sanitize("// // note")
    assert sanitizer.sanitize(cleaned_once) != cleaned_once
    assert "//" in sanitizer.sanitize("// visit https://example.test/a//b")


def test_sanitizer_failure_records_actionable_provenance(monkeypatch):
    fuzzer = _load_fuzzer()

    def reject_case(*args, **kwargs):
        raise fuzzer._InvariantFailure("forced_cleaner_invariant", "forced detail")

    monkeypatch.setattr(fuzzer, "_check_sanitizer_case", reject_case)
    run = fuzzer.run_fuzz(
        languages=("java",),
        cases_per_language=1,
        campaign="sanitizer",
        sanitizer_payloads_per_example=0,
        max_failures=1,
    )

    assert len(run.failures) == 1
    failure = run.failures[0]
    assert failure.campaign == "sanitizer"
    assert failure.mutation == "random_text"
    assert failure.invariant == "forced_cleaner_invariant"
    assert failure.detail == "forced detail"
