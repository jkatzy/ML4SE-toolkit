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
        aliases=("2_dimensional_array",),
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
        aliases=("asp", "asp_net"),
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
            r"(?<!-)#(?!-)[^\r\n]*",
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
        family_name="classic_asp_style",
        canonical_name="classic_asp",
        regex_patterns=(
            r"<!--[\S\s]*?-->",
            r"(?im)<%[ \t]*(?:'|rem\b)(?:(?!%>)[^\r\n])*(?:%>)?",
        ),
        shared_regex_examples=(
            CommentExample(
                "<!-- note -->\n<% Response.Write Now() %>",
                "<!-- note -->",
                "Classic ASP HTML comment.",
                kind="block",
                inline_compatible=True,
            ),
            CommentExample(
                "<% ' note %>\n<%= Now() %>",
                "<% ' note %>",
                "Classic ASP VBScript apostrophe comment in a server tag.",
                kind="line",
            ),
            CommentExample(
                "<% Rem note %>\n<%= Now() %>",
                "<% Rem note %>",
                "Classic ASP VBScript REM comment in a server tag.",
                kind="line",
            ),
        ),
        documentation_source=(
            "https://learn.microsoft.com/en-us/dotnet/visual-basic/"
            "language-reference/statements/rem-statement"
        ),
        confidence="cross-checked",
        notes=(
            "Classic ASP defaults to VBScript comments. The regex handles full "
            "server-side comment tags and markup comments, without trying to "
            "parse arbitrary mixed ASP block state."
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
        family_name="c_style",
        canonical_name="java",
        aliases=(
            "c",
            "c++",
            "c#",
            "c_sharp",
            "csharp",
            "javascript",
            "jsx",
            "typescript",
            "objective-c",
            "objective_cpp",
            "objective_c_plus_plus",
            "go",
            "kotlin",
            "vue",
            "scala",
            "dart",
            "hack",
            "less",
            "groovy",
            "genie",
            "processing",
            "apex",
            "cuda",
            "scilab",
            "antlr",
            "swift",
            "php",
            "four_d",
            "4d",
            "actionscript",
            "ags_script",
            "aidl",
            "al",
            "angelscript",
            "arduino",
            "aspectj",
            "asymptote",
            "avro_idl",
            "ballerina",
            "bison",
            "chuck",
            "cycript",
            "dataweave",
            "edje_data_collection",
            "eq",
            "fantom",
            "faust",
            "filterscript",
            "gaml",
            "glsl",
            "gradle",
            "haxe",
            "hlsl",
            "idl",
            "jsonc",
            "json_with_comments",
            "imagej_macro",
            "jest_snapshot",
            "json5",
            "jison",
            "jison_lex",
            "krl",
            "lasso",
            "lex",
            "linker_script",
            "logos",
            "loomscript",
            "lsl",
            "mask",
            "metal",
            "minid",
            "modelica",
            "monkey_c",
            "mql",
            "mql4",
            "mql5",
            "mupad",
            "nemerle",
            "nextflow",
            "objective_j",
            "odin",
            "opencl",
            "openstep_property_list",
            "openscad",
            "opa",
            "ox",
            "pawn",
            "pov_ray_sdl",
            "pony",
            "protocol_buffer",
            "peg_js",
            "pegjs",
            "prisma",
            "qml",
            "renderscript",
            "rescript",
            "sass",
            "scss",
            "solidity",
            "soong",
            "sourcepawn",
            "sqf",
            "squirrel",
            "stan",
            "stylus",
            "sugarss",
            "swig",
            "systemverilog",
            "tsx",
            "type_language",
            "upc",
            "unified_parallel_c",
            "unrealscript",
            "vala",
            "verilog",
            "webidl",
            "whiley",
            "x10",
            "xc",
            "xs",
            "xtend",
            "yacc",
            "yang",
            "yara",
            "yul",
            "dtrace",
            "ecl",
            "ec",
            "game_maker_language",
            "gosu",
            "cap_cds",
            "abap_cds",
            "codeql",
            "gsc",
            "hyphy",
            "holyc",
            "nesc",
            "jolie",
            "nwscript",
            "ooc",
            "p4",
            "pike",
            "qt_script",
            "quake",
            "rascal",
            "rpc",
            "rpgle",
            "shaderlab",
            "slice",
            "smpl",
            "uno",
            "volt",
            "witcher_script",
            "wollok",
            "x_bit_map",
            "x_bitmap",
            "x_pix_map",
            "x_pixmap",
            "zenscript",
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
        family_name="cue_style",
        canonical_name="cue",
        regex_patterns=(r"/{2}[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "value: 1 // note\nother: 2",
                "// note",
                "CUE line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="https://cuelang.org/docs/reference/spec/",
        implementation_source="https://github.com/cue-lang/cue",
        confidence="verified",
        notes=(
            "CUE v0.16.1 accepts // line comments and rejects C-style "
            "/* ... */ block comments."
        ),
    ),
    CommentSyntax(
        family_name="csound_style",
        canonical_name="csound",
        aliases=("csound_document", "csound_score"),
        regex_patterns=(
            r"/\*[\S\s]*?\*/",
            r"(?:;|//)[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "instr 1\n; note\nendin",
                "; note",
                "Csound semicolon line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "instr 1\n// note\nendin",
                "// note",
                "Csound slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "instr 1\n/* note */\nendin",
                "/* note */",
                "Csound block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://csound.com/docs/manual/",
        implementation_source=(
            "https://github.com/pygments/pygments/blob/2.20.0/"
            "pygments/lexers/csound.py"
        ),
        confidence="cross-checked",
        notes=(
            "The Csound lexer accepts semicolon and // line comments plus "
            "non-nested /* ... */ comments across orchestra, document, and score files."
        ),
    ),
    CommentSyntax(
        family_name="cweb_style",
        canonical_name="cweb",
        regex_patterns=(
            r"@q[^\r\n]*?@>",
            r"/\*[\S\s]*?\*/",
            r"//[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "@q reader note @>\n@c",
                "@q reader note @>",
                "CWEB ignored control-text comment.",
                kind="line",
                inline_compatible=True,
            ),
            CommentExample(
                "@c\nint x; /* note */",
                "/* note */",
                "CWEB C fragment block comment.",
                kind="block",
                inline_compatible=True,
            ),
            CommentExample(
                "@c\nint x; // note",
                "// note",
                "CWEB C++ fragment line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://ctan.math.illinois.edu/info/knuth/cwebman.pdf"
        ),
        confidence="verified",
        notes=(
            "CWEB control text after @q up to @> is ignored by CTANGLE/CWEAVE. "
            "Program fragments can also contain C or C++ comments."
        ),
    ),
    CommentSyntax(
        family_name="openqasm_style",
        canonical_name="openqasm",
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "OPENQASM 3.0;\n// note\nqubit q;",
                "// note",
                "OpenQASM line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "OPENQASM 3.0;\n/* note */\nqubit q;",
                "/* note */",
                "OpenQASM block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://openqasm.com/language/comments.html",
        implementation_source="https://github.com/openqasm/openqasm",
        confidence="verified",
        notes=(
            "OpenQASM 3 supports // line comments and non-nested /* ... */ "
            "block comments."
        ),
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
            "bro",
            "cap_n_proto",
            "capn_proto",
            "codeowners",
            "conll_u",
            "curl_config",
            "cython",
            "cucumber",
            "debian_package_control_file",
            "desktop",
            "dircolors",
            "e",
            "easybuild",
            "denizenscript",
            "earthly",
            "elvish",
            "fish",
            "filebench_wml",
            "fluent",
            "gap",
            "gas",
            "gdb",
            "gdscript",
            "gentoo_ebuild",
            "gentoo_eclass",
            "gherkin",
            "git_attributes",
            "git_revision_list",
            "gettext_catalog",
            "glyph",
            "gn",
            "gnuplot",
            "haproxy",
            "ignore_list",
            "jq",
            "janet",
            "kaitai_struct",
            "kakoune_script",
            "kakounescript",
            "kvlang",
            "lookml",
            "makefile",
            "meson",
            "mcfunction",
            "mirah",
            "mini_yaml",
            "miniyaml",
            "nanorc",
            "nasal",
            "nasl",
            "nearley",
            "nginx",
            "ninja",
            "nit",
            "nu",
            "openrc_runscript",
            "open_policy_agent",
            "opentype_feature_file",
            "org",
            "parrot",
            "parrot_assembly",
            "parrot_internal_representation",
            "pic",
            "picolisp",
            "protocol_buffer_text_format",
            "puppet",
            "qmake",
            "raml",
            "readline_config",
            "routeros_script",
            "rpm_spec",
            "robotframework",
            "robots_txt",
            "sage",
            "saltstack",
            "shell",
            "shellcheck_config",
            "shellsession",
            "singularity",
            "smali",
            "ssh_config",
            "sparql",
            "sed",
            "selinux_policy",
            "talon",
            "tcl",
            "tcsh",
            "toml",
            "turtle",
            "vyper",
            "wavefront_material",
            "wavefront_object",
            "hxml",
            "common_workflow_language",
            "fancy",
            "kicad_layout",
            "kicad_legacy_layout",
            "kicad_schematic",
            "pan",
            "procfile",
            "proguard",
            "limbo",
            "neon",
            "textmate_properties",
            "unix_assembly",
            "vim_snippet",
            "wdl",
            "wget_config",
            "xonsh",
            "xcompose",
            "yaml",
            "yasnippet",
            "zeek",
            "zimpl",
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
            "q_sharp",
            "go_module",
            "onec_enterprise",
            "1c_enterprise",
            "cairo",
            "gleam",
            "mint",
            "mlir",
            "flux",
            "zig",
            "grace",
            "cloud_firestore_security_rules",
            "igor_pro",
            "valve_data_format",
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
        aliases=("asl", "moocode", "postcss"),
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
        family_name="sieve_style",
        canonical_name="sieve",
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r"#[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "if true {\n  # note\n}",
                "# note",
                "Sieve hash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "if true {\n  /* note */\n}",
                "/* note */",
                "Sieve bracketed comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://datatracker.ietf.org/doc/html/rfc5228",
        implementation_source="https://github.com/roundcube/sievelib",
        confidence="verified",
        notes=(
            "RFC 5228 defines hash line comments and bracketed /* ... */ "
            "comments. Bracketed comments may span lines and do not nest."
        ),
    ),
    CommentSyntax(
        family_name="hash_style",
        canonical_name="python",
        aliases=(
            "r",
            "elixir",
            "nix",
            "starlark",
            "graphql",
            "crystal",
            "numpy",
            "ren_py",
        ),
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
        aliases=(
            "eiffel",
            "futhark",
            "asn1",
            "asn_1",
            "object_data_instance_notation",
            "vhdl",
        ),
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
        aliases=("elm", "frege", "grammatical_framework", "literate_agda"),
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
            "abnf",
            "clarity",
            "gcc_machine_description",
            "mirc_script",
            "motorola_68k_assembly",
            "netlogo",
            "pep8",
            "scheme",
            "lisp",
            "clojure",
            "dns_zone",
            "edn",
            "hy",
            "ioke",
            "jasmin",
            "llvm",
            "m",
            "newlisp",
            "papyrus",
            "red",
            "redcode",
            "rouge",
            "srecode_template",
            "smt",
            "zap",
            "zil",
            "windows_registry_entries",
            "rebol",
            "purebasic",
            "wisp",
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
        family_name="module_management_system_style",
        canonical_name="module_management_system",
        regex_patterns=(
            r"(?m)(?<!\S)[#!][^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "! note\nMAIN.EXE : MAIN.OBJ",
                "! note",
                "OpenVMS MMS exclamation comment line.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "MAIN.EXE : MAIN.OBJ # note\n\tLINK MAIN",
                "# note",
                "OpenVMS MMS target-line number-sign comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://docs.vmssoftware.com/"
            "vsi-decset-for-openvms-guide-to-the-module-management-system/"
        ),
        confidence="verified",
        notes=(
            "MMS permits ! and # comments on target/source lines, but action "
            "lines only use !. The regex only treats a delimiter at token "
            "boundary as a comment start."
        ),
    ),
    CommentSyntax(
        family_name="muse_style",
        canonical_name="muse",
        regex_patterns=(
            r"(?m)^; [^\r\n]*",
            r"(?ms)<comment\b[^>]*>[\S\s]*?</comment>",
        ),
        shared_regex_examples=(
            CommentExample(
                "; note\nParagraph text",
                "; note",
                "Muse line omitted from published output.",
                kind="directive",
            ),
            CommentExample(
                "<comment>\nnote\n</comment>\nParagraph text",
                "<comment>\nnote\n</comment>",
                "Muse comment tag region omitted from published output.",
                kind="block",
            ),
        ),
        documentation_source="https://www.gnu.org/software/emacs-muse/manual/muse.txt",
        confidence="verified",
        notes=(
            "Muse treats a semicolon followed by a literal space at the start "
            "of a line as a comment, and also supports <comment> regions."
        ),
    ),
    CommentSyntax(
        family_name="cue_sheet_style",
        canonical_name="cue_sheet",
        regex_patterns=(r"(?im)^[ \t]*REM(?:[ \t][^\r\n]*)?$",),
        shared_regex_examples=(
            CommentExample(
                'REM note\nFILE "album.wav" WAVE',
                "REM note",
                "CUE sheet REM comment command.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="https://wyday.com/cuesharp/specification.php",
        confidence="verified",
        notes="CUE sheets use REM as a command that begins a comment line.",
    ),
    CommentSyntax(
        family_name="ltspice_symbol_style",
        canonical_name="ltspice_symbol",
        regex_patterns=(
            r";[^\r\n]*",
            r"(?m)^\*[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "LINE Normal 0 0 16 0 ; note",
                "; note",
                "LTspice semicolon comment after a symbol instruction.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "* note\nVersion 4",
                "* note",
                "SPICE-style leading-asterisk comment line.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://ltwiki.org/LTspiceHelp/LTspiceHelp/"
            "A_General_Structure_and_Conventions.htm"
        ),
        implementation_source=(
            "https://ez.analog.com/cfs-filesystemfile/__key/"
            "communityserver-discussions-components-files/1020/"
            "LTspice-Symbols-_2800_2_2900_.doc"
        ),
        confidence="cross-checked",
        notes=(
            "LTspice symbol files can comment out symbol instructions with ;. "
            "The broader LTspice/SPICE text convention also treats leading * "
            "lines as ignored comments."
        ),
    ),
    CommentSyntax(
        family_name="pod_style",
        canonical_name="pod",
        regex_patterns=(
            r"(?ms)^=begin[ \t]+comment\b[^\r\n]*(?:\r?\n[\S\s]*?)^=end[ \t]+comment\b[^\r\n]*",
            r"(?m)^=for[ \t]+comment\b[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "=for comment note\n\n=head1 NAME",
                "=for comment note",
                "Pod single-paragraph comment directive.",
                kind="line",
            ),
            CommentExample(
                "=begin comment\nnote\n=end comment\n\n=head1 NAME",
                "=begin comment\nnote\n=end comment",
                "Pod delimited comment block.",
                kind="block",
            ),
        ),
        documentation_source="https://perldoc.perl.org/perldocstyle",
        confidence="verified",
        notes=(
            "Pod uses =for comment for short comments and =begin/=end comment "
            "blocks for longer source-only notes."
        ),
    ),
    CommentSyntax(
        family_name="pod6_style",
        canonical_name="pod_6",
        regex_patterns=(
            r"(?ms)^=begin[ \t]+comment\b[^\r\n]*(?:\r?\n[\S\s]*?)^=end[ \t]+comment\b[^\r\n]*",
            r"(?m)^=comment\b[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "=comment note\n\n=head1 Name",
                "=comment note",
                "Rakudoc single-line comment marker.",
                kind="line",
            ),
            CommentExample(
                "=begin comment\nnote\n=end comment\n\n=head1 Name",
                "=begin comment\nnote\n=end comment",
                "Rakudoc delimited comment block.",
                kind="block",
            ),
        ),
        documentation_source="https://docs.raku.org/language/pod",
        confidence="verified",
        notes="Rakudoc comments are ignored by renderers.",
    ),
    CommentSyntax(
        family_name="record_jar_style",
        canonical_name="record_jar",
        regex_patterns=(r"(?m)^%%[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "Name: Barney\n%% note\nName: Samson",
                "%% note",
                "Record-Jar separator line with comment text.",
                kind="directive",
            ),
        ),
        documentation_source="https://openrj.sourceforge.net/",
        confidence="verified",
        notes=(
            "Record-Jar record separators begin with %%; text after the first "
            "two characters acts as a comment."
        ),
    ),
    CommentSyntax(
        family_name="redirect_rules_style",
        canonical_name="redirect_rules",
        regex_patterns=(r"(?m)^[ \t]*#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "# note\n/home /",
                "# note",
                "Netlify _redirects comment line.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://docs.netlify.com/manage/routing/redirects/overview/"
        ),
        confidence="verified",
        notes="Netlify _redirects comments are lines beginning with #.",
    ),
    CommentSyntax(
        family_name="star_style",
        canonical_name="star",
        regex_patterns=(r"(?m)(?<!\S)#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "data_demo\n# note\n_loop",
                "# note",
                "STAR/CIF hash comment at whitespace boundary.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="https://www.iucr.org/__data/iucr/cif/standard/cifstd4.html",
        confidence="verified",
        notes=(
            "STAR comments begin with # only at the beginning of a line or "
            "after blanks, not inside text strings."
        ),
    ),
    CommentSyntax(
        family_name="stringtemplate_style",
        canonical_name="stringtemplate",
        regex_patterns=(
            r"<![\S\s]*?!>",
            r"\$![\S\s]*?!\$",
        ),
        shared_regex_examples=(
            CommentExample(
                "name ::= <<<! note !><name>>>",
                "<! note !>",
                "StringTemplate angle-delimited comment.",
                kind="block",
                inline_compatible=True,
            ),
            CommentExample(
                "name ::= <<$! note !$ $name$>>",
                "$! note !$",
                "StringTemplate dollar-delimited comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://github.com/antlr/stringtemplate4/blob/master/doc/"
            "cheatsheet.md"
        ),
        confidence="verified",
        notes="StringTemplate supports template comments in both delimiter modes.",
    ),
    CommentSyntax(
        family_name="win32_message_file_style",
        canonical_name="win32_message_file",
        regex_patterns=(
            r"(?m)^[ \t]*;/\*[^\r\n]*(?:\r?\n[ \t]*;[^\r\n]*)*?\r?\n[ \t]*;\*/[^\r\n]*",
            r"(?m)^[ \t]*;[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                ";// note\nMessageId=1",
                ";// note",
                "Win32 message text semicolon comment line.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                ";/* note\n;*/\nMessageId=1",
                ";/* note\n;*/",
                "Win32 message text block represented as semicolon-prefixed lines.",
                kind="directive",
            ),
        ),
        documentation_source=(
            "https://learn.microsoft.com/en-us/windows/win32/eventlog/"
            "message-text-files"
        ),
        confidence="verified",
        notes=(
            "Message compiler files use semicolon-prefixed comment lines; C/C++ "
            "comment markers after the semicolon are for generated-header safety."
        ),
    ),
    CommentSyntax(
        family_name="world_of_warcraft_addon_data_style",
        canonical_name="world_of_warcraft_addon_data",
        regex_patterns=(r"(?m)^#[^#\r\n][^\r\n]*|^#$",),
        shared_regex_examples=(
            CommentExample(
                "## Interface: 100000\n# note\nAddon.lua",
                "# note",
                "WoW TOC single-hash comment line.",
                kind="directive",
            ),
        ),
        documentation_source="https://addonstudio.org/wiki/WoW%3ATOC_format",
        confidence="cross-checked",
        notes=(
            "WoW TOC metadata tags begin with ## and are not comments, so the "
            "regex only captures single-hash comment lines."
        ),
    ),
    CommentSyntax(
        family_name="webvtt_style",
        canonical_name="webvtt",
        regex_patterns=(
            r"\ANOTE(?:[ \t][^\r\n]*)?(?=\r?\n|$)(?:\r?\n(?!\r?\n)[^\r\n]*)*",
            r"(?<=\n\n)NOTE(?:[ \t][^\r\n]*)?(?=\r?\n|$)(?:\r?\n(?!\r?\n)[^\r\n]*)*",
            r"(?<=\r\n\r\n)NOTE(?:[ \t][^\r\n]*)?(?=\r?\n|$)(?:\r?\n(?!\r?\n)[^\r\n]*)*",
        ),
        shared_regex_examples=(
            CommentExample(
                "WEBVTT\n\nNOTE cue timing\nmore detail\n\n00:01.000 --> 00:02.000\nHi",
                "NOTE cue timing\nmore detail",
                "WebVTT NOTE comment block between cue boundaries.",
                kind="cue_block",
            ),
        ),
        documentation_source="https://www.w3.org/TR/webvtt1/",
        confidence="verified",
        notes=(
            "WebVTT comments are NOTE blocks that begin at the start of the "
            "file or after a blank line and continue until the next blank line."
        ),
    ),
    CommentSyntax(
        family_name="runoff_style",
        canonical_name="runoff",
        regex_patterns=(
            r"(?m)^[ \t]*\.[!;][^\r\n]*",
            r"![^;\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                ".LEFT MARGIN 0.RIGHT MARGIN 60!note;.SKIP",
                "!note",
                "RUNOFF inline comment flag.",
                kind="line",
                inline_compatible=True,
            ),
            CommentExample(
                ".!Place comment here.\n.LEFT MARGIN 0",
                ".!Place comment here.",
                "RUNOFF control/comment flag pair at line start.",
                kind="directive",
            ),
        ),
        documentation_source=(
            "https://docs.vmssoftware.com/"
            "digital-standard-runoff-reference-manual/"
        ),
        confidence="verified",
        notes=(
            "DSR/RUNOFF uses ! as the comment flag by default; .! and .; are "
            "line-start control/comment forms. A semicolon terminates an inline "
            "comment."
        ),
    ),
    CommentSyntax(
        family_name="regular_expression_style",
        canonical_name="regular_expression",
        regex_patterns=(r"\(\?#[^)]*\)",),
        shared_regex_examples=(
            CommentExample(
                r"^foo(?# note)bar$",
                "(?# note)",
                "PCRE/Perl-style inline regular-expression comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://www.pcre.org/original/doc/html/pcrepattern.html",
        confidence="verified",
        notes=(
            "The portable in-pattern comment form is (?#...). Verbose-mode # "
            "comments are option-dependent and intentionally excluded."
        ),
    ),
    CommentSyntax(
        family_name="ti_program_style",
        canonical_name="ti_program",
        regex_patterns=(r"\N{COPYRIGHT SIGN}[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "Disp 1 \N{COPYRIGHT SIGN} note",
                "\N{COPYRIGHT SIGN} note",
                "TI-Basic comment introduced by the copyright-sign command.",
                kind="line",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://education.ti.com/en/customer-support/knowledge-base/"
            "other-graphing/product-usage/11775"
        ),
        confidence="verified",
        notes=(
            "TI-89/TI-92/Voyage 200 TI-Basic comments begin at the copyright "
            "sign command and continue to the end of the line."
        ),
    ),
    CommentSyntax(
        family_name="x_font_directory_index_style",
        canonical_name="x_font_directory_index",
        regex_patterns=(r"(?m)^![^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                (
                    "! font alias note\n"
                    "fixed -misc-fixed-medium-r-normal--13-120-75-75-c-70-iso10646-1"
                ),
                "! font alias note",
                "X fonts.alias comment line.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://xorg.freedesktop.org/archive/X11R7.5/doc/man/man1/"
            "mkfontdir.1.html"
        ),
        confidence="verified",
        notes="X fonts.alias ignores lines beginning with ! as comments.",
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
        aliases=("oxygene", "portugol"),
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
        aliases=("bibtex", "charity", "postscript", "tex"),
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
        aliases=("ats", "f_sharp", "fsharp"),
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
        aliases=("muf",),
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
            "eagle",
            "jetbrains_mps",
            "kit",
            "labview",
            "markdown",
            "maven_pom",
            "mediawiki",
            "mtml",
            "riot",
            "rmarkdown",
            "svelte",
            "svg",
            "web_ontology_language",
            "wikitext",
            "xml_property_list",
            "xpages",
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
        aliases=("moonscript", "terra"),
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
        aliases=(
            "augeas",
            "component_pascal",
            "ebnf",
            "isabelle",
            "isabelle_root",
            "modula_2",
            "modula_3",
            "standard_ml",
            "urweb",
        ),
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
        aliases=("lilypond", "turing", "txl"),
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
        aliases=("eclipse", "logtalk", "mercury", "oz"),
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
        aliases=("perl6",),
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
        aliases=("opal", "ragel_in_ruby_host"),
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
        aliases=("hiveql", "piglatin", "plpgsql", "plsql", "sqlpl", "tsql"),
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
        aliases=(
            "basic",
            "realbasic",
            "vba",
            "vbscript",
            "visual_basic",
            "xojo",
        ),
        regex_patterns=(
            r"'[^\r\n]*",
            r"(?im)^[ \t]*rem\b[^\r\n]*",
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
        aliases=("smalltalk", "viml"),
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
        aliases=("common_lisp",),
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
        family_name="emacs_lisp_style",
        canonical_name="emacs_lisp",
        regex_patterns=(r";[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "(message \"before\") ; note\n(message \"after\")",
                "; note",
                "Emacs Lisp semicolon line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://www.gnu.org/software/emacs/manual/html_node/elisp/"
            "Comment-Tips.html"
        ),
        implementation_source="https://git.savannah.gnu.org/cgit/emacs.git",
        confidence="verified",
        notes=(
            "Emacs Lisp uses semicolon line comments. Common Lisp #| ... |# "
            "block comments are not valid Emacs Lisp syntax."
        ),
    ),
    CommentSyntax(
        family_name="nim_style",
        canonical_name="nim",
        aliases=("nimrod",),
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
            "graphviz_dot",
            "hcl",
            "html_php",
            "html_plus_php",
            "io",
            "ring",
            "thrift",
            "vcl",
            "zephir",
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
        family_name="directx_3d_file_style",
        canonical_name="directx_3d_file",
        regex_patterns=(
            r"/{2}[^\r\n]*",
            r"#[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "xof 0303txt 0032\n// note\n",
                "// note",
                "DirectX .x slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "xof 0303txt 0032\n# note\n",
                "# note",
                "DirectX .x hash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://learn.microsoft.com/en-us/windows/win32/direct3d9/"
            "reserved-words--header--and-comments"
        ),
        implementation_source=(
            "https://github.com/MicrosoftDocs/win32/blob/docs/desktop-src/"
            "direct3d9/reserved-words--header--and-comments.md"
        ),
        confidence="verified",
        notes=(
            "DirectX .x text files support // and # comments to end of line. "
            "The Microsoft reference does not define /* ... */ block comments."
        ),
    ),
    CommentSyntax(
        family_name="hocon_style",
        canonical_name="hocon",
        aliases=("lark",),
        regex_patterns=(
            r"/{2}[^\r\n]*",
            r"#[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "service {\n  // note\n  host = \"localhost\"\n}",
                "// note",
                "HOCON slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "service {\n  # note\n  host = \"localhost\"\n}",
                "# note",
                "HOCON hash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="https://github.com/lightbend/config/blob/main/HOCON.md",
        implementation_source="https://github.com/lightbend/config/blob/main/HOCON.md",
        confidence="verified",
        notes=(
            "HOCON supports # and // line comments. C-style /* ... */ block "
            "comments are not part of the documented HOCON syntax."
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
        regex_patterns=(
            r"#\[\[[\S\s]*?\]\]",
            r"#\[(=+)\[[\S\s]*?\]\1\]",
            r"#(?!\[=*\[)[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n# note\nsuffix",
                "# note",
                "CMake line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "before #[[ note ]] after",
                "#[[ note ]]",
                "CMake bracket comment.",
                kind="block",
                inline_compatible=True,
            ),
            CommentExample(
                "before #[=[ note ]=] after",
                "#[=[ note ]=]",
                "CMake equal-delimited bracket comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://cmake.org/cmake/help/latest/manual/"
            "cmake-language.7.html"
        ),
        implementation_source="https://gitlab.kitware.com/cmake/cmake",
        confidence="verified",
        notes=(
            "CMake bracket comments use the same equal-delimited bracket "
            "syntax as bracket arguments, and bracket arguments do not nest."
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
        aliases=(
            "html_eex",
            "html_erb",
            "html_plus_eex",
            "html_plus_erb",
            "javascript_erb",
            "javascript_plus_erb",
        ),
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
        family_name="html_ecr_style",
        canonical_name="html_ecr",
        aliases=("rhtml", "html_plus_ecr"),
        regex_patterns=(
            r"<!--[\S\s]*?-->",
            r"<%-?\s*#(?:(?!-?%>)[\S\s])*-?%>",
        ),
        shared_regex_examples=(
            CommentExample(
                "prefix\n<%# note %>\nsuffix",
                "<%# note %>",
                "Crystal ECR comment tag.",
                kind="block",
                inline_compatible=True,
            ),
            CommentExample(
                "prefix\n<% # note %>\nsuffix",
                "<% # note %>",
                "Crystal code tag containing a Crystal comment.",
                kind="block",
                inline_compatible=True,
            ),
            CommentExample(
                "<p>before</p>\n<!-- note -->\n<p>after</p>",
                "<!-- note -->",
                "HTML comment in an ECR template.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://crystal-lang.org/api/latest/ECR.html",
        implementation_source="https://github.com/crystal-lang/crystal/tree/master/src/ecr",
        confidence="verified",
        notes=(
            "Crystal ECR strips <%# ... %> and <% # ... %> comments. HTML "
            "comments remain template text but are still source comments in "
            "html_ecr files."
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
        aliases=("html_django", "html_plusdjango", "html_plus_django"),
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
        family_name="genshi_style",
        canonical_name="genshi",
        regex_patterns=(r"<!--[\S\s]*?-->",),
        shared_regex_examples=(
            CommentExample(
                "<div><!-- note --><span>${value}</span></div>",
                "<!-- note -->",
                "Genshi XML/HTML template comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://genshi.readthedocs.io/en/latest/xml-templates.html; "
            "https://github.com/github-linguist/linguist/blob/master/"
            "lib/linguist/languages.yml"
        ),
        implementation_source="https://github.com/edgewall/genshi",
        confidence="verified",
        notes=(
            "The Stack/GitHub Genshi language is XML-based .kid content "
            "(text.xml.genshi), so this registry key follows Genshi XML "
            "templates and accepts normal HTML comments. Genshi's separate "
            "text-template dialects use {# ... #} and legacy ## comments, but "
            "they are not part of this language key."
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
        aliases=(
            "c2hs_haskell",
            "curry",
            "dhall",
            "idris",
            "literate_haskell",
            "purescript",
        ),
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
        aliases=("scaml",),
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
        aliases=("groovy_server_pages", "java_server_pages"),
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
        aliases=("html_plus_razor",),
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
            r"\{%-?\s*comment\s*-?%\}[\S\s]*?\{%-?\s*endcomment\s*-?%\}",
            r"\{%-?\s*(?:#[^\r\n]*(?:\r?\n\s*#[^\r\n]*)*)\s*-?%\}",
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
                "prefix\n{%\n  # note\n  # more\n%}\nsuffix",
                "{%\n  # note\n  # more\n%}",
                "Liquid multiline inline comment tag.",
                kind="line",
                inline_compatible=False,
            ),
            CommentExample(
                "prefix\n{% comment %}\nblock note\n{% endcomment %}\nsuffix",
                "{% comment %}\nblock note\n{% endcomment %}",
                "Liquid block comment tag.",
                kind="block",
            ),
        ),
        documentation_source="https://shopify.dev/docs/api/liquid/tags/comment",
        implementation_source="https://github.com/Shopify/liquid",
        confidence="verified",
        notes=(
            "Liquid supports {% comment %} blocks plus inline {% # ... %} "
            "comment tags. Multiline inline comment tags require each content "
            "line to begin with #."
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
        aliases=("jade",),
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
        aliases=("groff", "roff_manpage"),
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
        aliases=("genero_forms",),
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
        family_name="brainfuck_style",
        canonical_name="brainfuck",
        regex_patterns=(
            r"(?<=(?:^|[\r\n.,+\-<>\[\]])[ \t]*)"
            r"[^\s.,+\-<>\[\]][^\r\n.,+\-<>\[\]]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "+++++[>++++<-] Brainfuck note\n.",
                "Brainfuck note",
                "Brainfuck ignored non-command text.",
                kind="ignored",
            ),
        ),
        documentation_source="https://esolangs.org/wiki/Brainfuck",
        implementation_source=(
            "https://github.com/pygments/pygments/blob/2.20.0/"
            "pygments/lexers/esoteric.py"
        ),
        confidence="cross-checked",
        notes=(
            "Brainfuck has no delimiter token; interpreters ignore characters "
            "outside the eight command symbols. The regex captures non-whitespace "
            "ignored text runs at command and line boundaries while avoiding "
            "invisible whitespace-only matches."
        ),
    ),
    CommentSyntax(
        family_name="dogescript_style",
        canonical_name="dogescript",
        regex_patterns=(
            r"(?ims)^[ \t]*quiet\b[^\r\n]*(?:\r?\n[\S\s]*?)^[ \t]*loud\b[^\r\n]*",
            r"(?im)^[ \t]*shh\b[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "shh much note\nvery doge is 'wow'",
                "shh much note",
                "Dogescript shh line comment.",
                kind="line",
            ),
            CommentExample(
                "quiet\n  much note\nloud\nvery doge is 'wow'",
                "quiet\n  much note\nloud",
                "Dogescript quiet/loud multiline comment.",
                kind="block",
            ),
        ),
        documentation_source=(
            "https://github.com/dogescript/dogescript/blob/master/LANGUAGE.md"
        ),
        confidence="verified",
        notes="Dogescript documents shh line comments and quiet/loud multiline comments.",
    ),
    CommentSyntax(
        family_name="graph_modeling_language_style",
        canonical_name="graph_modeling_language",
        regex_patterns=(r'\bcomment\s+"(?:\\.|[^"\\])*"',),
        shared_regex_examples=(
            CommentExample(
                'graph [\n  comment "Graph note"\n  directed 1\n]',
                'comment "Graph note"',
                "GML comment string attribute.",
                kind="attribute",
            ),
        ),
        documentation_source=(
            "https://raw.githubusercontent.com/GunterMueller/"
            "UNI_PASSAU_FMI_Graph_Drawing/master/GML/gml-technical-report.pdf"
        ),
        confidence="cross-checked",
        notes=(
            "The original Graph Modeling Language report defines a comment "
            "string attribute that applications ignore. Some parsers also accept "
            "# lines, but this entry keeps to the documented portable form."
        ),
    ),
    CommentSyntax(
        family_name="http_request_file_style",
        canonical_name="http",
        regex_patterns=(r"(?m)^[ \t]*(?:#|//)[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "# note\nGET https://example.test",
                "# note",
                ".http hash comment line.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "// note\nGET https://example.test",
                "// note",
                ".http slash comment line.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://learn.microsoft.com/en-us/aspnet/core/test/"
            "http-files?view=aspnetcore-10.0"
        ),
        confidence="verified",
        notes=(
            "The Stack HTTP key maps to .http request files, where Visual Studio "
            "documents lines beginning with # or // as comments. Raw HTTP wire "
            "messages do not have source-level comments."
        ),
    ),
    CommentSyntax(
        family_name="kicad_style",
        canonical_name="kicad",
        regex_patterns=(r'\(comment\s+[1-9]\s+"(?:\\.|[^"\\])*"\)',),
        shared_regex_examples=(
            CommentExample(
                '(title_block\n  (comment 1 "Board note")\n)',
                '(comment 1 "Board note")',
                "KiCad title-block comment token.",
                kind="attribute",
            ),
        ),
        documentation_source=(
            "https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html"
        ),
        confidence="verified",
        notes=(
            "Generic Stack KiCad files use KiCad s-expressions. The common "
            "title_block syntax defines numbered comment attributes as quoted "
            "document comments."
        ),
    ),
    CommentSyntax(
        family_name="myghty_style",
        canonical_name="myghty",
        regex_patterns=(r"(?m)^#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "# note\n% print('ok')",
                "# note",
                "Myghty leading hash comment line.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="https://pythonhosted.org/Myghty/documentation.html",
        implementation_source=(
            "https://github.com/pygments/pygments/blob/2.20.0/"
            "pygments/lexers/templates.py"
        ),
        confidence="cross-checked",
        notes="Myghty template comment lines begin with # at the start of a line.",
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
                "x = 5 ; note\ny = 6",
                "; note",
                "NCL semicolon line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "begin\n/;\n  note\n;/\nend",
                "/;\n  note\n;/",
                "NCL bracketed block comment.",
                kind="block",
            ),
        ),
        documentation_source=(
            "https://www.ncl.ucar.edu/Document/Manuals/Ref_Manual/"
            "NclStatements.shtml"
        ),
        implementation_source=(
            "https://github.com/pygments/pygments/blob/2.20.0/"
            "pygments/lexers/ncl.py"
        ),
        confidence="verified",
        notes="NCL supports semicolon line comments and /; ... ;/ block comments.",
    ),
    CommentSyntax(
        family_name="shen_style",
        canonical_name="shen",
        regex_patterns=(
            r"\\\*[\S\s]*?\*\\",
            r"\\\\[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "(define x\n  \\\\ note\n  1)",
                "\\\\ note",
                "Shen double-backslash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "(define x \\* note *\\ 1)",
                "\\* note *\\",
                "Shen backslash-star block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://shen-language.github.io/",
        implementation_source=(
            "https://github.com/pygments/pygments/blob/2.20.0/"
            "pygments/lexers/lisp.py"
        ),
        confidence="cross-checked",
        notes="The Shen lexer recognizes \\\\ line comments and \\* ... *\\ block comments.",
    ),
    CommentSyntax(
        family_name="tea_style",
        canonical_name="tea",
        regex_patterns=(
            r"<!--[\S\s]*?-->",
            r"/\*[\S\s]*?\*/",
            r"//[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "<template><!-- note --><% call(); %></template>",
                "<!-- note -->",
                "Tea template XML comment.",
                kind="block",
                inline_compatible=True,
            ),
            CommentExample(
                "<% // note\n call(); %>",
                "// note",
                "Tea language slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "<% /* note */ call(); %>",
                "/* note */",
                "Tea language block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://github.com/teatrove/teatrove",
        implementation_source=(
            "https://github.com/pygments/pygments/blob/2.20.0/"
            "pygments/lexers/templates.py"
        ),
        confidence="cross-checked",
        notes=(
            "Tea templates are XML-like templates with embedded Tea language; "
            "the lexer delegates XML comments and Tea // plus /* ... */ comments."
        ),
    ),
    CommentSyntax(
        family_name="textile_style",
        canonical_name="textile",
        regex_patterns=(
            r"<!--[\S\s]*?-->",
            r"(?ms)^###\.\.[\S\s]*?(?=^p\.|\Z)",
            r"(?m)^###\.[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "Text <!-- note --> here",
                "<!-- note -->",
                "Textile-respected HTML comment.",
                kind="block",
                inline_compatible=True,
            ),
            CommentExample(
                "Some text\n###. Textile note\nMore text",
                "###. Textile note",
                "Textile ###. comment line.",
                kind="textile",
            ),
        ),
        documentation_source="https://textile-lang.com/doc/textile-comments",
        confidence="verified",
        notes=(
            "Textile comments start with ###.; multiline comments start with "
            "###.. and continue until a p. paragraph marker. HTML comments are "
            "also respected."
        ),
    ),
    CommentSyntax(
        family_name="texinfo_style",
        canonical_name="texinfo",
        regex_patterns=(r"(?m)^[ \t]*@(?:c|comment)\b[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "@c note\n@node Top",
                "@c note",
                "Texinfo @c comment line.",
                kind="directive",
            ),
            CommentExample(
                "@comment note\n@node Top",
                "@comment note",
                "Texinfo @comment line.",
                kind="directive",
            ),
        ),
        documentation_source="https://www.gnu.org/software/texinfo/manual/texinfo/html_node/Comments.html",
        confidence="verified",
        notes="Texinfo comments are introduced by @c or @comment at the start of a command line.",
    ),
    CommentSyntax(
        family_name="cool_style",
        canonical_name="cool",
        regex_patterns=(r"--.*",),
        nested_delimiters=(("(*", "*)"),),
        shared_regex_examples=(
            CommentExample(
                "class Main inherits IO {\n  -- note\n};",
                "-- note",
                "Cool line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "class Main {\n  (* outer (* inner *) outer *)\n};",
                "(* outer (* inner *) outer *)",
                "Cool nested block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://theory.stanford.edu/~aiken/software/cool/cool-manual.pdf",
        confidence="verified",
        notes="Cool supports -- line comments and nested (* ... *) comments.",
    ),
    CommentSyntax(
        family_name="livescript_style",
        canonical_name="livescript",
        regex_patterns=(
            r"/\*[\S\s]*?\*/",
            r"#.*",
        ),
        shared_regex_examples=(
            CommentExample(
                "value = 1\n# note\nvalue",
                "# note",
                "LiveScript line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "value = 1\n/* note */\nvalue",
                "/* note */",
                "LiveScript preserved multiline comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://livescript.net/",
        confidence="verified",
        notes="LiveScript uses # line comments and preserved /* ... */ multiline comments.",
    ),
    CommentSyntax(
        family_name="monkey_style",
        canonical_name="monkey",
        regex_patterns=(
            r"(?ims)^[ \t]*#rem\b[^\r\n]*(?:\r?\n[\S\s]*?)^[ \t]*#end\b[^\r\n]*",
            r"'[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "Print \"Hello\" ' note\nEnd",
                "' note",
                "Monkey apostrophe line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "Print \"before\"\n#Rem\nnote\n#End\nPrint \"after\"",
                "#Rem\nnote\n#End",
                "Monkey #Rem block comment.",
                kind="block",
            ),
        ),
        documentation_source=(
            "https://regal-internet-brothers.github.io/monkey/docs/"
            "Programming_Language%20reference.html"
        ),
        confidence="verified",
        notes=(
            "Monkey uses apostrophe line comments and #Rem/#End block comments. "
            "The block form may nest, but this regex implementation captures the "
            "common non-nested corpus form."
        ),
    ),
    CommentSyntax(
        family_name="netlinx_style",
        canonical_name="netlinx",
        aliases=("netlinx_plus_erb",),
        regex_patterns=(
            r"/\*[\S\s]*?\*/",
            r"\(\*[\S\s]*?\*\)",
            r"//[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "DEFINE_PROGRAM\n// note\nWAIT 10 {}",
                "// note",
                "NetLinx slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "DEFINE_PROGRAM\n(* note *)\nWAIT 10 {}",
                "(* note *)",
                "NetLinx parenthesized block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://www.amx.com/en/site_elements/style-guide-netlinx-studio-v-4",
        confidence="verified",
        notes=(
            "NetLinx style guidance documents // comments plus /* ... */ and "
            "preferred (* ... *) multiline comments."
        ),
    ),
    CommentSyntax(
        family_name="openedge_abl_style",
        canonical_name="openedge_abl",
        regex_patterns=(r"/\*[\S\s]*?\*/",),
        shared_regex_examples=(
            CommentExample(
                "MESSAGE \"before\".\n/* note */\nMESSAGE \"after\".",
                "/* note */",
                "OpenEdge ABL block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://docs.progress.com/bundle/openedge-abl-basic-guided-journey/"
            "page/Comments.html"
        ),
        confidence="verified",
        notes="OpenEdge ABL documents /* ... */ comments.",
    ),
    CommentSyntax(
        family_name="maxscript_style",
        canonical_name="maxscript",
        regex_patterns=(
            r"/\*[\S\s]*?\*/",
            r"--.*",
        ),
        shared_regex_examples=(
            CommentExample(
                "x = 1\n-- note\nx",
                "-- note",
                "MAXScript line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "x = 1\n/* note */\nx",
                "/* note */",
                "MAXScript block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://help.autodesk.com/cloudhelp/2026/ENU/MAXScript-Help/"
        ),
        confidence="cross-checked",
        notes="MAXScript uses -- line comments and C-style /* ... */ block comments.",
    ),
    CommentSyntax(
        family_name="supercollider_style",
        canonical_name="supercollider",
        aliases=(
            "cameligo",
            "ligolang",
            "reason",
            "reason_ligo",
            "reasonligo",
            "reasonml",
            "wren",
        ),
        regex_patterns=(r"//[^\r\n]*",),
        nested_delimiters=(("/*", "*/"),),
        shared_regex_examples=(
            CommentExample(
                "SynthDef(\\demo, { // note\n}).add;",
                "// note",
                "SuperCollider line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "value = 1; /* outer /* inner */ outer */ value;",
                "/* outer /* inner */ outer */",
                "SuperCollider nested block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://doc.sccode.org/Reference/Comments.html",
        confidence="verified",
        notes="SuperCollider supports // comments and nested /* ... */ block comments.",
    ),
    CommentSyntax(
        family_name="propeller_spin_style",
        canonical_name="propeller_spin",
        regex_patterns=(
            r"\{\{[\S\s]*?\}\}",
            r"\{[\S\s]*?\}",
            r"'{1,2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "PUB Main\n  ' note\n  return",
                "' note",
                "Propeller Spin apostrophe line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "PUB Main\n  { note }\n  return",
                "{ note }",
                "Propeller Spin brace block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://forums.parallax.com/discussion/download/85706/"
            "Propeller_Tutorial_1.01.pdf"
        ),
        confidence="verified",
        notes=(
            "Propeller Spin supports apostrophe line comments and brace-delimited "
            "code or documentation comments."
        ),
    ),
    CommentSyntax(
        family_name="xbase_style",
        canonical_name="xbase",
        aliases=("harbour",),
        regex_patterns=(
            r"/\*[\S\s]*?\*/",
            r"//[^\r\n]*",
            r"&&[^\r\n]*",
            r"(?im)^[ \t]*(?:\*|note\b).*$",
        ),
        shared_regex_examples=(
            CommentExample(
                '? "before"\n// note\n? "after"',
                "// note",
                "xBase slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                '? "before"\n/* note */\n? "after"',
                "/* note */",
                "xBase C-style block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://harbour.github.io/doc/harbour.html",
        implementation_source="https://github.com/harbour/core",
        confidence="cross-checked",
        notes="Harbour/xBase accepts //, &&, leading *, NOTE, and /* ... */ comments.",
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
        aliases=("cson", "emberscript", "literate_coffeescript"),
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


def _language_lookup_candidates(language: str) -> Tuple[str, ...]:
    """Return lookup keys for canonical aliases and raw Stack-style labels."""

    normalized = language.strip().lower()
    expanded = normalized.replace("+", "_plus_").replace("#", "sharp")
    parts = []
    previous_separator = False
    for char in expanded:
        if char.isalnum():
            parts.append(char)
            previous_separator = False
            continue
        if not previous_separator:
            parts.append("_")
            previous_separator = True
    stack_style = "".join(parts).strip("_")
    if stack_style == normalized:
        return (normalized,)
    return (normalized, stack_style)


def get_comment_syntax(language: str) -> CommentSyntax:
    """Return syntax metadata for one supported language.

    Args:
        language: Registry key or alias. Lookup is case-insensitive.

    Returns:
        The matching ``CommentSyntax`` entry.

    Raises:
        NotImplementedError: If the language is not in the registry.
    """

    for key in _language_lookup_candidates(language):
        try:
            return LANGUAGE_SYNTAX[key]
        except KeyError:
            continue
    raise NotImplementedError(f"Unsupported language: {language}")


def iter_comment_syntaxes() -> Iterable[CommentSyntax]:
    """Return all canonical syntax-family entries in registry order."""

    return COMMENT_SYNTAXES
