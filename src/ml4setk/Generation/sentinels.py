"""Resolve a model's FIM sentinel or diffusion mask tokens from a name or HF object."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SentinelTokens:
    """FIM sentinel strings and the order the prompt sections are laid out in.

    ``order`` is ``"psm"`` (prefix, suffix, middle) or ``"spm"``
    (suffix, prefix, middle).
    """

    prefix: str
    suffix: str
    middle: str
    order: str = "psm"


_STARCODER = SentinelTokens("<fim_prefix>", "<fim_suffix>", "<fim_middle>")
_PIPE_FIM = SentinelTokens("<|fim_prefix|>", "<|fim_suffix|>", "<|fim_middle|>")

# Checked in order against the lowercased model name (and HF ``model_type``);
# the first entry whose every fragment appears wins.
MODEL_SENTINELS = (
    (("santacoder",), SentinelTokens("<fim-prefix>", "<fim-suffix>", "<fim-middle>")),
    (("starcoder",), _STARCODER),
    (("gpt_bigcode",), _STARCODER),
    (("stable-code",), _STARCODER),
    (("granite", "code"), _STARCODER),
    (("codellama",), SentinelTokens("<PRE> ", " <SUF>", " <MID>")),
    (("code-llama",), SentinelTokens("<PRE> ", " <SUF>", " <MID>")),
    (
        ("deepseek", "coder"),
        SentinelTokens("<｜fim▁begin｜>", "<｜fim▁hole｜>", "<｜fim▁end｜>"),
    ),
    (("qwen", "coder"), _PIPE_FIM),
    (("codegemma",), _PIPE_FIM),
    (("codestral",), SentinelTokens("[PREFIX]", "[SUFFIX]", "", order="spm")),
)

# Mask tokens of masked diffusion LLMs, matched the same way. ``dream`` covers
# Dream, Dream-Coder and DreamOn, and DiffuCoder's ``model_type`` ("Dream").
MODEL_MASK_TOKENS = (
    (("llada",), "<|mdm_mask|>"),
    (("dream",), "<|mask|>"),
    (("diffucoder",), "<|mask|>"),
)


def _model_names(model):
    if isinstance(model, str):
        return [model]
    config = getattr(model, "config", None)
    names = [
        getattr(model, "name_or_path", None),
        getattr(config, "_name_or_path", None),
        getattr(config, "model_type", None),
    ]
    return [name for name in names if isinstance(name, str) and name]


def _tokenizer_vocab(model):
    for candidate in (model, getattr(model, "tokenizer", None)):
        get_vocab = getattr(candidate, "get_vocab", None)
        if callable(get_vocab):
            return get_vocab()
    return None


def _in_vocab(token, vocab):
    stripped = token.strip()
    return not stripped or stripped in vocab or "▁" + stripped in vocab


def _resolve(model, registry, tokens_of):
    for name in _model_names(model):
        lowered = name.lower()
        for fragments, entry in registry:
            if all(fragment in lowered for fragment in fragments):
                return entry

    vocab = _tokenizer_vocab(model)
    if vocab:
        for _fragments, entry in registry:
            if all(_in_vocab(token, vocab) for token in tokens_of(entry)):
                return entry
    return None


def get_sentinel_tokens(model):
    """Return the :class:`SentinelTokens` for ``model``.

    ``model`` may be a model name such as ``"bigcode/starcoder2-3b"``, or a
    Hugging Face model, tokenizer, or pipeline. Names are matched against the
    built-in ``MODEL_SENTINELS`` registry first; otherwise, when a tokenizer is
    available, the first registry entry whose tokens are all in its vocabulary
    is used.
    """

    tokens = _resolve(model, MODEL_SENTINELS, lambda t: (t.prefix, t.suffix, t.middle))
    if tokens is None:
        raise ValueError(
            f"Could not resolve FIM sentinel tokens for {model!r}. "
            "Pass the tokens to FIMInput explicitly."
        )
    return tokens


def get_mask_token(model):
    """Return the diffusion mask token for ``model``, resolved like
    :func:`get_sentinel_tokens` but against ``MODEL_MASK_TOKENS``."""

    token = _resolve(model, MODEL_MASK_TOKENS, lambda t: (t,))
    if token is None:
        raise ValueError(
            f"Could not resolve a diffusion mask token for {model!r}. "
            "Pass the mask token explicitly."
        )
    return token
