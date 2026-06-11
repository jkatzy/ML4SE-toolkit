# Chunk 6 Q-S Implementation Confirmation

## Raw token data

- Registry key: `raw_token_data`
- Backlog status: `needs_research_or_confirmation`
- Source report: `docs/comment_research/chunk_6_q_s_report.md`
- Current hypothesis: unsupported data artifact label; no source-language standard or lexical comments found.
- Implementation artifact: GitHub Linguist `languages.yml`
- Implementation version: `github-linguist/linguist` commit `1d7ac7ed569bd6edef5d0cfc73feea2573cb0e03`
- Local scratch path: `tmp/comment_research_confirmation/chunk_6_q_s/raw_token_data/`
- Designated hello-world source: none found; `find ... -iname '*.raw'` over Linguist samples returned `0` paths.
- Parser command: not available; Linguist metadata is a classifier table, not a parser or tokenizer for `.raw` files.
- Confirmation verdict: `blocked`
- Recommended report update: keep this entry unsupported or non-actionable unless a real `.raw` token-data specification and parser fixture is found.
- Blockers: no official parser, grammar, language implementation, hello-world file, or parser fixture was discoverable from the assigned Linguist implementation source.
- Notes: Linguist records `type: data`, extension `.raw`, and `tm_scope: none`, which supports the non-language interpretation but is not a parser confirmation.

### Probe Results

| Probe | Scratch file | Expected parser result | Actual parser result | Evidence |
| --- | --- | --- | --- | --- |
| line comment | unsupported | not tested | blocked | no parser or `.raw` fixture available |
| block comment | unsupported | not tested | blocked | no parser or `.raw` fixture available |
| nested comment | unsupported | not tested | blocked | no parser or `.raw` fixture available |
| unsupported form | unsupported | not tested | blocked | no parser or `.raw` fixture available |

### Confirmed Examples

No parser-confirmed examples.

## Regular Expression

- Registry key: `regular_expression`
- Backlog status: `needs_research_or_confirmation`
- Source report: `docs/comment_research/chunk_6_q_s_report.md`
- Current hypothesis: flavor-dependent; Python and Perl extended modes use `#` line comments, Perl and PCRE2 accept `(?#...)`, ECMAScript has no native comment syntax.
- Implementation artifact: Python `re`, Perl regular expressions, PCRE2 `pcre2test`, and ECMAScript `RegExp` via Node.js.
- Implementation version: Python `3.13.9`; Perl `5.38.2`; PCRE2 `10.47 2025-10-21`; Node.js `v18.19.1`.
- Local scratch path: `tmp/comment_research_confirmation/chunk_6_q_s/regular_expression/`
- Designated hello-world source: no single official hello-world exists for the aggregate Linguist `Regular Expression` data label; scratch flavor-specific compiler fixtures were used.
- Parser command: `python3 tmp/comment_research_confirmation/chunk_6_q_s/regular_expression/python_regex_probe.py`; `perl tmp/comment_research_confirmation/chunk_6_q_s/regular_expression/perl_regex_probe.pl`; `node tmp/comment_research_confirmation/chunk_6_q_s/regular_expression/node_regex_probe.js`; `tmp/comment_research_confirmation/chunk_6_q_s/tools/bin/pcre2test tmp/comment_research_confirmation/chunk_6_q_s/regular_expression/pcre2_regex_probe.txt`.
- Confirmation verdict: `contradicted`
- Recommended report update: revise the Python flavor wording to include `(?#...)` inline comments; keep the registry key out of implementation unless the project splits regex comment handling by flavor and mode.
- Blockers: no single parser can confirm the aggregate Linguist label because comment support depends on regex flavor and flags.
- Notes: The flavor-dependent warning is confirmed, but the current source report is too narrow for Python inline comments.

### Probe Results

| Probe | Scratch file | Expected parser result | Actual parser result | Evidence |
| --- | --- | --- | --- | --- |
| line comment | `tmp/comment_research_confirmation/chunk_6_q_s/regular_expression/python_regex_probe.py` | accepted in Python verbose mode | accepted | `ok: python verbose # line comment: compiled` |
| line comment | `tmp/comment_research_confirmation/chunk_6_q_s/regular_expression/perl_regex_probe.pl` | accepted in Perl `/x` mode | accepted | `ok: perl /x # line comment: compiled` |
| line comment | `tmp/comment_research_confirmation/chunk_6_q_s/regular_expression/pcre2_regex_probe.txt` | accepted in PCRE2 `(?x)` mode | accepted | PCRE2 matched `123.45` |
| line comment | `tmp/comment_research_confirmation/chunk_6_q_s/regular_expression/node_regex_probe.js` | unsupported as comment in ECMAScript | treated as literal text | `ok: ecmascript # is literal, not a verbose line comment: true` |
| block comment | `tmp/comment_research_confirmation/chunk_6_q_s/regular_expression/python_regex_probe.py` | expected unsupported by current report | accepted | `ok: python inline (?#...) comment: compiled` |
| block comment | `tmp/comment_research_confirmation/chunk_6_q_s/regular_expression/perl_regex_probe.pl` | accepted | accepted | `ok: perl inline (?#...) comment: compiled` |
| block comment | `tmp/comment_research_confirmation/chunk_6_q_s/regular_expression/pcre2_regex_probe.txt` | accepted | accepted | PCRE2 matched `123.45` |
| block comment | `tmp/comment_research_confirmation/chunk_6_q_s/regular_expression/node_regex_probe.js` | rejected | rejected | `ok: ecmascript inline (?#...) comment is rejected: true` |
| nested comment | `tmp/comment_research_confirmation/chunk_6_q_s/regular_expression/python_regex_probe.py` | unsupported | rejected as unterminated comment when malformed | `missing ), unterminated comment` |
| unsupported form | `tmp/comment_research_confirmation/chunk_6_q_s/regular_expression/pcre2_regex_probe.txt` | rejected | rejected | `missing ) after (?# comment` |

### Confirmed Examples

#### Line comment
```text
(?x)
\d+  # CONFIRM_LINE_COMMENT
\.\d*
```

#### Block comment
```text
\d+(?# CONFIRM_INLINE_COMMENT)\.\d*
```

#### Nested comment
Unsupported.

## Rouge

- Registry key: `rouge`
- Backlog status: `needs_research_or_confirmation`
- Source report: `docs/comment_research/chunk_6_q_s_report.md`
- Current hypothesis: unresolved Linguist `.rg` label; do not infer grammar from editor mode aliases.
- Implementation artifact: GitHub Linguist `languages.yml`
- Implementation version: `github-linguist/linguist` commit `1d7ac7ed569bd6edef5d0cfc73feea2573cb0e03`
- Local scratch path: `tmp/comment_research_confirmation/chunk_6_q_s/rouge/`
- Designated hello-world source: none found; `find ... -iname '*.rg'` over Linguist samples returned `0` paths.
- Parser command: not available; no authoritative Rouge parser, grammar, or fixture was found in the assigned implementation source.
- Confirmation verdict: `blocked`
- Recommended report update: keep this entry unresolved and out of registry work until a real Rouge language implementation or grammar is identified.
- Blockers: Linguist maps `.rg` to Clojure editor modes, but the cloned Linguist tree has no `.rg` samples and provides no parser.
- Notes: The Clojure editor-mode mapping is insufficient evidence for comment syntax.

### Probe Results

| Probe | Scratch file | Expected parser result | Actual parser result | Evidence |
| --- | --- | --- | --- | --- |
| line comment | unsupported | not tested | blocked | no parser or `.rg` fixture available |
| block comment | unsupported | not tested | blocked | no parser or `.rg` fixture available |
| nested comment | unsupported | not tested | blocked | no parser or `.rg` fixture available |
| unsupported form | unsupported | not tested | blocked | no parser or `.rg` fixture available |

### Confirmed Examples

No parser-confirmed examples.

## RPGLE

- Registry key: `rpgle`
- Backlog status: `needs_research_or_confirmation`
- Source report: `docs/comment_research/chunk_6_q_s_report.md`
- Current hypothesis: free-form RPGLE uses `//`; block comments unsupported; fixed-form comment forms not fully reverified.
- Implementation artifact: `rpgleparser`, an ANTLR v4 grammar/parser for IBM ILE RPG.
- Implementation version: `rpgleparser/rpgleparser` commit `1cd596ded2edff26f7f82639d5ca7ee51ebbfeb9`, Maven project version `1.0.0`.
- Local scratch path: `tmp/comment_research_confirmation/chunk_6_q_s/rpgle/`
- Designated hello-world source: parser fixtures `src/test/resources/org/rpgleparser/tests/comments/slashslashaftercode.rpgle` and `src/test/resources/org/rpgleparser/tests/comments/slashsplat.rpgle`.
- Parser command: `JAVA_HOME=/home/jovyan/work/tmp/comment_research_confirmation/chunk_6_q_s/tools MAVEN_OPTS=-Dmaven.repo.local=/home/jovyan/work/tmp/comment_research_confirmation/chunk_6_q_s/rpgle/m2repo /home/jovyan/work/tmp/comment_research_confirmation/chunk_6_q_s/tools/bin/mvn -q -Dtest=ConfirmationCommentProbeTest -DconfirmationProbeDir=/home/jovyan/work/tmp/comment_research_confirmation/chunk_6_q_s/rpgle/probes test`
- Confirmation verdict: `contradicted`
- Recommended report update: retain `//` line comments, but revise the block-comment claim; this parser accepts `/** ... */`-style comment blocks used in its own fixtures. Verify against IBM compiler documentation before marking broad RPGLE block-comment support registry-ready.
- Blockers: IBM's production compiler was not available locally; this confirmation uses the packet's strongest runnable parser alternative.
- Notes: The nested-looking slash-star probe was accepted as comment text by this parser; that does not prove true recursive block-comment nesting.

### Probe Results

| Probe | Scratch file | Expected parser result | Actual parser result | Evidence |
| --- | --- | --- | --- | --- |
| line comment | `tmp/comment_research_confirmation/chunk_6_q_s/rpgle/probes/line_comment_probe.rpgle` | accepted | accepted | Maven exit `0`; Surefire: `Tests run: 4, Failures: 0, Errors: 0` |
| block comment | `tmp/comment_research_confirmation/chunk_6_q_s/rpgle/probes/block_comment_probe.rpgle` | expected unsupported by current report | accepted | same Maven probe passed |
| nested comment | `tmp/comment_research_confirmation/chunk_6_q_s/rpgle/probes/nested_block_probe.rpgle` | unsupported true nesting | accepted as comment text | same Maven probe passed |
| unsupported form | `tmp/comment_research_confirmation/chunk_6_q_s/rpgle/probes/hash_negative_probe.rpgle` | rejected | rejected | log contains `no viable alternative at input '#CONFIRM_UNSUPPORTED_HASH_COMMENT'` |

### Confirmed Examples

#### Line comment
```text
      /FREE
          // CONFIRM_LINE_COMMENT standalone
          If Pos > 0; // CONFIRM_LINE_COMMENT trailing
      /END-FREE
```

#### Block comment
```text
      /FREE
          If Pos > 0;
    /** CONFIRM_BLOCK_COMMENT start
      * between statements
      * CONFIRM_BLOCK_COMMENT end */
             Pos = Pos + 1;
      /END-FREE
```

#### Nested comment
```text
    /** CONFIRM_NESTED_COMMENT start
      * nested opener /* inner */
      * CONFIRM_NESTED_COMMENT end */
```

## SELinux Policy

- Registry key: `selinux_policy`
- Backlog status: `needs_research_or_confirmation`
- Source report: `docs/comment_research/chunk_6_q_s_report.md`
- Current hypothesis: SELinux policy sources use `#` line comments; block comments unsupported.
- Implementation artifact: SELinux userspace `checkpolicy` / `checkmodule` built locally from source, plus SELinux refpolicy examples.
- Implementation version: `SELinuxProject/selinux` commit `57cd62c23c0842fd287ae00cb492830163bf0ddd`; `SELinuxProject/refpolicy` commit `7ceced6be407446d6cdc986f8a71551fe36ba9b1`; `checkpolicy -V` reported `35 (compatibility range 35-15)`.
- Local scratch path: `tmp/comment_research_confirmation/chunk_6_q_s/selinux_policy/`
- Designated hello-world source: `checkpolicy/tests/policy_minimal.conf` parser fixture; refpolicy `doc/example.te` used as policy-source example context.
- Parser command: `tmp/comment_research_confirmation/chunk_6_q_s/selinux_policy/selinux/checkpolicy/checkpolicy -o /dev/null tmp/comment_research_confirmation/chunk_6_q_s/selinux_policy/probes/policy_line_comments.conf`; `tmp/comment_research_confirmation/chunk_6_q_s/selinux_policy/selinux/checkpolicy/checkmodule -m -o tmp/comment_research_confirmation/chunk_6_q_s/selinux_policy/confirmation.mod tmp/comment_research_confirmation/chunk_6_q_s/selinux_policy/probes/module_line_comments.te`
- Confirmation verdict: `confirmed`
- Recommended report update: move forward with `#` line comments to end-of-line and no block comments for SELinux policy sources.
- Blockers: none for the checked source policy and `.te` module probes.
- Notes: The local build used scratch-only `flex` and `bison`; `libsepol.a` was produced even though shared `libsepol.so` linking failed, and that static library was sufficient for `checkpolicy`.

### Probe Results

| Probe | Scratch file | Expected parser result | Actual parser result | Evidence |
| --- | --- | --- | --- | --- |
| line comment | `tmp/comment_research_confirmation/chunk_6_q_s/selinux_policy/probes/policy_line_comments.conf` | accepted | accepted | `checkpolicy` exit `0`, no stderr |
| line comment | `tmp/comment_research_confirmation/chunk_6_q_s/selinux_policy/probes/module_line_comments.te` | accepted | accepted | `checkmodule` exit `0`, output `confirmation.mod` written under scratch |
| block comment | `tmp/comment_research_confirmation/chunk_6_q_s/selinux_policy/probes/policy_block_negative.conf` | rejected | rejected | `syntax error` at token `/*` |
| nested comment | `tmp/comment_research_confirmation/chunk_6_q_s/selinux_policy/probes/policy_nested_block_negative.conf` | rejected | rejected | `syntax error` at token `/*` |
| unsupported form | `tmp/comment_research_confirmation/chunk_6_q_s/selinux_policy/probes/module_block_negative.te` | rejected | rejected | `checkmodule` reports `syntax error` at token `/*` |

### Confirmed Examples

#### Line comment
```text
# CONFIRM_LINE_COMMENT standalone
class CLASS1 { PERM1 } # CONFIRM_LINE_COMMENT trailing
```

#### Block comment
Unsupported.

#### Nested comment
Unsupported.

## SRecode Template

- Registry key: `srecode_template`
- Backlog status: `needs_research_or_confirmation`
- Source report: `docs/comment_research/chunk_6_q_s_report.md`
- Current hypothesis: unresolved; examples suggest Lisp-style semicolon comments, but no stable language-wide delimiter was confirmed.
- Implementation artifact: GNU Emacs SRecode parser/compiler and `srecode-template-mode`.
- Implementation version: Emacs source commit `8486669e373fb8e9962428c42b427462cc655e3c`; scratch Emacs binary `GNU Emacs 30.2`; SRecode version variable `1.2`.
- Local scratch path: `tmp/comment_research_confirmation/chunk_6_q_s/srecode_template/`
- Designated hello-world source: GNU Emacs fixture `etc/srecode/test.srt`.
- Parser command: `tmp/comment_research_confirmation/chunk_6_q_s/tools/bin/emacs --batch -Q --load tmp/comment_research_confirmation/chunk_6_q_s/srecode_template/srecode_syntax_probe.el`
- Confirmation verdict: `confirmed`
- Recommended report update: record `;;` line comments to end-of-line for SRecode template files. Also note the template-language comment macro `$! ... $`, terminated by the configured escape end delimiter, for comment-like template inserters.
- Blockers: none for semicolon line comments; block-comment rejection is based on `srecode-template-mode` syntax tokenization rather than compiler rejection, because the compiler tolerated `#| ... |#` text without recognizing it as comment syntax.
- Notes: The SRecode mode source sets `comment-start` to `;;` and `comment-end` to the empty string; the batch syntax probe confirmed that markers inside `#| ... |#` were not comment text.

### Probe Results

| Probe | Scratch file | Expected parser result | Actual parser result | Evidence |
| --- | --- | --- | --- | --- |
| line comment | `tmp/comment_research_confirmation/chunk_6_q_s/srecode_template/probes/srecode_comment_probe.srt` | accepted and tokenized as comment | accepted | `ok: CONFIRM_LINE_COMMENT standalone in-comment=t expected=t` |
| line comment | `tmp/comment_research_confirmation/chunk_6_q_s/srecode_template/probes/srecode_comment_probe.srt` | accepted and tokenized as trailing comment | accepted | `ok: CONFIRM_LINE_COMMENT trailing in-comment=t expected=t` |
| block comment | `tmp/comment_research_confirmation/chunk_6_q_s/srecode_template/probes/srecode_block_negative.srt` | unsupported as lexical comment | not tokenized as comment | `ok: CONFIRM_UNSUPPORTED_BLOCK_COMMENT in-comment=nil expected=nil` |
| nested comment | `tmp/comment_research_confirmation/chunk_6_q_s/srecode_template/probes/srecode_nested_block_negative.srt` | unsupported as lexical comment | not tokenized as comment | `ok: CONFIRM_UNSUPPORTED_NESTED_BLOCK in-comment=nil expected=nil` |
| unsupported form | `tmp/comment_research_confirmation/chunk_6_q_s/srecode_template/probes/srecode_comment_probe.srt` | `$! ... $` should compile as template comment macro | accepted | `ok: $! template comment macro compiled in srecode_comment_probe.srt` |

### Confirmed Examples

#### Line comment
```text
;; CONFIRM_LINE_COMMENT standalone
set mode "srecode-template-mode" ;; CONFIRM_LINE_COMMENT trailing
```

#### Block comment
```text
$! CONFIRM_TEMPLATE_COMMENT macro comment. $
```

#### Nested comment
Unsupported for lexical comments.
