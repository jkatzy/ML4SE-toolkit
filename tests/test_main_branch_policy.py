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
        "AGENTS.md",
        "docs/comment_research/chunk_0_nonalpha_a_report.md",
        "docs/comment_syntax_matrix.md",
        "tmp/scratch.txt",
        "notes.tmp",
        "src/ml4setk/__init__.py",
    ]

    assert MODULE.find_disallowed_paths(paths) == [
        "AGENTS.md",
        "docs/comment_research/chunk_0_nonalpha_a_report.md",
        "docs/comment_syntax_matrix.md",
        "notes.tmp",
        "tmp/scratch.txt",
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
