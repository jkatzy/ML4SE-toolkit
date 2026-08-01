# Stack v3 Full Comment Research: batch 07

## Dataset provenance

- Dataset/project: HuggingFaceCode/stack-v3-full
- Statistics repository: HuggingFaceCode/stack-v3-train
- Immutable revision: 716a043a6c2adc34a2032b159364908a09ffe4ec
- Full statistics SHA-256:
  804cbdea6fc5329282096628a9865f5e91079f845dbcb82cd0da7af4be0a6d45
- Retrieved: 2026-08-01
- Inventory source and label column: pinned full statistics table, aggregated
  from files[].language
- Researcher or agent: /root/research_batch_07
- Review status: `reviewed`

Registry lookup candidates were checked on 2026-08-01. None of the raw labels
or proposed normalized keys in this record resolved at research time.

## OMNeT++ MSG

### Identity and scope

- Raw dataset label: `OMNeT++ MSG` (8,302,487 files; 6,194,079,541 tokens)
- Proposed registry key: `omnet_plus_plus_msg`
- Existing family or aliases checked: `slash_line_style` and `c_style`; neither
  contains this key, and an unguarded delimiter alias would ignore MSG lexer
  modes.
- Classification: `language`
- Versions or releases checked: OMNeT++ 6.4.0 development source, commit
  `820d04e7bb0ef53acaf6a41858ee7ea29f2754ca`; MSG-2 lexer.
- Dialects checked: ordinary message-definition source, property values, quoted
  literals, and `cplusplus {{ ... }}` bodies.
- Intended support scope: comments recognized by the MSG-2 host lexer.
- Explicitly excluded scope: generated C++, C++ inside `{{ ... }}`, property
  value text, and markers inside string or character literals.

### Syntax contract

- Line comments: `//` in the initial MSG lexer state, through the physical line.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: the implementation loop stops at
  LF or EOF and leaves LF for the whitespace rule. With CRLF, CR is traversed
  before LF. Extraction should exclude line-ending bytes and test lone CR
  conservatively rather than infer an undocumented normalization rule.
- Inline use: valid in ordinary MSG syntax.
- Adjacent-line grouping: valid for consecutive host `//` lines.
- Unclosed delimiter behavior: not applicable; a line comment may end at EOF.
- Lexical or structural context: `propertyvalue` and `cplusplusbody` are
  exclusive lexer states, so the initial-state comment rule is inactive there.
  Double-quoted strings and character constants also protect their contents.
- Conflicts with strings, operators, directives, or embedded languages:
  `"https://host/a//b"`, `'/'`, `@meta(http://host/a//b)`, and `//` inside a
  `{{ ... }}` C++ body are not MSG host comments.
- Sanitizer line wrappers: `("//", "")`.
- Sanitizer block wrappers: none.
- Content-preservation expectations: remove only the two-slash scaffolding and
  preserve payload, indentation, Unicode, and surrounding MSG source. Never
  clean a property value or embedded-C++ marker as an MSG comment.

### Evidence

- Official documentation permalink:
  [OMNeT++ message-definition examples](https://github.com/omnetpp/omnetpp/blob/820d04e7bb0ef53acaf6a41858ee7ea29f2754ca/doc/src/manual/ch-message-definitions.tex#L636-L648)
- Documentation version and relevant section: OMNeT++ 6.4 manual source,
  message-field declarations; the examples use inline `//` comments.
- Official implementation or grammar permalink:
  [MSG-2 lexer](https://github.com/omnetpp/omnetpp/blob/820d04e7bb0ef53acaf6a41858ee7ea29f2754ca/src/nedxml/msg2.lex#L58-L144)
- Implementation version, file, and relevant symbol: commit above,
  `src/nedxml/msg2.lex`; the initial `"//"` rule and exclusive
  `propertyvalue`/`cplusplusbody` states.
- Conformance test or official example permalink:
  [inline MSG comment example](https://github.com/omnetpp/omnetpp/blob/820d04e7bb0ef53acaf6a41858ee7ea29f2754ca/doc/src/manual/ch-message-definitions.tex#L690-L700)
- Secondary source, if needed: none.
- Evidence conflicts or gaps: documentation establishes the marker but does not
  spell out all exclusive states; the official lexer is definitive. Bare-CR
  input behavior is not documented.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: source-level lexer trace; OMNeT++ was not built.
- Exact version or commit: `820d04e7bb0ef53acaf6a41858ee7ea29f2754ca`
- Probe method: followed the unqualified `//` rule and Flex exclusive-state
  declarations through `propertyvalue` and `cplusplusbody`.
- Probe input:

~~~text
packet Ping {
  int sequence; // host comment
  @note(http://host/a//b)
}
cplusplus {{
// embedded C++, not an MSG host comment
}}
~~~

- Observed result: only `// host comment` is seen by the initial-state MSG
  comment rule; the other markers are consumed by exclusive-state rules.
- Conclusion and limits of the probe: confirms the contextual exclusions from
  source; malformed property/body recovery still needs deterministic tests.

### Representative examples

#### Line comment

~~~text
packet Ping {
    int sequence; // sequence number
}
~~~

Expected region: `// sequence number`.

#### Block comment

Unsupported.

#### Nested or contextual comment

~~~text
@note(http://host/a//b)
cplusplus {{
// embedded C++
}}
// host comment
~~~

Expected region: only the final `// host comment`.

### Adversarial boundaries

- Negative cases: double-quoted URLs, character literals, property values with
  `//`, embedded C++ comments, division-like single slash, and a bare slash.
- Malformed-input cases: unterminated string, property parenthesis, or
  `cplusplus {{` body; conservatively protect the remainder instead of exposing
  false host comments.
- Line-ending and Unicode cases: LF, CRLF, EOF without newline, lone CR as an
  explicit compatibility case, and Unicode payload with exact source offsets.
- Version or dialect counterexamples: generated C++ has C++ block comments and
  must not be merged into the MSG host contract.
- Cleaner preservation cases: keep a second slash in payload, URL text,
  indentation, empty `//`, and all property/embedded-body text.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add canonical `omnet_plus_plus_msg` with `//`,
  wrapper metadata, pinned evidence, and an MSG helper that skips string,
  character, property-value, and `{{ ... }}` body ranges.
- Deterministic tests to add: raw-label lookup, inline/full-line/EOF comments,
  strings and characters, nested property parentheses, embedded C++, malformed
  protected regions, grouping, all line endings, Unicode, and sanitizer
  preservation.
- Remaining blocker: define conservative recovery for malformed exclusive
  states before implementation is promoted.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## Option List

### Identity and scope

- Raw dataset label: `Option List` (3,892,154 files; 88,900,559 tokens)
- Proposed registry key: `option_list` only as an unsupported lookup identity;
  it is not a syntax key suitable for implementation.
- Existing family or aliases checked: `hash_line_style`, shell/config families,
  and filename-specific formats; no family represents every member.
- Classification: `aggregate`
- Versions or releases checked: upstream GitHub Linguist metadata commit
  `537297cdae3ab05f8d5dd1c03627a5bd73707b19` (v9.5.0).
- Dialects checked: the aggregate's listed filenames: `.ackrc`, `ackrc`,
  `.rspec`, `.yardopts`, and `mocha.opts`.
- Intended support scope: unresolved until inventory retains the exact filename
  and consuming tool for each record.
- Explicitly excluded scope: inferring a universal syntax from the `opts` or
  `ackrc` aliases, TextMate scope, Ace mode, or shell highlighting metadata.

### Syntax contract

- Line comments: unresolved; the label combines option files for unrelated
  programs and does not define a common lexer.
- Block comments: unresolved.
- Nested comments: unresolved.
- Termination at newline, delimiter, or EOF: unresolved.
- Inline use: unresolved and consumer-specific.
- Adjacent-line grouping: unresolved.
- Unclosed delimiter behavior: unresolved.
- Lexical or structural context: command-line option tokenization is delegated
  to each consuming tool and version; the aggregate supplies no dispatcher key
  beyond filename.
- Conflicts with strings, operators, directives, or embedded languages: `#`
  may be a comment in one member, an option argument or literal in another, and
  shell editor metadata is not a syntax specification.
- Sanitizer line wrappers: none until the member format is identified.
- Sanitizer block wrappers: none until the member format is identified.
- Content-preservation expectations: do not remove any bytes under the raw
  aggregate label. A future filename-aware dispatcher must preserve option
  values and pass each member to a separately researched contract.

### Evidence

- Official documentation permalink:
  [Linguist Option List metadata](https://github.com/github-linguist/linguist/blob/537297cdae3ab05f8d5dd1c03627a5bd73707b19/lib/linguist/languages.yml#L5489-L5505)
- Documentation version and relevant section: Linguist v9.5.0 classifies
  `Option List` as data and enumerates five exact filenames plus aliases.
- Official implementation or grammar permalink: no common implementation
  exists; representative consumers document independent formats in
  [RSpec option-file documentation](https://rspec.info/features/3-12/rspec-core/configuration/read-options-from-file/)
  and [ack documentation](https://beyondgrep.com/documentation/).
- Implementation version, file, and relevant symbol: not applicable to the
  aggregate; the pinned Linguist `languages.yml` entry is classifier metadata,
  not a parser.
- Conformance test or official example permalink:
  [Linguist Option List samples](https://github.com/github-linguist/linguist/tree/537297cdae3ab05f8d5dd1c03627a5bd73707b19/samples/Option%20List)
- Secondary source, if needed: none.
- Evidence conflicts or gaps: exact filenames are known, but Stack statistics
  expose only the aggregate label here. Consumer/version distribution and a
  per-record filename discriminator are missing.
- Confidence: `unresolved`

### Implementation confirmation

- Implementation tested: pinned classifier metadata inspected; no universal
  parser can be probed.
- Exact version or commit: `537297cdae3ab05f8d5dd1c03627a5bd73707b19`
- Probe method: enumerated all filenames assigned to the label and compared the
  named consuming tools.
- Probe input:

~~~text
.ackrc
.rspec
.yardopts
mocha.opts
~~~

- Observed result: these names are intentionally collapsed into one data label
  despite belonging to different command-line consumers.
- Conclusion and limits of the probe: proves aggregate identity, not shared
  comment syntax; no delimiter is accepted by this record.

### Representative examples

#### Line comment

Unresolved. A hash-prefixed line from one member is not evidence for all five.

#### Block comment

Unresolved.

#### Nested or contextual comment

The required context is the exact filename and tool version, which is absent
from the aggregated inventory.

### Adversarial boundaries

- Negative cases: `--option=#value`, URL fragments, shell-like quotes, regex
  arguments, option values beginning with punctuation, and any file whose
  basename is not retained.
- Malformed-input cases: unmatched quotes, continuations, and missing option
  arguments are consumer-specific and cannot define aggregate extraction.
- Line-ending and Unicode cases: unresolved independently for every member.
- Version or dialect counterexamples: `mocha.opts` and current Mocha
  configuration, RSpec `.rspec`, Yard `.yardopts`, and ack rc files are distinct
  formats even though Linguist groups them for classification.
- Cleaner preservation cases: preserve the entire file until routing is
  evidence-backed; especially keep hashes embedded in option values.

### Decision

- Recommended action: `defer`
- Registry fields to change: none; do not register `option_list` as a delimiter
  alias. Add a filename-aware routing layer only after each member is researched.
- Deterministic tests to add: raw aggregate label remains unsupported; later
  tests must route each exact filename and prove that punctuation in option
  values survives extraction and cleaning.
- Remaining blocker: a per-record exact filename/tool discriminator and
  separate evidence records for each member format.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## OverpassQL

### Identity and scope

- Raw dataset label: `OverpassQL` (3,327 files; 1,475,088 tokens)
- Proposed registry key: `overpassql`
- Existing family or aliases checked: `c_style` has the same `//` and
  non-nested `/* ... */` delimiter contract; no key collision exists.
- Classification: `language`
- Versions or releases checked: Overpass API `osm3s_v0.7.62`, commit
  `a0db4f392f744d5e1304331edbf542ef6d6ce2fa`.
- Dialects checked: textual Overpass QL; Overpass XML is excluded.
- Intended support scope: comments in Overpass QL outside single- and
  double-quoted strings.
- Explicitly excluded scope: XML comments, URL/string contents, shell wrappers,
  and comments in generated host-language clients.

### Syntax contract

- Line comments: `//` through the end of line.
- Block comments: `/* ... */`, ending at the first closer.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: line comments terminate at newline
  or EOF. A complete block terminates at `*/`.
- Inline use: valid for both forms.
- Adjacent-line grouping: valid for consecutive `//` lines.
- Unclosed delimiter behavior: invalid under the language documentation; only
  closed block matches are accepted. The current replacer consumes an unfinished
  block to stream end instead of clearly diagnosing it, so extraction must
  follow the documented complete-comment contract.
- Lexical or structural context: both quote forms protect comment markers and
  support backslash escapes. Block comments are a flat scanner, not recursive.
- Conflicts with strings, operators, directives, or embedded languages:
  `'https://host/a//b'`, `"/*literal*/"`, division-like slash, and a
  nested-looking opener inside a block must not widen the match.
- Sanitizer line wrappers: `("//", "")`.
- Sanitizer block wrappers: `("/*", "*/")`.
- Content-preservation expectations: remove only the outer wrapper; preserve
  block newlines, stars, URL payloads, and query text around inline comments.

### Evidence

- Official documentation permalink:
  [Overpass QL comments reference](https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL#Comments)
- Documentation version and relevant section: Overpass QL “Comments”; documents
  line and block forms and requires block closure.
- Official implementation or grammar permalink:
  [Comment_Replacer](https://github.com/drolbr/Overpass-API/blob/a0db4f392f744d5e1304331edbf542ef6d6ce2fa/src/expat/map_ql_input.cc#L31-L170)
- Implementation version, file, and relevant symbol: `osm3s_v0.7.62`,
  `map_ql_input.cc`, `Comment_Replacer::get` and its plain/single/double states.
- Conformance test or official example permalink:
  [Overpass QL source test inputs](https://github.com/drolbr/Overpass-API/tree/a0db4f392f744d5e1304331edbf542ef6d6ce2fa/osm-3s_testing/input)
- Secondary source, if needed: none.
- Evidence conflicts or gaps: documentation calls an unclosed block erroneous;
  the current preprocessing implementation silently reaches EOF. The supported
  contract deliberately accepts only closed blocks.
- Confidence: `cross-checked`

### Implementation confirmation

- Implementation tested: pinned source-level state-machine trace; binary not
  built.
- Exact version or commit: `a0db4f392f744d5e1304331edbf542ef6d6ce2fa`
- Probe method: traced slash lookahead in plain state and quote/escape state
  transitions.
- Probe input:

~~~text
node["website"="https://host/a//b"]; // line
/* outer /* inner */ out;
~~~

- Observed result: the URL remains protected; the suffix is a line comment; the
  block ends at the first `*/` and the remaining text is query input.
- Conclusion and limits of the probe: proves non-nesting and quote protection;
  the malformed-EOF policy is resolved normatively from documentation.

### Representative examples

#### Line comment

~~~text
node["amenity"="cafe"]; // cafes
~~~

Expected region: `// cafes`.

#### Block comment

~~~text
/* collect named cafes */
node["amenity"="cafe"]["name"];
~~~

Expected region: `/* collect named cafes */`.

#### Nested or contextual comment

~~~text
node["website"="https://host/a//b"]; /* host query comment */
~~~

Only the block is a comment.

### Adversarial boundaries

- Negative cases: both quote forms, escaped quotes/backslashes, URLs, single
  slash, and comment-looking query values.
- Malformed-input cases: unclosed block, stray `*/`, unterminated quote before a
  marker, and nested-looking blocks that close at the first delimiter.
- Line-ending and Unicode cases: LF, CRLF, EOF line comment, Unicode tag values
  and payloads, and exact offsets around escaped text.
- Version or dialect counterexamples: Overpass XML uses XML comment syntax and
  is not an alias.
- Cleaner preservation cases: block interior newlines/stars, empty comments,
  Unicode, and untouched quoted URL markers.

### Decision

- Recommended action: `alias`
- Registry fields to change: add `overpassql` to `c_style.aliases` with pinned
  evidence/notes and documented closed-block behavior.
- Deterministic tests to add: raw-label lookup, both forms, both quote forms and
  escapes, first-close non-nesting, unclosed block rejection, stray closer,
  inline/grouping, line endings, Unicode, and sanitizer preservation.
- Remaining blocker: none; tests must lock the documentation-first unclosed
  behavior.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## Pact

### Identity and scope

- Raw dataset label: `Pact` (14,751 files; 109,427,776 tokens)
- Proposed registry key: `pact`
- Existing family or aliases checked: `semicolon_style` exactly matches Pact's
  single-semicolon line delimiter; no key collision exists.
- Classification: `language`
- Versions or releases checked: Pact 5.4, commit
  `6c81f4cf0631a4087f8350230bd9b7c3714f9751`.
- Dialects checked: Pact 5 source and checked-in Pact contract examples.
- Intended support scope: lexical comments in Pact source outside strings.
- Explicitly excluded scope: JSON/YAML request data, Markdown documentation,
  REPL output, and comments in host-language SDK code.

### Syntax contract

- Line comments: one `;` begins a comment and consumes through newline or EOF.
  Conventional `;;` starts the same token; the second semicolon is payload.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: newline or EOF. The lexer pattern
  optionally consumes newline, but extraction must exclude line-ending bytes.
- Inline use: valid; official contracts use suffix comments.
- Adjacent-line grouping: valid for consecutive semicolon-comment lines.
- Unclosed delimiter behavior: not applicable.
- Lexical or structural context: a quote invokes `stringLiteral`, which consumes
  and validates the whole double-quoted literal before scanning resumes.
- Conflicts with strings, operators, directives, or embedded languages:
  semicolons inside strings are data. Semicolon is absent from Pact's identifier
  symbol class and has no operator role.
- Sanitizer line wrappers: `(";", "")`.
- Sanitizer block wrappers: none.
- Content-preservation expectations: remove exactly the first semicolon. For
  `;; documentation-style text`, preserve the second semicolon as payload.

### Evidence

- Official documentation permalink:
  [Pact core syntax semantics](https://github.com/kadena-io/pact-5/blob/6c81f4cf0631a4087f8350230bd9b7c3714f9751/pact/Pact/Core/Semantics.md#L28-L42)
- Documentation version and relevant section: Pact 5.4 lexical grammar;
  `comment ::= ';'` followed by characters through newline.
- Official implementation or grammar permalink:
  [Pact lexer](https://github.com/kadena-io/pact-5/blob/6c81f4cf0631a4087f8350230bd9b7c3714f9751/pact/Pact/Core/Syntax/Lexer.x#L23-L43)
- Implementation version, file, and relevant symbol: Pact 5.4,
  `Lexer.x`, `@comment` and skipped token rule.
- Conformance test or official example permalink:
  [accounts.pact](https://github.com/kadena-io/pact-5/blob/6c81f4cf0631a4087f8350230bd9b7c3714f9751/examples/accounts/accounts.pact#L1-L18)
- Secondary source, if needed: none.
- Evidence conflicts or gaps: none; the grammar, lexer, and examples agree.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: pinned grammar/lexer trace and official example
  inspection; Pact executable not built.
- Exact version or commit: `6c81f4cf0631a4087f8350230bd9b7c3714f9751`
- Probe method: compared `@comment` token priority with the quote action and
  identifier symbol set.
- Probe input:

~~~text
(defconst note "semi;colon") ; suffix
;; heading at EOF
~~~

- Observed result: the string semicolon is inside one string token; each later
  first semicolon starts a skipped comment through line end/EOF.
- Conclusion and limits of the probe: establishes the lexical contract without
  executing Pact.

### Representative examples

#### Line comment

~~~text
(use system) ;; mock system library
~~~

Expected region: `;; mock system library`, with one semicolon retained after
cleaning.

#### Block comment

Unsupported.

#### Nested or contextual comment

~~~text
(defconst url "https://host/a;b") ; deployment note
~~~

Only `; deployment note` is a comment.

### Adversarial boundaries

- Negative cases: semicolon in ordinary/continued strings, escaped quotes,
  apostrophe identifiers, and punctuation in docstrings.
- Malformed-input cases: empty `;`/`;;` at EOF and an unterminated string before
  a semicolon; do not expose markers inside the malformed string.
- Line-ending and Unicode cases: LF, CRLF, EOF without newline, Unicode payload,
  and exact source ranges despite the lexer's optional newline consumption.
- Version or dialect counterexamples: host Haskell comments and request-data
  formats are excluded.
- Cleaner preservation cases: preserve the second semicolon in `;;`, indentation,
  code-like payloads, URLs, and empty bodies.

### Decision

- Recommended action: `alias`
- Registry fields to change: add `pact` to `semicolon_style.aliases` and attach
  Pact-specific pinned evidence/notes where supported.
- Deterministic tests to add: raw-label lookup, single/double semicolon,
  inline/full-line/EOF, strings and continuation escapes, grouping, CRLF,
  Unicode, and sanitizer preservation of the second semicolon.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## OMNeT++ NED

### Identity and scope

- Raw dataset label: `OMNeT++ NED` (215,986 files; 297,461,483 tokens)
- Proposed registry key: `omnet_plus_plus_ned`
- Existing family or aliases checked: `slash_line_style` and `c_style`; neither
  contains this key, and neither records the NED property-value mode.
- Classification: `language`
- Versions or releases checked: OMNeT++ 6.4.0 development source, commit
  `820d04e7bb0ef53acaf6a41858ee7ea29f2754ca`; NED-2 lexer.
- Dialects checked: NED declarations, expressions, properties, and both
  single- and double-quoted literals.
- Intended support scope: comments recognized by the NED-2 host lexer.
- Explicitly excluded scope: `omnetpp.ini`, MSG files, NED property-value text,
  quoted strings, XML payloads, generated C++, and documentation rendering.

### Syntax contract

- Line comments: `//` in the initial NED lexer state, through the physical line.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: the lexer stops at LF or EOF and
  leaves LF for whitespace. CRLF traverses CR before LF; extraction should not
  include line-ending bytes and should test lone CR separately.
- Inline use: valid; the manual explicitly permits comments at line ends.
- Adjacent-line grouping: valid for consecutive host `//` lines.
- Unclosed delimiter behavior: not applicable; EOF terminates a line comment.
- Lexical or structural context: single- and double-quoted strings are exclusive
  states. `@property(...)` values use another exclusive state, including nested
  parentheses/brackets/braces, so `//` there is ordinary property content.
- Conflicts with strings, operators, directives, or embedded languages:
  `"https://host/a//b"`, `'a//b'`, and `@display("t=//";url=http://x//y)` are
  protected. NED has no `/* ... */` source-comment form.
- Sanitizer line wrappers: `("//", "")`.
- Sanitizer block wrappers: none.
- Content-preservation expectations: remove only `//` from verified host
  comments; preserve payload and never alter property or quoted content.

### Evidence

- Official documentation permalink:
  [NED reference, Comments](https://github.com/omnetpp/omnetpp/blob/820d04e7bb0ef53acaf6a41858ee7ea29f2754ca/doc/src/manual/appendix-ned-ref.tex#L113-L119)
- Documentation version and relevant section: OMNeT++ 6.4 manual source,
  Appendix NED Reference, “Comments”; `//` continues to line end.
- Official implementation or grammar permalink:
  [NED-2 lexer](https://github.com/omnetpp/omnetpp/blob/820d04e7bb0ef53acaf6a41858ee7ea29f2754ca/src/nedxml/ned2.lex#L58-L182)
- Implementation version, file, and relevant symbol: commit above,
  `src/nedxml/ned2.lex`; initial comment rule, literal states, and exclusive
  `propertyvalue` rules.
- Conformance test or official example permalink:
  [NED language manual example](https://github.com/omnetpp/omnetpp/blob/820d04e7bb0ef53acaf6a41858ee7ea29f2754ca/doc/src/manual/ch-ned-lang.tex#L133-L150)
- Secondary source, if needed: none.
- Evidence conflicts or gaps: the reference does not discuss property-state
  exclusions or bare CR; the official lexer supplies the former.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: source-level lexer trace; OMNeT++ was not built.
- Exact version or commit: `820d04e7bb0ef53acaf6a41858ee7ea29f2754ca`
- Probe method: compared the initial `//` rule with the exclusive
  `stringliteral`, `stringliteral2`, and `propertyvalue` rules.
- Probe input:

~~~text
simple Server {
    parameters:
        string endpoint = "http://host/a//b"; // host comment
        @note(url=http://host/a//b)
}
~~~

- Observed result: the suffix is an initial-state comment; both earlier markers
  are consumed as string/property content.
- Conclusion and limits of the probe: establishes lexer-state boundaries from
  pinned source; malformed-state recovery was not executed.

### Representative examples

#### Line comment

~~~text
double delay = 1ms; // propagation delay
~~~

Expected region: `// propagation delay`.

#### Block comment

Unsupported.

#### Nested or contextual comment

~~~text
@metadata(url=http://host/a//b)
// NED host comment
~~~

Expected region: only `// NED host comment`.

### Adversarial boundaries

- Negative cases: `//` in both quote forms, escaped quotes, nested property
  values, URL text, `/*literal*/`, and a single slash.
- Malformed-input cases: unterminated quotes and properties; protect the
  remainder rather than recover permissively.
- Line-ending and Unicode cases: LF, CRLF, EOF comment, lone CR compatibility,
  Unicode identifiers/payloads, and exact offsets near multibyte text.
- Version or dialect counterexamples: INI uses hash comments and MSG has an
  embedded-C++ mode; neither contract may be aliased to NED.
- Cleaner preservation cases: empty comments, documentation punctuation,
  indentation, URL payloads, and untouched property/string markers.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add canonical `omnet_plus_plus_ned` with `//` and
  a NED helper that protects both quote modes and balanced property values.
- Deterministic tests to add: raw-label lookup, inline/full-line/EOF comments,
  both strings and escapes, nested properties, malformed regions, grouping,
  LF/CRLF/lone CR, Unicode, and sanitizer preservation.
- Remaining blocker: specify conservative malformed property/string recovery.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## PDDL

### Identity and scope

- Raw dataset label: `PDDL` (2,781,326 files; 17,825,018,143 tokens)
- Proposed registry key: `pddl`
- Existing family or aliases checked: `semicolon_style` has the same line
  delimiter; no `pddl` collision exists.
- Classification: `language`
- Versions or releases checked: original PDDL 1.2 definition and the maintained
  VAL PDDL 2.2 lexer at commit
  `3c7a1f330bdab0ba28a4762bb45c3f06c27fb6d4`.
- Dialects checked: domain/problem syntax and VAL-supported temporal/numeric
  extensions; planner-specific preprocessing languages are excluded.
- Intended support scope: lexical PDDL comments beginning with semicolon.
- Explicitly excluded scope: planner command files, Lisp implementation source,
  generated plans, and non-PDDL solver extensions with their own literal syntax.

### Syntax contract

- Line comments: `;` through the end of the physical line.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: newline or EOF; extraction excludes
  the line-ending bytes.
- Inline use: valid.
- Adjacent-line grouping: valid for consecutive semicolon-comment lines.
- Unclosed delimiter behavior: not applicable.
- Lexical or structural context: the VAL lexer defines `comment ;.*$` and skips
  it before grammar tokens. Core PDDL has no ordinary quoted-string token that
  changes semicolon recognition.
- Conflicts with strings, operators, directives, or embedded languages:
  parentheses, colon-prefixed requirements/fields, minus, and equality are not
  comment markers; `;;` is one comment whose payload starts with semicolon.
- Sanitizer line wrappers: `(";", "")`.
- Sanitizer block wrappers: none.
- Content-preservation expectations: remove exactly one semicolon and preserve
  payload, indentation, domain symbols, and Unicode.

### Evidence

- Official documentation permalink:
  [PDDL 1.2 language manual](https://ipc08.icaps-conference.org/deterministic/data/mcdermott-et-al-tr-1998.pdf)
- Documentation version and relevant section: McDermott et al., PDDL 1.2
  lexical conventions; semicolon comments extend through line end.
- Official implementation or grammar permalink:
  [VAL PDDL lexer](https://github.com/KCL-Planning/VAL/blob/3c7a1f330bdab0ba28a4762bb45c3f06c27fb6d4/libraries/VAL/src/Parser/pddl%2B.l#L15-L25)
- Implementation version, file, and relevant symbol: current VAL commit,
  `pddl+.l`; `comment ;.*$`, skipped at the lexer rule near line 163.
- Conformance test or official example permalink:
  [VAL PDDL samples](https://github.com/KCL-Planning/VAL/tree/3c7a1f330bdab0ba28a4762bb45c3f06c27fb6d4/samples)
- Secondary source, if needed:
  [IPC PDDL resources](https://ipc02.icaps-conference.org/pddl.html)
- Evidence conflicts or gaps: no delimiter conflict across the checked core
  versions; arbitrary planner extensions were not generalized.
- Confidence: `cross-checked`

### Implementation confirmation

- Implementation tested: pinned lexer/source examples inspected; VAL not built.
- Exact version or commit: `3c7a1f330bdab0ba28a4762bb45c3f06c27fb6d4`
- Probe method: traced the Flex comment definition to its skipped rule and
  checked VAL sample domains containing `;` and `;;` comments.
- Probe input:

~~~text
(:action move ; move one object
  :parameters (?x))
;; note at EOF
~~~

- Observed result: each first semicolon consumes the remaining physical line;
  the following PDDL form resumes on the next line.
- Conclusion and limits of the probe: confirms lexical behavior in VAL; it does
  not claim syntax for vendor-specific preprocessor extensions.

### Representative examples

#### Line comment

~~~text
(:requirements :strips) ; baseline domain
~~~

Expected region: `; baseline domain`.

#### Block comment

Unsupported.

#### Nested or contextual comment

~~~text
;; temporal notes
(:durative-action travel)
~~~

The first semicolon is scaffolding; the second is preserved payload.

### Adversarial boundaries

- Negative cases: colons in `:requirements`, parentheses, minus signs, equality,
  slash-like planner names, and `#` directives from unrelated formats.
- Malformed-input cases: empty `;`/`;;` at EOF, unbalanced PDDL parentheses
  around a valid comment, and a stray block-comment-looking sequence.
- Line-ending and Unicode cases: LF, CRLF, EOF without newline, Unicode payloads,
  and exact ranges beside non-ASCII names.
- Version or dialect counterexamples: planner command/config files and embedded
  Lisp are not PDDL source.
- Cleaner preservation cases: retain the second semicolon in `;;`, PDDL-looking
  payload, indentation, and blank comment bodies.

### Decision

- Recommended action: `alias`
- Registry fields to change: add `pddl` to `semicolon_style.aliases` with pinned
  PDDL/VAL evidence.
- Deterministic tests to add: raw-label lookup, inline/full-line/EOF,
  single/double semicolon, grouping, parentheses/colon negatives, LF/CRLF,
  Unicode, and sanitizer preservation.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## Pip Requirements

### Identity and scope

- Raw dataset label: `Pip Requirements` (10,340,460 files; 2,778,709,779 tokens)
- Proposed registry key: `pip_requirements`
- Existing family or aliases checked: `hash_line_style` is too broad because it
  treats every hash as a comment; `star_style` has the boundary regex but its
  ordinary quote protection would not reproduce pip's preprocessing order.
- Classification: `document-format`
- Versions or releases checked: pip `26.3.dev0`, commit
  `6236392d41f0623476b9dbca2f1c55b832ee7e43`.
- Dialects checked: pip requirements-file format, URL requirements, supported
  options, encoding declarations, and line continuations.
- Intended support scope: comments removed by pip's requirements preprocessor.
- Explicitly excluded scope: PEP 508 requirement syntax outside files,
  constraints semantics beyond the shared preprocessor, pyproject/TOML,
  shell command lines, and URL fragments without a whitespace boundary.

### Syntax contract

- Line comments: `#` through line end only when it begins a logical line or is
  preceded by one or more whitespace characters.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: physical line end or EOF.
- Inline use: valid only at the whitespace boundary. `name#fragment` is data.
- Adjacent-line grouping: valid for consecutive physical comment lines; retain
  their distinct source ranges even when continuation preprocessing associates
  a comment with an earlier logical line.
- Unclosed delimiter behavior: not applicable.
- Lexical or structural context: pip joins lines ending in an unescaped
  backslash before applying `(^|\s+)#.*$`. A standalone continued comment is
  deliberately padded so it is still recognized. The regex is not quote-aware.
- Conflicts with strings, operators, directives, or embedded languages: URL
  fragments such as `#egg=wat` and `#sha256=...` are not comments without
  whitespace. Conversely, quote-looking option text does not protect a
  whitespace-prefixed hash from pip's preprocessor.
- Sanitizer line wrappers: `("#", "")`; do not remove the whitespace that made
  the marker valid.
- Sanitizer block wrappers: none.
- Content-preservation expectations: remove only the verified hash wrapper,
  preserve payload and source positioning, and never truncate URL fragments or
  requirement names.

### Evidence

- Official documentation permalink:
  [pip requirements-file comments](https://github.com/pypa/pip/blob/6236392d41f0623476b9dbca2f1c55b832ee7e43/docs/html/reference/requirements-file-format.md#L57-L75)
- Documentation version and relevant section: pip 26.3.dev0, “Encoding,” “Line
  continuations,” and “Comments”; comment stripping follows continuation joins.
- Official implementation or grammar permalink:
  [requirements preprocessor](https://github.com/pypa/pip/blob/6236392d41f0623476b9dbca2f1c55b832ee7e43/src/pip/_internal/req/req_file.py#L39-L42)
- Implementation version, file, and relevant symbol: commit above,
  `req_file.py`; `COMMENT_RE`, `join_lines`, and `ignore_comments` at
  [lines 496-533](https://github.com/pypa/pip/blob/6236392d41f0623476b9dbca2f1c55b832ee7e43/src/pip/_internal/req/req_file.py#L496-L533).
- Conformance test or official example permalink:
  [pip URL/comment tests](https://github.com/pypa/pip/blob/6236392d41f0623476b9dbca2f1c55b832ee7e43/tests/unit/test_req_file.py#L878-L944)
- Secondary source, if needed: none.
- Evidence conflicts or gaps: none for the marker boundary. Exact extraction
  spans must be mapped back from pip's logical joined lines to physical source.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: official preprocessing tests and pinned source
  inspected; pip's suite was not rerun.
- Exact version or commit: `6236392d41f0623476b9dbca2f1c55b832ee7e43`
- Probe method: traced `preprocess` ordering and compared checked-in continuation,
  suffix-comment, and `#egg` test expectations.
- Probe input:

~~~text
req1 \
# continued comment
https://host/pkg.tgz#egg=pkg
pkg==1 # pinned
~~~

- Observed result: both physical comment markers are stripped; `#egg=pkg` is
  retained as URL data.
- Conclusion and limits of the probe: verifies logical boundary behavior from
  tests/source; an extractor still needs its own exact physical-span tests.

### Representative examples

#### Line comment

~~~text
requests==2.32.0  # application dependency
~~~

Expected region: `# application dependency`.

#### Block comment

Unsupported.

#### Nested or contextual comment

~~~text
package @ https://host/pkg.tgz#sha256=abc
other-package \
    # comment after continuation
~~~

Only the second hash region is a comment.

### Adversarial boundaries

- Negative cases: URL `#egg`/`#sha256` fragments, hashes adjacent to names,
  hashes inside unspaced option values, PEP 508 semicolons, and ordinary URL
  schemes.
- Malformed-input cases: trailing unescaped backslash at EOF, multiple
  backslashes, a continued empty/comment line, and unmatched quote-looking text.
- Line-ending and Unicode cases: LF, CRLF, EOF comments, UTF-8/PEP 263 encoding
  comments, Unicode URLs/payloads, and exact physical offsets across joins.
- Version or dialect counterexamples: shell `requirements` commands and TOML
  dependency arrays use different syntax.
- Cleaner preservation cases: keep boundary whitespace, URL fragments,
  backslashes/newlines, hash-like payloads, and encoding declaration contents.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add canonical `pip_requirements` with a helper that
  reproduces pip's whitespace boundary and continuation order while emitting
  exact physical `#...` ranges; bypass generic quote shielding for this format.
- Deterministic tests to add: official continuation cases, URL fragments,
  inline/full-line/EOF, quote-looking option values, escaped backslashes,
  encodings, grouping, LF/CRLF, Unicode, exact slices, and sanitizer
  preservation.
- Remaining blocker: specify and test logical-to-physical span mapping across
  continuations before implementation.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## Pkl

### Identity and scope

- Raw dataset label: `Pkl` (65,293 files; 2,151,192,141 tokens)
- Proposed registry key: `pkl`
- Existing family or aliases checked: `c_style` shares the current delimiters,
  but its generic quote scan does not model Pkl's pound-delimited/multiline
  strings or interpolation.
- Classification: `language`
- Versions or releases checked: Pkl 0.33.0, commit
  `417c08ae113740fd26b05fcb032c23cc5be0d425`, plus the documented 0.29
  block-nesting change.
- Dialects checked: Pkl 0.29+ modules, ordinary/doc comments, all string
  delimiter widths, multiline strings, interpolation, and the initial shebang.
- Intended support scope: unresolved for the unversioned raw label; Pkl 0.29+
  and Pkl 0.28-and-earlier assign different spans to the same nested-looking
  block source.
- Explicitly excluded scope: shebang directives, generated JSON/YAML, and
  comments in embedded resource text. Neither Pkl version line is discarded as
  irrelevant to the full-dataset contract.

### Syntax contract

- Line comments: `//` and `///` doc comments through CR, LF, or EOF.
- Block comments: `/* ... */`, non-nested in Pkl 0.29+.
- Nested comments: unsupported in the intended current scope; the first `*/`
  closes the block. Pkl 0.28 and earlier instead balance nested `/* ... */`, so
  this rule cannot be selected from the raw label alone.
- Termination at newline, delimiter, or EOF: line forms stop before CR/LF or at
  EOF; blocks require a closer.
- Inline use: valid for line and block comments.
- Adjacent-line grouping: ordinary `//` lines may group; consecutive `///`
  lines are explicitly merged by Pkldoc and should retain doc-line identity.
- Unclosed delimiter behavior: invalid; the current lexer throws at EOF.
- Lexical or structural context: ordinary, multiline, and arbitrary
  pound-delimited strings protect markers in string text. `\#*(...)`
  interpolation returns to default lexer state, where comments are real.
- Conflicts with strings, operators, directives, or embedded languages:
  markers in `"..."`, `"""..."""`, and `#"..."#` are data; `/` and `~/` are
  operators. An initial `#!` is a shebang token, not an extracted source comment.
- Sanitizer line wrappers: longest-first `("///", "")` then `("//", "")`.
- Sanitizer block wrappers: `("/*", "*/")`.
- Content-preservation expectations: strip the full doc introducer, preserve
  Markdown/doc payload, block newlines, and raw string text; expose only genuine
  comments in interpolation code.

### Evidence

- Official documentation permalink:
  [Pkl comment reference](https://github.com/apple/pkl/blob/417c08ae113740fd26b05fcb032c23cc5be0d425/docs/modules/language-reference/pages/index.adoc#L50-L88)
- Documentation version and relevant section: Pkl 0.33.0 language reference,
  “Comments” and doc comments.
- Official implementation or grammar permalink:
  [Pkl lexer comment rules](https://github.com/apple/pkl/blob/417c08ae113740fd26b05fcb032c23cc5be0d425/pkl-parser/src/main/java/org/pkl/parser/Lexer.java#L598-L633)
- Implementation version, file, and relevant symbol: 0.33.0 `Lexer.java`,
  `lexSlash`/`lexBlockComment` and string/interpolation states.
- Conformance test or official example permalink:
  [Pkl 0.29 release note](https://github.com/apple/pkl/blob/417c08ae113740fd26b05fcb032c23cc5be0d425/docs/modules/release-notes/pages/0.29.adoc#L303-L327)
- Secondary source, if needed: none.
- Evidence conflicts or gaps: the current language-reference text still calls
  blocks nestable, but the 0.29 release note says nesting was removed and the
  0.33 lexer terminates at the first closer. Release note plus implementation
  define the current contract; pre-0.29 files remain excluded.
- Confidence: `cross-checked`

### Implementation confirmation

- Implementation tested: pinned lexer state machine inspected; Pkl not built.
- Exact version or commit: `417c08ae113740fd26b05fcb032c23cc5be0d425`
- Probe method: traced `lexSlash`/`lexBlockComment`, pound-counted string states,
  and the interpolation transition back to `DEFAULT`.
- Probe input:

~~~text
value = #"https://host/a//b /* text */"#
/* outer /* inner */ tail */
/// docs
~~~

- Observed result: string markers are protected; the block token ends at the
  first closer; the trailing `tail */` is code/error input; `/// docs` is a doc
  token.
- Conclusion and limits of the probe: establishes current source behavior but
  cannot determine which rule applies to an unversioned dataset record.

### Representative examples

#### Line comment

~~~text
/// Port used by the service.
port = 8080 // local default
~~~

Expected regions: the complete `///` and `//` lines.

#### Block comment

~~~text
/* deployment
   defaults */
environment = "prod"
~~~

Expected region: the closed block.

#### Nested or contextual comment

~~~text
literal = #"""// not a comment
/* still string */
"""#
text = "value \(1 + 2 /* interpolation comment */)"
~~~

Only the block inside interpolation code is a comment.

### Adversarial boundaries

- Negative cases: all pound widths, multiline strings, escaped quotes,
  string-text markers, division, integer division, and initial shebang.
- Malformed-input cases: unclosed block/string/interpolation, mismatched pound
  count, stray `*/`, and nested-looking block ending at the first closer.
- Line-ending and Unicode cases: LF, CRLF, CR, EOF line comments, Unicode doc
  payloads/string text, and exact offsets through interpolation.
- Version or dialect counterexamples: Pkl <=0.28 nests blocks; the same sample
  has a different outer span and must not silently share the 0.29+ oracle.
- Cleaner preservation cases: remove all three doc slashes, preserve Markdown,
  raw/multiline string markers, inner block text, and interpolation surroundings.

### Decision

- Recommended action: `defer`
- Registry fields to change: none; do not register `pkl` with either nested or
  first-close block behavior while the full-dataset record has no version
  discriminator.
- Deterministic tests to add after resolution: raw-label lookup,
  line/doc/block forms, both version-specific block spans, every string form,
  interpolation comments, operators, shebang, malformed input, line endings,
  Unicode, grouping, and cleaning.
- Remaining blocker: a deterministic source-version signal or an explicit
  corpus policy for the incompatible pre-0.29 and 0.29+ block contracts.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## Polar

### Identity and scope

- Raw dataset label: `Polar` (8,491 files; 3,421,274 tokens)
- Proposed registry key: `polar`
- Existing family or aliases checked: `hash_line_style` has the same unrestricted
  hash-to-line-end delimiter outside strings; no key collision exists.
- Classification: `language`
- Versions or releases checked: Oso/Polar core 0.27.3, commit
  `7292df01679c8b3d7c92fbc08754bbb66647c1cc`.
- Dialects checked: Polar policy files loaded by Oso, including inline comments
  and escaped double-quoted strings.
- Intended support scope: comments recognized by the Polar lexer.
- Explicitly excluded scope: comments in host Python/Ruby/Java/Rust code,
  Markdown documentation, generated policy data, and Oso Cloud APIs.

### Syntax contract

- Line comments: `#` anywhere outside a string, through CR, LF, or EOF.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: CR, LF, or EOF; line-ending bytes
  are excluded from the extracted range.
- Inline use: valid, with or without whitespace before the hash.
- Adjacent-line grouping: valid for consecutive hash-comment lines.
- Unclosed delimiter behavior: not applicable.
- Lexical or structural context: `skip_whitespace` consumes comments between
  tokens; the string scanner consumes escaped double-quoted strings as one token.
- Conflicts with strings, operators, directives, or embedded languages: hashes
  in strings are data. `?=`, semicolon, pipe, comparison, slash, `mod`, and
  `rem` are tokens/operators, not comments.
- Sanitizer line wrappers: `("#", "")`.
- Sanitizer block wrappers: none.
- Content-preservation expectations: remove only the first hash and retain any
  additional heading hashes, payload whitespace, Unicode, and policy text.

### Evidence

- Official documentation permalink:
  [Polar syntax guide](https://github.com/osohq/oso/blob/7292df01679c8b3d7c92fbc08754bbb66647c1cc/docs/content/any/reference/polar/polar-syntax/index.md#L11-L55)
- Documentation version and relevant section: archived Oso documentation at the
  pinned commit; syntax guide and its checked-in policy examples use `#` comments
  and define escaped double-quoted strings.
- Official implementation or grammar permalink:
  [Polar lexer comment loop](https://github.com/osohq/oso/blob/7292df01679c8b3d7c92fbc08754bbb66647c1cc/polar-core/src/lexer.rs#L149-L173)
- Implementation version, file, and relevant symbol: `polar-core 0.27.3`,
  `lexer.rs`, `Lexer::skip_whitespace` and `scan_string`.
- Conformance test or official example permalink:
  [official inline-comment policy](https://github.com/osohq/oso/blob/7292df01679c8b3d7c92fbc08754bbb66647c1cc/languages/python/oso/tests/parity/policies/test_api.polar#L38-L54)
- Secondary source, if needed: none.
- Evidence conflicts or gaps: no syntax conflict; the prose guide demonstrates
  rather than separately specifies comment termination.
- Confidence: `verified`

### Implementation confirmation

- Implementation tested: pinned Rust lexer and official policies inspected; Oso
  test suite not run.
- Exact version or commit: `7292df01679c8b3d7c92fbc08754bbb66647c1cc`
- Probe method: traced token completion into `skip_whitespace` and the
  independent escaped-string scanner.
- Probe input:

~~~text
allow(user, "read#literal", resource);#inline
# full line at EOF
~~~

- Observed result: the string hash remains in `Token::String`; both later hashes
  consume through line end/EOF.
- Conclusion and limits of the probe: establishes lexical spans from source; no
  runtime build was needed for the undisputed delimiter.

### Representative examples

#### Line comment

~~~text
allow(user, "read", resource); # default read rule
~~~

Expected region: `# default read rule`.

#### Block comment

Unsupported.

#### Nested or contextual comment

~~~text
matches(value, "role#admin"); # hash in string is data
~~~

Only the suffix is a comment.

### Adversarial boundaries

- Negative cases: escaped double-quoted strings containing hashes, `?=`,
  semicolon, slash, pipe, and host-language comment forms.
- Malformed-input cases: empty `#` at EOF and an unterminated string before a
  hash; conservatively protect the malformed string remainder.
- Line-ending and Unicode cases: LF, CRLF, lone CR, EOF, Unicode policy strings
  and payloads, and exact ranges near multibyte characters.
- Version or dialect counterexamples: Oso SDK host files use their host
  language's comments and are excluded.
- Cleaner preservation cases: retain extra hashes in `### heading`, indentation,
  escaped string text, empty payloads, and Unicode.

### Decision

- Recommended action: `alias`
- Registry fields to change: add `polar` to `hash_line_style.aliases` with
  pinned Oso/Polar evidence.
- Deterministic tests to add: raw-label lookup, inline/full-line/EOF without
  required whitespace, strings and escapes, empty/multiple hashes, grouping,
  CR/LF/CRLF, Unicode, and sanitizer preservation.
- Remaining blocker: none.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01

## Praat

### Identity and scope

- Raw dataset label: `Praat` (10,121 files; 18,396,552 tokens)
- Proposed registry key: `praat`
- Existing family or aliases checked: `hash_line_style` and
  `semicolon_style` each cover only part of Praat and would falsely accept
  inline `#`/`!` or miss the other markers.
- Classification: `language`
- Versions or releases checked: current Praat development source
  `7.0beta`, commit `5d452fe3490bdc8d0edd12196a74127795b6a20a`, with
  current scripting/formula manuals and checked-in scripts.
- Dialects checked: Praat scripts, formulas, form bodies, continuation lines,
  straight/curly quoted strings, and current implementation-only bang lines.
- Intended support scope: source comments ignored by the current Praat script
  interpreter and formula lexer.
- Explicitly excluded scope: Praat TextGrid/data files, manual markup, C++
  implementation comments, vector/matrix variable suffixes, and hashes or bangs
  used inside formulas.

### Syntax contract

- Line comments: after leading horizontal whitespace, `#`, `;`, or `!` makes
  the whole physical line a comment. `#` and `;` are documented; `!` is accepted
  by the current interpreter implementation. In addition, `;` outside a string
  terminates a formula/command and makes the physical-line remainder comment
  text.
- Block comments: unsupported.
- Nested comments: unsupported.
- Termination at newline, delimiter, or EOF: all accepted forms end at CR, LF,
  or EOF and exclude the line-ending bytes.
- Inline use: `;` is valid inline. `#` and `!` are whole-line-only after leading
  whitespace.
- Adjacent-line grouping: valid for consecutive whole-line comments, including
  mixed markers; ordinary inline suffixes remain separate around their code.
- Unclosed delimiter behavior: not applicable.
- Lexical or structural context: the helper must skip straight double-quoted
  strings with doubled quotes and Praat's curly-quoted string form. It must
  recognize leading horizontal whitespace and continuation lines.
- Conflicts with strings, operators, directives, or embedded languages:
  `values#` and `matrix##` are numeric vector/matrix symbols; `!=` and unary
  `!` are formula operators; marker characters in quoted strings are data.
- Sanitizer line wrappers: contextual `("#", "")`, `(";", "")`, and
  `("!", "")`.
- Sanitizer block wrappers: none.
- Content-preservation expectations: remove exactly the validated marker and
  preserve payload, vector/matrix suffixes, operators, quotes, indentation, and
  script code before an inline semicolon.

### Evidence

- Official documentation permalink:
  [Praat scripting layout/comments](https://github.com/praat/praat/blob/5d452fe3490bdc8d0edd12196a74127795b6a20a/fon/manual_scripting.cpp#L942-L975)
- Documentation version and relevant section: current scripting manual,
  “Scripting 3.7. Layout”; leading whitespace and whole-line `#`/`;` comments.
  Official examples also show
  [inline semicolon comments](https://github.com/praat/praat/blob/5d452fe3490bdc8d0edd12196a74127795b6a20a/fon/manual_scripting.cpp#L1029-L1049).
- Official implementation or grammar permalink:
  [Praat interpreter line skipping](https://github.com/praat/praat/blob/5d452fe3490bdc8d0edd12196a74127795b6a20a/sys/Interpreter.cpp#L369-L381)
- Implementation version, file, and relevant symbol: `7.0beta` source;
  `Interpreter.cpp` skips first-nonspace `#`/`;`/`!` lines,
  [praat_executeCommand](https://github.com/praat/praat/blob/5d452fe3490bdc8d0edd12196a74127795b6a20a/sys/praat_script.cpp#L182-L190)
  skips the same command-leading markers, and
  [Formula lexical analysis](https://github.com/praat/praat/blob/5d452fe3490bdc8d0edd12196a74127795b6a20a/sys/Formula.cpp#L887-L938)
  treats semicolon as end while parsing both quote forms.
- Conformance test or official example permalink:
  [checked-in Praat script comments](https://github.com/praat/praat/blob/5d452fe3490bdc8d0edd12196a74127795b6a20a/dwtest/test_Matrix_solve.praat#L35-L45)
- Secondary source, if needed: none.
- Evidence conflicts or gaps: the user manual names only `#` and `;` for
  whole-line comments; current interpreter code also accepts `!`. The latter is
  scoped explicitly to the pinned implementation and needs a regression test.
- Confidence: `cross-checked`

### Implementation confirmation

- Implementation tested: current interpreter/formula source and official
  scripts inspected; Praat binary not built.
- Exact version or commit: `5d452fe3490bdc8d0edd12196a74127795b6a20a`
- Probe method: traced leading-space removal and command skipping; compared the
  formula `END_` semicolon token with vector/hash and bang operator tokens.
- Probe input:

~~~text
  # heading
value# = { 1, 2 } ; vector note
ok = value# [1] != 0
  ! implementation comment at EOF
~~~

- Observed result: first and last lines are skipped whole; the semicolon starts
  a suffix comment; vector hashes and `!=` remain formula tokens.
- Conclusion and limits of the probe: proves current contextual distinctions
  from source; legacy Praat bang-line portability is not claimed.

### Representative examples

#### Line comment

~~~text
# Create the analysis object
Play   ; the Sound is selected, so it plays
~~~

Expected regions: both comment portions, with `Play   ` preserved.

#### Block comment

Unsupported.

#### Nested or contextual comment

~~~text
values# = { 1, 2 }
label$ = "semi; hash# bang!"
assert values# [1] != 0 ; verified
~~~

Only `; verified` is a comment.

### Adversarial boundaries

- Negative cases: `vector#`/`matrix##` names, inline `#`, `!=`/unary `!`,
  straight and curly strings, doubled quotes, and semicolons inside strings.
- Malformed-input cases: unterminated straight/curly string, continuation at
  EOF, empty marker-only lines, and a semicolon immediately after a closing
  quote.
- Line-ending and Unicode cases: LF, CRLF, lone CR, EOF comments, leading tabs,
  Unicode/curly quotes, Unicode payloads, and exact source offsets.
- Version or dialect counterexamples: `!` whole-line behavior is pinned to the
  current implementation; TextGrid/data formats and C++ sources are separate.
- Cleaner preservation cases: retain hashes on vectors/matrices, bangs in
  operators, string punctuation, code before inline semicolon, mixed-marker
  grouping, and Unicode payload.

### Decision

- Recommended action: `contextual-helper`
- Registry fields to change: add canonical `praat` with a helper for
  first-nonspace `#`/`;`/`!` plus quote-aware inline `;`; register contextual
  wrapper metadata and pinned implementation notes.
- Deterministic tests to add: raw-label lookup, all three whole-line forms,
  inline semicolon, leading tabs, straight/curly/doubled-quote strings,
  vector/matrix hashes, bang operators, continuation lines, malformed strings,
  grouping, all line endings, Unicode, exact slices, and cleaning.
- Remaining blocker: define conservative recovery for an unterminated quote or
  continuation so later punctuation is not exposed as a false comment.
- Reviewer: /root/research_batch_09
- Review date: 2026-08-01
