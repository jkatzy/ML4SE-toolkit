"""Comment syntax registry used by comment extraction queries.

This module is intentionally data-heavy. Add or correct comment-language
support by updating ``COMMENT_SYNTAXES`` with regex patterns, nested delimiters,
and seeded examples instead of branching in parser code.
"""

from dataclasses import dataclass
from typing import Dict, Iterable, Tuple


@dataclass(frozen=True)
class CommentExample:
    """One seeded example that exercises a comment syntax.

    Attributes:
        sample: Source fragment containing the target comment.
        expected_match: Exact substring the parser should extract.
        description: Human-readable evidence or purpose for the example.
        kind: Comment category, usually ``line``, ``block``, or ``nested``.
        inline_compatible: Whether the example can appear beside code on the
            same line.
        grouped_line_compatible: Whether adjacent examples can be grouped into
            one logical line-comment block.
    """

    sample: str
    expected_match: str
    description: str = ""
    kind: str = "line"
    inline_compatible: bool = False
    grouped_line_compatible: bool = False


@dataclass(frozen=True)
class CommentSyntax:
    """Structured comment syntax data for one canonical language family.

    Attributes:
        family_name: Stable identifier for a syntax family shared by languages.
        canonical_name: Primary registry key for the family.
        aliases: Additional lowercase language keys with the same syntax.
        regex_patterns: Regexes for line comments and non-nested block comments.
        nested_delimiters: Recursive block comment delimiter pairs.
        shared_regex_examples: Seeded examples that apply to every alias.
        canonical_regex_examples: Seeded examples only for ``canonical_name``.
        shared_nested_examples: Nested examples that apply to every alias.
        canonical_nested_examples: Nested examples only for ``canonical_name``.
        documentation_source: Reference used to justify the syntax entry.
        implementation_source: File that owns this implementation.
        confidence: Research confidence level for the syntax entry.
        notes: Maintainer-facing caveats for parser behavior or dialect scope.
    """

    family_name: str
    canonical_name: str
    aliases: Tuple[str, ...] = ()
    regex_patterns: Tuple[str, ...] = ()
    nested_delimiters: Tuple[Tuple[str, str], ...] = ()
    shared_regex_examples: Tuple[CommentExample, ...] = ()
    canonical_regex_examples: Tuple[CommentExample, ...] = ()
    shared_nested_examples: Tuple[CommentExample, ...] = ()
    canonical_nested_examples: Tuple[CommentExample, ...] = ()
    documentation_source: str = "TODO"
    implementation_source: str = "src/ml4setk/Parsing/Comments/registry.py"
    confidence: str = "seeded-from-implementation"
    notes: str = ""

    @property
    def language_names(self) -> Tuple[str, ...]:
        """Return the canonical language key followed by all aliases."""

        return (self.canonical_name,) + self.aliases


COMMENT_SYNTAXES: Tuple[CommentSyntax, ...] = (
    CommentSyntax(
        family_name="two_dimensional_array_style",
        canonical_name="two_dimensional_array",
        regex_patterns=(r"(?m)^[#/][^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "# table note\nROW VALUE",
                "# table note",
                "GemRB 2DA hash comment at column zero.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "// table note\nROW VALUE",
                "// table note",
                "Current GemRB 2DA slash comment at column zero.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://gibberlings3.github.io/iesdp/file_formats/ie_formats/2da.htm"
        ),
        implementation_source=(
            "https://github.com/gemrb/gemrb/blob/master/gemrb/plugins/"
            "2DAImporter/2DAImporter.cpp"
        ),
        confidence="cross-checked",
        notes=(
            "GemRB v0.8.8 accepts column-zero # comments; current GemRB also "
            "accepts lines beginning with /. The registry implements that union."
        ),
    ),
    CommentSyntax(
        family_name="api_blueprint_style",
        canonical_name="api_blueprint",
        regex_patterns=(r"<!--[\S\s]*?-->",),
        shared_regex_examples=(
            CommentExample(
                "FORMAT: 1A\n<!-- note -->\n# My API",
                "<!-- note -->",
                "API Blueprint GFM HTML comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://apiblueprint.org/documentation/specification.html"
        ),
        implementation_source=(
            "https://github.com/apiaryio/api-blueprint/issues/263"
        ),
        confidence="cross-checked",
        notes=(
            "API Blueprint inherits GitHub Flavored Markdown HTML comments. "
            "Embedded body formats do not add source-level comment syntax."
        ),
    ),
    CommentSyntax(
        family_name="apollo_guidance_computer_style",
        canonical_name="apollo_guidance_computer",
        regex_patterns=(r"#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "SPCOS AD HALF # note\nTS TEMK",
                "# note",
                "yaYUL AGC inline comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://www.ibiblio.org/apollo/assembly_language_manual.html"
        ),
        implementation_source=(
            "https://github.com/virtualagc/virtualagc/blob/master/yaYUL/Pass.c"
        ),
        confidence="verified",
        notes="The yaYUL assembler treats everything following # as a comment.",
    ),
    CommentSyntax(
        family_name="arc_style",
        canonical_name="arc",
        regex_patterns=(r";[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "(do ; note\n  (prn \"hello\"))",
                "; note",
                "Arc semicolon line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="https://arclanguage.github.io/tut-stable.html",
        implementation_source=(
            "https://github.com/arclanguage/anarki/blob/master/"
            "lib/tests/parser-test.arc"
        ),
        confidence="cross-checked",
        notes="Arc inherits semicolon line comments from its Lisp reader.",
    ),
    CommentSyntax(
        family_name="aspnet_style",
        canonical_name="aspnet",
        regex_patterns=(
            r"<%--[\S\s]*?--%>",
            r"<!--[\S\s]*?-->",
        ),
        shared_regex_examples=(
            CommentExample(
                "<%-- note --%>\n<asp:Label runat=\"server\" />",
                "<%-- note --%>",
                "ASP.NET Web Forms server-side comment.",
                kind="block",
                inline_compatible=True,
            ),
            CommentExample(
                "<!-- note -->\n<div>content</div>",
                "<!-- note -->",
                "ASP.NET markup HTML comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://learn.microsoft.com/en-us/troubleshoot/developer/"
            "webapps/aspnet/development/inline-expressions"
        ),
        implementation_source=(
            "https://github.com/textmate/asp.tmbundle/blob/master/"
            "Syntaxes/HTML-ASP.plist"
        ),
        confidence="verified",
        notes=(
            "The ASP.NET Stack key covers Web Forms markup. Embedded C#, VB, "
            "and JavaScript comment tokens are intentionally excluded."
        ),
    ),
    CommentSyntax(
        family_name="beef_style",
        canonical_name="beef",
        regex_patterns=(r"/{2}[^\r\n]*",),
        nested_delimiters=(("/*", "*/"),),
        shared_regex_examples=(
            CommentExample(
                "int value = 1; // note\nvalue++;",
                "// note",
                "Beef slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "int value = 1;\n/* outer /* note */ outer */\nvalue++;",
                "/* outer /* note */ outer */",
                "Beef nested block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://www.beeflang.org/docs/language-guide/",
        implementation_source=(
            "https://github.com/beefytech/Beef/blob/master/"
            "IDEHelper/Compiler/BfParser.cpp"
        ),
        confidence="verified",
        notes=(
            "Native Beef mode supports recursive /* ... */ comments. Current "
            "master and release 0.42.1 agree; C++ compatibility mode is "
            "intentionally outside this registry key."
        ),
    ),
    CommentSyntax(
        family_name="berry_style",
        canonical_name="berry",
        regex_patterns=(
            r"#-[\S\s]*?-#",
            r"#(?!-)[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "value = 1 # note\nvalue += 1",
                "# note",
                "Berry hash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "value = 1\n#- note -#\nvalue += 1",
                "#- note -#",
                "Berry non-nested block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://berry.readthedocs.io/en/latest/source/en/Chapter-1.html"
        ),
        implementation_source=(
            "https://github.com/berry-lang/berry/blob/master/src/be_lexer.c"
        ),
        confidence="verified",
        notes=(
            "Berry block comments stop at the first -# delimiter and do not "
            "nest. Current master and release v1.1.0 agree."
        ),
    ),
    CommentSyntax(
        family_name="bikeshed_style",
        canonical_name="bikeshed",
        regex_patterns=(r"<!--[\S\s]*?-->",),
        shared_regex_examples=(
            CommentExample(
                "<p>before</p>\n<!-- note -->\n<p>after</p>",
                "<!-- note -->",
                "Bikeshed HTML comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://speced.github.io/bikeshed/#big-text",
        implementation_source=(
            "https://github.com/speced/bikeshed/blob/main/"
            "bikeshed/h/parser/parser.py"
        ),
        confidence="verified",
        notes=(
            "HTML comments are valid throughout Bikeshed documents and stop "
            "at the first --> delimiter. Hash comments are scoped to embedded "
            "InfoTree data and are intentionally excluded."
        ),
    ),
    CommentSyntax(
        family_name="c_style",
        canonical_name="java",
        aliases=(
            "c",
            "c++",
            "c#",
            "javascript",
            "typescript",
            "objective-c",
            "objective_cpp",
            "go",
            "kotlin",
            "vue",
            "scala",
            "dart",
            "hack",
            "less",
            "groovy",
            "processing",
            "apex",
            "cuda",
            "scilab",
            "antlr",
            "swift",
            "php",
            "four_d",
            "actionscript",
            "ags_script",
            "aidl",
            "al",
            "angelscript",
            "aspectj",
            "asymptote",
            "avro_idl",
            "ballerina",
            "chuck",
            "cue",
            "dataweave",
            "fantom",
            "faust",
            "glsl",
            "gradle",
            "haxe",
            "hlsl",
            "idl",
            "jsonc",
            "imagej_macro",
            "json5",
            "modelica",
            "nextflow",
            "objective_j",
            "odin",
            "opencl",
            "openscad",
            "protocol_buffer",
            "qml",
            "sass",
            "scss",
            "systemverilog",
            "tsx",
            "upc",
            "unrealscript",
            "vala",
            "verilog",
            "webidl",
            "xtend",
            "yara",
            "yul",
            "dtrace",
            "ecl",
            "game_maker_language",
            "gosu",
            "cap_cds",
            "codeql",
            "gsc",
            "hyphy",
            "openqasm",
            "pike",
            "quake",
        ),
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r"/{2}.*.*",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n// note\nsuffix",
                "// note",
                "Slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "prefix\n/* note */\nsuffix",
                "/* note */",
                "C-style block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        notes="Slash-based line and non-nested block comments.",
    ),
    CommentSyntax(
        family_name="rust_style",
        canonical_name="rust",
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n// note\nsuffix",
                "// note",
                "Rust line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "prefix\n//! note\nsuffix",
                "//! note",
                "Rust inner documentation line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "prefix\n/* note */\nsuffix",
                "/* note */",
                "Rust block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="hash_line_style",
        canonical_name="dockerfile",
        aliases=(
            "apacheconf",
            "awk",
            "alpine_abuild",
            "capn_proto",
            "codeowners",
            "conll_u",
            "cython",
            "debian_package_control_file",
            "desktop",
            "dircolors",
            "easybuild",
            "elvish",
            "fish",
            "fluent",
            "gap",
            "gdb",
            "gdscript",
            "gentoo_ebuild",
            "gentoo_eclass",
            "gherkin",
            "git_attributes",
            "gettext_catalog",
            "gn",
            "gnuplot",
            "haproxy",
            "ignore_list",
            "jq",
            "makefile",
            "meson",
            "mini_yaml",
            "nginx",
            "ninja",
            "open_policy_agent",
            "protocol_buffer_text_format",
            "puppet",
            "qmake",
            "readline_config",
            "robotframework",
            "robots_txt",
            "shell",
            "sparql",
            "tcl",
            "tcsh",
            "toml",
            "turtle",
            "vyper",
            "wavefront_material",
            "wavefront_object",
            "hxml",
            "common_workflow_language",
            "kicad_layout",
            "kicad_schematic",
            "procfile",
            "proguard",
            "limbo",
            "neon",
            "textmate_properties",
            "wdl",
            "xonsh",
            "yaml",
            "zeek",
            "ragel",
            "slash",
        ),
        regex_patterns=(r"#.*",),
        shared_regex_examples=(
            CommentExample(
                "prefix\n# note\nsuffix",
                "# note",
                "Hash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="slash_line_style",
        canonical_name="qsharp",
        aliases=(
            "go_module",
            "onec_enterprise",
            "zig",
            "grace",
            "cloud_firestore_security_rules",
            "igor_pro",
        ),
        regex_patterns=(r"/{2}.*.*",),
        shared_regex_examples=(
            CommentExample(
                "prefix\n// note\nsuffix",
                "// note",
                "Slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="c_block_style",
        canonical_name="css",
        aliases=("asl", "postcss"),
        regex_patterns=(r"\/\*[\S\s]*?\*\/",),
        shared_regex_examples=(
            CommentExample(
                "prefix\n/* note */\nsuffix",
                "/* note */",
                "C-style block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="hash_c_style",
        canonical_name="ampl",
        aliases=("sieve",),
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r"#.*",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n# note\nsuffix",
                "# note",
                "Hash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "prefix\n/* note */\nsuffix",
                "/* note */",
                "Hash-plus-block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="hash_style",
        canonical_name="python",
        aliases=("r", "elixir", "nix", "starlark", "graphql", "crystal"),
        regex_patterns=(
            r"#.*",
            r"\"{3}([\S\s]*?)\"{3}",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n# note\nsuffix",
                "# note",
                "Hash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        canonical_regex_examples=(
            CommentExample(
                'prefix\n"""note"""\nsuffix',
                '"""note"""',
                "Triple-quoted block form.",
                kind="block",
            ),
        ),
        notes="Hash comments plus Python-style triple-quoted blocks in the current implementation.",
    ),
    CommentSyntax(
        family_name="dash_style",
        canonical_name="ada",
        aliases=("eiffel", "futhark", "asn1", "vhdl"),
        regex_patterns=(r"--.*",),
        shared_regex_examples=(
            CommentExample(
                "prefix\n-- note\nsuffix",
                "-- note",
                "Dash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="nested_dash_style",
        canonical_name="agda",
        aliases=("elm", "frege", "grammatical_framework"),
        regex_patterns=(r"--.*",),
        nested_delimiters=(("{-", "-}"),),
        shared_regex_examples=(
            CommentExample(
                "prefix\n-- note\nsuffix",
                "-- note",
                "Dash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "before {- outer {- inner -} outer -} after",
                "{- outer {- inner -} outer -}",
                "Nested dash block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="semicolon_style",
        canonical_name="assembly",
        aliases=(
            "netlogo",
            "scheme",
            "lisp",
            "clojure",
            "dns_zone",
            "edn",
            "hy",
            "llvm",
            "windows_registry_entries",
            "rebol",
            "purebasic",
        ),
        regex_patterns=(r";.*",),
        shared_regex_examples=(
            CommentExample(
                "prefix\n; note\nsuffix",
                "; note",
                "Semicolon line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="cobol_style",
        canonical_name="cobol",
        regex_patterns=(
            r"(?m)^.{6}(\*|/).*",
            r"\*>.*",
        ),
        shared_regex_examples=(
            CommentExample(
                "      * note",
                "      * note",
                "Indicator-column comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        canonical_regex_examples=(
            CommentExample(
                "prefix\n*> note\nsuffix",
                "*> note",
                "Inline COBOL comment.",
                kind="line",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="nested_star_style",
        canonical_name="coq",
        aliases=("ocaml",),
        nested_delimiters=(("(*", "*)"),),
        shared_nested_examples=(
            CommentExample(
                "before (* outer (* inner *) outer *) after",
                "(* outer (* inner *) outer *)",
                "Nested star block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        notes="Current implementation treats these languages as nested-comment only.",
    ),
    CommentSyntax(
        family_name="d_doc_style",
        canonical_name="d",
        regex_patterns=(
            r"\/\*\*[\S\s]*?\*\/",
            r"\/\+\+[\S\s]*?\+\/",
            r"\/\/\/.*",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n/// note\nsuffix",
                "/// note",
                "Triple-slash doc comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        canonical_regex_examples=(
            CommentExample(
                "prefix\n/** note */\nsuffix",
                "/** note */",
                "Block doc comment.",
                kind="block",
                inline_compatible=True,
            ),
            CommentExample(
                "prefix\n/++ note +/\nsuffix",
                "/++ note +/",
                "Plus-delimited doc comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="pascal_style",
        canonical_name="pascal",
        regex_patterns=(
            r"\{[\S\s]*?\}",
            r"/{2}.*.*",
        ),
        nested_delimiters=(
            ("{", "}"),
            ("(*", "*)"),
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n// note\nsuffix",
                "// note",
                "Pascal line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "prefix\n{ note }\nsuffix",
                "{ note }",
                "Brace-delimited Pascal block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        canonical_nested_examples=(
            CommentExample(
                "before { outer { inner } outer } after",
                "{ outer { inner } outer }",
                "Nested brace Pascal comment in Free Pascal normal mode.",
                kind="nested",
                inline_compatible=True,
            ),
            CommentExample(
                "before (* outer (* inner *) outer *) after",
                "(* outer (* inner *) outer *)",
                "Nested paren-star Pascal comment in Free Pascal normal mode.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        notes=(
            "The generic Pascal key implements the union of Free Pascal, TP/Delphi, "
            "and Pascal65 comment forms. It accepts //, { ... }, and (* ... *)."
        ),
    ),
    CommentSyntax(
        family_name="percent_style",
        canonical_name="erlang",
        aliases=("bibtex", "postscript", "tex"),
        regex_patterns=(r"%.*",),
        shared_regex_examples=(
            CommentExample(
                "prefix\n% note\nsuffix",
                "% note",
                "Percent line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="fsharp_style",
        canonical_name="f#",
        aliases=("ats",),
        regex_patterns=(r"\/\/.*",),
        nested_delimiters=(("(*", "*)"),),
        shared_regex_examples=(
            CommentExample(
                "prefix\n// note\nsuffix",
                "// note",
                "Slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "before (* outer (* inner *) outer *) after",
                "(* outer (* inner *) outer *)",
                "Nested star block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="f_star_style",
        canonical_name="f_star",
        regex_patterns=(r"/{2}[^\r\n]*",),
        nested_delimiters=(("(*", "*)"),),
        shared_regex_examples=(
            CommentExample(
                "let x = 1 // note\nin x",
                "// note",
                "F* slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "let x = 1\n(* outer (* inner *) outer *)\nin x",
                "(* outer (* inner *) outer *)",
                "F* nested block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://fstar-lang.org/tutorial/book/part1/"
            "part1_getting_off_the_ground.html"
        ),
        implementation_source=(
            "https://github.com/FStarLang/FStar/blob/master/src/ml/"
            "FStarC_Parser_LexFStar.ml"
        ),
        confidence="verified",
        notes="F* supports // comments and true nested (* ... *) comments.",
    ),
    CommentSyntax(
        family_name="forth_style",
        canonical_name="forth",
        regex_patterns=(
            r"(?m)(?<!\S)\\(?:[ \t][^\r\n]*)?\r?",
            r"\(\s[\s\S]*?\)",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n\\ note\nsuffix",
                "\\ note",
                "Backslash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        canonical_regex_examples=(
            CommentExample(
                "prefix\n( note )\nsuffix",
                "( note )",
                "Parenthesized comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="bang_style",
        canonical_name="fortran",
        aliases=("digital_command_language", "factor", "fortran_free_form"),
        regex_patterns=(r"!.*",),
        shared_regex_examples=(
            CommentExample(
                "prefix\n! note\nsuffix",
                "! note",
                "Bang line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="julia_style",
        canonical_name="julia",
        regex_patterns=(r"#(?![=]).*",),
        nested_delimiters=(("#=", "=#"),),
        shared_regex_examples=(
            CommentExample(
                "prefix\n# note\nsuffix",
                "# note",
                "Hash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        canonical_nested_examples=(
            CommentExample(
                "before #= outer #= inner =# outer =# after",
                "#= outer #= inner =# outer =#",
                "Nested hash-equals block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="markup_style",
        canonical_name="html",
        aliases=(
            "xml",
            "ant_build_system",
            "collada",
            "maven_pom",
            "rmarkdown",
            "svelte",
            "svg",
            "wikitext",
            "xml_property_list",
            "xproc",
            "xslt",
        ),
        regex_patterns=(r"<!--([\S\s]*?)-->",),
        shared_regex_examples=(
            CommentExample(
                "prefix\n<!-- note -->\nsuffix",
                "<!-- note -->",
                "Markup block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="lua_style",
        canonical_name="lua",
        regex_patterns=(
            r"--\[(=*)\[[\s\S]*?\]\1\]",
            r"--(?!\[[=]*\[).*",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n-- note\nsuffix",
                "-- note",
                "Dash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        canonical_regex_examples=(
            CommentExample(
                "prefix\n--[[ note ]]\nsuffix",
                "--[[ note ]]",
                "Bracketed block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="nested_star_only_style",
        canonical_name="mathematica",
        aliases=("augeas", "isabelle", "isabelle_root"),
        nested_delimiters=(("(*", "*)"),),
        canonical_nested_examples=(
            CommentExample(
                "before (* outer (* inner *) outer *) after",
                "(* outer (* inner *) outer *)",
                "Nested star block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="matlab_style",
        canonical_name="matlab",
        aliases=("lilypond",),
        regex_patterns=(
            r"%{([\S\s]*?)%}",
            r"%(?!\{|\}).*",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n% note\nsuffix",
                "% note",
                "Percent line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        canonical_regex_examples=(
            CommentExample(
                "prefix\n%{ note %}\nsuffix",
                "%{ note %}",
                "Percent-brace block comment.",
                kind="block",
            ),
        ),
    ),
    CommentSyntax(
        family_name="perl_style",
        canonical_name="perl",
        regex_patterns=(
            r"(?ms)^[ \t]*=pod\b[\s\S]*?^[ \t]*=cut\b[ \t]*$",
            r"#.*",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n# note\nsuffix",
                "# note",
                "Hash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        canonical_regex_examples=(
            CommentExample(
                "prefix\n=pod\nnote\n=cut\nsuffix",
                "=pod\nnote\n=cut",
                "POD block comment.",
                kind="block",
            ),
        ),
    ),
    CommentSyntax(
        family_name="prolog_style",
        canonical_name="prolog",
        aliases=("eclipse",),
        regex_patterns=(
            r"%.*",
            r"\/\*[\s\S]*?\*\/",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n% note\nsuffix",
                "% note",
                "Percent line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        canonical_regex_examples=(
            CommentExample(
                "prefix\n/* note */\nsuffix",
                "/* note */",
                "Slash block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="raku_style",
        canonical_name="raku",
        regex_patterns=(
            r"#`(?P<raku_paren>\((?:[^()]|(?P>raku_paren))*\))",
            r"#`(?P<raku_brace>\{(?:[^{}]|(?P>raku_brace))*\})",
            r"#`(?P<raku_bracket>\[(?:[^\[\]]|(?P>raku_bracket))*\])",
            r"#`<[\s\S]*?>",
            r"#(?:\||=)(?P<raku_decl_paren>\((?:[^()]|(?P>raku_decl_paren))*\))",
            r"#(?:\||=)(?P<raku_decl_brace>\{(?:[^{}]|(?P>raku_decl_brace))*\})",
            r"#(?:\||=)(?P<raku_decl_bracket>\[(?:[^\[\]]|(?P>raku_decl_bracket))*\])",
            r"#(?:\||=)<[\s\S]*?>",
            (
                r"(?ms)^[ \t]*=begin[ \t]+comment\b[^\r\n]*"
                r"(?:\r?\n[\s\S]*?)^[ \t]*=end[ \t]+comment\b[^\r\n]*"
            ),
            r"#(?:\||=)(?![({\[<]).*",
            r"#(?![`|=]).*",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n# note\nsuffix",
                "# note",
                "Hash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        canonical_regex_examples=(
            CommentExample(
                "prefix\n#| note\nsuffix",
                "#| note",
                "Leading declarator line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "prefix\n#= note\nsuffix",
                "#= note",
                "Trailing declarator line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "prefix\n#`(note)\nsuffix",
                "#`(note)",
                "Bracketed embedded comment.",
                kind="block",
                inline_compatible=True,
            ),
            CommentExample(
                "prefix\n#`[note]\nsuffix",
                "#`[note]",
                "Square-bracket embedded comment.",
                kind="block",
                inline_compatible=True,
            ),
            CommentExample(
                "prefix\n#|(note)\nsuffix",
                "#|(note)",
                "Declarator paired block comment.",
                kind="block",
                inline_compatible=True,
            ),
            CommentExample(
                "prefix\n=begin comment\nnote\n=end comment\nsuffix",
                "=begin comment\nnote\n=end comment",
                "Rakudoc comment block.",
                kind="block",
            ),
        ),
    ),
    CommentSyntax(
        family_name="ruby_style",
        canonical_name="ruby",
        regex_patterns=(
            r"#.*",
            r"(?ms)^[ \t]*=begin\b[\s\S]*?^[ \t]*=end\b[ \t]*$",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n# note\nsuffix",
                "# note",
                "Hash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        canonical_regex_examples=(
            CommentExample(
                "prefix\n=begin\nnote\n=end\nsuffix",
                "=begin\nnote\n=end",
                "Ruby begin/end block.",
                kind="block",
            ),
        ),
    ),
    CommentSyntax(
        family_name="sql_style",
        canonical_name="sql",
        aliases=("hiveql", "plpgsql", "plsql", "tsql"),
        regex_patterns=(
            r"\/\*[\s\S]*?\*\/",
            r"--.*",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n-- note\nsuffix",
                "-- note",
                "Dash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        canonical_regex_examples=(
            CommentExample(
                "prefix\n/* note */\nsuffix",
                "/* note */",
                "SQL block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="webassembly_style",
        canonical_name="webassembly",
        regex_patterns=(r";;.*",),
        nested_delimiters=(("(;", ";)"),),
        shared_regex_examples=(
            CommentExample(
                "prefix\n;; note\nsuffix",
                ";; note",
                "Double-semicolon line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        canonical_nested_examples=(
            CommentExample(
                "before (; outer (; inner ;) outer ;) after",
                "(; outer (; inner ;) outer ;)",
                "Nested paren-semicolon block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="batchfile_style",
        canonical_name="batchfile",
        regex_patterns=(r"(?mi)^[ \t]*(?:rem\b.*|::.*)$",),
        shared_regex_examples=(
            CommentExample(
                "REM note\nafter",
                "REM note",
                "Batch REM comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="apostrophe_style",
        canonical_name="visual_basic_net",
        aliases=("basic", "vba", "vbscript"),
        regex_patterns=(
            r"'.*",
            r"(?im)^[ \t]*rem\b.*$",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n' note\nsuffix",
                "' note",
                "Apostrophe line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="quote_line_style",
        canonical_name="vim_script",
        aliases=("smalltalk",),
        regex_patterns=(r"\".*",),
        shared_regex_examples=(
            CommentExample(
                'prefix\n" note\nsuffix',
                '" note',
                "Double-quote line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="editorconfig_style",
        canonical_name="editorconfig",
        regex_patterns=(r"(?m)^[ \t]*[;#].*$",),
        shared_regex_examples=(
            CommentExample(
                "# note\nafter",
                "# note",
                "Start-of-line EditorConfig comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="ini_style",
        canonical_name="git_config",
        aliases=("ini", "npm_config"),
        regex_patterns=(r"[;#].*",),
        shared_regex_examples=(
            CommentExample(
                "prefix\n# note\nsuffix",
                "# note",
                "INI-style line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "prefix\n; note\nsuffix",
                "; note",
                "INI-style semicolon line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="java_properties_style",
        canonical_name="java_properties",
        regex_patterns=(r"(?m)^[ \t]*[#!].*",),
        shared_regex_examples=(
            CommentExample(
                "prefix\n# note\nsuffix",
                "# note",
                "Properties file line comment.",
                kind="line",
                inline_compatible=False,
                grouped_line_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="semicolon_c_style",
        canonical_name="autohotkey",
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r";[^\r\n]*\r?",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n; note\nsuffix",
                "; note",
                "Semicolon line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "prefix\n/* note */\nsuffix",
                "/* note */",
                "Slash block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="autoit_style",
        canonical_name="autoit",
        regex_patterns=(
            r"#cs[\S\s]*?#ce",
            r";.*",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n; note\nsuffix",
                "; note",
                "Semicolon line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "before\n#cs\nblock note\n#ce\nafter",
                "#cs\nblock note\n#ce",
                "AutoIt block comment.",
                kind="block",
            ),
        ),
    ),
    CommentSyntax(
        family_name="nsis_style",
        canonical_name="nsis",
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r"#.*",
            r";.*",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n; note\nsuffix",
                "; note",
                "NSIS line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "prefix\n/* note */\nsuffix",
                "/* note */",
                "NSIS block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="applescript_style",
        canonical_name="applescript",
        regex_patterns=(
            r"#.*",
            r"--.*",
        ),
        nested_delimiters=(("(*", "*)"),),
        shared_regex_examples=(
            CommentExample(
                "prefix\n-- note\nsuffix",
                "-- note",
                "AppleScript line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "before (* outer (* inner *) outer *) after",
                "(* outer (* inner *) outer *)",
                "Nested star block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="hash_pipe_style",
        canonical_name="racket",
        aliases=("emacs_lisp",),
        regex_patterns=(r";.*",),
        nested_delimiters=(("#|", "|#"),),
        shared_regex_examples=(
            CommentExample(
                "prefix\n; note\nsuffix",
                "; note",
                "Semicolon line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "before #| outer #| inner |# outer |# after",
                "#| outer #| inner |# outer |#",
                "Hash-pipe nested block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="nim_style",
        canonical_name="nim",
        regex_patterns=(r"(?<!\])#(?!\[).*",),
        nested_delimiters=(("#[", "]#"),),
        shared_regex_examples=(
            CommentExample(
                "prefix\n# note\nsuffix",
                "# note",
                "Hash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "before #[ outer #[ inner ]# outer ]# after",
                "#[ outer #[ inner ]# outer ]#",
                "Nim nested block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="powershell_style",
        canonical_name="powershell",
        regex_patterns=(
            r"<#[\S\s]*?#>",
            r"(?<!<)#(?!>).*",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n# note\nsuffix",
                "# note",
                "PowerShell line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "prefix\n<# note #>\nsuffix",
                "<# note #>",
                "PowerShell block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="freebasic_style",
        canonical_name="freebasic",
        regex_patterns=(
            r"\/'[\S\s]*?'\/",
            r"(?<!/)'(?!/).*",
            r"(?im)^[ \t]*rem\b.*$",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n' note\nsuffix",
                "' note",
                "Apostrophe line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "prefix\n/' note '/\nsuffix",
                "/' note '/",
                "Slash-apostrophe block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="jsonnet_style",
        canonical_name="jsonnet",
        aliases=(
            "directx_3d_file",
            "graphviz_dot",
            "hcl",
            "hocon",
            "html_php",
            "io",
            "ring",
            "thrift",
        ),
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r"/{2}.*.*",
            r"#.*",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n// note\nsuffix",
                "// note",
                "Slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "prefix\n/* note */\nsuffix",
                "/* note */",
                "Slash block comment.",
                kind="block",
                inline_compatible=True,
            ),
            CommentExample(
                "prefix\n# note\nsuffix",
                "# note",
                "Hash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="xquery_style",
        canonical_name="xquery",
        aliases=("jsoniq",),
        nested_delimiters=(("(:", ":)"),),
        shared_nested_examples=(
            CommentExample(
                "before (: outer (: inner :) outer :) after",
                "(: outer (: inner :) outer :)",
                "Nested XQuery block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="email_header_style",
        canonical_name="e_mail",
        nested_delimiters=(("(", ")"),),
        shared_nested_examples=(
            CommentExample(
                "From: Alice (team (platform)) <alice@example.com>\nSubject: status",
                "(team (platform))",
                "Nested RFC 5322 header comment.",
                kind="nested",
            ),
        ),
        notes="This covers parenthesized header comments, not programming-language comments.",
    ),
    CommentSyntax(
        family_name="cmake_style",
        canonical_name="cmake",
        regex_patterns=(r"(?<!\])#(?!\[\[).*",),
        nested_delimiters=(("#[[", "]]"),),
        shared_regex_examples=(
            CommentExample(
                "prefix\n# note\nsuffix",
                "# note",
                "CMake line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "before #[[ outer #[[ inner ]] outer ]] after",
                "#[[ outer #[[ inner ]] outer ]]",
                "Bracketed CMake block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="antlers_style",
        canonical_name="antlers",
        regex_patterns=(r"\{\{#[\S\s]*?#\}\}",),
        shared_regex_examples=(
            CommentExample(
                "prefix\n{{# note #}}\nsuffix",
                "{{# note #}}",
                "Antlers block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="blade_style",
        canonical_name="blade",
        regex_patterns=(r"\{\{--[\S\s]*?--\}\}",),
        shared_regex_examples=(
            CommentExample(
                "prefix\n{{-- note --}}\nsuffix",
                "{{-- note --}}",
                "Blade block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="ejs_style",
        canonical_name="ejs",
        aliases=("html_ecr", "html_eex", "html_erb"),
        regex_patterns=(r"<%#[\S\s]*?%>",),
        shared_regex_examples=(
            CommentExample(
                "prefix\n<%# note %>\nsuffix",
                "<%# note %>",
                "EJS block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="freemarker_style",
        canonical_name="freemarker",
        regex_patterns=(r"<#--[\S\s]*?-->",),
        shared_regex_examples=(
            CommentExample(
                "prefix\n<#-- note -->\nsuffix",
                "<#-- note -->",
                "FreeMarker block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="jinja_style",
        canonical_name="jinja",
        aliases=("genshi",),
        regex_patterns=(
            r"\{#[\S\s]*?#\}",
            r"##.*",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n## note\nsuffix",
                "## note",
                "Jinja line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "prefix\n{# note #}\nsuffix",
                "{# note #}",
                "Jinja block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="nunjucks_style",
        canonical_name="nunjucks",
        aliases=("twig",),
        regex_patterns=(r"\{#[\S\s]*?#\}",),
        shared_regex_examples=(
            CommentExample(
                "prefix\n{# note #}\nsuffix",
                "{# note #}",
                "Template block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="mako_style",
        canonical_name="mako",
        regex_patterns=(
            r"<%doc>[\S\s]*?<\/%doc>",
            r"##.*",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n## note\nsuffix",
                "## note",
                "Mako line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "prefix\n<%doc>note</%doc>\nsuffix",
                "<%doc>note</%doc>",
                "Mako block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="velocity_template_style",
        canonical_name="velocity_template_language",
        regex_patterns=(
            r"#\*[\S\s]*?\*#",
            r"##.*",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n## note\nsuffix",
                "## note",
                "Velocity line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "prefix\n#* note *#\nsuffix",
                "#* note *#",
                "Velocity block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="latte_style",
        canonical_name="latte",
        regex_patterns=(r"\{\*[\S\s]*?\*\}",),
        shared_regex_examples=(
            CommentExample(
                "prefix\n{* note *}\nsuffix",
                "{* note *}",
                "Latte block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="sas_style",
        canonical_name="sas",
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r"(?m)^\*.*$",
        ),
        shared_regex_examples=(
            CommentExample(
                "* note\nafter",
                "* note",
                "SAS line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "prefix\n/* note */\nsuffix",
                "/* note */",
                "SAS block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="haskell_style",
        canonical_name="haskell",
        aliases=("c2hs_haskell", "curry", "dhall", "idris", "purescript"),
        regex_patterns=(r"--.*",),
        nested_delimiters=(("{-", "-}"),),
        shared_regex_examples=(
            CommentExample(
                "prefix\n-- note\nsuffix",
                "-- note",
                "Dash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "before {- outer {- inner -} outer -} after",
                "{- outer {- inner -} outer -}",
                "Nested dash block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="abap_style",
        canonical_name="abap",
        regex_patterns=(
            r"(?m)^[ \t]*\*.*$",
            r"\".*",
        ),
        shared_regex_examples=(
            CommentExample(
                "* note\nafter",
                "* note",
                "Column-1 ABAP comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        canonical_regex_examples=(
            CommentExample(
                'DATA lv_value TYPE i.\n" note\nWRITE lv_value.',
                '" note',
                "Inline ABAP quote comment.",
                kind="line",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="comment_record_style",
        canonical_name="adobe_font_metrics",
        aliases=("glyph_bitmap_distribution_format",),
        regex_patterns=(r"(?im)\bcomment\b.*",),
        shared_regex_examples=(
            CommentExample(
                "Comment note\nafter",
                "Comment note",
                "Keyword-based comment record.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="apl_style",
        canonical_name="apl",
        regex_patterns=(r"⍝[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "value <- 1 ⍝ note\nvalue <- value + 1",
                "⍝ note",
                "APL lamp comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="alloy_style",
        canonical_name="alloy",
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r"/{2}.*.*",
            r"--.*",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n// note\nsuffix",
                "// note",
                "Alloy slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "prefix\n/* note */\nsuffix",
                "/* note */",
                "Alloy block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        canonical_regex_examples=(
            CommentExample(
                "prefix\n-- note\nsuffix",
                "-- note",
                "Alloy dash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="asciidoc_style",
        canonical_name="asciidoc",
        regex_patterns=(
            r"(?m)^(/{4,})[ \t]*(?:\r\n|\r|\n)[\S\s]*?^\1[ \t]*$",
            r"(?m)\/\/.*$",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n// note\nsuffix",
                "// note",
                "AsciiDoc line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "prefix\n////\nblock note\n////\nsuffix",
                "////\nblock note\n////",
                "AsciiDoc block comment.",
                kind="block",
            ),
        ),
    ),
    CommentSyntax(
        family_name="astro_style",
        canonical_name="astro",
        aliases=("marko",),
        regex_patterns=(
            r"<!--[\S\s]*?-->",
            r"\/\*[\S\s]*?\*\/",
            r"/{2}.*.*",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n// note\nsuffix",
                "// note",
                "Astro frontmatter line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "prefix\n/* note */\nsuffix",
                "/* note */",
                "Astro frontmatter block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        canonical_regex_examples=(
            CommentExample(
                "prefix\n<!-- note -->\nsuffix",
                "<!-- note -->",
                "Astro template block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="nested_c_style",
        canonical_name="dafny",
        aliases=("dm", "dylan", "jflex", "powerbuilder", "v"),
        regex_patterns=(r"/{2}.*.*",),
        nested_delimiters=(("/*", "*/"),),
        shared_regex_examples=(
            CommentExample(
                "prefix\n// note\nsuffix",
                "// note",
                "Slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "before /* outer /* inner */ outer */ after",
                "/* outer /* inner */ outer */",
                "Nested slash block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="dash_c_style",
        canonical_name="euphoria",
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r"--.*",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n-- note\nsuffix",
                "-- note",
                "Dash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "prefix\n/* note */\nsuffix",
                "/* note */",
                "Slash block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="gcode_style",
        canonical_name="g_code",
        regex_patterns=(
            r"\([\S\s]*?\)",
            r";.*",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n; note\nsuffix",
                "; note",
                "G-code semicolon comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "prefix\n( note )\nsuffix",
                "( note )",
                "G-code parenthesized comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="gams_style",
        canonical_name="gams",
        regex_patterns=(
            r"(?m)^\*[^\r\n]*",
            r"!![^\r\n]*",
            r"\/\*[\S\s]*?\*\/",
            (
                r"(?i)(?<![^\r\n])\$onText\b[^\r\n]*(?:\r\n|\r|\n)"
                r"[\S\s]*?(?<![^\r\n])\$offText\b[^\r\n]*"
            ),
        ),
        shared_regex_examples=(
            CommentExample(
                "* note\nafter",
                "* note",
                "Column-1 GAMS line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "prefix\n/* note */\nsuffix",
                "/* note */",
                "Inline GAMS block comment.",
                kind="block",
                inline_compatible=True,
            ),
            CommentExample(
                "prefix\n$ontext\nblock note\n$offtext\nsuffix",
                "$ontext\nblock note\n$offtext",
                "GAMS text block comment.",
                kind="block",
            ),
        ),
        canonical_regex_examples=(
            CommentExample(
                "value = 1 !! note\nDISPLAY value;",
                "!! note",
                "End-of-line GAMS comment when $onEolCom is enabled.",
                kind="line",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="golo_style",
        canonical_name="golo",
        regex_patterns=(r"#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "let x = 1 # note\nprintln(x)",
                "# note",
                "Golo hash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://github.com/eclipse-archived/golo-lang/blob/master/"
            "doc/basics.adoc"
        ),
        implementation_source=(
            "https://github.com/eclipse-archived/golo-lang/blob/master/"
            "src/main/jjtree/org/eclipse/golo/compiler/parser/Golo.jjt"
        ),
        confidence="verified",
        notes=(
            "Golo uses # line comments. The ---- delimited form is a "
            "documentation token, not a comment."
        ),
    ),
    CommentSyntax(
        family_name="gerber_style",
        canonical_name="gerber_image",
        regex_patterns=(r"G04.*\*.*",),
        shared_regex_examples=(
            CommentExample(
                "G04 note *\nafter",
                "G04 note *",
                "Gerber comment record.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="hoon_style",
        canonical_name="hoon",
        regex_patterns=(r"::.*",),
        shared_regex_examples=(
            CommentExample(
                "prefix\n:: note\nsuffix",
                ":: note",
                "Hoon line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="haml_style",
        canonical_name="haml",
        regex_patterns=(
            r"(?m)^([ \t]*)/[^\n]*(?:\n\1[ \t]+.*)*",
            r"(?m)^[ \t]*-#.*$",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n-# note\nsuffix",
                "-# note",
                "Haml silent comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "prefix\n/ note\nsuffix",
                "/ note",
                "Haml slash comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="handlebars_style",
        canonical_name="handlebars",
        regex_patterns=(
            r"\{\{!--[\S\s]*?--\}\}",
            r"\{\{![\S\s]*?\}\}",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n{{! note }}\nsuffix",
                "{{! note }}",
                "Handlebars inline comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "prefix\n{{!-- note --}}\nsuffix",
                "{{!-- note --}}",
                "Handlebars block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="inno_setup_style",
        canonical_name="inno_setup",
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r"/{2}.*.*",
            r";.*",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n; note\nsuffix",
                "; note",
                "Inno Setup script comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "prefix\n/* note */\nsuffix",
                "/* note */",
                "Inno Setup preprocessor block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        canonical_regex_examples=(
            CommentExample(
                "prefix\n// note\nsuffix",
                "// note",
                "Inno Setup preprocessor line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="jsp_style",
        canonical_name="jsp",
        aliases=("groovy_server_pages",),
        regex_patterns=(
            r"<%--[\S\s]*?--%>",
            r"<!--[\S\s]*?-->",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n<%-- note --%>\nsuffix",
                "<%-- note --%>",
                "JSP comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "prefix\n<!-- note -->\nsuffix",
                "<!-- note -->",
                "Markup block comment in JSP.",
                kind="block",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="razor_style",
        canonical_name="html_razor",
        regex_patterns=(r"@\*[\S\s]*?\*@",),
        shared_regex_examples=(
            CommentExample(
                "prefix\n@* note *@\nsuffix",
                "@* note *@",
                "Razor block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="lean_style",
        canonical_name="lean",
        regex_patterns=(r"--.*",),
        nested_delimiters=(("/-", "-/"),),
        shared_regex_examples=(
            CommentExample(
                "prefix\n-- note\nsuffix",
                "-- note",
                "Lean line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "before /- outer /- inner -/ outer -/ after",
                "/- outer /- inner -/ outer -/",
                "Nested Lean block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="liquid_style",
        canonical_name="liquid",
        regex_patterns=(
            r"\{%\s*comment\s*%\}[\S\s]*?\{%\s*endcomment\s*%\}",
            r"\{%\s*#.*?%\}",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n{% # note %}\nsuffix",
                "{% # note %}",
                "Liquid inline comment tag.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "prefix\n{% comment %}\nblock note\n{% endcomment %}\nsuffix",
                "{% comment %}\nblock note\n{% endcomment %}",
                "Liquid block comment tag.",
                kind="block",
            ),
        ),
    ),
    CommentSyntax(
        family_name="lolcode_style",
        canonical_name="lolcode",
        regex_patterns=(
            r"OBTW[\S\s]*?TLDR",
            r"BTW.*",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\nBTW note\nsuffix",
                "BTW note",
                "LOLCODE line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "prefix\nOBTW\nblock note\nTLDR\nsuffix",
                "OBTW\nblock note\nTLDR",
                "LOLCODE block comment.",
                kind="block",
            ),
        ),
    ),
    CommentSyntax(
        family_name="mustache_style",
        canonical_name="mustache",
        regex_patterns=(r"\{\{![\S\s]*?\}\}",),
        shared_regex_examples=(
            CommentExample(
                "prefix\n{{! note }}\nsuffix",
                "{{! note }}",
                "Mustache comment tag.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="pug_style",
        canonical_name="pug",
        regex_patterns=(
            r"(?m)^([ \t]*)//-?[^\n]*(?:\n\1[ \t]+.*)*",
            r"(?m)^[ \t]*//-?.*$",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n// note\nsuffix",
                "// note",
                "Pug line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="q_style",
        canonical_name="q",
        regex_patterns=(
            r"(?ms)(?<!\S)/[ \t]*\n[\S\s]*?\n\\(?!\S)",
            r"(?m)(?<!\S)/(?![/*]).*$",
        ),
        shared_regex_examples=(
            CommentExample(
                "a:42 / note\nb:0",
                "/ note",
                "q trailing line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="restructuredtext_style",
        canonical_name="restructuredtext",
        regex_patterns=(r"(?m)^\.\.\s.*(?:\n[ \t]+.*)*",),
        shared_regex_examples=(
            CommentExample(
                "Heading\n\n.. note\n\ntext",
                ".. note",
                "reStructuredText comment block.",
                kind="block",
            ),
        ),
    ),
    CommentSyntax(
        family_name="rexx_style",
        canonical_name="rexx",
        nested_delimiters=(("/*", "*/"),),
        shared_nested_examples=(
            CommentExample(
                "before /* outer /* inner */ outer */ after",
                "/* outer /* inner */ outer */",
                "Nested REXX block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="roff_style",
        canonical_name="roff",
        aliases=("roff_manpage",),
        regex_patterns=(r"\\\".*",),
        shared_regex_examples=(
            CommentExample(
                '.\\" note\nafter',
                '\\" note',
                "Roff escaped-quote comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="stata_style",
        canonical_name="stata",
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r"/{2}.*.*",
            r"(?m)^\*.*$",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n// note\nsuffix",
                "// note",
                "Stata slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "prefix\n/* note */\nsuffix",
                "/* note */",
                "Stata block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        canonical_regex_examples=(
            CommentExample(
                "* note\nafter",
                "* note",
                "Column-1 Stata line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="coldfusion_style",
        canonical_name="coldfusion",
        aliases=("coldfusion_cfc",),
        nested_delimiters=(("<!---", "--->"),),
        shared_nested_examples=(
            CommentExample(
                "before <!--- note ---> after",
                "<!--- note --->",
                "ColdFusion block comment.",
                kind="block",
                inline_compatible=True,
            ),
            CommentExample(
                "before <!--- outer <!--- inner ---> outer ---> after",
                "<!--- outer <!--- inner ---> outer --->",
                "Nested ColdFusion block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="genero_style",
        canonical_name="genero",
        regex_patterns=(
            r"\{[\S\s]*?\}",
            r"--.*",
            r"#.*",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n-- note\nsuffix",
                "-- note",
                "Genero dash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "prefix\n{ note }\nsuffix",
                "{ note }",
                "Genero brace comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        canonical_regex_examples=(
            CommentExample(
                "prefix\n# note\nsuffix",
                "# note",
                "Genero hash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="inform7_style",
        canonical_name="inform_7",
        regex_patterns=(r"\[[\S\s]*?\]",),
        shared_regex_examples=(
            CommentExample(
                "The China Shop is a room. [Remember the bull.]",
                "[Remember the bull.]",
                "Inform 7 bracket comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="j_style",
        canonical_name="j",
        regex_patterns=(r"(?m)(?<!\S)NB\..*$",),
        shared_regex_examples=(
            CommentExample(
                "NB. note\nafter",
                "NB. note",
                "J line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        canonical_regex_examples=(
            CommentExample(
                "value =: 1 NB. inline note\nvalue",
                "NB. inline note",
                "J inline comment.",
                kind="line",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="objectscript_style",
        canonical_name="objectscript",
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r"/{2}.*.*",
            r"##;.*",
            r"(?m)^#;.*$",
            r";.*",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n// note\nsuffix",
                "// note",
                "ObjectScript slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "prefix\n/* note */\nsuffix",
                "/* note */",
                "ObjectScript block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        canonical_regex_examples=(
            CommentExample(
                "Set x = 1 ; note\nSet y = 2",
                "; note",
                "ObjectScript semicolon line comment.",
                kind="line",
                inline_compatible=True,
            ),
            CommentExample(
                '#define alphalen ##function($LENGTH("abcdefghijklmnopqrstuvwxyz")) ##; + 100',
                "##; + 100",
                "ObjectScript macro comment.",
                kind="line",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="promela_style",
        canonical_name="promela",
        regex_patterns=(r"\/\*[\S\s]*?\*\/",),
        shared_regex_examples=(
            CommentExample(
                "prefix\n/* note */\nsuffix",
                "/* note */",
                "Native Promela block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        notes=(
            "This entry intentionally models only native Promela comments. "
            "C-preprocessor // comments are not included."
        ),
    ),
    CommentSyntax(
        family_name="plantuml_style",
        canonical_name="plantuml",
        regex_patterns=(
            r"/'[\S\s]*?'/",
            r"'.*",
        ),
        shared_regex_examples=(
            CommentExample(
                "@startuml\n' note\nAlice -> Bob : hello\n@enduml",
                "' note",
                "PlantUML apostrophe line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "@startuml\n/' note '/\nAlice -> Bob : hello\n@enduml",
                "/' note '/",
                "PlantUML block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="rdoc_style",
        canonical_name="rdoc",
        regex_patterns=(
            r"(?ms)^[ \t]*=begin\b[\s\S]*?^[ \t]*=end\b[ \t]*$",
            r"\/\*[\S\s]*?\*\/",
            r"#.*",
        ),
        shared_regex_examples=(
            CommentExample(
                "# note\ndef hello(name)\n  name\nend",
                "# note",
                "RDoc line comment in Ruby source.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "before\n/* note */\nafter",
                "/* note */",
                "RDoc block comment in C source.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        canonical_regex_examples=(
            CommentExample(
                "before\n=begin\nnote\n=end\nafter",
                "=begin\nnote\n=end",
                "RDoc begin/end block comment.",
                kind="block",
            ),
        ),
    ),
    CommentSyntax(
        family_name="self_style",
        canonical_name="self",
        regex_patterns=(r'"[\S\s]*?"',),
        shared_regex_examples=(
            CommentExample(
                'before\n"note"\nafter',
                '"note"',
                "Self double-quoted comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="slim_style",
        canonical_name="slim",
        regex_patterns=(r"(?m)^([ \t]*)/!?[^\n]*(?:\n\1[ \t]+.*)*",),
        shared_regex_examples=(
            CommentExample(
                "body\n  / note\n  p Visible content.",
                "  / note",
                "Slim line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        canonical_regex_examples=(
            CommentExample(
                "body\n  /! note\n  p Visible content.",
                "  /! note",
                "Slim HTML-comment form opener.",
                kind="block",
            ),
        ),
    ),
    CommentSyntax(
        family_name="smarty_style",
        canonical_name="smarty",
        regex_patterns=(r"\{\*[\S\s]*?\*\}",),
        shared_regex_examples=(
            CommentExample(
                "before\n{* note *}\nafter",
                "{* note *}",
                "Smarty template comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="tla_style",
        canonical_name="tla",
        regex_patterns=(r"\\\*.*",),
        nested_delimiters=(("(*", "*)"),),
        shared_regex_examples=(
            CommentExample(
                "prefix\n\\* note\nsuffix",
                "\\* note",
                "TLA+ line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "before (* outer (* inner *) outer *) after",
                "(* outer (* inner *) outer *)",
                "Nested TLA+ block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="bicep_style",
        canonical_name="bicep",
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r"/{2}.*.*",
        ),
        shared_regex_examples=(
            CommentExample(
                "param name string\n// note\noutput x string = name",
                "// note",
                "Bicep single-line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "param name string\n/* note */\noutput x string = name",
                "/* note */",
                "Bicep multiline comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/file"
        ),
        confidence="verified",
        notes="Microsoft Bicep file syntax supports // and /* ... */ comments.",
    ),
    CommentSyntax(
        family_name="bitbake_style",
        canonical_name="bitbake",
        regex_patterns=(r"(?m)^[ \t]*#.*$",),
        shared_regex_examples=(
            CommentExample(
                'SUMMARY = "Example"\n# note\nLICENSE = "MIT"',
                "# note",
                "BitBake recipe comment line.",
                kind="line",
                inline_compatible=False,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="https://docs.yoctoproject.org/5.3.4/dev-manual/new-recipe.html",
        confidence="verified",
        notes="Yocto recipe syntax treats lines beginning with # as comments.",
    ),
    CommentSyntax(
        family_name="coffeescript_style",
        canonical_name="coffeescript",
        regex_patterns=(
            r"###[\S\s]*?###",
            r"#.*",
        ),
        shared_regex_examples=(
            CommentExample(
                "x = 1\n# note\ny = 2",
                "# note",
                "CoffeeScript line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "x = 1\n###\nnote\n###\ny = 2",
                "###\nnote\n###",
                "CoffeeScript block comment.",
                kind="block",
            ),
        ),
        documentation_source="https://coffeescript.org/",
        confidence="verified",
        notes="CoffeeScript uses # line comments and ### block comments.",
    ),
    CommentSyntax(
        family_name="fennel_style",
        canonical_name="fennel",
        regex_patterns=(r";.*",),
        shared_regex_examples=(
            CommentExample(
                "(print :hello)\n; note\n(print :bye)",
                "; note",
                "Fennel semicolon line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://raw.githubusercontent.com/bakpakin/Fennel/main/reference.md"
        ),
        confidence="verified",
        notes="Fennel comments run from ; to the end of the line.",
    ),
    CommentSyntax(
        family_name="kusto_style",
        canonical_name="kusto",
        regex_patterns=(r"/{2}.*.*",),
        shared_regex_examples=(
            CommentExample(
                "StormEvents\n// note\n| count",
                "// note",
                "Kusto line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://learn.microsoft.com/en-us/kusto/query/comment?view=microsoft-fabric"
        ),
        confidence="verified",
        notes="Kusto Query Language comments use // and run to end of line.",
    ),
    CommentSyntax(
        family_name="lfe_style",
        canonical_name="lfe",
        regex_patterns=(r";.*",),
        shared_regex_examples=(
            CommentExample(
                "(defun ping ()\n  ; note\n  'pong)",
                "; note",
                "LFE semicolon line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="https://docs.lfe.io/current/prog-rules/8.html",
        confidence="verified",
        notes="LFE uses semicolon comments, with repeated semicolons as style levels.",
    ),
    CommentSyntax(
        family_name="m4_style",
        canonical_name="m4",
        aliases=("m4sugar",),
        regex_patterns=(r"#.*",),
        shared_regex_examples=(
            CommentExample(
                "define([name], [value])\n# note\nname",
                "# note",
                "GNU m4 default comment delimiter.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="https://www.gnu.org/software/m4/manual/html_node/Comments.html",
        confidence="verified",
        notes="GNU m4 defaults to # through newline; changecom can alter delimiters.",
    ),
    CommentSyntax(
        family_name="macaulay2_style",
        canonical_name="macaulay2",
        regex_patterns=(
            r"-\*[\S\s]*?\*-",
            r"--.*",
        ),
        shared_regex_examples=(
            CommentExample(
                "x = 1 -- note\ny = 2",
                "-- note",
                "Macaulay2 line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "x = 1\ny = -* note *- 2",
                "-* note *-",
                "Macaulay2 enclosed comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://macaulay2.com/doc/Macaulay2/share/doc/Macaulay2/"
            "Macaulay2Doc/html/_comments.html"
        ),
        confidence="verified",
        notes="Macaulay2 uses -- line comments and -* ... *- enclosed comments.",
    ),
    CommentSyntax(
        family_name="motoko_style",
        canonical_name="motoko",
        regex_patterns=(r"/{2}.*.*",),
        nested_delimiters=(("/*", "*/"),),
        shared_regex_examples=(
            CommentExample(
                "actor {\n  // note\n}",
                "// note",
                "Motoko line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "actor { /* outer /* inner */ outer */ }",
                "/* outer /* inner */ outer */",
                "Motoko nested block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://docs.internetcomputer.org/motoko/language-manual/",
        confidence="verified",
        notes="Motoko supports // comments and nested /* ... */ comments.",
    ),
    CommentSyntax(
        family_name="move_style",
        canonical_name="move",
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r"/{2}.*.*",
        ),
        shared_regex_examples=(
            CommentExample(
                "module 0x1::m {\n// note\n}",
                "// note",
                "Move single-line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "module 0x1::m {\n/* note */\n}",
                "/* note */",
                "Move block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://move-language.github.io/move/coding-conventions.html",
        confidence="verified",
        notes="Move supports //, /* ... */, ///, and /** ... */ comment forms.",
    ),
)


def _build_language_lookup() -> Dict[str, CommentSyntax]:
    """Build and validate the lowercase language-to-syntax lookup.

    Returns:
        Mapping from each supported language key to its ``CommentSyntax``.

    Raises:
        ValueError: If a registry entry lacks examples, uses mixed-case keys, or
            duplicates an existing language key.
    """

    lookup = {}
    for syntax in COMMENT_SYNTAXES:
        if syntax.regex_patterns and not (
            syntax.shared_regex_examples or syntax.canonical_regex_examples
        ):
            raise ValueError(
                "Registry entries with regex patterns must provide seeded regex examples: "
                + syntax.family_name
            )

        if syntax.nested_delimiters and not (
            syntax.shared_nested_examples or syntax.canonical_nested_examples
        ):
            raise ValueError(
                "Registry entries with nested delimiters must provide seeded nested examples: "
                + syntax.family_name
            )

        for language in syntax.language_names:
            if language != language.lower():
                raise ValueError(f"Language names must be lowercase: {language}")
            if language in lookup:
                raise ValueError(f"Duplicate comment syntax entry for language: {language}")
            lookup[language] = syntax
    return lookup


LANGUAGE_SYNTAX = _build_language_lookup()
SUPPORTED_LANGUAGES = tuple(sorted(LANGUAGE_SYNTAX))


def get_supported_comment_languages() -> list[str]:
    """Return the implemented comment-parser language keys as a sorted list."""

    return list(SUPPORTED_LANGUAGES)


def get_comment_syntax(language: str) -> CommentSyntax:
    """Return syntax metadata for one supported language.

    Args:
        language: Registry key or alias. Lookup is case-insensitive.

    Returns:
        The matching ``CommentSyntax`` entry.

    Raises:
        NotImplementedError: If the language is not in the registry.
    """

    try:
        return LANGUAGE_SYNTAX[language.lower()]
    except KeyError as exc:
        raise NotImplementedError(f"Unsupported language: {language}") from exc


def iter_comment_syntaxes() -> Iterable[CommentSyntax]:
    """Return all canonical syntax-family entries in registry order."""

    return COMMENT_SYNTAXES
