import importlib.util
from pathlib import Path

import pytest

pytestmark = pytest.mark.unit

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "check_main_branch_policy.py"
SPEC = importlib.util.spec_from_file_location("check_main_branch_policy", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def test_find_disallowed_paths_flags_development_only_artifacts():
    paths = [
        ".idea/workspace.xml",
        "AGENTS.md",
        "docs/comment_research/chunk_0_nonalpha_a_report.md",
        "docs/comment_research/stack_v3_full/batch_00.md",
        "docs/comment_testing/chunk_0_findings.md",
        "docs/comment_testing/runs/stack_v3/findings.md",
        "docs/comment_syntax_matrix.md",
        "docs/two_stage_comment_cleaner_judge.md",
        "src/ml4setk/EBNF/RRD/.idea/misc.xml",
        "src/ml4setk/EBNF/RRD/generated/.idea/workspace.xml",
        "tmp/scratch.txt",
        "tmp/stack_v3/reports/result.json",
        "notes.tmp",
        "src/ml4setk/__init__.py",
    ]

    assert MODULE.find_disallowed_paths(paths) == [
        ".idea/workspace.xml",
        "AGENTS.md",
        "docs/comment_research/chunk_0_nonalpha_a_report.md",
        "docs/comment_research/stack_v3_full/batch_00.md",
        "docs/comment_syntax_matrix.md",
        "docs/comment_testing/chunk_0_findings.md",
        "docs/comment_testing/runs/stack_v3/findings.md",
        "docs/two_stage_comment_cleaner_judge.md",
        "notes.tmp",
        "src/ml4setk/EBNF/RRD/.idea/misc.xml",
        "src/ml4setk/EBNF/RRD/generated/.idea/workspace.xml",
        "tmp/scratch.txt",
        "tmp/stack_v3/reports/result.json",
    ]


def test_find_disallowed_paths_ignores_normal_repository_files():
    paths = [
        "README.md",
        "docs/comment_extractor.md",
        "scripts/build_comment_research_views.py",
        "src/ml4setk/Parsing/Comments/registry.py",
        "tests/test_comment_queries.py",
    ]

    assert MODULE.find_disallowed_paths(paths) == []
