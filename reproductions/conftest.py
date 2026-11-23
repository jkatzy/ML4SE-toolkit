"""Shared fixtures for the opt-in paper reproductions."""

import os
import sys
from pathlib import Path

# Import the toolkit's benchmark helpers from the checkout, never from an artifact.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))


def pytest_addoption(parser):
    parser.addoption("--fse-artifact", default=os.environ.get("ML4SETK_AST_PAC_ARTIFACT"))
    parser.addoption(
        "--fse-paper",
        default=os.environ.get("ML4SETK_FSE_PDF"),
        help="Final proceedings PDF for Table 1",
    )
    parser.addoption(
        "--exact-fse",
        action="store_true",
        help="Also require equality at printed precision for every FSE area",
    )
    parser.addoption("--fse-model", choices=("SC2-3B", "SC2-7B", "mellum", "smollm"))
    parser.addoption(
        "--fse-pilot", action="store_true", help="Score the 225-file published stratum"
    )
