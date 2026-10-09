# Input formatting

Every query returns a `QueryMatch(prefix, suffix, match)`. An input formatter
turns that match into a `(model_input, ground_truth)` pair, where the ground
truth is always `match`. This page covers the formatters for code models:
`FIMInput` for fill-in-the-middle (FIM) prompts, `CausalInput` for
autoregressive (AR) prompts, and three
[masked diffusion](#masked-diffusion-prompts) formatters.

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

## Masked diffusion prompts

Masked diffusion LLMs (dLLMs) such as LLaDA, Dream, Dream-Coder, DiffuCoder
and DreamOn do not use FIM sentinels. They read the whole sequence at once and
denoise a run of mask tokens in place, so the prompt is the visible code with
the target replaced by masks. Published models and papers use three settings,
which differ in where the masks go and how many there are:

| Setting | Formatter | Model input | Used by |
| --- | --- | --- | --- |
| Completion | `DiffusionCompletionInput(mask, num_masks=128)` | prefix + `num_masks` masks | LLaDA, Dream, DiffuCoder, Seed Diffusion |
| Fixed-length infilling | `DiffusionInfillInput(mask, tokenizer)` | prefix + one mask per target token + suffix | LLaDA, Dream, Dream-Coder (as evaluated by DreamOn) |
| Variable-length infilling | `DiffusionExpandingInfillInput(mask, num_masks=4)` | prefix + `num_masks` masks + suffix | DreamOn |

```python
from ml4setk import (
    DiffusionCompletionInput,
    DiffusionExpandingInfillInput,
    QueryMatch,
)

match = QueryMatch(prefix="def add(a, b):\n    ", suffix="\n", match="return a + b")

completion = DiffusionCompletionInput.from_model("GSAI-ML/LLaDA-8B-Base", num_masks=2)
model_input, ground_truth = completion.generate(match)
assert model_input == "def add(a, b):\n    <|mdm_mask|><|mdm_mask|>"
assert ground_truth == "return a + b"

expanding = DiffusionExpandingInfillInput.from_model("Dream-org/DreamOn-v0-7B", num_masks=1)
model_input, _ = expanding.generate(match)
assert model_input == "def add(a, b):\n    <|mask|>\n"
```

### Completion

The default generation mode of every dLLM: the prompt is followed by a fixed
budget of masks, and the suffix is dropped, as with `CausalInput`. LLaDA's
reference `generate` builds exactly this sequence with `gen_length=128` by
default, Dream and DiffuCoder do the same through `diffusion_generate(...,
max_new_tokens=...)`, and Seed Diffusion decodes block by block from an
all-mask sequence. Masks the target does not need are filled with end-of-text
or pad tokens by the model, so pick `num_masks` at least as long as the
longest target in tokens.

### Fixed-length infilling

Because attention is bidirectional, a dLLM can fill a hole without sentinels:
the masks go between the prefix and the suffix. The model cannot change the
sequence length, so the number of masks fixes the length of the answer.
`DiffusionInfillInput` uses the oracle length, one mask per token of the
ground truth under `tokenizer.encode(match, add_special_tokens=False)`, the
oracle setting DreamOn uses as the upper bound for these models. DreamOn reports
that a wrong mask count costs these models an average of 38% on
HumanEval-Infilling, so results with a guessed length are not comparable to
oracle-length results.

`DiffusionInfillInput.from_model(tokenizer)` takes the mask token and the
length from one tokenizer. With a model name, pass the tokenizer as well:
`DiffusionInfillInput.from_model("Dream-org/Dream-Coder-v0-Base-7B",
tokenizer)`.

### Variable-length infilling

DreamOn adds expand and delete states, so the model starts from a small
canvas between the prefix and the suffix and grows or shrinks it while
decoding. The input carries no length hint; its model card example starts
from 4 masks, which is the default here. DreamOn's own helper also wraps the
sequence in BOS and EOS token ids; add those when tokenizing if your
tokenizer does not.

### Mask-token registry

`from_model` resolves the mask token through `MODEL_MASK_TOKENS` in
`ml4setk.Generation.sentinels`, with the same name matching and
[tokenizer fallback](#tokenizer-fallback) as the FIM registry.
`get_mask_token(model)` returns the token on its own, and an unknown model
raises `ValueError`; pass the mask token to the formatter directly instead.

| Family | Matched by | Mask token |
| --- | --- | --- |
| LLaDA | `llada` | `<|mdm_mask|>` (id 126336) |
| Dream, Dream-Coder, DreamOn | `dream` (also DiffuCoder's `model_type`) | `<|mask|>` (id 151666) |
| DiffuCoder | `diffucoder` | `<|mask|>` (id 151666) |

Mercury (Inception) and Seed Diffusion are closed models. Mercury's FIM
endpoint takes the prefix and suffix as separate `prompt` and `suffix`
fields and never exposes a mask token, so it needs no formatter here.

### Sources

- LLaDA reference sampler, `generate.py`:
  <https://github.com/ML-GSAI/LLaDA/blob/main/generate.py>
- Dream and Dream-Coder: <https://github.com/DreamLM/Dream>,
  `config.json` and `tokenizer_config.json` of
  `Dream-org/Dream-Coder-v0-Base-7B` (`mask_token_id` 151666, `<|mask|>`)
- DiffuCoder: <https://arxiv.org/abs/2506.20639>, and
  `apple/DiffuCoder-7B-Base` `tokenizer_config.json`
- DreamOn (ICLR 2026): <https://arxiv.org/abs/2602.01326>, and the
  `Dream-org/DreamOn-v0-7B` model card
- Seed Diffusion: <https://arxiv.org/abs/2508.02193>
- Mercury FIM API: <https://docs.inceptionlabs.ai/capabilities/fim>
