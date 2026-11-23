"""Koohestani et al. (FSE Companion 2026), Table 1 baselines and RQ2/RQ3 stratum comparisons."""

import pytest


@pytest.mark.parametrize("method", ["loss", "pac", "pac_ast"])
def test_fse_paper(method, artifact, model_name, fse_cohort, fse_checkpoint, pytestconfig):
    from fse import score_and_compare

    score_and_compare(
        artifact,
        model_name,
        fse_cohort,
        fse_checkpoint,
        method,
        pytestconfig,
    )
