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
        source_region_patterns: Optional regexes limiting extraction to
            language-bearing source regions, useful for literate formats.
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
    source_region_patterns: Tuple[str, ...] = ()
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
        family_name="blitzbasic_style",
        canonical_name="blitzbasic",
        regex_patterns=(r";[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "Function Redraw() ; note\nEnd Function",
                "; note",
                "BlitzBasic semicolon line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://github.com/blitz-research/blitz3d/blob/master/"
            "_release/help/language/lang_ref_comments.html"
        ),
        implementation_source=(
            "https://github.com/blitz-research/blitz3d/blob/master/"
            "compiler/toker.cpp"
        ),
        confidence="verified",
        notes=(
            "Semicolon comments run to the end of the line and may follow "
            "code. The archived master and v1.108b sources agree."
        ),
    ),
    CommentSyntax(
        family_name="blitzmax_style",
        canonical_name="blitzmax",
        regex_patterns=(
            r"(?im)^[ \t]*rem\b[\S\s]*?^[ \t]*end[ \t]*rem\b[^\r\n]*",
            r"'[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                'Print "Comment Test"    \' note\nPrint "done"',
                "' note",
                "BlitzMax apostrophe line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "Rem\nnote\nEnd Rem\nPrint \"done\"",
                "Rem\nnote\nEnd Rem",
                "BlitzMax Rem block comment.",
                kind="block",
            ),
        ),
        documentation_source="https://blitzmax.org/docs/en/language/comments/",
        implementation_source=(
            "https://github.com/bmx-ng/bcc/blob/master/toker.bmx"
        ),
        confidence="verified",
        notes=(
            "Apostrophe comments run to newline. Rem blocks are line-oriented, "
            "non-nested, and accept EndRem or End Rem; current bcc and archived "
            "BlitzMax v1.51 agree."
        ),
    ),
    CommentSyntax(
        family_name="bluespec_style",
        canonical_name="bluespec",
        regex_patterns=(
            r"/\*[\S\s]*?\*/",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "rule update;\n  // note\n  value <= 1;\nendrule",
                "// note",
                "Bluespec one-line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "rule update;\n  /* note */\n  value <= 1;\nendrule",
                "/* note */",
                "Bluespec non-nested block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://github.com/B-Lang-org/bsc/blob/main/"
            "doc/BSV_ref_guide/BSV_lang.tex"
        ),
        implementation_source=(
            "https://github.com/B-Lang-org/bsc/blob/main/"
            "src/comp/SystemVerilogPreprocess.lhs"
        ),
        confidence="verified",
        notes=(
            "The BSV reference explicitly states that comments do not nest. "
            "Current main and the 2021.07 compiler preprocessor agree."
        ),
    ),
    CommentSyntax(
        family_name="boo_style",
        canonical_name="boo",
        regex_patterns=(
            r"#[^\r\n]*",
            r"/{2}[^\r\n]*",
        ),
        nested_delimiters=(("/*", "*/"),),
        shared_regex_examples=(
            CommentExample(
                "value = 1 # note\nvalue += 1",
                "# note",
                "Boo hash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "value = 1 // note\nvalue += 1",
                "// note",
                "Boo slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "value = 1\n/* outer /* note */ outer */\nvalue += 1",
                "/* outer /* note */ outer */",
                "Boo nested block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://github.com/boo-lang/boo/wiki/Language-guide%3A-comments"
        ),
        implementation_source=(
            "https://github.com/boo-lang/boo/blob/master/"
            "src/Boo.Lang.Parser/boo.g"
        ),
        confidence="verified",
        notes=(
            "Boo accepts # and // line comments and recursively parses nested "
            "/* ... */ blocks. Current master and the unstable tag agree."
        ),
    ),
    CommentSyntax(
        family_name="boogie_style",
        canonical_name="boogie",
        regex_patterns=(r"/{2}[^\r\n]*",),
        nested_delimiters=(("/*", "*/"),),
        shared_regex_examples=(
            CommentExample(
                "var value:int; // note\nassume value > 0;",
                "// note",
                "Boogie slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "var value:int;\n/* outer /* note */ outer */\n"
                "assume value > 0;",
                "/* outer /* note */ outer */",
                "Boogie nested block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://boogie-docs.readthedocs.io/en/latest/LangRef.html#comments"
        ),
        implementation_source=(
            "https://github.com/boogie-org/boogie/blob/master/"
            "Source/Core/BoogiePL.atg"
        ),
        confidence="verified",
        notes=(
            "The language reference documents // comments; the authoritative "
            "grammar additionally declares nested /* ... */ comments. Current "
            "master and release v3.5.6 agree."
        ),
    ),
    CommentSyntax(
        family_name="brighterscript_style",
        canonical_name="brighterscript",
        regex_patterns=(
            r"'[^\r\n]*",
            r"(?i:(?<![.\w])rem\b[^\r\n]*)",
        ),
        shared_regex_examples=(
            CommentExample(
                "value = 1 ' note\nvalue++",
                "' note",
                "BrighterScript apostrophe line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "REM note\nvalue = 1",
                "REM note",
                "BrighterScript REM line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://github.com/rokucommunity/brighterscript/blob/master/"
            "docs/readme.md"
        ),
        implementation_source=(
            "https://github.com/rokucommunity/brighterscript/blob/master/"
            "src/lexer/Lexer.ts"
        ),
        confidence="verified",
        notes=(
            "BrighterScript inherits apostrophe and case-insensitive REM line "
            "comments from BrightScript. The lexer preserves .rem as member "
            "access and explicitly has no block comments. v0.72.5 and v0.71.1 "
            "agree."
        ),
    ),
    CommentSyntax(
        family_name="brightscript_style",
        canonical_name="brightscript",
        regex_patterns=(
            r"'[^\r\n]*",
            r"(?i:(?<![.\w])rem\b[^\r\n]*)",
        ),
        shared_regex_examples=(
            CommentExample(
                "value = 1 ' note\nvalue = value + 1",
                "' note",
                "BrightScript apostrophe line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "REM note\nvalue = 1",
                "REM note",
                "BrightScript REM line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://developer.roku.com/dev/docs/expressions-variables-types"
        ),
        implementation_source=(
            "https://github.com/rokucommunity/brighterscript/blob/master/"
            "src/lexer/Lexer.ts"
        ),
        confidence="verified",
        notes=(
            "Roku documents apostrophe and case-insensitive REM comments through "
            "the end of line and states that BrightScript has no block-comment "
            "form. The compatible BrighterScript lexer preserves .rem as member "
            "access."
        ),
    ),
    CommentSyntax(
        family_name="browserslist_style",
        canonical_name="browserslist",
        regex_patterns=(r"#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "defaults # note\nlast 2 versions",
                "# note",
                "Browserslist trailing hash comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://github.com/browserslist/browserslist#browserslistrc"
        ),
        implementation_source=(
            "https://github.com/browserslist/browserslist/blob/main/node.js"
        ),
        confidence="verified",
        notes=(
            "Browserslist strips # through newline before splitting config "
            "queries, so both full-line and trailing comments are supported. "
            "Versions 4.28.2 and 4.27.0 agree."
        ),
    ),
    CommentSyntax(
        family_name="cabal_config_style",
        canonical_name="cabal_config",
        regex_patterns=(r"(?m)^[ \t]*--[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "-- note\nremote-repo-cache: /tmp/cabal",
                "-- note",
                "Cabal configuration comment-only line.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="https://cabal.readthedocs.io/en/stable/config.html",
        implementation_source=(
            "https://github.com/haskell/cabal/blob/master/Cabal-syntax/src/"
            "Distribution/Fields/Lexer.x"
        ),
        confidence="verified",
        notes=(
            "Cabal configuration uses the Cabal field-file lexer. Comments begin "
            "with -- after optional leading whitespace on their own line; "
            "ordinary trailing comments are excluded because values may contain "
            "program options. Current master and 3.14.2.0 agree."
        ),
    ),
    CommentSyntax(
        family_name="cadence_style",
        canonical_name="cadence",
        regex_patterns=(r"/{2}[^\r\n]*",),
        nested_delimiters=(("/*", "*/"),),
        shared_regex_examples=(
            CommentExample(
                "let value = 1 // note\nlog(value)",
                "// note",
                "Cadence slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "let value = 1\n/* outer /* note */ outer */\nlog(value)",
                "/* outer /* note */ outer */",
                "Cadence balanced nested block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://cadence-lang.org/docs/language/syntax#comments",
        implementation_source=(
            "https://github.com/onflow/cadence/blob/master/parser/comment.go"
        ),
        confidence="verified",
        notes=(
            "Cadence line comments run to newline and block comments are "
            "balanced with recursive nesting. Documentation-comment forms are "
            "subsets of these delimiters. Current master and v1.8.9 agree."
        ),
    ),
    CommentSyntax(
        family_name="cartocss_style",
        canonical_name="cartocss",
        regex_patterns=(
            r"/{2}[^\r\n]*",
            r"/\*[\S\s]*?\*/",
        ),
        shared_regex_examples=(
            CommentExample(
                "#layer {\n  line-color: #fff; // note\n}",
                "// note",
                "CartoCSS silent Less-style line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "#layer {\n  /* note */\n  line-color: #fff;\n}",
                "/* note */",
                "CartoCSS CSS block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://cartocss.readthedocs.io/en/latest/language_elements.html"
        ),
        implementation_source=(
            "https://github.com/cartocss/carto/blob/master/lib/carto/parser.js"
        ),
        confidence="verified",
        notes=(
            "CartoCSS skips // comments silently and retains /* ... */ comments "
            "as comment nodes. Block comments stop at the first closing "
            "delimiter and do not nest. v1.3.1 and v1.2.0 agree."
        ),
    ),
    CommentSyntax(
        family_name="ceylon_style",
        canonical_name="ceylon",
        regex_patterns=(
            r"/{2}[^\r\n]*",
            r"\#![^\r\n]*",
        ),
        nested_delimiters=(("/*", "*/"),),
        shared_regex_examples=(
            CommentExample(
                'shared void run() {\n  print("hi"); // note\n}',
                "// note",
                "Ceylon slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "#!/usr/bin/ceylon\nshared void run() {}",
                "#!/usr/bin/ceylon",
                "Ceylon shebang comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "shared void run() {\n  /* outer /* note */ outer */\n}",
                "/* outer /* note */ outer */",
                "Ceylon recursively nested block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://web.mit.edu/ceylon_v1.3.3/ceylon-1.3.3/doc/en/spec/"
            "html_single/#comments"
        ),
        implementation_source=(
            "https://github.com/eclipse-archived/ceylon/blob/master/typechecker/"
            "antlr/org/eclipse/ceylon/compiler/typechecker/parser/Ceylon.g"
        ),
        confidence="verified",
        notes=(
            "Ceylon 1.3 defines // and #! end-of-line comments plus recursively "
            "nested /* ... */ comments. The archived 1.3.4-SNAPSHOT compiler "
            "grammar implements the same forms."
        ),
    ),
    CommentSyntax(
        family_name="chapel_style",
        canonical_name="chapel",
        regex_patterns=(r"/{2}[^\r\n]*",),
        nested_delimiters=(("/*", "*/"),),
        shared_regex_examples=(
            CommentExample(
                'proc main() {\n  writeln("hello"); // note\n}',
                "// note",
                "Chapel slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "proc main() {\n  /* outer /* note */ outer */\n}",
                "/* outer /* note */ outer */",
                "Chapel recursively nested block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://chapel-lang.org/docs/language/spec/lexical-structure.html"
            "#comments"
        ),
        implementation_source=(
            "https://github.com/chapel-lang/chapel/blob/main/frontend/lib/"
            "parsing/lexer-help.h"
        ),
        confidence="verified",
        notes=(
            "Chapel line comments run to newline and /* ... */ comments are "
            "balanced with recursive nesting. The current 2.8 specification, "
            "the 0.98 specification, and the current compiler scanner agree."
        ),
    ),
    CommentSyntax(
        family_name="cil_style",
        canonical_name="cil",
        regex_patterns=(
            r"/{2}[^\r\n]*",
            r"/\*[\S\s]*?\*/",
        ),
        shared_regex_examples=(
            CommentExample(
                ".method public static void Main() cil managed {\n"
                "  ret // note\n"
                "}",
                "// note",
                "ILAsm slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                ".method public static void Main() cil managed {\n"
                "  /* note */\n"
                "  ret\n"
                "}",
                "/* note */",
                "ILAsm non-nested block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://learn.microsoft.com/en-us/archive/msdn-magazine/2001/may/"
            "bugslayer-ildasm-is-your-new-best-friend"
        ),
        implementation_source=(
            "https://github.com/dotnet/runtime/blob/main/src/coreclr/ilasm/"
            "grammar_after.cpp"
        ),
        confidence="verified",
        notes=(
            "The ILAsm lexer treats // as an end-of-line comment and /* ... */ "
            "as a non-nested block comment that stops at the first closing "
            "delimiter. .NET 6, .NET 10, and current main agree."
        ),
    ),
    CommentSyntax(
        family_name="clarion_style",
        canonical_name="clarion",
        regex_patterns=(r"![^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "PROGRAM ! note\nCODE",
                "! note",
                "Clarion inline exclamation comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://clarion.help/doku.php?id=special_characters.htm"
        ),
        implementation_source=(
            "https://github.com/fushnisoft/SublimeClarion/blob/master/"
            "clarion.configuration.json"
        ),
        confidence="verified",
        notes=(
            "Clarion ! comments run to the end of the source line and may "
            "follow code. Clarion# multiline comments are a separate dialect "
            "and are intentionally excluded from the Clarion Stack key."
        ),
    ),
    CommentSyntax(
        family_name="clean_style",
        canonical_name="clean",
        regex_patterns=(r"/{2}[^\r\n]*",),
        nested_delimiters=(("/*", "*/"),),
        shared_regex_examples=(
            CommentExample(
                "Start = 0 // note\n",
                "// note",
                "Clean slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "Start = 0\n/* outer /* note */ outer */\n",
                "/* outer /* note */ outer */",
                "Clean recursively nested block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://clean.cs.ru.nl/download/doc/CleanLangRep.2.2.pdf"
        ),
        implementation_source=(
            "https://gitlab.science.ru.nl/clean-compiler-and-rts/compiler/"
            "-/blob/master/frontend/scanner.icl"
        ),
        confidence="verified",
        notes=(
            "Clean line comments run to newline and /* ... */ comments are "
            "balanced recursively. The 2.2 language report and current "
            "compiler scanner agree."
        ),
    ),
    CommentSyntax(
        family_name="click_style",
        canonical_name="click",
        regex_patterns=(
            r"/{2}[^\r\n]*",
            r"/\*[\S\s]*?\*/",
        ),
        shared_regex_examples=(
            CommentExample(
                "src -> queue; // note\nqueue -> sink;",
                "// note",
                "Click slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "src -> /* note */ queue;",
                "/* note */",
                "Click non-nested block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://github.com/kohler/click/blob/master/doc/click.5"
        ),
        implementation_source=(
            "https://github.com/kohler/click/blob/master/lib/lexer.cc"
        ),
        confidence="verified",
        notes=(
            "Click uses // and non-nested /* ... */ comments throughout "
            "configuration files and strings. Column-zero # forms are line "
            "directives, not comments, and are intentionally excluded."
        ),
    ),
    CommentSyntax(
        family_name="clips_style",
        canonical_name="clips",
        regex_patterns=(r";[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "(defrule example ; note\n  =>\n  (printout t \"ok\" crlf))",
                "; note",
                "CLIPS semicolon line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://www.clipsrules.net/documentation/v642/bpg642.pdf"
        ),
        implementation_source=(
            "https://github.com/noxdafox/clips/blob/master/core/scanner.c"
        ),
        confidence="verified",
        notes=(
            "CLIPS semicolon comments run to the next newline. The scanner "
            "removes semicolon comments while skipping whitespace; no CLIPS "
            "block-comment delimiter is documented or implemented."
        ),
    ),
    CommentSyntax(
        family_name="closure_templates_style",
        canonical_name="closure_templates",
        regex_patterns=(
            r"(?m)(?<![^\s])//[^\r\n]*",
            r"/\*[\S\s]*?\*/",
        ),
        shared_regex_examples=(
            CommentExample(
                "{template .example}\n  // note\n  <div>content</div>\n{/template}",
                "// note",
                "Soy single-line comment with required leading whitespace.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "{template .example}\n  /* note */\n  <div>content</div>\n{/template}",
                "/* note */",
                "Soy non-nested multiline comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://github.com/google/closure-templates/blob/master/"
            "documentation/reference/comments.md"
        ),
        implementation_source=(
            "https://github.com/google/closure-templates/blob/master/java/src/"
            "com/google/template/soy/soyparse/SoyFileParser.jj"
        ),
        confidence="verified",
        notes=(
            "Current Soy uses // and non-nested /* ... */ comments, including "
            "SoyDoc /** ... */ as a block-comment subset. In template text, "
            "the parser only accepts // after whitespace to avoid treating URI "
            "schemes as comments; the registry encodes the same constraint."
        ),
    ),
    CommentSyntax(
        family_name="component_pascal_style",
        canonical_name="component_pascal",
        nested_delimiters=(("(*", "*)"),),
        shared_nested_examples=(
            CommentExample(
                "(* outer (* inner *) outer *)\nMODULE Example;",
                "(* outer (* inner *) outer *)",
                "Component Pascal nested block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://blackbox.oberon.org/cp-lang.pdf",
        confidence="high",
        notes=(
            "Component Pascal uses Oberon-family nested (* ... *) comments. "
            "Pascal brace comments and // line comments are intentionally excluded."
        ),
    ),
    CommentSyntax(
        family_name="cool_style",
        canonical_name="cool",
        regex_patterns=(r"--[^\r\n]*",),
        nested_delimiters=(("(*", "*)"),),
        shared_regex_examples=(
            CommentExample(
                "-- note\nclass Main inherits IO {\n}",
                "-- note",
                "Cool dash line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "(* outer (* inner *) outer *)\nclass Main inherits IO {\n}",
                "(* outer (* inner *) outer *)",
                "Cool nested block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://theory.stanford.edu/~aiken/software/cool/cool-manual.pdf"
        ),
        implementation_source=(
            "https://theory.stanford.edu/~aiken/software/cooldist/assignments/"
            "PA2/cool.flex.SKEL"
        ),
        confidence="verified",
        notes="Cool supports -- line comments and true nested (* ... *) comments.",
    ),
    CommentSyntax(
        family_name="csound_style",
        canonical_name="csound",
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r";[^\r\n]*",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "; note\ninstr 1\nendin",
                "; note",
                "Csound orchestra semicolon line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "instr 1\n  a1 oscili 0.5, 440 // note\nendin",
                "// note",
                "Csound orchestra slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/* note */\ninstr 1\nendin",
                "/* note */",
                "Csound orchestra block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://csound.com/docs/manual/OrchTop.html; "
            "https://csound.com/get-started.html"
        ),
        implementation_source=(
            "https://github.com/nwhetsell/language-csound/blob/master/"
            "grammars/csound.cson"
        ),
        confidence="verified",
        notes="Generic Csound covers orchestra-style ;, //, and non-nested /* ... */ comments.",
    ),
    CommentSyntax(
        family_name="csound_document_style",
        canonical_name="csound_document",
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r";[^\r\n]*",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "<CsoundSynthesizer>\n<CsInstruments>\n; note\n</CsInstruments>\n</CsoundSynthesizer>",
                "; note",
                "Csound document instrument semicolon comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "<CsoundSynthesizer>\n<CsInstruments>\n// note\n</CsInstruments>\n</CsoundSynthesizer>",
                "// note",
                "Csound document instrument slash comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "<CsoundSynthesizer>\n<CsInstruments>\n/* note */\n</CsInstruments>\n</CsoundSynthesizer>",
                "/* note */",
                "Csound document instrument block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://csound.com/docs/manual/CommandUnifile.html; "
            "https://csound.com/docs/manual/PrefaceGettingStarted.html; "
            "https://csound.com/docs/manual/ScoreStatements.html"
        ),
        implementation_source=(
            "https://github.com/nwhetsell/language-csound/blob/master/"
            "grammars/csound-document.cson"
        ),
        confidence="high",
        notes=(
            "Encodes the registry-safe Csound document delimiters only. "
            "CsOptions # comments and CsScore c statements are section-specific "
            "and are excluded from this global lexical entry."
        ),
    ),
    CommentSyntax(
        family_name="csound_score_style",
        canonical_name="csound_score",
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r"(?m)^[ \t]*c(?:[ \t][^\r\n]*)?$",
            r";[^\r\n]*",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "; note\nf 1 0 1024 10 1",
                "; note",
                "Csound score semicolon line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "// note\ni 1 0 1",
                "// note",
                "Csound score slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "c note\ni 1 0 1",
                "c note",
                "Csound score c comment statement.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/* note */\ni 1 0 1",
                "/* note */",
                "Csound score block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://csound.com/docs/manual/ScoreStatements.html",
        implementation_source=(
            "https://github.com/nwhetsell/language-csound/blob/master/"
            "grammars/csound-score.cson"
        ),
        confidence="high",
        notes=(
            "Score c comments are line-start statements; the regex keeps them "
            "anchored so p-field text is not treated as a comment."
        ),
    ),
    CommentSyntax(
        family_name="cue_sheet_style",
        canonical_name="cue_sheet",
        regex_patterns=(r"(?mi)^[ \t]*REM\b[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "REM note\nTRACK 01 AUDIO",
                "REM note",
                "Cue sheet REM remark command.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://wiki.hydrogenaudio.org/index.php?title=Cue_sheet; "
            "https://github.com/libyal/libodraw/blob/main/documentation/"
            "CUE%20sheet%20format.asciidoc"
        ),
        implementation_source=(
            "https://github.com/lipnitsk/libcue/blob/master/cue_scanner.l"
        ),
        confidence="high",
        notes=(
            "Only standard line-anchored REM remarks are encoded. Non-standard "
            "semicolon and // variants are excluded."
        ),
    ),
    CommentSyntax(
        family_name="cweb_style",
        canonical_name="cweb",
        regex_patterns=(r"@q[^\r\n]*?@>",),
        shared_regex_examples=(
            CommentExample(
                "@q source-only note@>\n@* Introduction.",
                "@q source-only note@>",
                "CWEB control text ignored by CTANGLE and CWEAVE.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://mirrors.ctan.org/web/c_cpp/cweb/cwebman.pdf; "
            "https://www-cs-faculty.stanford.edu/~knuth/cweb.html"
        ),
        implementation_source="https://github.com/ascherer/cweb/blob/master/ctangle.w",
        confidence="high",
        notes=(
            "Only CWEB-specific @q ... @> control text is encoded. C/C++ and "
            "TeX comments are context-dependent within CWEB and are excluded."
        ),
    ),
    CommentSyntax(
        family_name="cycript_style",
        canonical_name="cycript",
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "// note\nvar x = 1;",
                "// note",
                "Cycript slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/* note */\nvar x = 1;",
                "/* note */",
                "Cycript block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://www.cycript.org/manual/; https://www.cycript.org/; "
            "https://tc39.es/ecma262/#sec-comments"
        ),
        confidence="high",
        notes="Cycript uses JavaScript/Objective-C-family non-nested slash comments.",
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
        family_name="object_data_instance_notation_style",
        canonical_name="object_data_instance_notation",
        regex_patterns=(r"--[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                'name = <"Django Reinhardt"> -- note\nbirthdate = <1919-01-23>',
                "-- note",
                "ODIN double-hyphen line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://specifications.openehr.org/releases/LANG/latest/odin.html#_comments"
        ),
        implementation_source="unresolved",
        confidence="verified",
        notes="ODIN comments use -- through newline; multiline comments repeat --.",
    ),
    CommentSyntax(
        family_name="ooc_style",
        canonical_name="ooc",
        regex_patterns=(r"/{2}[^\r\n]*",),
        nested_delimiters=(("/*", "*/"),),
        shared_regex_examples=(
            CommentExample(
                'println("hello") // note\nprintln("done")',
                "// note",
                "ooc slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                '/* outer /* note */ outer */\nprintln("hello")',
                "/* outer /* note */ outer */",
                "ooc recursively nested block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://ooc-lang.org/docs/lang/",
        implementation_source=(
            "https://github.com/ooc-lang/rock/blob/master/source/rock/frontend/"
            "NagaQueen.c"
        ),
        confidence="verified",
        notes="The rock parser recursively recognizes /* ... */ comments.",
    ),
    CommentSyntax(
        family_name="opa_style",
        canonical_name="opa",
        regex_patterns=(r"/{2}[^\r\n]*",),
        nested_delimiters=(("/*", "*/"),),
        shared_regex_examples=(
            CommentExample(
                "x = 1 // note\ny = x + 1",
                "// note",
                "Opa slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "/* outer /* note */ outer */\nx = 1",
                "/* outer /* note */ outer */",
                "Opa nested star comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        documentation_source="unresolved",
        implementation_source=(
            "https://github.com/MLstate/opalang/blob/master/compiler/opalang/"
            "classic_syntax/opa_lexer.trx"
        ),
        confidence="verified",
        notes="The classic syntax lexer handles slash lines and nested star blocks.",
    ),
    CommentSyntax(
        family_name="openedge_abl_style",
        canonical_name="openedge_abl",
        regex_patterns=(r"(?<!\S)/{2}[^\r\n]*",),
        nested_delimiters=(("/*", "*/"),),
        shared_regex_examples=(
            CommentExample(
                'MESSAGE "hello". // note\nMESSAGE "done".',
                "// note",
                "OpenEdge ABL single-line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                '/* outer /* note */ outer */\nMESSAGE "hello".',
                "/* outer /* note */ outer */",
                "OpenEdge ABL nested block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://docs.progress.com/bundle/abl-reference/page/"
            "Single-line-comments.html; "
            "https://docs.progress.com/bundle/abl-reference/page/"
            "Multi-line-comments.html"
        ),
        implementation_source="unresolved",
        confidence="verified",
        notes=(
            "/* ... */ comments are supported across ABL versions checked; // "
            "single-line comments are current OpenEdge syntax introduced in 11.6."
        ),
    ),
    CommentSyntax(
        family_name="openrc_runscript_style",
        canonical_name="openrc_runscript",
        regex_patterns=(r"#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                'description="Example service"\n# note\ncommand="/usr/bin/example"',
                "# note",
                "OpenRC runscript shell-style hash comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://github.com/OpenRC/openrc/blob/master/service-script-guide.md"
        ),
        implementation_source="https://github.com/OpenRC/openrc",
        confidence="verified",
        notes="Runscripts are shell scripts executed through openrc-run.",
    ),
    CommentSyntax(
        family_name="openstep_property_list_style",
        canonical_name="openstep_property_list",
        regex_patterns=(
            r"/\*[\S\s]*?\*/",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "{\n  Name = Example; // note\n}",
                "// note",
                "OpenStep property-list slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "{\n  /* note */\n  Name = Example;\n}",
                "/* note */",
                "OpenStep property-list slash-star block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://developer.apple.com/library/archive/documentation/Cocoa/"
            "Conceptual/PropertyLists/OldStylePlists/OldStylePLists.html"
        ),
        implementation_source=(
            "https://github.com/textmate/property-list.tmbundle/blob/textmate-1.x/"
            "Syntaxes/Property%20List.tmLanguage"
        ),
        confidence="verified",
        notes="Old-style OpenStep property lists use // and /* ... */ comments.",
    ),
    CommentSyntax(
        family_name="opentype_feature_file_style",
        canonical_name="opentype_feature_file",
        regex_patterns=(r"#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "# note\nfeature liga {\n  sub f i by fi;\n} liga;",
                "# note",
                "OpenType feature-file hash comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://adobe-type-tools.github.io/afdko/"
            "OpenTypeFeatureFileSpecification.html"
        ),
        implementation_source=(
            "https://github.com/adobe-type-tools/afdko/blob/develop/docs/"
            "OpenTypeFeatureFileSpecification.md"
        ),
        confidence="verified",
        notes="The feature-file specification uses # comments through newline.",
    ),
    CommentSyntax(
        family_name="org_style",
        canonical_name="org",
        regex_patterns=(
            r"(?im)^[ \t]*#\+begin_comment\b[^\r\n]*(?:\r?\n[\S\s]*?)"
            r"^[ \t]*#\+end_comment\b[^\r\n]*",
            r"(?m)^[ \t]*#(?:[ \t][^\r\n]*|[ \t]*$)",
        ),
        shared_regex_examples=(
            CommentExample(
                "* Task\n# note\nBody text",
                "# note",
                "Org comment line whose first non-space character is #.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "#+BEGIN_COMMENT\nnote\n#+END_COMMENT\nVisible text",
                "#+BEGIN_COMMENT\nnote\n#+END_COMMENT",
                "Org comment block.",
                kind="block",
            ),
        ),
        documentation_source="https://orgmode.org/manual/Comment-Lines.html",
        implementation_source="https://git.savannah.gnu.org/cgit/emacs/org-mode.git/plain/lisp/org.el",
        confidence="verified",
        notes=(
            "The line pattern excludes #+ keyword lines. COMMENT subtrees and "
            "inline Org comment constructs are structural features outside this "
            "lexical registry entry."
        ),
    ),
    CommentSyntax(
        family_name="ox_style",
        canonical_name="ox",
        regex_patterns=(r"/{2}[^\r\n]*",),
        nested_delimiters=(("/*", "*/"),),
        shared_regex_examples=(
            CommentExample(
                "decl value = 1; // note\ndecl next = value + 1;",
                "// note",
                "Ox slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "/* outer /* note */ outer */\ndecl value = 1;",
                "/* outer /* note */ outer */",
                "Ox nested slash-star block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        documentation_source="http://fmwww.bc.edu/ec-p/obsolete/oxsyntax.htm",
        implementation_source="unresolved",
        confidence="verified",
        notes="The Ox syntax manual documents nested block comments.",
    ),
    CommentSyntax(
        family_name="oz_style",
        canonical_name="oz",
        regex_patterns=(r"%[^\r\n]*",),
        nested_delimiters=(("/*", "*/"),),
        shared_regex_examples=(
            CommentExample(
                "declare X = 1 % note\n{Browse X}",
                "% note",
                "Oz percent line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "/* outer /* note */ outer */\ndeclare X = 1",
                "/* outer /* note */ outer */",
                "Oz nested slash-star block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://mozart2.org/mozart-v1/doc-1.4.0/notation/node2.html",
        implementation_source="unresolved",
        confidence="verified",
        notes="Mozart Oz supports % line comments and nested slash-star blocks.",
    ),
    CommentSyntax(
        family_name="p4_style",
        canonical_name="p4",
        regex_patterns=(
            r"/\*[\S\s]*?\*/",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "// note\ncontrol MyIngress() { apply { } }",
                "// note",
                "P4 line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/* note */\ncontrol MyIngress() { apply { } }",
                "/* note */",
                "P4 block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        canonical_regex_examples=(
            CommentExample(
                "/** note */\ncontrol MyIngress() { apply { } }",
                "/** note */",
                "P4 documentation block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://p4.org/p4-spec/docs/P4-16-v1.2.3.html",
        implementation_source=(
            "https://github.com/p4lang/p4c/blob/main/frontends/parsers/p4/"
            "p4lexer.ll"
        ),
        confidence="verified",
        notes="P4_16 uses C-family comments and explicitly does not nest them.",
    ),
    CommentSyntax(
        family_name="pan_style",
        canonical_name="pan",
        regex_patterns=(r"#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "variable VALUE = 1; # note\nvariable NEXT = VALUE + 1;",
                "# note",
                "Pan hash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="unresolved",
        implementation_source=(
            "https://github.com/quattor/pan/blob/master/panc/src/main/jjtree/"
            "PanParser.jjt"
        ),
        confidence="verified",
        notes="The Pan JavaCC grammar defines # comments through line end.",
    ),
    CommentSyntax(
        family_name="papyrus_style",
        canonical_name="papyrus",
        regex_patterns=(
            r";/[\S\s]*?/;",
            r";[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "int value = 1 ; note\nint next = value + 1",
                "; note",
                "Papyrus semicolon line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                ";/\nnote\n/;\nint value = 1",
                ";/\nnote\n/;",
                "Papyrus slash-delimited block comment.",
                kind="block",
            ),
        ),
        documentation_source="https://ck.uesp.net/wiki/Comment_Reference",
        implementation_source=(
            "https://github.com/Gawdl3y/atom-language-papyrus/blob/master/"
            "grammars/papyrus-skyrim.cson"
        ),
        confidence="high",
        notes="Papyrus block comments stop at the first /; delimiter.",
    ),
    CommentSyntax(
        family_name="parrot_assembly_style",
        canonical_name="parrot_assembly",
        regex_patterns=(
            r"(?ms)^[ \t]*=pod\b[\s\S]*?^[ \t]*=cut\b[^\r\n]*",
            r"#[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "set I0, 1 # note\ninc I0",
                "# note",
                "Parrot Assembly hash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "=pod\nnote\n=cut\nset I0, 1",
                "=pod\nnote\n=cut",
                "Parrot Assembly ignored POD block.",
                kind="block",
            ),
        ),
        documentation_source=(
            "https://parrot.github.io/parrot-docs1/1.1.0/html/docs/book/"
            "ch09_pasm.pod.html"
        ),
        implementation_source="https://github.com/parrot/parrot/blob/master/compilers/imcc/imcc.l",
        confidence="verified",
        notes="PASM uses # line comments and ignores POD regions.",
    ),
    CommentSyntax(
        family_name="parrot_internal_representation_style",
        canonical_name="parrot_internal_representation",
        regex_patterns=(
            r"(?ms)^[ \t]*=pod\b[\s\S]*?^[ \t]*=cut\b[^\r\n]*",
            r"#[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                ".sub 'main'\n  $I0 = 1 # note\n.end",
                "# note",
                "PIR hash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "=pod\nnote\n=cut\n.sub 'main'\n.end",
                "=pod\nnote\n=cut",
                "PIR ignored POD block.",
                kind="block",
            ),
        ),
        documentation_source=(
            "https://parrot.github.io/parrot-docs1/1.1.0/html/docs/book/"
            "ch09_pasm.pod.html"
        ),
        implementation_source="https://github.com/parrot/parrot/blob/master/compilers/imcc/imcc.l",
        confidence="verified",
        notes="PIR uses the IMCC lexer, which skips hash comments and POD blocks.",
    ),
    CommentSyntax(
        family_name="pawn_style",
        canonical_name="pawn",
        regex_patterns=(
            r"/\*[\S\s]*?\*/",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "new value = 1; // note\nnew next = value + 1;",
                "// note",
                "Pawn line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "new value = 1;\n/* note */\nnew next = value + 1;",
                "/* note */",
                "Pawn non-nested block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://www.compuphase.com/pawn/pawnfeatures.htm",
        implementation_source="unresolved",
        confidence="verified",
        notes="Pawn comments use C-family delimiters and do not nest.",
    ),
    CommentSyntax(
        family_name="peg_js_style",
        canonical_name="peg_js",
        regex_patterns=(
            r"/\*[\S\s]*?\*/",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "// note\nstart = 'a'",
                "// note",
                "PEG.js grammar line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/* note */\nstart = 'a'",
                "/* note */",
                "PEG.js grammar block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://pegjs.org/documentation; https://peggyjs.org/documentation.html",
        implementation_source="https://github.com/pegjs/pegjs",
        confidence="verified",
        notes="PEG.js grammars accept JavaScript-style comments.",
    ),
    CommentSyntax(
        family_name="pep8_style",
        canonical_name="pep8",
        regex_patterns=(r";[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "LDWA 0,i ; note\nSTOP",
                "; note",
                "Pep/8 assembler semicolon comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="unresolved",
        implementation_source="https://github.com/StanWarford/pep8/blob/master/asm.cpp",
        confidence="verified",
        notes="This key refers to Pep/8 assembly, not Python PEP 8.",
    ),
    CommentSyntax(
        family_name="pic_style",
        canonical_name="pic",
        regex_patterns=(r"#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                ".PS\n# note\nbox\n.PE",
                "# note",
                "GNU pic hash line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="https://man7.org/linux/man-pages/man1/pic.1.html",
        implementation_source=(
            "https://github.com/dbarowy/groff/blob/master/src/preproc/pic/"
            "lex.cpp"
        ),
        confidence="verified",
        notes="pic uses # comments; semicolon is statement syntax.",
    ),
    CommentSyntax(
        family_name="picolisp_style",
        canonical_name="picolisp",
        regex_patterns=(r"#(?!\{)[^\r\n]*",),
        nested_delimiters=(("#{", "}#"),),
        shared_regex_examples=(
            CommentExample(
                "(setq Value 1) # note\n(setq Next 2)",
                "# note",
                "PicoLisp hash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "#{ outer #{ note }# outer }#\n(setq Value 1)",
                "#{ outer #{ note }# outer }#",
                "PicoLisp nested block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://software-lab.de/doc/ref.html",
        implementation_source="unresolved",
        confidence="verified",
        notes="PicoLisp documents nested #{ ... }# block comments.",
    ),
    CommentSyntax(
        family_name="piglatin_style",
        canonical_name="piglatin",
        regex_patterns=(
            r"/\*[\S\s]*?\*/",
            r"--[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "LOAD 'data.csv';\n-- note\nfiltered = FILTER data BY age > 18;",
                "-- note",
                "PigLatin dash line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "LOAD 'data.csv';\n/* note */\nfiltered = FILTER data BY age > 18;",
                "/* note */",
                "PigLatin non-nested block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://pig.apache.org/docs/latest/basic.html",
        implementation_source="https://github.com/apache/pig/blob/trunk/src/org/apache/pig/parser/QueryLexer.g",
        confidence="verified",
        notes="PigLatin uses SQL-style line comments and non-nested slash-star blocks.",
    ),
    CommentSyntax(
        family_name="pod_style",
        canonical_name="pod",
        regex_patterns=(
            r"(?ms)^[ \t]*=begin[ \t]+comment\b[^\r\n]*"
            r"(?:\r?\n[\s\S]*?)^[ \t]*=end[ \t]+comment\b[^\r\n]*",
            r"(?m)^[ \t]*=for[ \t]+comment\b[^\r\n]*(?:\r?\n(?!\s*$)[^\r\n]*)*",
        ),
        shared_regex_examples=(
            CommentExample(
                "=begin comment\nnote\n=end comment\n\n=head1 NAME",
                "=begin comment\nnote\n=end comment",
                "POD comment block.",
                kind="block",
            ),
            CommentExample(
                "=for comment note\n\n=head1 NAME",
                "=for comment note",
                "POD comment paragraph.",
                kind="block",
            ),
        ),
        documentation_source="https://perldoc.perl.org/perlpod",
        implementation_source="https://github.com/Perl/perl5",
        confidence="verified",
        notes="POD comments are document comment paragraphs/blocks, not Perl # source comments.",
    ),
    CommentSyntax(
        family_name="pod_6_style",
        canonical_name="pod_6",
        regex_patterns=(
            r"(?ms)^[ \t]*=begin[ \t]+comment\b[^\r\n]*"
            r"(?:\r?\n[\s\S]*?)^[ \t]*=end[ \t]+comment\b[^\r\n]*",
            r"(?m)^[ \t]*=comment\b[^\r\n]*(?:\r?\n(?!\s*$)[^\r\n]*)*",
        ),
        shared_regex_examples=(
            CommentExample(
                "=begin comment\nnote\n=end comment\n\n=head1 Example",
                "=begin comment\nnote\n=end comment",
                "Pod 6 comment block.",
                kind="block",
            ),
            CommentExample(
                "=comment note\n\n=head1 Example",
                "=comment note",
                "Pod 6 comment paragraph.",
                kind="block",
            ),
        ),
        documentation_source="https://docs.raku.org/language/pod",
        implementation_source="https://github.com/raku/roast",
        confidence="verified",
        notes="Pod 6 comment markup is document syntax, not Raku source comments.",
    ),
    CommentSyntax(
        family_name="pogoscript_style",
        canonical_name="pogoscript",
        regex_patterns=(
            r"/\*[\S\s]*?\*/",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "value = 1 // note\nnext = value + 1",
                "// note",
                "PogoScript line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/* note */\nvalue = 1",
                "/* note */",
                "PogoScript block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="unresolved",
        implementation_source=(
            "https://github.com/featurist/pogoscript/blob/master/lib/parser/"
            "grammar.js"
        ),
        confidence="verified",
        notes="PogoScript uses JavaScript-style comments; hashbang handling is excluded.",
    ),
    CommentSyntax(
        family_name="pony_style",
        canonical_name="pony",
        regex_patterns=(r"/{2}[^\r\n]*",),
        nested_delimiters=(("/*", "*/"),),
        shared_regex_examples=(
            CommentExample(
                "actor Main\n  // note\n  new create(env: Env) => None",
                "// note",
                "Pony slash line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "/* outer /* note */ outer */\nactor Main",
                "/* outer /* note */ outer */",
                "Pony nested block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://tutorial.ponylang.io/appendices/syntax.html",
        implementation_source="https://github.com/ponylang/ponyc/blob/main/src/libponyc/ast/lexer.c",
        confidence="verified",
        notes="The Pony lexer uses depth-counted nested block-comment scanning.",
    ),
    CommentSyntax(
        family_name="pov_ray_sdl_style",
        canonical_name="pov_ray_sdl",
        regex_patterns=(r"/{2}[^\r\n]*",),
        nested_delimiters=(("/*", "*/"),),
        shared_regex_examples=(
            CommentExample(
                "sphere { <0, 0, 0>, 1 } // note",
                "// note",
                "POV-Ray SDL line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "/* outer /* note */ outer */\nsphere { <0, 0, 0>, 1 }",
                "/* outer /* note */ outer */",
                "POV-Ray SDL nested block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://www.povray.org/documentation/view/3.7.1/228/",
        implementation_source=(
            "https://github.com/POV-Ray/povray/blob/master/source/parser/"
            "scanner.cpp"
        ),
        confidence="verified",
        notes=(
            "Current scanner defaults support nested blocks; compatibility mode "
            "can disable nesting for older behavior."
        ),
    ),
    CommentSyntax(
        family_name="prisma_style",
        canonical_name="prisma",
        regex_patterns=(
            r"/\*[\S\s]*?\*/",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "// note\nmodel User { id Int @id }",
                "// note",
                "Prisma reader line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/* note */\nmodel User { id Int @id }",
                "/* note */",
                "Prisma block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        canonical_regex_examples=(
            CommentExample(
                "/// note\nid Int @id",
                "/// note",
                "Prisma documentation line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/** note */\nmodel User { id Int @id }",
                "/** note */",
                "Prisma documentation block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://www.prisma.io/docs/orm/prisma-schema/overview#comments",
        implementation_source=(
            "https://github.com/prisma/prisma-engines/blob/main/psl/"
            "schema-ast/src/parser/datamodel.pest"
        ),
        confidence="verified",
        notes="Prisma also attaches /// and /** */ documentation comments to AST nodes.",
    ),
    CommentSyntax(
        family_name="propeller_spin_style",
        canonical_name="propeller_spin",
        regex_patterns=(
            r"\{\{[\S\s]*?\}\}",
            r"\{(?!\{)[\S\s]*?\}",
            r"'{1,2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "PUB Main\n  value := 1 ' note\n  next := value + 1",
                "' note",
                "Propeller Spin apostrophe line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "{ note }\nPUB Main",
                "{ note }",
                "Propeller Spin brace block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        canonical_regex_examples=(
            CommentExample(
                "'' note\nPUB Main",
                "'' note",
                "Propeller Spin documentation line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "{{ note }}\nPUB Main",
                "{{ note }}",
                "Propeller Spin documentation block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://forums.parallax.com/uploads/editor/3l/lzpix2by2k4r.pdf; "
            "https://raw.githubusercontent.com/parallaxinc/spin-docs/master/pdf/"
            "P8X32A-Web-PropellerManual-v1.2_0.pdf"
        ),
        implementation_source="unresolved",
        confidence="verified",
        notes="Spin2 ... continuation comments are excluded because they are version-specific.",
    ),
    CommentSyntax(
        family_name="qt_script_style",
        canonical_name="qt_script",
        regex_patterns=(
            r"/\*[\S\s]*?\*/",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "var value = 1; // note\nvalue;",
                "// note",
                "Qt Script ECMAScript line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "var value = 1;\n/* note */\nvalue;",
                "/* note */",
                "Qt Script ECMAScript block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://doc.qt.io/archives/qt-5.15/qtscript-index.html; "
            "https://tc39.es/ecma262/multipage/ecmascript-language-lexical-grammar.html#sec-comments"
        ),
        implementation_source="GitHub Linguist languages.yml",
        confidence="high",
        notes="Qt Script uses ECMAScript comment forms.",
    ),
    CommentSyntax(
        family_name="raml_style",
        canonical_name="raml",
        regex_patterns=(r"#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "title: Example\n# note\nversion: v1",
                "# note",
                "RAML YAML-style hash comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://github.com/raml-org/raml-spec/blob/master/versions/"
            "raml-10/raml-10.md; https://yaml.org/spec/1.2.2/#comments"
        ),
        implementation_source="GitHub Linguist languages.yml",
        confidence="high",
        notes="RAML inherits YAML hash comments.",
    ),
    CommentSyntax(
        family_name="rascal_style",
        canonical_name="rascal",
        regex_patterns=(
            r"/\*[\S\s]*?\*/",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "int value = 1; // note\nreturn value;",
                "// note",
                "Rascal line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "int value = 1;\n/* note */\nreturn value;",
                "/* note */",
                "Rascal block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://www.rascal-mpl.org/docs/Rascal/Declarations/"
            "SyntaxDefinition/"
        ),
        implementation_source=(
            "https://github.com/usethesource/rascal/blob/"
            "6b23b1a0624a94ecad422564fa5eb136e3ed2497/src/org/rascalmpl/"
            "library/lang/rascal/syntax/Rascal.rsc; GitHub Linguist languages.yml"
        ),
        confidence="high",
        notes="Rascal accepts Java/C-style comments.",
    ),
    CommentSyntax(
        family_name="realbasic_style",
        canonical_name="realbasic",
        regex_patterns=(
            r"/{2}[^\r\n]*",
            r"'[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "Var value As Integer = 1 ' note\nVar next As Integer = 2",
                "' note",
                "REALbasic/Xojo apostrophe line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "// note\nVar value As Integer = 1",
                "// note",
                "REALbasic/Xojo slash line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="https://documentation.xojo.com/api/language/commenting.html",
        implementation_source="GitHub Linguist languages.yml",
        confidence="verified",
        notes="Current Xojo docs list // and apostrophe comments.",
    ),
    CommentSyntax(
        family_name="reason_style",
        canonical_name="reason",
        regex_patterns=(
            r"/\*[\S\s]*?\*/",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "let value = 1; // note\nvalue;",
                "// note",
                "Reason line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "let value = 1;\n/* note */\nvalue;",
                "/* note */",
                "Reason block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://reasonml.github.io/docs/en/syntax-cheatsheet",
        implementation_source="GitHub Linguist languages.yml",
        confidence="verified",
        notes="Reason documentation lists // and /* */ comments.",
    ),
    CommentSyntax(
        family_name="redcode_style",
        canonical_name="redcode",
        regex_patterns=(r";[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "MOV 0, 1 ; note\nEND",
                "; note",
                "Redcode semicolon line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://corewar.co.uk/standards/icws94.htm; "
            "https://corewar.co.uk/standards/icws88.txt"
        ),
        implementation_source="GitHub Linguist languages.yml",
        confidence="verified",
        notes="Redcode standards use semicolon line comments.",
    ),
    CommentSyntax(
        family_name="redirect_rules_style",
        canonical_name="redirect_rules",
        regex_patterns=(r"(?m)^[ \t]*#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "# note\n/old-page /new-page 301",
                "# note",
                "Redirect rules hash comment line.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://docs.netlify.com/manage/routing/redirects/redirect-options/#comments; "
            "https://developers.cloudflare.com/pages/configuration/redirects/"
        ),
        implementation_source="GitHub Linguist languages.yml",
        confidence="verified",
        notes="This key maps to _redirects files, not unrelated redirect formats.",
    ),
    CommentSyntax(
        family_name="renpy_style",
        canonical_name="renpy",
        regex_patterns=(r"#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "value = 1 # note\nvalue = 2",
                "# note",
                "Ren'Py Python-style hash comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="https://www.renpy.org/doc/html/language_basics.html#comments",
        implementation_source="GitHub Linguist languages.yml",
        confidence="verified",
        notes="Ren'Py scripts follow Python-style hash comments.",
    ),
    CommentSyntax(
        family_name="renderscript_style",
        canonical_name="renderscript",
        regex_patterns=(
            r"/\*[\S\s]*?\*/",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "int value = 1; // note\nreturn value;",
                "// note",
                "RenderScript C-style line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "int value = 1;\n/* note */\nreturn value;",
                "/* note */",
                "RenderScript C-style block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://developer.android.com/guide/topics/renderscript/compute",
        implementation_source="GitHub Linguist languages.yml",
        confidence="high",
        notes="RenderScript .rs files are C99-like source files.",
    ),
    CommentSyntax(
        family_name="rescript_style",
        canonical_name="rescript",
        regex_patterns=(
            r"/\*[\S\s]*?\*/",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "let value = 1 // note\nvalue",
                "// note",
                "ReScript line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "let value = 1\n/* note */\nvalue",
                "/* note */",
                "ReScript block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://rescript-lang.org/docs/manual/latest/overview#comments",
        implementation_source=(
            "https://github.com/rescript-lang/rescript-lang.org/blob/"
            "02f7b35815c6020ed09f11e20d44a2e8ff250fba/apps/docs/markdown-pages/"
            "syntax-lookup/language_line_comment.mdx; "
            "https://github.com/rescript-lang/rescript-lang.org/blob/"
            "02f7b35815c6020ed09f11e20d44a2e8ff250fba/apps/docs/markdown-pages/"
            "syntax-lookup/language_block_comment.mdx; GitHub Linguist languages.yml"
        ),
        confidence="verified",
        notes="ReScript documentation lists // and /* */ comments.",
    ),
    CommentSyntax(
        family_name="rpc_style",
        canonical_name="rpc",
        regex_patterns=(r"/\*[\S\s]*?\*/",),
        shared_regex_examples=(
            CommentExample(
                "/* note */\nconst MAX_VALUE = 10;",
                "/* note */",
                "ONC RPC/XDR block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://datatracker.ietf.org/doc/html/rfc4506#section-6.1",
        implementation_source="GitHub Linguist languages.yml",
        confidence="verified",
        notes="This key is scoped to ONC RPC/XDR interface definitions.",
    ),
    CommentSyntax(
        family_name="rpm_spec_style",
        canonical_name="rpm_spec",
        regex_patterns=(r"(?m)^[ \t]*#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "Name: example\n# note\nVersion: 1",
                "# note",
                "RPM spec hash comment line.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="https://rpm-software-management.github.io/rpm/manual/spec.html",
        implementation_source="GitHub Linguist languages.yml",
        confidence="verified",
        notes="RPM spec comments are hash-prefixed lines.",
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
        aliases=("cson", "emberscript"),
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
        documentation_source=(
            "https://coffeescript.org/; https://github.com/bevry/cson; "
            "https://github.com/ghempton/ember-script"
        ),
        implementation_source=(
            "https://registry.npmjs.org/cson-parser/-/cson-parser-4.0.9.tgz; "
            "https://github.com/ghempton/ember-script/blob/master/src/grammar.pegjs"
        ),
        confidence="verified",
        notes=(
            "CoffeeScript, CSON, and EmberScript use # line comments and "
            "non-nested ### block comments."
        ),
    ),
    CommentSyntax(
        family_name="denizenscript_style",
        canonical_name="denizenscript",
        regex_patterns=(r"(?m)^[ \t]*#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "pay_command:\n  type: command\n  # note\n  script:\n  - narrate \"ready # text\"",
                "  # note",
                "DenizenScript full-line hash comment after indentation.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://guide.denizenscript.com/guides/troubleshooting/"
            "common-mistakes.html; https://meta.denizenscript.com/Docs/Commands/"
        ),
        implementation_source=(
            "https://github.com/DenizenScript/Denizen-Core/blob/"
            "31300d6ab58c840a3168bd15bc46caf00b5fc418/src/main/java/com/"
            "denizenscript/denizencore/scripts/ScriptHelper.java"
        ),
        confidence="verified",
        notes=(
            "Only trimmed full-line # comments are encoded. Inline # in command "
            "lines is script text and is intentionally excluded."
        ),
    ),
    CommentSyntax(
        family_name="e_style",
        canonical_name="e",
        regex_patterns=(r"#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "# note\ndef a := 3",
                "# note",
                "E line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://www.skyhunter.com/marcs/ewalnut.html; "
            "https://erights.org/elang/quick-ref.html"
        ),
        confidence="high",
        notes=(
            "Ordinary # comments are encoded. Edoc /** ... */ comments are "
            "definition-context dependent and ordinary /* ... */ was not confirmed."
        ),
    ),
    CommentSyntax(
        family_name="eagle_style",
        canonical_name="eagle",
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "int i; // note",
                "// note",
                "EAGLE ULP slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/* note */\nint i = 0;",
                "/* note */",
                "EAGLE ULP block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://help.autodesk.com/cloudhelp/ENU/Fusion-ECAD/files/"
            "ECD-ULP-COMMENT-REF.htm; https://web.mit.edu/xavid/arch/i386_rhel4/"
            "help/133.htm"
        ),
        confidence="verified",
        notes="EAGLE ULP block comments stop at the first */ and do not nest.",
    ),
    CommentSyntax(
        family_name="ebnf_style",
        canonical_name="ebnf",
        nested_delimiters=(("(*", "*)"),),
        shared_nested_examples=(
            CommentExample(
                "(* outer (* inner *) outer *)\nsyntax = syntax rule;",
                "(* outer (* inner *) outer *)",
                "ISO EBNF nested textual comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://www.cl.cam.ac.uk/~mgk25/iso-14977.pdf; "
            "https://www.cl.cam.ac.uk/~mgk25/iso-ebnf.html"
        ),
        implementation_source=(
            "https://slebok.github.io/zoo/%C2%A7wip/metasyntax/"
            "ebnf-iso-1/extracted/index.html"
        ),
        confidence="verified",
        notes="ISO/IEC 14977 EBNF uses recursive (* ... *) comments; ABNF ; is excluded.",
    ),
    CommentSyntax(
        family_name="ec_style",
        canonical_name="ec",
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "PrintLn(\"hello\"); // note",
                "// note",
                "eC slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/* note */\nclass Greeter : Window { }",
                "/* note */",
                "eC block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://github.com/ecere/ecere-sdk; "
            "https://opensource.com/article/17/9/ecere"
        ),
        implementation_source=(
            "https://github.com/ecere/eC/blob/8a633973133bb007e446bead00f30f5492d5a23b/"
            "ectp/src/lexer.l"
        ),
        confidence="cross-checked",
        notes="eC uses // and non-nested /* ... */ comments; # is preprocessor input.",
    ),
    CommentSyntax(
        family_name="edje_data_collection_style",
        canonical_name="edje_data_collection",
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "collections {\n  // note\n  group { }\n}",
                "// note",
                "Edje Data Collection slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "collections {\n  /* note */\n  group { }\n}",
                "/* note */",
                "Edje Data Collection block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://www.enlightenment.org/_legacy_embed/edje_main.html; "
            "https://github.com/Enlightenment/efl/blob/master/src/examples/edje/"
            "entry.edc"
        ),
        implementation_source=(
            "https://github.com/Enlightenment/efl/blob/"
            "12494e95d4070a32bde155e85fe815900651c9c4/src/bin/edje/"
            "edje_cc_parse.c"
        ),
        confidence="verified",
        notes=(
            "EDC uses // and non-nested /* ... */ comments outside strings. "
            "# preprocessor metadata is excluded."
        ),
    ),
    CommentSyntax(
        family_name="filebench_wml_style",
        canonical_name="filebench_wml",
        regex_patterns=(r"#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "# note\nset $dir=/tmp\nrun 60",
                "# note",
                "Filebench WML hash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://github.com/filebench/filebench; "
            "https://github-wiki-see.page/m/filebench/filebench/wiki/"
            "Workload-model-language"
        ),
        implementation_source="https://github.com/filebench/filebench/blob/master/parser_lex.l",
        confidence="verified",
        notes="Filebench WML uses # line comments and has no block-comment rule.",
    ),
    CommentSyntax(
        family_name="flux_style",
        canonical_name="flux",
        regex_patterns=(r"/{2}[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "from(bucket: \"example\")\n  // note\n  |> range(start: -1h)",
                "// note",
                "Flux slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://docs.influxdata.com/flux/v0/spec/lexical-elements/; "
            "https://docs.influxdata.com/flux/v0/spec/"
        ),
        implementation_source=(
            "https://github.com/influxdata/flux/blob/master/libflux/flux-core/"
            "src/scanner/scanner.rl"
        ),
        confidence="verified",
        notes="Flux v0 supports // line comments only; multiline comments are excluded.",
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
        family_name="gaml_style",
        canonical_name="gaml",
        regex_patterns=(
            r"/\*[\S\s]*?\*/",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "species pedestrian {\n  int speed <- 4; // movement speed\n}",
                "// movement speed",
                "GAML slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/* temporary note */\nexperiment main type: gui { }",
                "/* temporary note */",
                "GAML non-nested block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://gama-platform.org/wiki/1.9.3/Statements; "
            "https://gama-platform.org/wiki/1.9.3/GamlReference"
        ),
        implementation_source=(
            "https://github.com/gama-platform/gama/blob/main/gaml.grammar/src/"
            "gaml/grammar/Gaml.xtext"
        ),
        confidence="high",
        notes="GAML uses // line comments and non-nested /* ... */ block comments.",
    ),
    CommentSyntax(
        family_name="gcc_machine_description_style",
        canonical_name="gcc_machine_description",
        regex_patterns=(
            r"/\*[\S\s]*?\*/",
            r";[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "(define_attr \"type\" \"alu\" (const_string \"alu\")) ; note",
                "; note",
                "GCC machine-description semicolon comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/* constraint note */\n(define_attr \"type\" \"alu\")",
                "/* constraint note */",
                "GCC machine-description C-style block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://gcc.gnu.org/onlinedocs/gccint/Machine-Desc.html",
        implementation_source=(
            "https://github.com/gcc-mirror/gcc/blob/master/gcc/read-md.cc"
        ),
        confidence="high",
        notes=(
            "The reader treats semicolon line comments and C-style block "
            "comments as whitespace. Block comments are non-nested."
        ),
    ),
    CommentSyntax(
        family_name="git_revision_list_style",
        canonical_name="git_revision_list",
        regex_patterns=(r"#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa  # formatting pass",
                "# formatting pass",
                "Git revision-list trailing hash comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="https://git-scm.com/docs/git-blame",
        implementation_source="https://github.com/git/git/blob/master/oidset.c",
        confidence="high",
        notes=(
            "Git ignore-revs style files discard # and following text before "
            "trimming whitespace; no block form is supported."
        ),
    ),
    CommentSyntax(
        family_name="harbour_style",
        canonical_name="harbour",
        regex_patterns=(
            r"/\*[\S\s]*?\*/",
            r"/{2}[^\r\n]*",
            r"&&[^\r\n]*",
            r"(?m)^[ \t]*\*[^\r\n]*",
            r"(?im)^[ \t]*note\b[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "QOut( \"Ok!\" )  && inline legacy comment",
                "&& inline legacy comment",
                "Harbour inline legacy line comment.",
                kind="line",
                inline_compatible=True,
            ),
            CommentExample(
                "PROCEDURE Main()\n   // file header comment\nRETURN",
                "// file header comment",
                "Harbour slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "* legacy full-line comment\nPROCEDURE Main()",
                "* legacy full-line comment",
                "Harbour first-token star line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "NOTE old-style full-line comment\nPROCEDURE Main()",
                "NOTE old-style full-line comment",
                "Harbour first-token NOTE line comment.",
                kind="line",
            ),
            CommentExample(
                "PROCEDURE Main()\n   /* multiple\n      note lines */\nRETURN",
                "/* multiple\n      note lines */",
                "Harbour non-nested block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        implementation_source=(
            "https://github.com/harbour/core/blob/master/src/pp/ppcore.c; "
            "https://github.com/harbour/core/blob/master/include/hbpp.h"
        ),
        confidence="high",
        notes=(
            "Harbour supports //, &&, first-token *, first-token NOTE, and "
            "non-nested /* ... */ comments. Semicolon is a command separator."
        ),
    ),
    CommentSyntax(
        family_name="holyc_style",
        canonical_name="holyc",
        regex_patterns=(r"/{2}[^\r\n]*",),
        nested_delimiters=(("/*", "*/"),),
        shared_regex_examples=(
            CommentExample(
                "U8 *message = \"hello\"; // greeting",
                "// greeting",
                "HolyC slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "/* outer note\n   /* nested disabled code */\n   still inside outer */",
                "/* outer note\n   /* nested disabled code */\n   still inside outer */",
                "HolyC nested block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        implementation_source=(
            "https://github.com/cia-foundation/TempleOS/blob/archive/Compiler/Lex.HC; "
            "https://github.com/Zeal-Operating-System/ZealOS/blob/master/src/Compiler/Lex.ZC"
        ),
        confidence="high",
        notes="HolyC supports // comments and recursively nested /* ... */ blocks.",
    ),
    CommentSyntax(
        family_name="jasmin_style",
        canonical_name="jasmin",
        regex_patterns=(r";[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "; default constructor follows\n.method public <init>()V",
                "; default constructor follows",
                "Jasmin semicolon line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="https://jasmin.sourceforge.net/guide.html",
        implementation_source="https://github.com/davidar/jasmin",
        confidence="verified",
        notes="Jasmin assembly uses semicolon line comments and no block form.",
    ),
    CommentSyntax(
        family_name="javascript_erb_style",
        canonical_name="javascript_erb",
        regex_patterns=(
            r"<%#[\S\s]*?%>",
            r"/\*[\S\s]*?\*/",
            r"\A#![^\r\n]*",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "const user = \"Ada\"; // rendered by ERB",
                "// rendered by ERB",
                "JavaScript+ERB JavaScript line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "#!/usr/bin/env node\nconst user = \"Ada\";",
                "#!/usr/bin/env node",
                "JavaScript+ERB script-start hashbang comment.",
                kind="line",
            ),
            CommentExample(
                "<%# server-side note: do not emit debug data %>\nconsole.log(user);",
                "<%# server-side note: do not emit debug data %>",
                "JavaScript+ERB server-side ERB comment tag.",
                kind="block",
                inline_compatible=True,
            ),
            CommentExample(
                "const total = 1 + 2;\n/* client-side note */",
                "/* client-side note */",
                "JavaScript+ERB JavaScript block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://tc39.es/ecma262/#sec-comments; "
            "https://docs.ruby-lang.org/en/3.4/ERB.html"
        ),
        implementation_source=(
            "https://github.com/tc39/ecma262; https://github.com/ruby/erb"
        ),
        confidence="verified",
        notes=(
            "Layered template syntax: JavaScript comments, script-start "
            "hashbangs, and ERB <%# ... %> comments are all recognized."
        ),
    ),
    CommentSyntax(
        family_name="jest_snapshot_style",
        canonical_name="jest_snapshot",
        regex_patterns=(r"/{2}[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "// Jest Snapshot v1, https://goo.gl/fbAQLP\n\nexports[`button renders 1`] = `<button>Save</button>`;",
                "// Jest Snapshot v1, https://goo.gl/fbAQLP",
                "Jest generated snapshot header comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="https://jestjs.io/docs/snapshot-testing",
        implementation_source="https://github.com/jestjs/jest/tree/main/packages/jest-snapshot",
        confidence="high",
        notes=(
            "Only generated // snapshot metadata is modeled; block comments "
            "inside serialized snapshot text are intentionally excluded."
        ),
    ),
    CommentSyntax(
        family_name="jison_style",
        canonical_name="jison",
        regex_patterns=(
            r"/\*[\S\s]*?\*/",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "%start expressions\n// parse a sequence of expressions",
                "// parse a sequence of expressions",
                "Jison grammar line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/* operator note */\n%left '+' '-'",
                "/* operator note */",
                "Jison non-nested block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://gerhobbelt.github.io/jison/docs/",
        implementation_source="https://github.com/zaach/jison; https://github.com/zaach/jison-lex",
        confidence="high",
        notes="Jison grammar files use JavaScript-style non-nested comments.",
    ),
    CommentSyntax(
        family_name="jolie_style",
        canonical_name="jolie",
        regex_patterns=(
            r"/\*[\S\s]*?\*/",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "main {\n  // receive a request\n}",
                "// receive a request",
                "Jolie slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/* shared service note */\ninterface PingInterface { }",
                "/* shared service note */",
                "Jolie non-nested block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://docs.jolie-lang.org/",
        implementation_source="https://github.com/jolie/jolie",
        confidence="high",
        notes="Jolie uses Java/C-style line and non-nested block comments.",
    ),
    CommentSyntax(
        family_name="kaitai_struct_style",
        canonical_name="kaitai_struct",
        regex_patterns=(r"#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "meta:\n  id: png\n  endian: be # multi-byte fields are big-endian",
                "# multi-byte fields are big-endian",
                "Kaitai Struct YAML hash comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://doc.kaitai.io/user_guide.html; "
            "https://yaml.org/spec/1.2.2/#61-indentation-spaces"
        ),
        implementation_source="https://github.com/kaitai-io/kaitai_struct_compiler",
        confidence="verified",
        notes="Kaitai .ksy schemas inherit YAML # comments and no block form.",
    ),
    CommentSyntax(
        family_name="kakounescript_style",
        canonical_name="kakounescript",
        regex_patterns=(r"#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "# load project options\ndeclare-option str project_root %sh{pwd}",
                "# load project options",
                "KakouneScript hash line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://github.com/mawww/kakoune/blob/master/doc/pages/"
            "command-parsing.asciidoc"
        ),
        implementation_source="https://github.com/mawww/kakoune",
        confidence="high",
        notes="Kakoune command files use # line comments outside quoted arguments.",
    ),
    CommentSyntax(
        family_name="kicad_legacy_layout_style",
        canonical_name="kicad_legacy_layout",
        regex_patterns=(r"#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "PCBNEW-BOARD Version 2 date 2024-01-01\n# Created by KiCad",
                "# Created by KiCad",
                "KiCad legacy board hash comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://dev-docs.kicad.org/en/file-formats/legacy-pcb/"
        ),
        implementation_source="https://gitlab.com/kicad/code/kicad",
        confidence="high",
        notes="KiCad legacy layout files use # line comments; ; was not confirmed.",
    ),
    CommentSyntax(
        family_name="kit_style",
        canonical_name="kit",
        regex_patterns=(r"#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "# normal comment\n## Documentation for the next definition",
                "# normal comment",
                "Kit hash line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "## Documentation for the next definition\nlet answer = 42",
                "## Documentation for the next definition",
                "Kit doc-comment line form.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="https://kit-lang.org/docs/2026.6.9/index.html",
        implementation_source="https://github.com/kitlang/kit",
        confidence="high",
        notes="Current Kit uses # comments, with ## as a documentation-comment subset.",
    ),
    CommentSyntax(
        family_name="krl_style",
        canonical_name="krl",
        regex_patterns=(r";[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "PTP HOME ; move to start position",
                "; move to start position",
                "KRL semicolon line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://support.industry.siemens.com/cs/attachments/109477421/"
            "KUKA_KRL_Reference_en.pdf"
        ),
        implementation_source="https://github.com/tree-sitter-grammars/tree-sitter-krl",
        confidence="high",
        notes="KRL comments begin with ; and continue to the end of the physical line.",
    ),
    CommentSyntax(
        family_name="kvlang_style",
        canonical_name="kvlang",
        regex_patterns=(r"(?m)^[ \t]*#(?!:)[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "# This label is shown on the home screen\nLabel:",
                "# This label is shown on the home screen",
                "Kivy language full-line hash comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="https://kivy.org/doc/stable/guide/lang.html",
        implementation_source="https://github.com/kivy/kivy/blob/master/kivy/lang/parser.py",
        confidence="verified",
        notes="kvlang strips # comment lines only when # is the first non-space character.",
    ),
    CommentSyntax(
        family_name="lark_style",
        canonical_name="lark",
        regex_patterns=(
            r"/{2}[^\r\n]*",
            r"#[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "start: item+\n// comment supported by baseline Lark grammar",
                "// comment supported by baseline Lark grammar",
                "Lark slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "# comment supported in Lark 1.1.6+\nitem: WORD",
                "# comment supported in Lark 1.1.6+",
                "Lark 1.1.6 hash line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://lark-parser.readthedocs.io/en/latest/grammar.html; "
            "https://github.com/lark-parser/lark/releases/tag/1.1.6"
        ),
        implementation_source="https://github.com/lark-parser/lark",
        confidence="verified",
        notes="Lark supports // comments and, since 1.1.6, # comments; no block form.",
    ),
    CommentSyntax(
        family_name="lex_style",
        canonical_name="lex",
        regex_patterns=(r"/\*[\S\s]*?\*/",),
        shared_regex_examples=(
            CommentExample(
                "%{\n#include <stdio.h>\n%}\n/* scanner rules for identifiers */\n%%",
                "/* scanner rules for identifiers */",
                "Lex/flex input block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://www.gnu.org/software/flex/manual/html_node/Comments-in-the-Input.html"
        ),
        implementation_source="https://github.com/westes/flex",
        confidence="verified",
        notes="Lex/flex input files support non-nested C-style block comments only.",
    ),
    CommentSyntax(
        family_name="linker_script_style",
        canonical_name="linker_script",
        regex_patterns=(r"/\*[\S\s]*?\*/",),
        shared_regex_examples=(
            CommentExample(
                "/* place text first */\nSECTIONS { .text : { *(.text) } }",
                "/* place text first */",
                "GNU ld linker-script block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://sourceware.org/binutils/docs/ld/Script-Format.html",
        implementation_source="https://sourceware.org/git/?p=binutils-gdb.git",
        confidence="verified",
        notes="GNU ld scripts use C-style block comments as whitespace; no line form.",
    ),
    CommentSyntax(
        family_name="linux_kernel_module_style",
        canonical_name="linux_kernel_module",
        regex_patterns=(
            r"/\*[\S\s]*?\*/",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "static int demo_init(void) {\n\t// short local note\n\treturn 0;\n}",
                "// short local note",
                "Linux kernel module C99 line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/* Module initialization note. */\nmodule_init(demo_init);",
                "/* Module initialization note. */",
                "Linux kernel module C block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://docs.kernel.org/process/coding-style.html; "
            "https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf"
        ),
        implementation_source="GCC/Clang C preprocessors used for kernel builds",
        confidence="verified",
        notes="Kernel modules are C sources; // and non-nested /* ... */ are accepted.",
    ),
    CommentSyntax(
        family_name="literate_agda_style",
        canonical_name="literate_agda",
        regex_patterns=(r"--[^\r\n]*",),
        nested_delimiters=(("{-", "-}"),),
        source_region_patterns=(
            r"(?s)\\begin\{code\}[\S\s]*?\\end\{code\}",
            r"(?ms)^```(?:[ \t]*agda)?[^\r\n]*\r?\n[\S\s]*?^```[ \t]*$",
        ),
        shared_regex_examples=(
            CommentExample(
                "\\begin{code}\nmodule Demo where\n-- visible only to Agda readers\n\\end{code}",
                "-- visible only to Agda readers",
                "Literate Agda code-block line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "\\begin{code}\n{- outer {- inner -} outer -}\nid : Set -> Set\n\\end{code}",
                "{- outer {- inner -} outer -}",
                "Literate Agda nested block comment inside code.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://agda.readthedocs.io/en/latest/language/lexical-structure.html; "
            "https://agda.readthedocs.io/en/latest/tools/literate-programming.html"
        ),
        implementation_source="https://github.com/agda/agda",
        confidence="verified",
        notes="Literate prose is not a delimiter; Agda code comments keep Agda syntax.",
    ),
    CommentSyntax(
        family_name="literate_coffeescript_style",
        canonical_name="literate_coffeescript",
        regex_patterns=(
            r"###[\S\s]*?###",
            r"#[^\r\n]*",
        ),
        source_region_patterns=(
            r"(?m)^(?:    |\t)[^\r\n]*(?:\r?\n|$)",
            r"(?ms)^~~~[^\r\n]*\r?\n[\S\s]*?^~~~[ \t]*$",
        ),
        shared_regex_examples=(
            CommentExample(
                "    square = (x) -> x * x\n    # code comment",
                "# code comment",
                "Literate CoffeeScript code line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "    ###\n    block note in code\n    ###\n    answer = 42",
                "###\n    block note in code\n    ###",
                "Literate CoffeeScript block comment inside code.",
                kind="block",
            ),
        ),
        documentation_source=(
            "https://coffeescript.org/#comments; https://coffeescript.org/#literate"
        ),
        implementation_source="https://github.com/jashkenas/coffeescript",
        confidence="verified",
        notes=(
            "Literate CoffeeScript prose is not a lexical comment; code uses "
            "CoffeeScript # and ### ... ### comments."
        ),
    ),
    CommentSyntax(
        family_name="literate_haskell_style",
        canonical_name="literate_haskell",
        regex_patterns=(r"--[^\r\n]*",),
        nested_delimiters=(("{-", "-}"),),
        source_region_patterns=(
            r"(?m)^>[^\r\n]*(?:\r?\n|$)",
            r"(?s)\\begin\{code\}[\S\s]*?\\end\{code\}",
        ),
        shared_regex_examples=(
            CommentExample(
                "> main = do\n>   -- print a greeting\n>   putStrLn \"hello\"",
                "-- print a greeting",
                "Literate Haskell bird-track line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "\\begin{code}\nmain = do\n  {- outer {- inner -} outer -}\n\\end{code}",
                "{- outer {- inner -} outer -}",
                "Literate Haskell nested block comment inside code.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://www.haskell.org/onlinereport/haskell2010/haskellch2.html; "
            "https://downloads.haskell.org/ghc/latest/docs/users_guide/exts/"
            "literate_haskell.html"
        ),
        implementation_source="https://gitlab.haskell.org/ghc/ghc",
        confidence="verified",
        notes="Literate source selects code regions; comments inside code use Haskell syntax.",
    ),
    CommentSyntax(
        family_name="livescript_style",
        canonical_name="livescript",
        regex_patterns=(
            r"/\*[\S\s]*?\*/",
            r"#[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "# compute a total\ntotal = 1 + 2",
                "# compute a total",
                "LiveScript hash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/* this note is preserved\n   in generated JavaScript */\ntotal = 1 + 2",
                "/* this note is preserved\n   in generated JavaScript */",
                "LiveScript non-nested block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://livescript.net/#literals-comments",
        implementation_source="https://github.com/gkz/LiveScript",
        confidence="verified",
        notes="LiveScript uses # line comments and /* ... */ multiline comments.",
    ),
    CommentSyntax(
        family_name="logos_style",
        canonical_name="logos",
        regex_patterns=(
            r"/\*[\S\s]*?\*/",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "%hook SpringBoard\n// called when SpringBoard finishes launching",
                "// called when SpringBoard finishes launching",
                "Logos Objective-C-style line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/* hook note for this tweak group */\n%group Enabled",
                "/* hook note for this tweak group */",
                "Logos non-nested block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://theos.dev/docs/logos-syntax",
        implementation_source="https://github.com/theos/logos",
        confidence="high",
        notes="Logos embeds Objective-C/C-like code; % directives are not comments.",
    ),
    CommentSyntax(
        family_name="logtalk_style",
        canonical_name="logtalk",
        regex_patterns=(
            r"/\*[\S\s]*?\*/",
            r"%[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                ":- object(counter).\n  % public predicate\n:- end_object.",
                "% public predicate",
                "Logtalk percent line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/* example note used in tests */\n:- object(example).",
                "/* example note used in tests */",
                "Logtalk non-nested block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://logtalk.org/manuals/refman/syntax.html",
        implementation_source="https://github.com/LogtalkDotOrg/logtalk3",
        confidence="verified",
        notes="Logtalk follows Prolog-style % line and non-nested /* ... */ comments.",
    ),
    CommentSyntax(
        family_name="lookml_style",
        canonical_name="lookml",
        regex_patterns=(r"#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "connection: order_database\ninclude: \"*.view\" # include all the views",
                "# include all the views",
                "LookML trailing hash comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://cloud.google.com/looker/docs/lookml-terms-and-concepts; "
            "https://cloud.google.com/looker/docs/reference/param-model-include"
        ),
        implementation_source="proprietary Looker parser; public Google Cloud examples",
        confidence="verified",
        notes="LookML uses # line comments; no block comment form was confirmed.",
    ),
    CommentSyntax(
        family_name="lsl_style",
        canonical_name="lsl",
        regex_patterns=(
            r"/\*[\S\s]*?\*/",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "state_entry() {\n    // say hello when rezzed\n}",
                "// say hello when rezzed",
                "LSL slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/* listen handler note disabled during setup */\ndefault { }",
                "/* listen handler note disabled during setup */",
                "LSL non-nested block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://wiki.secondlife.com/wiki/LSL_Portal",
        implementation_source="https://github.com/buildersbrewery/lsl-parser",
        confidence="high",
        notes="LSL uses C-style // line and non-nested /* ... */ block comments.",
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
        family_name="graph_modeling_language_style",
        canonical_name="graph_modeling_language",
        regex_patterns=(r"#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "graph [\n  # note\n  node [ id 1 ]\n]",
                "# note",
                "NetworkX GML hash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="docs/comment_research/chunk_3_g_i_report.md",
        implementation_source=(
            "docs/comment_research/confirmation_reports/"
            "chunk_3_g_i_confirmation.md"
        ),
        confidence="verified",
        notes=(
            "Confirmed against NetworkX GML parsing. The GML comment key is "
            "metadata, not a lexical comment delimiter."
        ),
    ),
    CommentSyntax(
        family_name="mask_style",
        canonical_name="mask",
        regex_patterns=(
            r"/\*[\S\s]*?\*/",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "define foo {\n  // note\n  @title > 'Foo'\n}",
                "// note",
                "MaskJS slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "define foo {\n  /* note */\n  @title > 'Foo'\n}",
                "/* note */",
                "MaskJS non-nested block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="docs/comment_research/chunk_4_j_m_report.md",
        implementation_source=(
            "docs/comment_research/confirmation_reports/"
            "chunk_4_j_m_confirmation.md"
        ),
        confidence="verified",
        notes="MaskJS accepts // and non-nested /* ... */ template comments.",
    ),
    CommentSyntax(
        family_name="selinux_policy_style",
        canonical_name="selinux_policy",
        regex_patterns=(r"#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "class CLASS1 { PERM1 } # note\nclass CLASS2 { PERM2 }",
                "# note",
                "SELinux policy hash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="docs/comment_research/chunk_6_q_s_report.md",
        implementation_source=(
            "docs/comment_research/confirmation_reports/"
            "chunk_6_q_s_confirmation.md"
        ),
        confidence="verified",
        notes="Confirmed with checkpolicy and checkmodule; block comments are unsupported.",
    ),
    CommentSyntax(
        family_name="srecode_template_style",
        canonical_name="srecode_template",
        regex_patterns=(r";;[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "set mode \"srecode-template-mode\" ;; note\nset priority 10",
                ";; note",
                "GNU Emacs SRecode template semicolon line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="docs/comment_research/chunk_6_q_s_report.md",
        implementation_source=(
            "docs/comment_research/confirmation_reports/"
            "chunk_6_q_s_confirmation.md"
        ),
        confidence="verified",
        notes=(
            "srecode-template-mode sets comment-start to ;;. Template comment "
            "macros are not implemented as lexical comments here."
        ),
    ),
    CommentSyntax(
        family_name="txl_style",
        canonical_name="txl",
        regex_patterns=(r"%[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "% note\ndefine program % trailing note\n  [expression]\nend define",
                "% note",
                "TXL percent line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        canonical_regex_examples=(
            CommentExample(
                "define program % trailing note\n  [expression]\nend define",
                "% trailing note",
                "TXL trailing percent line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="docs/comment_research/chunk_7_t_z_report.md",
        implementation_source=(
            "docs/comment_research/confirmation_reports/"
            "chunk_7_t_z_confirmation.md"
        ),
        confidence="verified",
        notes="FreeTXL confirms percent comments to end of line; block comments are unsupported.",
    ),
    CommentSyntax(
        family_name="unix_assembly_gas_x86_style",
        canonical_name="unix_assembly",
        regex_patterns=(
            r"/\*[\S\s]*?\*/",
            r"#[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                ".text\n# note\nquoted:",
                "# note",
                "x86-64 GNU as hash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                ".text\n/* note */\nquoted:",
                "/* note */",
                "GNU as non-nested block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="docs/comment_research/chunk_7_t_z_report.md",
        implementation_source=(
            "docs/comment_research/confirmation_reports/"
            "chunk_7_t_z_confirmation.md"
        ),
        confidence="verified",
        notes=(
            "Confirmed for x86-64 GNU as. Unix assembly line-comment markers "
            "are target-specific outside that scope."
        ),
    ),
    CommentSyntax(
        family_name="valve_data_format_style",
        canonical_name="valve_data_format",
        regex_patterns=(r"/{2}[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                '"root"\n{\n    // note\n    "key" "value"\n}',
                "// note",
                "Valve KeyValues/VDF slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="docs/comment_research/chunk_7_t_z_report.md",
        implementation_source=(
            "docs/comment_research/confirmation_reports/"
            "chunk_7_t_z_confirmation.md"
        ),
        confidence="verified",
        notes="ValvePython/vdf confirms // comments; /* ... */ is parsed as data.",
    ),
    CommentSyntax(
        family_name="x_bit_map_style",
        canonical_name="x_bit_map",
        regex_patterns=(r"/\*[\S\s]*?\*/",),
        shared_regex_examples=(
            CommentExample(
                "/* note */\n#define dot_width 16\n#define dot_height 16",
                "/* note */",
                "Portable C89 XBM block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="docs/comment_research/chunk_7_t_z_report.md",
        implementation_source=(
            "docs/comment_research/confirmation_reports/"
            "chunk_7_t_z_confirmation.md"
        ),
        confidence="verified",
        notes="XBM is C source; only portable C89 /* ... */ comments are seeded.",
    ),
    CommentSyntax(
        family_name="x_pix_map_style",
        canonical_name="x_pix_map",
        regex_patterns=(r"/\*[\S\s]*?\*/",),
        shared_regex_examples=(
            CommentExample(
                "/* note */\nstatic char * plaid[] = {",
                "/* note */",
                "XPM3 C-wrapper block comment.",
                kind="block",
                inline_compatible=True,
            ),
            CommentExample(
                "/* note */\nstatic char * plaid[] = {",
                "/* note */",
                "XPM3 additional C block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="docs/comment_research/chunk_7_t_z_report.md",
        implementation_source=(
            "docs/comment_research/confirmation_reports/"
            "chunk_7_t_z_confirmation.md"
        ),
        confidence="verified",
        notes="XPM3/C-style files use C block comments; // is carrier-dialect dependent.",
    ),
    CommentSyntax(
        family_name="xbase_harbour_style",
        canonical_name="xbase",
        regex_patterns=(
            r"/\*[\S\s]*?\*/",
            r"/{2}[^\r\n]*",
            r"&&[^\r\n]*",
            r"(?im)^[ \t]*(?:\*[^\r\n]*|note\*?(?=\s|$)[^\r\n]*)",
        ),
        shared_regex_examples=(
            CommentExample(
                '* note\n? "Goodbye!"',
                "* note",
                "Harbour/xBase leading star line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                'NOTE note\n? "Goodbye!"',
                "NOTE note",
                "Harbour/xBase NOTE statement comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                '? "Goodbye!" && note',
                "&& note",
                "Harbour/xBase trailing ampersand line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/* note */\nRETURN",
                "/* note */",
                "Harbour/xBase non-nested block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        canonical_regex_examples=(
            CommentExample(
                'NOTE* note\n? "Goodbye!"',
                "NOTE* note",
                "Harbour/xBase NOTE* statement comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                '? "Goodbye!" // note',
                "// note",
                "Harbour/xBase slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="docs/comment_research/chunk_7_t_z_report.md",
        implementation_source=(
            "docs/comment_research/confirmation_reports/"
            "chunk_7_t_z_confirmation.md"
        ),
        confidence="verified",
        notes=(
            "Confirmed against Harbour/Clipper scope. The broad xBase family "
            "may need dialect splitting if future corpora require stricter behavior."
        ),
    ),
    CommentSyntax(
        family_name="zil_string_comment_style",
        canonical_name="zil",
        regex_patterns=(r";\"(?:\\.|[^\"\\\r\n])*\"",),
        shared_regex_examples=(
            CommentExample(
                ';"note"\n<ROUTINE GO () <PRINTI "Hello">>',
                ';"note"',
                "ZIL semicolon string comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="docs/comment_research/chunk_7_t_z_report.md",
        implementation_source=(
            "docs/comment_research/confirmation_reports/"
            "chunk_7_t_z_confirmation.md"
        ),
        confidence="verified",
        notes=(
            "Conservatively implements only ;\"...\" string comments. General "
            "semicolon expression comments require a ZIL-aware parser."
        ),
    ),
    CommentSyntax(
        family_name="zimpl_style",
        canonical_name="zimpl",
        regex_patterns=(r"#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "# note\nmaximize profit: 25 * XB + 30 * XC; # trailing note",
                "# note",
                "Zimpl hash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        canonical_regex_examples=(
            CommentExample(
                "maximize profit: 25 * XB + 30 * XC; # trailing note",
                "# trailing note",
                "Zimpl trailing hash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="docs/comment_research/chunk_7_t_z_report.md",
        implementation_source=(
            "docs/comment_research/confirmation_reports/"
            "chunk_7_t_z_confirmation.md"
        ),
        confidence="verified",
        notes="Zimpl supports # comments to end of line; block comments are unsupported.",
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
    CommentSyntax(
        family_name="m_style",
        canonical_name="m",
        regex_patterns=(r";[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                'HELLO ; entry point\n WRITE "hello",!\n QUIT',
                "; entry point",
                "M/MUMPS semicolon line comment after a label.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://mumps.sourceforge.net/docs.html ; "
            "https://docs.yottadb.com/ProgrammersGuide/langfeat.html"
        ),
        implementation_source="https://gitlab.com/YottaDB/DB/YDB",
        confidence="verified",
        notes="M source uses semicolon comments to the end of the physical line.",
    ),
    CommentSyntax(
        family_name="maxscript_style",
        canonical_name="maxscript",
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r"--[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "-- create a box\nb = box length:10 width:10 height:10",
                "-- create a box",
                "MAXScript dash line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/* block note */\nb = sphere radius:5",
                "/* block note */",
                "MAXScript non-nested slash block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://help.autodesk.com/cloudhelp/2022/ENU/"
            "MAXDEV-Overview/files/overview/"
            "MAXDEV_Overview_overview_maxscript_html.html"
        ),
        implementation_source=(
            "Autodesk MAXScript interpreter; "
            "https://github.com/tree-sitter-grammars/tree-sitter-maxscript"
        ),
        confidence="verified",
        notes="MAXScript supports -- line comments and non-nested /* ... */ blocks.",
    ),
    CommentSyntax(
        family_name="mcfunction_style",
        canonical_name="mcfunction",
        regex_patterns=(r"(?m)^[ \t]*#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "# load setup commands\nsay ready",
                "# load setup commands",
                "Minecraft function comment-only line.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="https://minecraft.wiki/w/Function_(Java_Edition)",
        implementation_source="https://github.com/SpyglassMC/Spyglass",
        confidence="high",
        notes=(
            "Minecraft function comments must have # as the first non-whitespace "
            "character; trailing command comments are intentionally excluded."
        ),
    ),
    CommentSyntax(
        family_name="mercury_style",
        canonical_name="mercury",
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r"%[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                ":- module hello.\n% exported predicate\n:- interface.",
                "% exported predicate",
                "Mercury percent line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/* block note */\n:- implementation.",
                "/* block note */",
                "Mercury non-nested slash block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://www.mercurylang.org/information/doc-release/"
            "mercury_ref/Lexical-syntax.html"
        ),
        implementation_source="https://github.com/Mercury-Language/mercury",
        confidence="verified",
        notes="Mercury uses % line comments and non-nested /* ... */ blocks.",
    ),
    CommentSyntax(
        family_name="metal_style",
        canonical_name="metal",
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "kernel void fill() {\n  // write value\n}",
                "// write value",
                "Metal slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/* block note */\nfloat twice(float x) { return x * 2.0; }",
                "/* block note */",
                "Metal non-nested slash block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://developer.apple.com/metal/"
            "Metal-Shading-Language-Specification.pdf"
        ),
        implementation_source="https://github.com/tree-sitter-grammars/tree-sitter-metal",
        confidence="verified",
        notes="Metal source follows C++ lexical comments with non-nesting blocks.",
    ),
    CommentSyntax(
        family_name="mirah_style",
        canonical_name="mirah",
        regex_patterns=(
            r"(?ms)^[ \t]*=begin\b[\s\S]*?^[ \t]*=end\b[^\r\n]*",
            r"#[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "class Greeter\n  # print a greeting\nend",
                "# print a greeting",
                "Mirah hash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "=begin\nblock note\n=end\nclass Greeter\nend",
                "=begin\nblock note\n=end",
                "Mirah line-oriented begin/end block comment.",
                kind="block",
            ),
        ),
        documentation_source="https://github.com/mirah/mirah/wiki",
        implementation_source="https://github.com/mirah/mirah",
        confidence="high",
        notes="Mirah follows Ruby-style # line comments and =begin/=end blocks.",
    ),
    CommentSyntax(
        family_name="mirc_script_style",
        canonical_name="mirc_script",
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r";[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "alias hello {\n  ; show a message\n  echo -a hello\n}",
                "; show a message",
                "mIRC script semicolon line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/* block note\nalias oldhello { echo -a old }\n*/",
                "/* block note\nalias oldhello { echo -a old }\n*/",
                "mIRC script non-nested slash block comment.",
                kind="block",
            ),
        ),
        documentation_source="https://www.mirc.com/help/html/index.html",
        implementation_source="proprietary mIRC interpreter; no public lexer source found",
        confidence="high",
        notes="mIRC script supports semicolon line comments and /* ... */ blocks.",
    ),
    CommentSyntax(
        family_name="mlir_style",
        canonical_name="mlir",
        regex_patterns=(r"/{2}[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "// A function that returns its argument.\nfunc.func @id()",
                "// A function that returns its argument.",
                "MLIR slash line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="https://mlir.llvm.org/docs/LangRef/",
        implementation_source=(
            "https://github.com/llvm/llvm-project/tree/main/mlir/lib/AsmParser"
        ),
        confidence="verified",
        notes="MLIR supports // comments only; # has other grammar roles.",
    ),
    CommentSyntax(
        family_name="modula_2_style",
        canonical_name="modula_2",
        nested_delimiters=(("(*", "*)"),),
        shared_nested_examples=(
            CommentExample(
                "MODULE Demo;\n(* outer (* inner *) outer *)\nBEGIN\nEND Demo.",
                "(* outer (* inner *) outer *)",
                "Modula-2 nested star block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://www.modula2.org/reference/lexical.html ; "
            "https://gcc.gnu.org/onlinedocs/gm2/Comments.html"
        ),
        implementation_source="https://gcc.gnu.org/git/?p=gcc.git;a=tree;f=gcc/m2",
        confidence="verified",
        notes="Standard Modula-2 comments use nested (* ... *) blocks only.",
    ),
    CommentSyntax(
        family_name="modula_3_style",
        canonical_name="modula_3",
        nested_delimiters=(("(*", "*)"),),
        shared_nested_examples=(
            CommentExample(
                "MODULE Demo;\n(* outer (* inner *) outer *)\nBEGIN\nEND Demo.",
                "(* outer (* inner *) outer *)",
                "Modula-3 nested star block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://www.cs.purdue.edu/homes/hosking/m3/reference/lexical.html",
        implementation_source="https://github.com/modula3/cm3",
        confidence="verified",
        notes="Modula-3 comments use nested (* ... *) blocks only.",
    ),
    CommentSyntax(
        family_name="module_management_system_style",
        canonical_name="module_management_system",
        regex_patterns=(r"![^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "! Build the image from object files\nprogram.exe : main.obj",
                "! Build the image from object files",
                "OpenVMS MMS exclamation line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://docs.vmssoftware.com/"
            "vsi-decset-for-openvms-guide-to-the-module-management-system/"
        ),
        implementation_source="proprietary OpenVMS MMS; no public lexer source found",
        confidence="high",
        notes="Module Management System description files use ! to end of line.",
    ),
    CommentSyntax(
        family_name="monkey_style",
        canonical_name="monkey",
        regex_patterns=(
            r"(?ims)^[ \t]*#rem\b[\S\s]*?^[ \t]*#end\b[^\r\n]*",
            r"'[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                'Function Main()\n    \' show a greeting\n    Print "hello"\nEnd',
                "' show a greeting",
                "Monkey apostrophe line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "#Rem\nTemporary notes for this module.\n#End\nFunction Main()\nEnd",
                "#Rem\nTemporary notes for this module.\n#End",
                "Monkey #Rem/#End block comment.",
                kind="block",
            ),
        ),
        documentation_source=(
            "https://monkeycoder.co.nz/Community/posts.php?topic=3441 ; "
            "https://github.com/blitz-research/monkey"
        ),
        implementation_source="https://github.com/blitz-research/monkey",
        confidence="high",
        notes="Monkey uses apostrophe line comments and non-nested #Rem/#End blocks.",
    ),
    CommentSyntax(
        family_name="monkey_c_style",
        canonical_name="monkey_c",
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "function initialize() {\n    // configure the view\n}",
                "// configure the view",
                "Monkey C slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/* block note */\nfunction compute() {\n}",
                "/* block note */",
                "Monkey C non-nested slash block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://developer.garmin.com/connect-iq/core-topics/monkey-c/",
        implementation_source="Garmin Connect IQ compiler; no public lexer source found",
        confidence="verified",
        notes="Monkey C uses C/Java-style line and non-nested block comments.",
    ),
    CommentSyntax(
        family_name="moonscript_style",
        canonical_name="moonscript",
        regex_patterns=(
            r"--\[(=*)\[[\s\S]*?\]\1\]",
            r"--(?!\[[=]*\[)[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "-- compute a total\ntotal = 1 + 2",
                "-- compute a total",
                "MoonScript dash line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "--[[\nblock note\n]]\nprint total",
                "--[[\nblock note\n]]",
                "MoonScript Lua-style long block comment.",
                kind="block",
            ),
        ),
        documentation_source="https://moonscript.org/reference/#comments",
        implementation_source="https://github.com/leafo/moonscript",
        confidence="verified",
        notes="MoonScript uses -- line comments and Lua long-bracket block comments.",
    ),
    CommentSyntax(
        family_name="motorola_68k_assembly_style",
        canonical_name="motorola_68k_assembly",
        regex_patterns=(
            r";[^\r\n]*",
            r"(?m)^\*[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "* reset vector table\n        move.w  #1,d0",
                "* reset vector table",
                "Motorola 68K column-one star comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "        move.w  #1,d0      ; load flag\n        rts",
                "; load flag",
                "Motorola 68K semicolon trailing comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="https://www.nxp.com/docs/en/reference-manual/M68000PRM.pdf",
        implementation_source=(
            "https://sourceware.org/git/?p=binutils-gdb.git ; "
            "https://github.com/vasm-assembler/vasm"
        ),
        confidence="high",
        notes="The * form is intentionally column-sensitive; ; runs to newline.",
    ),
    CommentSyntax(
        family_name="mql4_style",
        canonical_name="mql4",
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "//--- Single-line comment\nint total = 0;",
                "//--- Single-line comment",
                "MQL4 slash line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/* block note */\nint total = 1;",
                "/* block note */",
                "MQL4 non-nested slash block comment.",
                kind="block",
            ),
        ),
        documentation_source="https://docs.mql4.com/basis/syntax/commentaries",
        implementation_source="MetaQuotes MQL4 compiler; no public lexer source found",
        confidence="verified",
        notes="Official MQL4 docs state multi-line comments cannot nest.",
    ),
    CommentSyntax(
        family_name="mql5_style",
        canonical_name="mql5",
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "//--- Single-line comment\nint total = 0;",
                "//--- Single-line comment",
                "MQL5 slash line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/* block note */\nint total = 1;",
                "/* block note */",
                "MQL5 non-nested slash block comment.",
                kind="block",
            ),
        ),
        documentation_source="https://www.mql5.com/en/docs/basis/syntax/commentaries",
        implementation_source="MetaQuotes MQL5 compiler; no public lexer source found",
        confidence="verified",
        notes="MQL5 mirrors the documented MQL4 comment behavior.",
    ),
    CommentSyntax(
        family_name="mtml_style",
        canonical_name="mtml",
        regex_patterns=(
            r"(?is)<mt:ignore\b[^>]*>[\S\s]*?</mt:ignore>",
            r"<!--[\S\s]*?-->",
        ),
        shared_regex_examples=(
            CommentExample(
                "<!-- block note in template output -->\n<mt:Entries />",
                "<!-- block note in template output -->",
                "MTML HTML comment block.",
                kind="block",
                inline_compatible=True,
            ),
            CommentExample(
                "<mt:Ignore>\nTemplate-only block note.\n</mt:Ignore>\n<mt:Entries />",
                "<mt:Ignore>\nTemplate-only block note.\n</mt:Ignore>",
                "Movable Type Ignore block.",
                kind="block",
            ),
        ),
        documentation_source=(
            "https://www.movabletype.org/documentation/appendices/tags/ ; "
            "https://www.movabletype.org/documentation/appendices/tags/ignore.html"
        ),
        implementation_source="https://github.com/movabletype/movabletype",
        confidence="high",
        notes="MTML supports HTML comments and <mt:Ignore> template blocks.",
    ),
    CommentSyntax(
        family_name="mupad_style",
        canonical_name="mupad",
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "// compute a symbolic result\nf := x -> x^2:",
                "// compute a symbolic result",
                "MuPAD slash line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/* block note */\ng := x -> x + 1:",
                "/* block note */",
                "MuPAD non-nested slash block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://www.mathworks.com/help/symbolic/mupad_programming.html",
        implementation_source="proprietary MuPAD engine; no public lexer source found",
        confidence="high",
        notes="MuPAD supports // line comments and non-nested /* ... */ blocks.",
    ),
    CommentSyntax(
        family_name="nanorc_style",
        canonical_name="nanorc",
        regex_patterns=(r"(?m)^[ \t]*#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "set tabsize 4\n# keep this aligned\nset softwrap",
                "# keep this aligned",
                "nanorc hash-prefixed config comment line.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="https://www.nano-editor.org/dist/latest/nanorc.5.html",
        implementation_source="https://github.com/madnight/nano/blob/master/src/rcfile.c",
        confidence="verified",
        notes="nanorc comments require # as the first non-blank line character.",
    ),
    CommentSyntax(
        family_name="nasal_style",
        canonical_name="nasal",
        regex_patterns=(r"#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "var throttle = 0.5; # clamp before use\nvar next = throttle + 0.1;",
                "# clamp before use",
                "Nasal hash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="https://wiki.flightgear.org/Nasal_scripting_language",
        implementation_source="https://github.com/andyross/nasal/blob/master/src/lex.c",
        confidence="verified",
        notes="The Nasal lexer skips from # to the line end.",
    ),
    CommentSyntax(
        family_name="nasl_style",
        canonical_name="nasl",
        regex_patterns=(r"#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                'display("probe"); # audit note\nexit(0);',
                "# audit note",
                "NASL hash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="unresolved",
        implementation_source=(
            "https://github.com/greenbone/openvas-scanner/blob/main/"
            "nasl/nasl_grammar.y"
        ),
        confidence="verified",
        notes="The NASL grammar enters a comment state after # and exits on newline.",
    ),
    CommentSyntax(
        family_name="ncl_style",
        canonical_name="ncl",
        regex_patterns=(
            r"/;[\S\s]*?;/",
            r";[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "x = 1\n; calibration note\ny = x + 1",
                "; calibration note",
                "NCL semicolon line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "x = 1\n/;\n  calibration note\n;/\ny = x + 1",
                "/;\n  calibration note\n;/",
                "NCL 6.4.0+ slash-semicolon block comment.",
                kind="block",
            ),
        ),
        documentation_source=(
            "https://www.ncl.ucar.edu/Document/Manuals/Ref_Manual/"
            "NclStatements.shtml#Comments"
        ),
        implementation_source="unresolved",
        confidence="verified",
        notes="NCL 6.4.0 and later add /; ... ;/ blocks; ; line comments are older.",
    ),
    CommentSyntax(
        family_name="nearley_style",
        canonical_name="nearley",
        regex_patterns=(r"#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "main -> word\n# parser note\nword -> [a-z]:+",
                "# parser note",
                "nearley hash line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="https://nearley.js.org/docs/grammar",
        implementation_source=(
            "https://github.com/kach/nearley/blob/master/"
            "lib/nearley-language-bootstrapped.ne"
        ),
        confidence="verified",
        notes="nearley tokenizes # through the rest of the line as a comment.",
    ),
    CommentSyntax(
        family_name="nemerle_style",
        canonical_name="nemerle",
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "def value = 1; // increment later\ndef next = value + 1;",
                "// increment later",
                "Nemerle slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "def value = 1;\n/* block note */\ndef next = value + 1;",
                "/* block note */",
                "Nemerle non-nested slash block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://github.com/rsdn/nemerle/wiki",
        implementation_source="https://github.com/rsdn/nemerle/blob/master/ncc/parsing/Lexer.n",
        confidence="verified",
        notes="Nemerle documentation comments are variants of // and /* ... */.",
    ),
    CommentSyntax(
        family_name="nesc_style",
        canonical_name="nesc",
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "int value = 1;\n// calibration\nint next = value + 1;",
                "// calibration",
                "nesC slash line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "int value = 1;\n/* block note */\nint next = value + 1;",
                "/* block note */",
                "nesC non-nested slash block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://nescc.sourceforge.net/papers/nesc-ref.pdf",
        implementation_source="https://github.com/tinyos/nesc/blob/master/src/c-lex.c",
        confidence="verified",
        notes="nesC inherits C-family lexical comments; doc forms are delimiter variants.",
    ),
    CommentSyntax(
        family_name="netlinx_style",
        canonical_name="netlinx",
        regex_patterns=(
            r"\(\*[\S\s]*?\*\)",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "DEFINE_DEVICE\ndvTP = 10001:1:0 // main touch panel",
                "// main touch panel",
                "NetLinx slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "(*\n  block note\n*)\nDEFINE_START",
                "(*\n  block note\n*)",
                "NetLinx non-nested paren-star block comment.",
                kind="block",
            ),
        ),
        documentation_source=(
            "https://dextra.com.mx/img/files/PRODUCTOS/AMX/NX-2200/"
            "NetLinx.LanguageReferenceGuide.pdf"
        ),
        implementation_source="unresolved",
        confidence="verified",
        notes="NetLinx supports // lines and non-nested (* ... *) blocks.",
    ),
    CommentSyntax(
        family_name="newlisp_style",
        canonical_name="newlisp",
        regex_patterns=(
            r";[^\r\n]*",
            r"#[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "(set 'value 1) ; increment later\n(+ value 1)",
                "; increment later",
                "newLISP semicolon line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "# same file can use hash comments\n(+ value 1)",
                "# same file can use hash comments",
                "newLISP hash line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://web.mit.edu/newlisp_v10.7.1/share/doc/newlisp/"
            "newlisp_manual.html"
        ),
        implementation_source="unresolved",
        confidence="verified",
        notes="newLISP documents both ; and # as line-comment leaders.",
    ),
    CommentSyntax(
        family_name="nit_style",
        canonical_name="nit",
        regex_patterns=(r"#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "var value = 1 # increment later\nvar next = value + 1",
                "# increment later",
                "Nit hash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="https://nitlanguage.org/doc/nitc/grammar.html",
        implementation_source=(
            "https://github.com/nitlang/nit/blob/master/src/parser/"
            "nit.sablecc3xx"
        ),
        confidence="verified",
        notes="Nit grammar defines # comments through the line end.",
    ),
    CommentSyntax(
        family_name="nwscript_style",
        canonical_name="nwscript",
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "void main() {\n  // initialise game state\n  int x = 1;\n}",
                "// initialise game state",
                "NWScript slash line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "void main() {\n  /* block note */\n  int x = 1;\n}",
                "/* block note */",
                "NWScript non-nested slash block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://nwnlexicon.com/index.php?title=NWScript",
        implementation_source=(
            "https://github.com/nwneetools/nwnsc/blob/master/"
            "_NscLib/NscContext.cpp"
        ),
        confidence="verified",
        notes="NWScript consumes // through line end and /* through the first */.",
    ),
    CommentSyntax(
        family_name="s_z_hash_line_style",
        canonical_name="sage",
        aliases=(
            "singularity",
            "smali",
            "ssh_config",
            "star",
            "unity3d_asset",
        ),
        regex_patterns=(r"#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "value = 1 # note\nvalue = 2",
                "# note",
                "Hash line comment for S-Z registry candidates.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "docs/comment_research/chunk_6_q_s_report.md; "
            "docs/comment_research/chunk_7_t_z_report.md"
        ),
        implementation_source="GitHub Linguist languages.yml",
        confidence="cross-checked",
        notes=(
            "Shared hash-line entry for Sage, Singularity definition files, "
            "Smali, OpenSSH config, STAR/CIF data, and UnityYAML assets."
        ),
    ),
    CommentSyntax(
        family_name="sed_style",
        canonical_name="sed",
        regex_patterns=(r"(?m)(?!\A#n[^\r\n]*)^[ \t]*#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "s/foo/bar/\n# note\np",
                "# note",
                "GNU sed script comment command.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://www.gnu.org/software/sed/manual/html_node/"
            "Common-Commands.html"
        ),
        implementation_source="GitHub Linguist languages.yml",
        confidence="verified",
        notes=(
            "Sed comments are line-oriented. A first line beginning with #n "
            "has special printing behavior and is excluded."
        ),
    ),
    CommentSyntax(
        family_name="saltstack_style",
        canonical_name="saltstack",
        regex_patterns=(
            r"\{#[\S\s]*?#\}",
            r"#[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "pkg.installed:\n  - name: vim\n# note",
                "# note",
                "Salt SLS YAML hash comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "pkg.installed:\n  - name: vim\n{# note #}",
                "{# note #}",
                "Salt SLS Jinja template comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://docs.saltproject.io/en/latest/topics/tutorials/"
            "starting_states.html; "
            "https://jinja.palletsprojects.com/en/stable/templates/#comments; "
            "https://yaml.org/spec/1.2.2/#comments"
        ),
        implementation_source="GitHub Linguist languages.yml",
        confidence="cross-checked",
        notes="Salt state files use the union of YAML # and Jinja {# ... #} comments.",
    ),
    CommentSyntax(
        family_name="s_z_c_style",
        canonical_name="shaderlab",
        aliases=(
            "slice",
            "smpl",
            "solidity",
            "soong",
            "sourcepawn",
            "sqf",
            "squirrel",
            "stan",
            "stylus",
            "sugarss",
            "supercollider",
            "swig",
            "type_language",
            "uno",
            "whiley",
            "witcher_script",
            "wollok",
            "yang",
            "zephir",
        ),
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "int value = 1;\n// note\nreturn value;",
                "// note",
                "C-style slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "int value = 1;\n/* note */\nreturn value;",
                "/* note */",
                "C-style block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "docs/comment_research/chunk_6_q_s_report.md; "
            "docs/comment_research/chunk_7_t_z_report.md"
        ),
        implementation_source=(
            "GitHub Linguist languages.yml and per-language references in "
            "the current S-Z reports"
        ),
        confidence="cross-checked",
        notes=(
            "Shared non-nested C/C++-style comment forms for S-Z candidates. "
            "Dialect-specific doc-comment variants are covered by the same "
            "block and line delimiters."
        ),
    ),
    CommentSyntax(
        family_name="smt_style",
        canonical_name="smt",
        regex_patterns=(r";[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "(assert true) ; note\n(check-sat)",
                "; note",
                "SMT-LIB semicolon line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="https://smt-lib.org/language.shtml",
        implementation_source="GitHub Linguist languages.yml",
        confidence="verified",
        notes="SMT-LIB 2.x comments begin with semicolon and run to newline.",
    ),
    CommentSyntax(
        family_name="sqlpl_style",
        canonical_name="sqlpl",
        regex_patterns=(r"--[^\r\n]*",),
        nested_delimiters=(("/*", "*/"),),
        shared_regex_examples=(
            CommentExample(
                "SELECT 1;\n-- note\nSELECT 2;",
                "-- note",
                "Db2 SQL PL simple comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "SELECT 1;\n/* outer /* inner */ outer */\nSELECT 2;",
                "/* outer /* inner */ outer */",
                "Db2 SQL PL nested bracketed comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://www.ibm.com/docs/en/db2-for-zos/12.0.0?"
            "topic=statements-sql-comments; "
            "https://www.ibm.com/docs/en/db2/11.5.x?topic=statements-comments"
        ),
        implementation_source="GitHub Linguist languages.yml",
        confidence="verified",
        notes="Db2 SQL PL supports -- comments and nested /* ... */ comments.",
    ),
    CommentSyntax(
        family_name="s_z_nested_star_style",
        canonical_name="standard_ml",
        aliases=("urweb",),
        nested_delimiters=(("(*", "*)"),),
        shared_nested_examples=(
            CommentExample(
                "let value = 1\n(* outer (* inner *) outer *)\nvalue",
                "(* outer (* inner *) outer *)",
                "Nested star block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://smlfamily.github.io/sml97-defn.pdf; "
            "https://enn.github.io/urweb-doc/manual.html"
        ),
        implementation_source="GitHub Linguist languages.yml",
        confidence="cross-checked",
        notes="Standard ML and Ur/Web use nested (* ... *) comments and no line comments.",
    ),
    CommentSyntax(
        family_name="stringtemplate_style",
        canonical_name="stringtemplate",
        regex_patterns=(r"<![\S\s]*?!>",),
        shared_regex_examples=(
            CommentExample(
                "Hello, <name>\n<! note !>",
                "<! note !>",
                "StringTemplate default-delimiter comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://www.stringtemplate.org/; "
            "https://github.com/antlr/stringtemplate4/blob/master/doc/cheatsheet.md"
        ),
        implementation_source=(
            "https://github.com/antlr/stringtemplate4/blob/master/src/org/"
            "stringtemplate/v4/compiler/STLexer.java"
        ),
        confidence="cross-checked",
        notes="ST4 comments use <! ... !> with the default delimiter pair.",
    ),
    CommentSyntax(
        family_name="terra_style",
        canonical_name="terra",
        regex_patterns=(
            r"--\[(=*)\[[\s\S]*?\]\1\]",
            r"--(?!\[[=]*\[)[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "local x = 1\n-- note\nlocal y = 2",
                "-- note",
                "Terra Lua-style line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "local x = 1\n--[=[ note ]=]\nlocal y = 2",
                "--[=[ note ]=]",
                "Terra depth-qualified Lua long comment.",
                kind="block",
                inline_compatible=True,
            ),
            CommentExample(
                "local x = 1\n--[[ note ]]\nlocal y = 2",
                "--[[ note ]]",
                "Terra plain Lua long comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://terralang.org/; "
            "https://www.lua.org/manual/5.4/manual.html#3.1"
        ),
        implementation_source="docs/comment_research/chunk_7_t_z_report.md",
        confidence="cross-checked",
        notes=(
            "Terra source is Lua-hosted; Lua line comments and long comments "
            "apply. Long-bracket equals depth is delimiter matching, not true "
            "same-depth nesting."
        ),
    ),
    CommentSyntax(
        family_name="texinfo_style",
        canonical_name="texinfo",
        regex_patterns=(
            r"(?ms)^[ \t]*@ignore\b[^\r\n]*(?:\r\n|\r|\n)[\S\s]*?"
            r"^[ \t]*@end[ \t]+ignore\b[^\r\n]*",
            r"(?m)^[ \t]*@(?:c|comment)\b[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "@node Top\n@c note\n@top Example",
                "@c note",
                "Texinfo @c source-line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "@node Top\n@comment note\n@top Example",
                "@comment note",
                "Texinfo @comment source-line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "@ignore\nnote\n@end ignore\n@node Top",
                "@ignore\nnote\n@end ignore",
                "Texinfo ignored region.",
                kind="block",
            ),
        ),
        documentation_source=(
            "https://www.gnu.org/software/texinfo/manual/texinfo/html_node/"
            "Comments.html; "
            "https://ftp.gnu.org/old-gnu/Manuals/texinfo-4.2/html_node/"
            "Comments.html"
        ),
        implementation_source="docs/comment_research/chunk_7_t_z_report.md",
        confidence="cross-checked",
        notes="@ignore and @end ignore are line-oriented and do not nest.",
    ),
    CommentSyntax(
        family_name="vcl_style",
        canonical_name="vcl",
        aliases=("zenscript",),
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r"/{2}[^\r\n]*",
            r"#[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "sub vcl_recv {\n  // note\n}",
                "// note",
                "Slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "sub vcl_recv {\n  # note\n}",
                "# note",
                "Hash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "sub vcl_recv {\n  /* note */\n}",
                "/* note */",
                "Slash block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://varnish-cache.readthedocs.io/reference/vcl.html; "
            "https://docs.blamejared.com/1.20.1/en/tutorial/"
            "IntroductionToScripting/"
        ),
        implementation_source="docs/comment_research/chunk_7_t_z_report.md",
        confidence="cross-checked",
        notes="Varnish VCL and ZenScript both support //, #, and /* ... */ comments.",
    ),
    CommentSyntax(
        family_name="volt_style",
        canonical_name="volt",
        regex_patterns=(r"\{#[\S\s]*?#\}",),
        shared_regex_examples=(
            CommentExample(
                "{# note #}\n{{ name }}",
                "{# note #}",
                "Volt template comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://docs.phalcon.io/5.11/volt/; "
            "https://docs.phalcon.io/3.4/volt/"
        ),
        implementation_source="docs/comment_research/chunk_7_t_z_report.md",
        confidence="cross-checked",
        notes="Volt comments are non-nested {# ... #} template comments.",
    ),
    CommentSyntax(
        family_name="webvtt_style",
        canonical_name="webvtt",
        regex_patterns=(
            r"(?:\A|(?<=\n\n)|(?<=\r\n\r\n))NOTE(?:[ \t][^\r\n]*)?(?:\r?\n(?!\r?\n)[^\r\n]*)*(?:\r?\n)?",
        ),
        shared_regex_examples=(
            CommentExample(
                "WEBVTT\n\nNOTE note\n\n00:00.000 --> 00:01.000\nHello",
                "NOTE note\n",
                "WebVTT NOTE block terminated by a blank line.",
                kind="block",
            ),
        ),
        documentation_source="https://www.w3.org/TR/webvtt1/",
        implementation_source="docs/comment_research/chunk_7_t_z_report.md",
        confidence="cross-checked",
        notes="WebVTT comments are NOTE blocks that terminate at the first blank line.",
    ),
    CommentSyntax(
        family_name="win32_message_file_style",
        canonical_name="win32_message_file",
        regex_patterns=(r"(?m)^[ \t]*;[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "; note\nMessageId=1",
                "; note",
                "Win32 Message Compiler semicolon comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://learn.microsoft.com/en-us/windows/win32/wes/"
            "message-compiler--mc-exe-; "
            "https://learn.microsoft.com/en-us/windows/win32/eventlog/"
            "message-files"
        ),
        implementation_source=(
            "https://github.com/MicrosoftDocs/win32/blob/docs/desktop-src/"
            "EventLog/sample-message-text-file.md"
        ),
        confidence="cross-checked",
        notes="Message text file comments are semicolon-prefixed lines.",
    ),
    CommentSyntax(
        family_name="world_of_warcraft_addon_data_style",
        canonical_name="world_of_warcraft_addon_data",
        regex_patterns=(r"(?m)^#(?!#)[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "## Interface: 110200\n# note\nMyAddon.lua",
                "# note",
                "World of Warcraft TOC comment line.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="https://warcraft.wiki.gg/wiki/TOC_format",
        implementation_source="https://addonstudio.org/wiki/WoW:TOC_format",
        confidence="cross-checked",
        notes=(
            "Only column-zero single-# TOC comment lines are matched; ## "
            "metadata tags and indented # file paths are not comments."
        ),
    ),
    CommentSyntax(
        family_name="wren_style",
        canonical_name="wren",
        regex_patterns=(r"/{2}[^\r\n]*",),
        nested_delimiters=(("/*", "*/"),),
        shared_regex_examples=(
            CommentExample(
                "class Example {}\n// note",
                "// note",
                "Wren slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "class Example {}\n/* outer /* inner */ outer */",
                "/* outer /* inner */ outer */",
                "Wren nested block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://wren.io/syntax.html",
        implementation_source=(
            "https://raw.githubusercontent.com/wren-lang/wren/main/src/vm/"
            "wren_compiler.c"
        ),
        confidence="cross-checked",
        notes="Wren supports // comments and nested /* ... */ comments.",
    ),
    CommentSyntax(
        family_name="xojo_style",
        canonical_name="xojo",
        regex_patterns=(
            r"/{2}[^\r\n]*",
            r"'[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "Dim x As Integer\n// note",
                "// note",
                "Xojo slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "Dim x As Integer\n' note",
                "' note",
                "Xojo apostrophe line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="https://documentation.xojo.com/api/language/commenting.html",
        implementation_source="docs/comment_research/chunk_7_t_z_report.md",
        confidence="cross-checked",
        notes="Current Xojo docs list // and apostrophe comments; Rem is not seeded.",
    ),
    CommentSyntax(
        family_name="xpages_style",
        canonical_name="xpages",
        regex_patterns=(r"<!--[\S\s]*?-->",),
        shared_regex_examples=(
            CommentExample(
                "<xp:view>\n  <!-- note -->\n</xp:view>",
                "<!-- note -->",
                "XPages XML source comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://www.ibm.com/docs/en/domino-designer/8.5.3?topic="
            "overview-understanding-xpages; https://www.w3.org/TR/xml/"
        ),
        implementation_source="docs/comment_research/chunk_7_t_z_report.md",
        confidence="cross-checked",
        notes="XPages source is XML; embedded script comments are excluded.",
    ),
    CommentSyntax(
        family_name="yacc_style",
        canonical_name="yacc",
        regex_patterns=(r"\/\*[\S\s]*?\*\/",),
        shared_regex_examples=(
            CommentExample(
                "%token NUMBER\n/* note */\n%%",
                "/* note */",
                "Portable POSIX yacc block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://pubs.opengroup.org/onlinepubs/9699919799/utilities/"
            "yacc.html; https://www.gnu.org/software/bison/manual/html_node/"
            "Comments.html"
        ),
        implementation_source="docs/comment_research/chunk_7_t_z_report.md",
        confidence="cross-checked",
        notes="Only portable /* ... */ comments are seeded; GNU Bison // is dialect-specific.",
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
