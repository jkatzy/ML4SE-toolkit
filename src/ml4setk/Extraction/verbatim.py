"""Known-suffix verification from Carlini et al., Quantifying Memorization Across
Neural Language Models, ICLR 2023. https://openreview.net/forum?id=TatRHT_1cK
"""


def verify_suffixes(token_rows, *, prefix_length, model=None):
    """Return one bool per complete token sequence using a local causal LM in eval mode.

    The default is the paper's GPT-Neo-2.7B configuration. Pass a compatible
    evaluation-mode model and its already-tokenized inputs to use another checkpoint.
    The caller supplies the full reference. Only agreement flags leave this function.
    """
    import torch

    ids = torch.as_tensor(token_rows)
    if ids.ndim != 2 or ids.shape[0] == 0 or not 0 < prefix_length < ids.shape[1]:
        raise ValueError("Expected a nonempty batch with a prefix and a nonempty suffix")
    if ids.dtype not in (torch.int32, torch.int64):
        raise ValueError("Expected integer token IDs")
    if model is None:
        from transformers import AutoModelForCausalLM

        model = AutoModelForCausalLM.from_pretrained(
            "EleutherAI/gpt-neo-2.7B", revision="e24fa291132763e59f4a5422741b424fb5d59056"
        ).to("cuda" if torch.cuda.is_available() else "cpu")
    if model.training:
        raise ValueError("Set the model to evaluation mode")
    ids = ids.to(model.device)
    with torch.inference_mode():
        logits = model(ids[:, :-1], use_cache=False).logits[:, prefix_length - 1 :]
        return logits.argmax(-1).eq(ids[:, prefix_length:]).all(dim=1).tolist()
