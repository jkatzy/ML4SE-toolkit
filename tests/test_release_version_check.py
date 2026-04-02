import importlib.util
from pathlib import Path

import pytest

pytestmark = pytest.mark.unit

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "check_release_version.py"
SPEC = importlib.util.spec_from_file_location("check_release_version", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def write_release_files(tmp_path: Path, *, pyproject_version: str, package_version: str) -> None:
    pyproject_path = tmp_path / "pyproject.toml"
    package_init_path = tmp_path / "src" / "ml4setk" / "__init__.py"
    package_init_path.parent.mkdir(parents=True)
    pyproject_path.write_text(
        f'[project]\nname = "ml4setk"\nversion = "{pyproject_version}"\n',
        encoding="utf-8",
    )
    package_init_path.write_text(
        f'__version__ = "{package_version}"\n',
        encoding="utf-8",
    )


def test_find_release_issues_passes_when_versions_and_tag_match(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    write_release_files(tmp_path, pyproject_version="0.0.2", package_version="0.0.2")
    monkeypatch.setattr(MODULE, "PYPROJECT_PATH", tmp_path / "pyproject.toml")
    monkeypatch.setattr(MODULE, "PACKAGE_INIT_PATH", tmp_path / "src" / "ml4setk" / "__init__.py")

    version, issues = MODULE.find_release_issues(tag="refs/tags/v0.0.2")

    assert version == "0.0.2"
    assert issues == []


def test_find_release_issues_flags_internal_version_mismatch(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    write_release_files(tmp_path, pyproject_version="0.0.2", package_version="0.0.3")
    monkeypatch.setattr(MODULE, "PYPROJECT_PATH", tmp_path / "pyproject.toml")
    monkeypatch.setattr(MODULE, "PACKAGE_INIT_PATH", tmp_path / "src" / "ml4setk" / "__init__.py")

    _, issues = MODULE.find_release_issues()

    assert issues == [
        "Version mismatch: pyproject.toml has 0.0.2, package __version__ has 0.0.3"
    ]


def test_find_release_issues_flags_tag_mismatch(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    write_release_files(tmp_path, pyproject_version="0.0.2", package_version="0.0.2")
    monkeypatch.setattr(MODULE, "PYPROJECT_PATH", tmp_path / "pyproject.toml")
    monkeypatch.setattr(MODULE, "PACKAGE_INIT_PATH", tmp_path / "src" / "ml4setk" / "__init__.py")

    _, issues = MODULE.find_release_issues(tag="v0.0.3")

    assert issues == [
        "Tag mismatch: expected v0.0.2 from pyproject.toml, got v0.0.3"
    ]


def test_normalize_tag_strips_github_prefix():
    assert MODULE.normalize_tag("refs/tags/v0.0.2") == "v0.0.2"
    assert MODULE.normalize_tag("v0.0.2") == "v0.0.2"
