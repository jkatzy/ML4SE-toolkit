"""Koohestani et al. (FSE Companion 2026), RQ3, with fixed published neighbor texts."""


def test_fse_ast_pac(artifact, model_name, fse_cohort, fse_checkpoint, pytestconfig):
    from fse import score_and_compare

    score_and_compare(
        artifact,
        model_name,
        fse_cohort,
        fse_checkpoint,
        "pac_ast",
        pytestconfig,
    )
