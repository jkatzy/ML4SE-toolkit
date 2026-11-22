"""Shared fixtures for the opt-in paper reproductions."""

import os
import sys
from pathlib import Path

import pytest

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


def pytest_generate_tests(metafunc):
    if "model_name" in metafunc.fixturenames:
        chosen = metafunc.config.getoption("--fse-model")
        metafunc.parametrize(
            "model_name",
            [chosen] if chosen else ["SC2-3B", "SC2-7B", "mellum", "smollm"],
            scope="module",
        )


@pytest.fixture(scope="session")
def artifact(pytestconfig):
    root = pytestconfig.getoption("--fse-artifact")
    if not root:
        pytest.fail("Supply the extracted FSE data with --fse-artifact or ML4SETK_AST_PAC_ARTIFACT")
    return Path(root)


@pytest.fixture(scope="module")
def fse_cohort(artifact, model_name, pytestconfig):
    from fse import source_rows

    return source_rows(artifact, model_name, pytestconfig.getoption("--fse-pilot"))


@pytest.fixture(scope="module")
def fse_checkpoint(model_name):
    import torch
    from fse_cohort import SNAPSHOTS
    from transformers import AutoModelForCausalLM, AutoTokenizer

    repo, revision = SNAPSHOTS[model_name]
    tokenizer = AutoTokenizer.from_pretrained(repo, revision=revision)
    model = (
        AutoModelForCausalLM.from_pretrained(
            repo, revision=revision, torch_dtype=torch.float16, attn_implementation="sdpa"
        )
        .eval()
        .to("cuda")
    )
    return model, tokenizer
