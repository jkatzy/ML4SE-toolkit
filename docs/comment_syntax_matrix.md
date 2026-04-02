# Comment Syntax Matrix

This file is the research handoff between exploration agents and implementation
agents for expanding comment parsing coverage.

## Workflow

1. Search the official language documentation or specification first.
2. Cross-check the syntax against a parser, grammar, or implementation source.
3. Update `src/ml4setk/Parsing/Comments/registry.py`.
4. Add or revise seeded examples so `tests/test_comment_queries.py` exercises
   the change automatically.
5. Replace `TODO` evidence cells below with concrete references and raise the
   confidence rating only after both sources agree.

## Evidence fields

- `Docs source`: official language documentation or specification.
- `Impl source`: parser, grammar, compiler, or other implementation reference.
- `Confidence`: `seeded-from-implementation`, `cross-checked`, or `verified`.
- `Status`: `implemented`, `candidate`, or `unsupported`.

## Seeded matrix

| Family | Canonical | Aliases | Regex patterns | Nested delimiters | Seeded examples | Docs source | Impl source | Confidence | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `c_style` | `java` | `c`, `c++`, `c#`, `javascript`, `typescript`, `objective-c`, `go`, `kotlin`, `vue`, `scala`, `dart`, `rust`, `hack`, `less`, `groovy`, `processing`, `apex`, `cuda`, `scilab`, `antlr`, `swift`, `php` | `/* */`, `//` | none | `// note`, `/* note */` | TODO | `src/ml4setk/Parsing/Comments/registry.py` | `seeded-from-implementation` | `implemented` | Shared slash-style family. |
| `hash_style` | `python` | `r`, `elixir`, `nix`, `starlark`, `graphql`, `crystal` | `#`, `""" """` | none | `# note`, `"""note"""` | TODO | `src/ml4setk/Parsing/Comments/registry.py` | `seeded-from-implementation` | `implemented` | Triple-quoted handling should be verified per language. |
| `dash_style` | `ada` | none | `--` | none | `-- note` | TODO | `src/ml4setk/Parsing/Comments/registry.py` | `seeded-from-implementation` | `implemented` | Simple dash line comments. |
| `nested_dash_style` | `agda` | `elm` | `--` | `{- -}` | `-- note`, `{- outer {- inner -} outer -}` | TODO | `src/ml4setk/Parsing/Comments/registry.py` | `seeded-from-implementation` | `implemented` | Dash plus nested block comments. |
| `semicolon_style` | `assembly` | `netlogo`, `scheme`, `lisp` | `;` | none | `; note` | TODO | `src/ml4setk/Parsing/Comments/registry.py` | `seeded-from-implementation` | `implemented` | Shared semicolon comments. |
| `cobol_style` | `cobol` | none | indicator column, `*>` | none | `      * note`, `*> note` | TODO | `src/ml4setk/Parsing/Comments/registry.py` | `seeded-from-implementation` | `implemented` | Needs evidence for fixed-column rules. |
| `nested_star_style` | `coq` | `ocaml` | none | `(* *)` | `(* outer (* inner *) outer *)` | TODO | `src/ml4setk/Parsing/Comments/registry.py` | `seeded-from-implementation` | `implemented` | Nested-only in current implementation. |
| `d_doc_style` | `d` | none | `/** */`, `/++ +/`, `///` | none | `/// note`, `/** note */`, `/++ note +/` | TODO | `src/ml4setk/Parsing/Comments/registry.py` | `seeded-from-implementation` | `implemented` | Doc-comment oriented patterns only. |
| `percent_style` | `erlang` | none | `%` | none | `% note` | TODO | `src/ml4setk/Parsing/Comments/registry.py` | `seeded-from-implementation` | `implemented` | Simple percent comments. |
| `fsharp_style` | `f#` | none | `//` | `(* *)` | `// note`, `(* outer (* inner *) outer *)` | TODO | `src/ml4setk/Parsing/Comments/registry.py` | `seeded-from-implementation` | `implemented` | Mixed line and nested block comments. |
| `forth_style` | `forth` | none | `\`, `( )` | none | `\ note`, `( note )` | TODO | `src/ml4setk/Parsing/Comments/registry.py` | `seeded-from-implementation` | `implemented` | Parenthesized comments should be cross-checked carefully. |
| `bang_style` | `fortran` | none | `!` | none | `! note` | TODO | `src/ml4setk/Parsing/Comments/registry.py` | `seeded-from-implementation` | `implemented` | Simple bang comments. |
| `julia_style` | `julia` | none | `#`, `#= =#` | none | `# note`, `#= note =#` | TODO | `src/ml4setk/Parsing/Comments/registry.py` | `seeded-from-implementation` | `implemented` | Hash plus block syntax. |
| `markup_style` | `html` | `xml` | `<!-- -->` | none | `<!-- note -->` | TODO | `src/ml4setk/Parsing/Comments/registry.py` | `seeded-from-implementation` | `implemented` | Shared markup comments. |
| `lua_style` | `lua` | none | `--`, `--[[ ]]` | none | `-- note`, `--[[ note ]]` | TODO | `src/ml4setk/Parsing/Comments/registry.py` | `seeded-from-implementation` | `implemented` | Bracketed blocks need docs evidence. |
| `nested_star_only_style` | `mathematica` | none | none | `(* *)` | `(* outer (* inner *) outer *)` | TODO | `src/ml4setk/Parsing/Comments/registry.py` | `seeded-from-implementation` | `implemented` | Nested-only in current implementation. |
| `matlab_style` | `matlab` | none | `%`, `%{ %}` | none | `% note`, `%{ note %}` | TODO | `src/ml4setk/Parsing/Comments/registry.py` | `seeded-from-implementation` | `implemented` | Line plus block comments. |
| `perl_style` | `perl` | none | `#`, `=...=cut` | none | `# note`, `=pod ... =cut` | TODO | `src/ml4setk/Parsing/Comments/registry.py` | `seeded-from-implementation` | `implemented` | POD handling needs formal source verification. |
| `prolog_style` | `prolog` | none | `%`, `/* */` | none | `% note`, `/* note */` | TODO | `src/ml4setk/Parsing/Comments/registry.py` | `seeded-from-implementation` | `implemented` | Mixed line and block syntax. |
| `raku_style` | `raku` | none | `#`, quoted bracket forms | none | `# note`, `#'(note)` | TODO | `src/ml4setk/Parsing/Comments/registry.py` | `seeded-from-implementation` | `implemented` | Complex quoted comment forms. |
| `ruby_style` | `ruby` | none | `#`, `=begin =end` | none | `# note`, `=begin ... =end` | TODO | `src/ml4setk/Parsing/Comments/registry.py` | `seeded-from-implementation` | `implemented` | Begin/end blocks need source verification. |
| `sql_style` | `sql` | none | `--`, `/* */` | none | `-- note`, `/* note */` | TODO | `src/ml4setk/Parsing/Comments/registry.py` | `seeded-from-implementation` | `implemented` | Standard SQL family comments. |
| `webassembly_style` | `webassembly` | none | `;;`, `(; ;)` | none | `;; note`, `(; note ;)` | TODO | `src/ml4setk/Parsing/Comments/registry.py` | `seeded-from-implementation` | `implemented` | S-expression style comment forms. |
| `haskell_style` | `haskell` | none | `--` | `{- -}` | `-- note`, `{- outer {- inner -} outer -}` | TODO | `src/ml4setk/Parsing/Comments/registry.py` | `seeded-from-implementation` | `implemented` | Line plus nested block comments. |
