# Chunk 3 G-I Implementation Confirmation

## Genero Forms

- Registry key: genero_forms
- Backlog status: needs_research_or_confirmation
- Source report: docs/comment_research/chunk_3_g_i_report.md, "Genero Forms"
- Current hypothesis: Genero Forms `.per` files use `--` line comments ending at newline; block comments and nested comments are unsupported for form files.
- Implementation artifact: Four Js Genero BDL `fglform` form compiler, documented by the official "Compiling form specification files (.per)" page; supporting official public sample `FourjsGenero/tool_fglped` delegates `.per` parsing to `fglform`.
- Implementation version: parser executable not available locally; downloaded docs are Genero BDL manual `GeneroDocVersionInfo=6.00.07-202603270957-1a27cf5e4f21a88700f1628614c3d305306204b3`, and `tool_fglped` was cloned at `d798b8dcff0cbe038ca3c2c7b1e4f1334578bf8c`.
- Local scratch path: `tmp/comment_research_confirmation/chunk_3_g_i/genero_forms/`
- Designated hello-world source: official minimal `form.per` example from https://4js.com/online_documentation/fjs-fgl-manual-html/fgl-topics/c_fgl_CompilingPrograms_forms.html, downloaded to `tmp/comment_research_confirmation/chunk_3_g_i/genero_forms/fgl_compiling_forms.html`.
- Parser command: `fglform -M tmp/comment_research_confirmation/chunk_3_g_i/genero_forms/line_comment_probe.per`
- Confirmation verdict: blocked
- Recommended report update: keep `needs_research_or_confirmation` until a licensed Genero BDL installation or redistributable form grammar can run `fglform` or an equivalent parser on the `.per` probes.
- Blockers: `command -v fglform` returned no executable, and attempted `fglform -M ...` commands failed with `bash: line 1: fglform: command not found`; the official install page states Genero BDL installation requires license credentials.
- Notes: The official compiler page identifies `fglform` as the required `.per` compiler and shows `-M` for direct error output. The public `tool_fglped` source is useful corroboration that `.per` tooling shells out to `fglform`, but it is not itself a parser.

### Probe Results

| Probe | Scratch file | Expected parser result | Actual parser result | Evidence |
| --- | --- | --- | --- | --- |
| line comment | `tmp/comment_research_confirmation/chunk_3_g_i/genero_forms/line_comment_probe.per` | accepted | not tested | `fglform_line_probe.log`: `fglform: command not found` |
| block comment | `tmp/comment_research_confirmation/chunk_3_g_i/genero_forms/block_comment_probe.per` | rejected | not tested | `fglform_block_probe.log`: `fglform: command not found` |
| nested comment | `tmp/comment_research_confirmation/chunk_3_g_i/genero_forms/nested_block_probe.per` | rejected | not tested | parser unavailable after `fglform` lookup failed |
| unsupported form | `tmp/comment_research_confirmation/chunk_3_g_i/genero_forms/hash_comment_probe.per` | rejected | not tested | parser unavailable after `fglform` lookup failed |

### Confirmed Examples

No examples were parser-confirmed because the required `fglform` executable was unavailable.

#### Line comment

```text
-- CONFIRM_LINE_COMMENT standalone before the form
LAYOUT
GRID
{
[f01   ] -- CONFIRM_LINE_COMMENT trailing in grid area
}
END -- CONFIRM_LINE_COMMENT trailing after container
END
ATTRIBUTES
-- CONFIRM_LINE_COMMENT standalone before an attribute
f01 = FORMONLY.field1; -- CONFIRM_LINE_COMMENT trailing after attribute
END
```

#### Block comment

```text
unsupported; scratch probe not parsed because `fglform` was unavailable
```

#### Nested comment

```text
unsupported; scratch probe not parsed because `fglform` was unavailable
```

## Graph Modeling Language

- Registry key: graph_modeling_language
- Backlog status: needs_research_or_confirmation
- Source report: docs/comment_research/chunk_3_g_i_report.md, "Graph Modeling Language"
- Current hypothesis: common GML parser behavior, represented by NetworkX, supports `#` line comments ending at the physical newline; block comments, nested comments, semicolon comments, and slash comments are unsupported; the `comment "..."` key is graph metadata, not a lexical comment delimiter.
- Implementation artifact: NetworkX GML reader/parser, `networkx/readwrite/gml.py`, from https://github.com/networkx/networkx.git.
- Implementation version: NetworkX tag `networkx-3.5`, commit `4fa222d2fb157e1b7f8c753c9f92e5907d1ddeb4`.
- Local scratch path: `tmp/comment_research_confirmation/chunk_3_g_i/graph_modeling_language/`
- Designated hello-world source: NetworkX parser fixture `networkx/readwrite/tests/test_gml.py`, `TestGraph.simple_data`, used by `test_parse_gml` and `test_read_gml` in the downloaded implementation checkout.
- Parser command: `PYTHONPATH=/home/jovyan/work/tmp/comment_research_confirmation/chunk_3_g_i/graph_modeling_language/networkx-3.5 python tmp/comment_research_confirmation/chunk_3_g_i/graph_modeling_language/run_gml_probe.py EXPECT_ACCEPT tmp/comment_research_confirmation/chunk_3_g_i/graph_modeling_language/line_comment_probe.gml`; rejection probes used the same command with `EXPECT_REJECT`.
- Confirmation verdict: confirmed
- Recommended report update: promote the NetworkX/common-parser dialect to implementation-confirmed for `#` line comments only; keep block comments, nested comments, semicolon comments, and slash comments unsupported; keep `comment "..."` documented as a metadata key rather than a lexical delimiter.
- Blockers: none for NetworkX/common-parser behavior.
- Notes: The parser command imported NetworkX from the cloned checkout, confirmed by `networkx_version.log`.

### Probe Results

| Probe | Scratch file | Expected parser result | Actual parser result | Evidence |
| --- | --- | --- | --- | --- |
| line comment | `tmp/comment_research_confirmation/chunk_3_g_i/graph_modeling_language/line_comment_probe.gml` | accepted | accepted | `line_comment_probe.log`: accepted with nodes `['Node 1', 'Node 2', 'Node 3']` and three directed edges |
| block comment | `tmp/comment_research_confirmation/chunk_3_g_i/graph_modeling_language/block_comment_probe.gml` | rejected | rejected | `unsupported_probe.log`: `cannot tokenize /* CONFIRM_BLOCK_COMMENT... */ at (2, 1)` |
| nested comment | `tmp/comment_research_confirmation/chunk_3_g_i/graph_modeling_language/nested_block_probe.gml` | rejected | rejected | `unsupported_probe.log`: `cannot tokenize /* CONFIRM_NESTED_COMMENT... */ at (2, 1)` |
| unsupported semicolon line comment | `tmp/comment_research_confirmation/chunk_3_g_i/graph_modeling_language/semicolon_comment_probe.gml` | rejected | rejected | `unsupported_probe.log`: `cannot tokenize ; CONFIRM_UNSUPPORTED_FORM... at (1, 1)` |
| unsupported slash line comment | `tmp/comment_research_confirmation/chunk_3_g_i/graph_modeling_language/slash_comment_probe.gml` | rejected | rejected | `unsupported_probe.log`: `cannot tokenize // CONFIRM_UNSUPPORTED_FORM... at (1, 1)` |

### Confirmed Examples

#### Line comment

```text
# CONFIRM_LINE_COMMENT standalone before graph data
Creator "me" # CONFIRM_LINE_COMMENT trailing after a key/value
Version "xx"
graph [
 # CONFIRM_LINE_COMMENT inside list
 comment "This is a sample graph"
 directed 1
]
```

#### Block comment

```text
/* CONFIRM_BLOCK_COMMENT unsupported block probe */
```

NetworkX rejected this form during tokenization.

#### Nested comment

```text
/* CONFIRM_NESTED_COMMENT outer /* inner */ outer */
```

NetworkX rejected this form during tokenization.
