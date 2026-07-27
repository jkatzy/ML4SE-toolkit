import importlib.util
import sys
import warnings
from pathlib import Path

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


def test_seeded_unicode_fuzz_contracts_hold_across_registry():
    fuzzer = _load_fuzzer()
    run = fuzzer.run_fuzz(
        seed=fuzzer.DEFAULT_SEED,
        cases_per_language=8,
        max_length=64,
        max_failures=1,
    )

    assert run.cases == run.languages * 8
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
