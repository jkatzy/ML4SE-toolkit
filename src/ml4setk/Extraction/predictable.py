"""Biderman et al., Emergent and Predictable Memorization in Large Language Models.

NeurIPS 2023. https://arxiv.org/abs/2304.11158
"""


def memorization_score(reference, continuation):
    """Fraction of aligned tokens that agree in two equal-length sequences (Equation 1)."""
    if len(reference) == 0 or len(reference) != len(continuation):
        raise ValueError("Expected nonempty sequences of equal length")
    return sum(int(a == b) for a, b in zip(reference, continuation)) / len(reference)


def memorization_overlap(predicted_ids, final_ids):
    """Precision and recall of a model's memorized IDs against a final checkpoint's IDs."""
    predicted, final = set(predicted_ids), set(final_ids)
    if not predicted or not final:
        raise ValueError("Both sets of memorized example IDs must be nonempty")
    common = len(predicted.intersection(final))
    return common / len(predicted), common / len(final)


def verify_pythia_records(token_rows, *, model=None):
    """Verify known 32-token continuations using the original Pythia-2.8B release."""
    import torch

    from .verbatim import verify_suffixes

    rows = torch.as_tensor(token_rows)
    if rows.ndim != 2 or rows.shape[1] != 64 or len(rows) == 0:
        raise ValueError("Expected a batch of complete 64-token benchmark records")
    if model is None:
        from transformers import AutoModelForCausalLM

        model = AutoModelForCausalLM.from_pretrained(
            "EleutherAI/pythia-2.8b-v0",
            revision="b9d8cace80b1a97f5ed380711aea31f2d1b24310",
            torch_dtype=torch.float16,
        ).to("cuda" if torch.cuda.is_available() else "cpu")
    return verify_suffixes(rows, prefix_length=32, model=model)
