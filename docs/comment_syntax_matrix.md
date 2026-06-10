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
| `two_dimensional_array_style` | `two_dimensional_array` | none | column-zero `#`, `/` | none | `# note`, `// note` | [IESDP 2DA format](https://gibberlings3.github.io/iesdp/file_formats/ie_formats/2da.htm) | [GemRB importer](https://github.com/gemrb/gemrb/blob/master/gemrb/plugins/2DAImporter/2DAImporter.cpp) | `cross-checked` | `implemented` | Implements the union of GemRB v0.8.8 and current comment handling. |
| `api_blueprint_style` | `api_blueprint` | none | `<!-- -->` | none | `<!-- note -->` | [API Blueprint specification](https://apiblueprint.org/documentation/specification.html) | [Parser behavior](https://github.com/apiaryio/api-blueprint/issues/263) | `cross-checked` | `implemented` | GFM HTML comments only; embedded payload syntax is excluded. |
| `apollo_guidance_computer_style` | `apollo_guidance_computer` | none | `#` | none | `# note` | [Virtual AGC manual](https://www.ibiblio.org/apollo/assembly_language_manual.html) | [yaYUL parser](https://github.com/virtualagc/virtualagc/blob/master/yaYUL/Pass.c) | `verified` | `implemented` | `#` may follow an operand and runs to newline. |
| `arc_style` | `arc` | none | `;` | none | `; note` | [Arc 3.1 tutorial](https://arclanguage.github.io/tut-stable.html) | [Anarki parser test](https://github.com/arclanguage/anarki/blob/master/lib/tests/parser-test.arc) | `cross-checked` | `implemented` | Semicolon comments run to newline. |
| `aspnet_style` | `aspnet` | none | `<%-- --%>`, `<!-- -->` | none | `<%-- note --%>`, `<!-- note -->` | [Microsoft Web Forms docs](https://learn.microsoft.com/en-us/troubleshoot/developer/webapps/aspnet/development/inline-expressions) | [ASP grammar](https://github.com/textmate/asp.tmbundle/blob/master/Syntaxes/HTML-ASP.plist) | `verified` | `implemented` | Web Forms host comments only; embedded language tokens are excluded. |
| `beef_style` | `beef` | none | `//` | `/* */` | `// note`, `/* outer /* note */ outer */` | [Beef language guide](https://www.beeflang.org/docs/language-guide/) | [Beef parser](https://github.com/beefytech/Beef/blob/master/IDEHelper/Compiler/BfParser.cpp) | `verified` | `implemented` | Native Beef comments nest; current master and release 0.42.1 agree. |
| `berry_style` | `berry` | none | `#`, `#- -#` | none | `# note`, `#- note -#` | [Berry 1.1.0 reference](https://berry.readthedocs.io/en/latest/source/en/Chapter-1.html) | [Berry lexer](https://github.com/berry-lang/berry/blob/master/src/be_lexer.c) | `verified` | `implemented` | Block comments are non-nested and stop at the first `-#`. |
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
| `f_star_style` | `f_star` | none | `//` | `(* *)` | `// note`, `(* outer (* inner *) outer *)` | [F* tutorial](https://fstar-lang.org/tutorial/book/part1/part1_getting_off_the_ground.html) | [F* lexer](https://github.com/FStarLang/FStar/blob/master/src/ml/FStarC_Parser_LexFStar.ml) | `verified` | `implemented` | Current master and v2025.12.15 agree; block comments truly nest. |
| `forth_style` | `forth` | none | `\`, `( )` | none | `\ note`, `( note )` | TODO | `src/ml4setk/Parsing/Comments/registry.py` | `seeded-from-implementation` | `implemented` | Parenthesized comments should be cross-checked carefully. |
| `bang_style` | `fortran` | none | `!` | none | `! note` | TODO | `src/ml4setk/Parsing/Comments/registry.py` | `seeded-from-implementation` | `implemented` | Simple bang comments. |
| `golo_style` | `golo` | none | `#` | none | `# note` | [Golo basics](https://github.com/eclipse-archived/golo-lang/blob/master/doc/basics.adoc) | [Golo grammar](https://github.com/eclipse-archived/golo-lang/blob/master/src/main/jjtree/org/eclipse/golo/compiler/parser/Golo.jjt) | `verified` | `implemented` | Current archived grammar and v2.1.0 agree; `----` delimits documentation, not comments. |
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
