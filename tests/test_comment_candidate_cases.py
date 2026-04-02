import csv
import re
from dataclasses import dataclass
from pathlib import Path

import pytest

from ml4setk import CommentQuery, QueryMatch
from ml4setk.Parsing.Comments import SUPPORTED_LANGUAGES

pytestmark = pytest.mark.unit

ROOT = Path(__file__).resolve().parents[1]
RESEARCH_DIR = ROOT / "docs" / "comment_research"
CANDIDATE_CSV_PATH = RESEARCH_DIR / "registry_ready_candidates.csv"
SECTION_RE = re.compile(r"^##\s+(.+?)\s*$")
FIELD_RE = re.compile(r"^-\s+([^:]+):\s*(.*)$")
EXAMPLE_HEADING_RE = re.compile(r"^####\s+(.+?)\s*$")
BACKTICK_TOKEN_RE = re.compile(r"`([^`]+)`")
SUPPORTED_LANGUAGE_KEYS = set(SUPPORTED_LANGUAGES)
UNSUPPORTED_VALUES = {"", "unsupported", "unresolved", "unknown", "no"}
RAW_LINE_TOKENS = (
    "//-",
    "///",
    "###",
    "##",
    "//",
    ";;",
    "--",
    "*>",
    "::",
    "REM",
    "#",
    ";",
    "%",
    "!",
    "'",
    '"',
    "⍝",
    "*",
)
LINE_TOKEN_OVERRIDES = {
    "jsp": ("<%-- ... --%>",),
    "liquid": ("{% # ... %}",),
    "mustache": ("{{! ... }}",),
    "roff": ('\\"',),
    "roff_manpage": ('\\"',),
}


@dataclass(frozen=True)
class CandidateLanguageSpec:
    language: str
    query_language: str
    fields: dict[str, str]
    examples: dict[str, str]
    report_file: str


@dataclass(frozen=True)
class CandidateCommentCase:
    language: str
    query_language: str
    kind: str
    sample: str
    expected_match: str
    case_id: str


def _expected_query_match(sample, expected_match):
    start = sample.index(expected_match)
    end = start + len(expected_match)
    return QueryMatch(sample[:start], sample[end:], expected_match)


def _normalize_text(value):
    return value.strip().strip("`").strip()


def _load_report_sections():
    reports = {}
    for path in RESEARCH_DIR.glob("chunk_*_report.md"):
        sections = {}
        current = None
        current_heading = None
        in_code_block = False
        code_lines = []

        for line in path.read_text(encoding="utf-8").splitlines():
            section_match = SECTION_RE.match(line)
            if section_match:
                current = {"fields": {}, "examples": {}}
                sections[section_match.group(1)] = current
                current_heading = None
                in_code_block = False
                code_lines = []
                continue

            if current is None:
                continue

            if in_code_block:
                if line.startswith("```"):
                    current["examples"][current_heading] = "\n".join(code_lines)
                    in_code_block = False
                    code_lines = []
                else:
                    code_lines.append(line)
                continue

            field_match = FIELD_RE.match(line)
            if field_match:
                current["fields"][field_match.group(1)] = field_match.group(2)
                continue

            example_heading_match = EXAMPLE_HEADING_RE.match(line)
            if example_heading_match:
                current_heading = example_heading_match.group(1)
                continue

            if line.startswith("```") and current_heading:
                in_code_block = True
                code_lines = []

        reports[str(path.relative_to(ROOT))] = sections

    return reports


def _load_candidate_specs():
    reports = _load_report_sections()
    specs = []
    with CANDIDATE_CSV_PATH.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            section = reports[row["report_file"]][row["language"]]
            specs.append(
                CandidateLanguageSpec(
                    language=row["language"],
                    query_language=row["registry_key"],
                    fields=section["fields"],
                    examples=section["examples"],
                    report_file=row["report_file"],
                )
            )
    return specs


def _extract_backtick_tokens(text):
    return [_normalize_text(token) for token in BACKTICK_TOKEN_RE.findall(text)]


def _extract_raw_line_tokens(text):
    tokens = []
    for token in RAW_LINE_TOKENS:
        if token in text and token not in tokens:
            tokens.append(token)
    return tokens


def _line_tokens(spec):
    override_tokens = LINE_TOKEN_OVERRIDES.get(spec.query_language)
    if override_tokens is not None:
        return list(override_tokens)

    text = spec.fields.get("Line comments", "")
    tokens = [
        token for token in _extract_backtick_tokens(text) if token.lower() not in UNSUPPORTED_VALUES
    ]
    if tokens:
        return tokens
    normalized = _normalize_text(text)
    if normalized.lower() in UNSUPPORTED_VALUES:
        return []
    if normalized.startswith("*") and normalized.endswith(";"):
        return ["*"]
    return _extract_raw_line_tokens(normalized)


def _standalone_line_token(spec):
    line_desc = spec.fields.get("Line comments", "")
    termination_desc = spec.fields.get("Termination behavior", "")
    lower_line_desc = line_desc.lower()
    lower_termination_desc = termination_desc.lower()

    if "dedent" in lower_termination_desc:
        return None

    tokens = _line_tokens(spec)
    if "column 1" in lower_line_desc and "*" in tokens:
        return "*"

    return tokens[0] if tokens else None


def _render_line_comment(token, text):
    token = _normalize_text(token)
    if "..." in token:
        return token.replace("...", text)
    return f"{token} {text}"


def _inline_line_token(spec):
    line_desc = spec.fields.get("Line comments", "")
    termination_desc = spec.fields.get("Termination behavior", "")
    lower_line_desc = line_desc.lower()
    lower_termination_desc = termination_desc.lower()

    if spec.query_language == "haml":
        return None

    blockers = (
        "beginning of a line",
        "column 1",
        "whole comment",
        "line-oriented",
        "inline comments are not part",
        "dedent",
    )

    if any(blocker in lower_line_desc or blocker in lower_termination_desc for blocker in blockers):
        if "column 1" in lower_line_desc and '"' in _line_tokens(spec):
            return '"'
        return None

    for token in _line_tokens(spec):
        if token in {"*", "REM", "::"}:
            continue
        return token

    return None


def _parse_block_token(token):
    token = _normalize_text(token)
    if not token or token.lower() in UNSUPPORTED_VALUES:
        return None
    if "..." in token:
        open_delim, close_delim = [part.strip() for part in token.split("...", 1)]
        if open_delim and close_delim:
            return open_delim, close_delim
    if token in {"/* */", "(* *)", "<!-- -->", "#| |#"}:
        open_delim, close_delim = token.split()
        return open_delim, close_delim
    if token == "////":
        return token, token
    if token.startswith("#'(") and token.endswith(")"):
        return "#'(", ")"
    if token.startswith("#'{") and token.endswith("}"):
        return "#'{", "}"
    if token.startswith("#'[") and token.endswith("]"):
        return "#'[", "]"
    if token.startswith("#'<") and token.endswith(">"):
        return "#'<", ">"
    if token.startswith("(") and token.endswith(")") and " " in token:
        open_delim, close_delim = token.split()
        return open_delim, close_delim
    return None


def _block_delimiters(spec):
    block_desc = spec.fields.get("Block comments", "")
    for token in _extract_backtick_tokens(block_desc):
        parsed = _parse_block_token(token)
        if parsed:
            return parsed

    normalized = _normalize_text(block_desc)
    if normalized.lower() in UNSUPPORTED_VALUES:
        return None

    return _parse_block_token(normalized)


def _build_line_case(spec):
    token = _standalone_line_token(spec)
    if token is None:
        return None

    expected_match = _render_line_comment(token, "note")
    sample = f"{expected_match}\nafter"
    return CandidateCommentCase(
        language=spec.language,
        query_language=spec.query_language,
        kind="single_line",
        sample=sample,
        expected_match=expected_match,
        case_id=f"{spec.query_language}-candidate-single-line",
    )


def _build_grouped_line_case(spec):
    token = _standalone_line_token(spec)
    if token is None:
        return None

    expected_match = "\n".join(
        (
            _render_line_comment(token, "first note"),
            _render_line_comment(token, "second note"),
        )
    )
    sample = f"{expected_match}\nafter"
    return CandidateCommentCase(
        language=spec.language,
        query_language=spec.query_language,
        kind="grouped_line",
        sample=sample,
        expected_match=expected_match,
        case_id=f"{spec.query_language}-candidate-grouped-line",
    )


def _build_inline_case(spec):
    line_token = _inline_line_token(spec)
    if line_token is not None:
        expected_match = _render_line_comment(line_token, "inline note")
        sample = f"value = 1 {expected_match}\nreturn value"
        return CandidateCommentCase(
            language=spec.language,
            query_language=spec.query_language,
            kind="inline",
            sample=sample,
            expected_match=expected_match,
            case_id=f"{spec.query_language}-candidate-inline",
        )

    block_delimiters = _block_delimiters(spec)
    if block_delimiters is None:
        return None

    open_delim, close_delim = block_delimiters
    if open_delim == close_delim or open_delim in {"#cs", "=begin", "=pod"}:
        return None

    expected_match = f"{open_delim} inline note {close_delim}"
    sample = f"value = 1 {expected_match} return value"
    return CandidateCommentCase(
        language=spec.language,
        query_language=spec.query_language,
        kind="inline",
        sample=sample,
        expected_match=expected_match,
        case_id=f"{spec.query_language}-candidate-inline",
    )


def _build_special_block_case(spec):
    if spec.language == "Pug":
        sample = spec.examples["Block comment"]
        expected_match = "  //- template writers note\n    this line stays inside the comment block"
        return CandidateCommentCase(
            language=spec.language,
            query_language=spec.query_language,
            kind="block",
            sample=sample,
            expected_match=expected_match,
            case_id=f"{spec.query_language}-candidate-block",
        )

    if spec.language == "reStructuredText":
        sample = spec.examples["Block comment"]
        expected_match = ".. keep the next paragraph hidden"
        return CandidateCommentCase(
            language=spec.language,
            query_language=spec.query_language,
            kind="block",
            sample=sample,
            expected_match=expected_match,
            case_id=f"{spec.query_language}-candidate-block",
        )

    if spec.language == "q":
        sample = spec.examples["Block comment"]
        expected_match = "/\nkeep the next assignment explicit\n\\"
        return CandidateCommentCase(
            language=spec.language,
            query_language=spec.query_language,
            kind="block",
            sample=sample,
            expected_match=expected_match,
            case_id=f"{spec.query_language}-candidate-block",
        )

    return None


def _build_block_case(spec):
    if "Block comment" in spec.examples and spec.language in {"Pug", "q", "reStructuredText"}:
        return _build_special_block_case(spec)

    block_delimiters = _block_delimiters(spec)
    if block_delimiters is None:
        return None

    open_delim, close_delim = block_delimiters
    if open_delim == close_delim or open_delim in {"#cs", "=begin", "=pod"}:
        expected_match = f"{open_delim}\nblock note\n{close_delim}"
        sample = f"before\n{expected_match}\nafter"
    else:
        expected_match = f"{open_delim} block note {close_delim}"
        sample = f"before {expected_match} after"

    return CandidateCommentCase(
        language=spec.language,
        query_language=spec.query_language,
        kind="block",
        sample=sample,
        expected_match=expected_match,
        case_id=f"{spec.query_language}-candidate-block",
    )


def _build_nested_case(spec):
    nested_desc = spec.fields.get("Nested comments", "").lower()
    is_nested_supported = nested_desc in {"yes", "supported"} or nested_desc.endswith(
        " is supported"
    ) or nested_desc.endswith(" are supported")
    if not is_nested_supported:
        return None

    block_delimiters = _block_delimiters(spec)
    if block_delimiters is None:
        if "Nested comment" not in spec.examples:
            return None
        sample = spec.examples["Nested comment"]
        if spec.query_language == "e_mail":
            expected_match = "(team (platform))"
            return CandidateCommentCase(
                language=spec.language,
                query_language=spec.query_language,
                kind="nested",
                sample=sample,
                expected_match=expected_match,
                case_id=f"{spec.query_language}-candidate-nested",
            )
        first_line = sample.splitlines()[0]
        expected_match = first_line[first_line.index("(") :]
        return CandidateCommentCase(
            language=spec.language,
            query_language=spec.query_language,
            kind="nested",
            sample=sample,
            expected_match=expected_match,
            case_id=f"{spec.query_language}-candidate-nested",
        )

    open_delim, close_delim = block_delimiters
    if open_delim == close_delim:
        return None

    expected_match = (
        f"{open_delim} outer {open_delim} inner {close_delim} outer {close_delim}"
    )
    sample = f"before {expected_match} after"
    return CandidateCommentCase(
        language=spec.language,
        query_language=spec.query_language,
        kind="nested",
        sample=sample,
        expected_match=expected_match,
        case_id=f"{spec.query_language}-candidate-nested",
    )


def _build_candidate_cases():
    specs = _load_candidate_specs()
    grouped_cases = {
        "single_line": [],
        "grouped_line": [],
        "inline": [],
        "block": [],
        "nested": [],
    }

    for spec in specs:
        for builder in (
            _build_line_case,
            _build_grouped_line_case,
            _build_inline_case,
            _build_block_case,
            _build_nested_case,
        ):
            case = builder(spec)
            if case is not None:
                grouped_cases[case.kind].append(case)

    return specs, grouped_cases


CANDIDATE_SPECS, GROUPED_CASES = _build_candidate_cases()
SINGLE_LINE_CASES = GROUPED_CASES["single_line"]
GROUPED_LINE_CASES = GROUPED_CASES["grouped_line"]
INLINE_CASES = GROUPED_CASES["inline"]
BLOCK_CASES = GROUPED_CASES["block"]
NESTED_CASES = GROUPED_CASES["nested"]
ALL_CASES = [
    *SINGLE_LINE_CASES,
    *GROUPED_LINE_CASES,
    *INLINE_CASES,
    *BLOCK_CASES,
    *NESTED_CASES,
]


def _covered_languages(cases):
    return {case.language for case in cases}


def _assert_candidate_case(case):
    if case.query_language not in SUPPORTED_LANGUAGE_KEYS:
        pytest.xfail(f"Candidate language not yet implemented: {case.query_language}")

    query = CommentQuery(case.query_language)
    assert query.contains(case.sample) is True
    assert query.parse(case.sample) == [_expected_query_match(case.sample, case.expected_match)]


def test_candidate_case_inventory_covers_all_registry_ready_languages():
    assert _covered_languages(ALL_CASES) == {spec.language for spec in CANDIDATE_SPECS}


@pytest.mark.parametrize("case", SINGLE_LINE_CASES, ids=lambda case: case.case_id)
def test_candidate_single_line_cases(case):
    _assert_candidate_case(case)


@pytest.mark.parametrize("case", GROUPED_LINE_CASES, ids=lambda case: case.case_id)
def test_candidate_grouped_line_cases(case):
    _assert_candidate_case(case)


@pytest.mark.parametrize("case", INLINE_CASES, ids=lambda case: case.case_id)
def test_candidate_inline_cases(case):
    _assert_candidate_case(case)


@pytest.mark.parametrize("case", BLOCK_CASES, ids=lambda case: case.case_id)
def test_candidate_block_cases(case):
    _assert_candidate_case(case)


@pytest.mark.parametrize("case", NESTED_CASES, ids=lambda case: case.case_id)
def test_candidate_nested_cases(case):
    _assert_candidate_case(case)
