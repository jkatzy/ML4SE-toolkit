# Implementation Confirmation Prompt: `chunk_6_q_s`

Use this packet together with:
- [implementation_confirmation_playbook.md](docs/comment_research/implementation_confirmation_playbook.md)
- [confirmation_report_template.md](docs/comment_research/confirmation_report_template.md)

## Mission

Confirm only the `needs_research_or_confirmation` entries in this packet by downloading a real language implementation, locating a designated hello-world or equivalent parser fixture, adding scratch comment probes, and parsing or tokenizing those scratch files with the implementation.

Target output file:
- `docs/comment_research/confirmation_reports/chunk_6_q_s_confirmation.md`

Allowed committed edit scope:
- `docs/comment_research/confirmation_reports/chunk_6_q_s_confirmation.md`

Scratch/output scope:
- `tmp/comment_research_confirmation/chunk_6_q_s/`

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
| Raw token data | raw_token_data | unresolved | GitHub Linguist data label for `.raw` token-data files; no source-language standard found | unsupported; this appears to be a data artifact label rather than a language with lexical comments | unsupported | unsupported | unresolved | unsupported | docs/comment_research/chunk_6_q_s_report.md | unresolved | GitHub Linguist languages.yml | unsupported |
| Regular Expression | regular_expression | cross-checked | Python 3.9-3.14 `re`, Perl 5.6+ `perlre`, PCRE2 current, ECMAScript 2026 regular expressions | Python `re.X`/`(?x)` and Perl `/x` use `#` line comments; Perl and PCRE2 also accept `(?#...)`; ECMAScript RegExp does not define a native comment syntax. The label is flavor-dependent, so a single union key would be misleading. | `#` in verbose / extended modes | `(?#...)` inline comments in Perl and PCRE2 only; otherwise unsupported | line comments terminate at the next newline in verbose / extended modes; Perl and PCRE2 also support inline `(?#...)` comments that terminate at `)` | no | docs/comment_research/chunk_6_q_s_report.md | https://docs.python.org/3/library/re.html; https://perldoc.perl.org/perlre; https://www.pcre.org/current/doc/html/pcre2pattern.html; https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Regular_expressions | GitHub Linguist languages.yml | needs manual research |
| Rouge | rouge | unresolved | GitHub Linguist `.rg` language label only; no authoritative Rouge language specification found in this pass | unresolved; do not infer a grammar from syntax-highlighter mode aliases alone | unresolved | unresolved | unresolved | unknown | docs/comment_research/chunk_6_q_s_report.md | unresolved | GitHub Linguist languages.yml | needs manual research |
| RPGLE | rpgle | medium | free-form IBM i RPGLE examples and community conversion examples; fixed-form RPG comment columns were not fully reverified in this pass | free-form RPGLE uses `//`; fixed-form comment forms should be researched before broadening the registry entry | // | unsupported | line comments terminate at end-of-line; block comments unsupported | no | docs/comment_research/chunk_6_q_s_report.md | unresolved | GitHub Linguist languages.yml | candidate |
| SELinux Policy | selinux_policy | medium | SELinux reference-policy style `.te` / `.if` / policy source files checked against Red Hat guidance and refpolicy sources | no version split found; policy sources use `#` line comments | # | unsupported | line comments terminate at end-of-line; block comments unsupported | no | docs/comment_research/chunk_6_q_s_report.md | https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/using_selinux/writing-a-custom-selinux-policy | https://github.com/SELinuxProject/refpolicy | candidate |
| SRecode Template | srecode_template | unresolved | GNU Emacs SRecode manual and CEDET template examples | unresolved; examples suggest Lisp-style semicolon comments in some template files, but I did not find a stable language-wide delimiter definition | unresolved | unresolved | unresolved | unknown | docs/comment_research/chunk_6_q_s_report.md | https://www.gnu.org/software/emacs/manual/html_node/srecode/Template-Naming-Conventions.html | GitHub Linguist languages.yml | needs manual research |

## Output Constraints

- Use one `## <Language>` section per assigned language.
- Keep every field from `confirmation_report_template.md`, including blocked fields.
- Do not claim confirmation from source inspection alone; the implementation must parse or tokenize the scratch file.
- Keep downloaded implementations and full command logs under `tmp/comment_research_confirmation/`.
- Leave unrelated worktree changes untouched.
