# Implementation Confirmation Prompt: `chunk_4_j_m`

Use this packet together with:
- [implementation_confirmation_playbook.md](docs/comment_research/implementation_confirmation_playbook.md)
- [confirmation_report_template.md](docs/comment_research/confirmation_report_template.md)

## Mission

Confirm only the `needs_research_or_confirmation` entries in this packet by downloading a real language implementation, locating a designated hello-world or equivalent parser fixture, adding scratch comment probes, and parsing or tokenizing those scratch files with the implementation.

Target output file:
- `docs/comment_research/confirmation_reports/chunk_4_j_m_confirmation.md`

Allowed committed edit scope:
- `docs/comment_research/confirmation_reports/chunk_4_j_m_confirmation.md`

Scratch/output scope:
- `tmp/comment_research_confirmation/chunk_4_j_m/`

Do not edit `src/`, `tests/`, `registry.py`, original chunk reports, backlog/candidate views, or other confirmation reports.

## Required Workflow

1. Read the playbook and template completely.
2. For each language, read the current source report entry first.
3. Download or clone the official implementation, grammar, lexer, parser, or syntax tool into the chunk scratch directory.
4. Locate the designated hello-world file using the playbook's source order. If none exists, record `blocked` with searched paths.
5. Build minimal scratch copies of the hello-world file with line, block, nested, and negative probes as applicable.
6. Run a parse-only, tokenize-only, syntax-check, or compile-without-run command from the downloaded implementation.
7. Record exact commands, local scratch paths, result summaries, and a verdict: `confirmed`, `partially-confirmed`, `contradicted`, or `blocked`.
8. If contradicted, recommend the smallest next action without changing production code or registry entries.

## Language Queue

| Language | Registry key | Confidence | Current version scope | Current version syntax | Current line | Current block | Current termination | Current nested | Source report | Docs source | Implementation source | Current recommendation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| JetBrains MPS | jetbrains_mps | medium | current JetBrains MPS documentation for model persistence and XML-based persisted model files checked. | MPS editors are projectional and do not define a universal textual comment token. The persisted `.mps`, `.mpl`, and `.msd` files are XML-family artifacts; only XML comments are defensible for persisted files. | unsupported | `<!-- ... -->` for XML persistence files only | first closing `-->` wins | unsupported | docs/comment_research/chunk_4_j_m_report.md | https://www.jetbrains.com/help/mps/custom-persistence-cookbook.html | https://github.com/JetBrains/MPS | confirm |
| Lasso | lasso | medium | Lasso 9 language guide references and syntax-highlighting grammars checked. | LassoScript uses `//` single-line and `/* ... */` block comments; no versioned nested comment form was found. | // | /* ... */ | `//` terminates at a line break; `/* ... */` terminates at the first `*/`. | unsupported | docs/comment_research/chunk_4_j_m_report.md | https://lassoguide.com/ | https://github.com/SublimeText/Lasso | confirm |
| LoomScript | loomscript | medium | archived Loom SDK / LoomScript documentation and grammar sources checked. | LoomScript is ActionScript/ECMAScript-like and uses `//` and `/* ... */` comments. No nested block form was found. | // | /* ... */ | `//` terminates at a line break; `/* ... */` terminates at the first `*/`. | unsupported | docs/comment_research/chunk_4_j_m_report.md | https://github.com/LoomSDK/LoomSDK/wiki | https://github.com/LoomSDK/LoomSDK | confirm |
| LTspice Symbol | ltspice_symbol | unresolved | LTspice `.asy` symbol examples and syntax references checked for current ASCII symbol files. | no official textual comment delimiter was confirmed for `.asy` symbol files. The format is record-oriented, and public examples do not show a stable comment token. | unresolved | unsupported | unresolved for line comments; no block terminator | unsupported | docs/comment_research/chunk_4_j_m_report.md | https://ltwiki.org/LTspiceHelp/LTspiceHelp/Symbol_Editor.htm | proprietary LTspice parser; no public parser source found | research |
| Mask | mask | medium | MaskJS/mask template documentation and parser sources checked. | Mask templates use JavaScript/CSS-style `//` line comments and `/* ... */` block comments in template source. No nested form was confirmed. | // | /* ... */ | `//` terminates at a line break; `/* ... */` terminates at the first `*/`. | unsupported | docs/comment_research/chunk_4_j_m_report.md | https://github.com/atmajs/maskjs/wiki | https://github.com/atmajs/maskjs | confirm |
| Microsoft Developer Studio Project | msdev_project | candidate | Visual C++ 5/6 `.dsp` Developer Studio project files checked via corpus and parser references. | `.dsp` files use `#`-prefixed lines for generated file headers, section markers, and comments. No block syntax was found. | # | unsupported | end of line | unsupported | docs/comment_research/chunk_4_j_m_report.md | unresolved | https://github.com/Kitware/CMake/blob/master/Source/cmDSPParser.cxx | add |
| MUF | muf | medium | TinyMUCK/FuzzBall MUF programmer references and source examples checked. | MUF uses parenthesized comments `( ... )` and backslash line comments in common Forth-derived implementations. No true nested comment support was confirmed. | \ | ( ... ) | backslash comments terminate at end of line; parenthesized comments terminate at the first `)`. | unsupported | docs/comment_research/chunk_4_j_m_report.md | https://www.mufarchive.com/programming/mufman/ | https://github.com/fuzzball-muck/fuzzball | confirm |
| Muse | muse | unresolved | Emacs Muse / Muse markup references and examples checked. | no stable, language-level comment delimiter was confirmed for Muse markup. HTML comments may occur in emitted/embedded HTML, but that is HTML rather than Muse-native syntax. | unresolved | unresolved for Muse-native syntax; embedded HTML may use `<!-- ... -->` | unresolved for native Muse comments; embedded HTML comments terminate at first `-->`. | unsupported | docs/comment_research/chunk_4_j_m_report.md | https://www.gnu.org/software/emacs-muse/manual/ | https://git.savannah.gnu.org/cgit/emacs/elpa.git/tree/packages/muse | research |

## Output Constraints

- Use one `## <Language>` section per assigned language.
- Keep every field from `confirmation_report_template.md`, including blocked fields.
- Do not claim confirmation from source inspection alone; the implementation must parse or tokenize the scratch file.
- Keep downloaded implementations and full command logs under `tmp/comment_research_confirmation/`.
- Leave unrelated worktree changes untouched.
