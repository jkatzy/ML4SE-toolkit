# Input formatting

Every query returns a `QueryMatch(prefix, suffix, match)`. An input formatter
turns that match into a `(model_input, ground_truth)` pair, where the ground
truth is always `match`. This page covers the two formatters for code models:
`FIMInput` for fill-in-the-middle (FIM) prompts and `CausalInput` for
autoregressive (AR) prompts.

## Quick start

```python
from ml4setk import CausalInput, FIMInput, QueryMatch

match = QueryMatch(prefix="def add(a, b):\n    ", suffix="\n", match="return a + b")

fim = FIMInput.from_model("bigcode/starcoder2-3b")
model_input, ground_truth = fim.generate(match)
assert model_input == "<fim_prefix>def add(a, b):\n    <fim_suffix>\n<fim_middle>"
assert ground_truth == "return a + b"

model_input, ground_truth = CausalInput().generate(match)
assert model_input == "def add(a, b):\n    "
assert ground_truth == "return a + b"
```

Any query output works in place of the hand-built `QueryMatch`, for example a
match from [`CommentQuery`](comment_extractor.md). `generate` also accepts a
plain `(prefix, suffix, match)` tuple.

## Fill-in-the-middle prompts

A FIM prompt shows the model the code on both sides of a hole, marked by three
sentinel tokens, and asks it to produce the middle. Each model family uses its
own sentinel strings, so a prompt built with the wrong ones is out of
distribution for the model.

### Picking tokens from a model

`FIMInput.from_model(model)` looks up the sentinel tokens and prompt order for
`model`, which can be:

- a model name, such as `"bigcode/starcoder2-3b"`;
- a Hugging Face model, matched by its `name_or_path` or `config.model_type`;
- a Hugging Face tokenizer or pipeline, matched by name first and then by
  its vocabulary (see [Tokenizer fallback](#tokenizer-fallback)).

```python
from transformers import AutoTokenizer

from ml4setk import FIMInput

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-Coder-1.5B")
fim = FIMInput.from_model(tokenizer)
```

`get_sentinel_tokens(model)` returns the resolved `SentinelTokens(prefix,
suffix, middle, order)` without building a formatter, which is useful for
logging or for passing the tokens to another tool.

### Sentinel-token registry

`MODEL_SENTINELS` in `ml4setk.Generation.sentinels` maps name fragments to
token sets. The model name and `model_type` are lowercased, the registry is
checked top to bottom, and the first entry whose fragments all appear in the
name wins.

| Family | Matched by | Prefix, suffix, middle | Order |
| --- | --- | --- | --- |
| SantaCoder | `santacoder` | `<fim-prefix>`, `<fim-suffix>`, `<fim-middle>` | PSM |
| StarCoder, StarCoder2 | `starcoder`, `gpt_bigcode` | `<fim_prefix>`, `<fim_suffix>`, `<fim_middle>` | PSM |
| Stable Code | `stable-code` | `<fim_prefix>`, `<fim_suffix>`, `<fim_middle>` | PSM |
| Granite Code | `granite` and `code` | `<fim_prefix>`, `<fim_suffix>`, `<fim_middle>` | PSM |
| Code Llama | `codellama`, `code-llama` | `<PRE> `, ` <SUF>`, ` <MID>` | PSM |
| DeepSeek-Coder | `deepseek` and `coder` | `<｜fim▁begin｜>`, `<｜fim▁hole｜>`, `<｜fim▁end｜>` | PSM |
| Qwen-Coder | `qwen` and `coder` | `<|fim_prefix|>`, `<|fim_suffix|>`, `<|fim_middle|>` | PSM |
| CodeGemma | `codegemma` | `<|fim_prefix|>`, `<|fim_suffix|>`, `<|fim_middle|>` | PSM |
| Codestral | `codestral` | `[PREFIX]`, `[SUFFIX]`, empty | SPM |

The Code Llama tokens carry their surrounding spaces, as the model expects.

### Tokenizer fallback

When no registry entry matches the name, `from_model` looks for a tokenizer
vocabulary: it calls `get_vocab()` on the object itself or on its `tokenizer`
attribute, as a pipeline has. It then picks the first registry entry whose
three tokens are all in that vocabulary, ignoring surrounding whitespace and
also accepting a SentencePiece `▁` prefix. This covers fine-tunes and local
checkpoints whose names do not mention their base family.

A bare model object has no vocabulary, so it resolves only by name. If neither
step finds a match, `from_model` raises `ValueError`; pass the tokens to
`FIMInput` directly instead:

```python
from ml4setk import FIMInput, QueryMatch

fim = FIMInput("<fim_prefix>", "<fim_suffix>", "<fim_middle>")
model_input, _ = fim.generate(QueryMatch("a = ", "\n", "1"))
assert model_input == "<fim_prefix>a = <fim_suffix>\n<fim_middle>"
```

### Prompt order: PSM and SPM

The `order` argument sets how the sections are laid out:

- `order="psm"` (the default): prefix, suffix, middle.
  `FIM_PREFIX + prefix + FIM_SUFFIX + suffix + FIM_MIDDLE`
- `order="spm"`: suffix, prefix, middle.
  `FIM_SUFFIX + suffix + FIM_PREFIX + prefix + FIM_MIDDLE`

`from_model` sets the order from the registry, so Codestral gets SPM without
any extra argument. Set it yourself when passing tokens by hand:

```python
from ml4setk import FIMInput, QueryMatch

match = QueryMatch(prefix="def add(a, b):\n    ", suffix="\n", match="return a + b")

fim = FIMInput("[PREFIX]", "[SUFFIX]", "", order="spm")
model_input, _ = fim.generate(match)
assert model_input == "[SUFFIX]\n[PREFIX]def add(a, b):\n    "
assert model_input == FIMInput.from_model("mistralai/Codestral-22B-v0.1").generate(match)[0]
```

Any other `order` value raises `ValueError`.

## Autoregressive prompts

`CausalInput` builds a left-to-right prompt: the model input is the prefix
alone and the ground truth is the match. The suffix is dropped, so the model
sees only the code before the target, the way a plain completion model does.

Compared with `FIMInput`:

- it needs no sentinel tokens, so it takes no arguments and works with any
  causal language model;
- it has no `from_model` and no `order`;
- the model never sees the code after the target, so scores from the two
  formats are not directly comparable.

To score a target token by token, `MultiTokenInput(tokenizer)` expands an AR
context and target into one `(context_tokens, next_token)` pair per target
token.
