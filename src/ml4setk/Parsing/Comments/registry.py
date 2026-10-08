"""Comment syntax registry used by comment extraction queries.

This module is intentionally data-heavy. Add or correct comment-language
support by updating ``COMMENT_SYNTAXES`` with regex patterns, nested delimiters,
and seeded examples instead of branching in parser code.
"""

import os
import re
import sys
import warnings
from dataclasses import dataclass, replace
from functools import lru_cache
from typing import Dict, Iterable, Optional, Tuple

import regex

from .contextual import SUPPORTED_CONTEXTUAL_EXTRACTORS


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
        standalone_compatible: Whether the comment marker is valid without
            language syntax before it on the same physical line.
        consumes_eof: Whether this seeded match intentionally consumes all
            remaining source and therefore must be placed last in a fixture.
    """

    sample: str
    expected_match: str
    description: str = ""
    kind: str = "line"
    inline_compatible: bool = False
    grouped_line_compatible: bool = False
    standalone_compatible: bool = True
    consumes_eof: bool = False


@dataclass(frozen=True)
class CommentLanguageVersion:
    """One version range of a language whose comment syntax changed over time.

    The default version of a language is implemented by its ``CommentSyntax``
    entry and declares no overlay. Every other version overlays only the
    fields it changes; ``None`` keeps the default version's value.

    Attributes:
        name: Canonical lowercase version id, for example ``c89``.
        aliases: Other accepted labels for the same range, for example ``c90``.
        release: First release of the range for numeric lookup, for example
            ``3.0``. When every version of a language declares one, any dotted
            release number selects the latest range that starts at or before it.
        span: Human-readable releases or standards covered by the range.
        comment_rules: Comment forms valid in this version.
        regex_patterns: Replacement line and non-nested block patterns.
        nested_delimiters: Replacement recursive block delimiters.
        excluded_comment_prefixes: Replacement exact-prefix exclusions.
        contextual_extractor: Replacement contextual extractor name; an empty
            string disables the default version's extractor.
        unclosed_block_openers: Replacement unclosed block openers.
        lexical_profile: Name of a literal-rule profile in ``lexical.py`` that
            replaces the language's string and literal protection rules.
        sanitizer_line_wrappers: Extra sanitizer line wrappers for comment
            forms that only this version accepts.
        sanitizer_block_wrappers: Extra sanitizer block wrappers for comment
            forms that only this version accepts.
        examples: Seeded examples whose ``expected_match`` is a comment under
            this version.
        documentation_source: Evidence for this version's comment rules.
    """

    name: str
    aliases: Tuple[str, ...] = ()
    release: str = ""
    span: str = ""
    comment_rules: str = ""
    regex_patterns: Optional[Tuple[str, ...]] = None
    nested_delimiters: Optional[Tuple[Tuple[str, str], ...]] = None
    excluded_comment_prefixes: Optional[Tuple[str, ...]] = None
    contextual_extractor: Optional[str] = None
    unclosed_block_openers: Optional[Tuple[str, ...]] = None
    lexical_profile: str = ""
    sanitizer_line_wrappers: Tuple[Tuple[str, str], ...] = ()
    sanitizer_block_wrappers: Tuple[Tuple[str, str], ...] = ()
    examples: Tuple[CommentExample, ...] = ()
    documentation_source: str = ""

    @property
    def labels(self) -> Tuple[str, ...]:
        """Return the canonical name followed by its aliases."""

        return (self.name,) + self.aliases

    @property
    def has_overlay(self) -> bool:
        """Return whether this version changes any extraction behavior."""

        return bool(
            self.regex_patterns is not None
            or self.nested_delimiters is not None
            or self.excluded_comment_prefixes is not None
            or self.contextual_extractor is not None
            or self.unclosed_block_openers is not None
            or self.lexical_profile
            or self.sanitizer_line_wrappers
            or self.sanitizer_block_wrappers
        )


@dataclass(frozen=True)
class CommentLanguageVersions:
    """Version table for registry languages with version-dependent comments.

    Attributes:
        languages: Registry keys from one family that share this table.
        versions: Version ranges in chronological order.
        default: Name of the version implemented by the ``CommentSyntax`` entry.
        notes: Maintainer-facing caveats for the version split.
    """

    languages: Tuple[str, ...]
    versions: Tuple[CommentLanguageVersion, ...]
    default: str
    notes: str = ""

    @property
    def version_names(self) -> Tuple[str, ...]:
        """Return canonical version names in chronological order."""

        return tuple(version.name for version in self.versions)

    def version(self, name: str) -> CommentLanguageVersion:
        """Return the version with canonical ``name``."""

        return next(version for version in self.versions if version.name == name)


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
        contextual_extractor: Optional named range extractor for formats whose
            comments depend on file-level structure rather than delimiters.
        shared_contextual_examples: Contextual examples for every alias.
        canonical_contextual_examples: Contextual examples only for the
            canonical language.
        sanitizer_line_wrappers: Explicit line-comment ``(open, close)``
            wrappers. These augment wrappers inferred from seeded examples and
            are useful when example prose would make inference ambiguous.
        sanitizer_block_wrappers: Explicit block-comment ``(open, close)``
            wrappers. These augment nested delimiters and wrappers inferred
            from seeded examples.
        unclosed_block_openers: Block openers that intentionally consume through
            end of file when no closing delimiter is present.
        excluded_comment_prefixes: Exact prefixes that resemble this family's
            comment syntax but belong to a source directive or operator.
        language_excluded_comment_prefixes: Per-language exact-prefix exclusions
            for directives that apply to only selected members of a syntax
            family.
        sanitizer_mode: ``wrapped`` for delimiter-based comments or ``raw`` for
            contextual comments whose text must be preserved verbatim.
        language_regex_patterns: Per-language regex replacements for family
            members whose comment openers are context-restricted (for example
            word-initial or line-initial ``#``). The listed language uses its
            patterns instead of ``regex_patterns``.
        language_versions: Version tables for family members whose comment
            syntax depends on the language version. A listed language requires
            a version: queries default to the table's default version and warn
            once when the caller does not choose one.
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
    # Preserve the published v0.0.2 positional field order above this line.
    contextual_extractor: str = ""
    shared_contextual_examples: Tuple[CommentExample, ...] = ()
    canonical_contextual_examples: Tuple[CommentExample, ...] = ()
    sanitizer_line_wrappers: Tuple[Tuple[str, str], ...] = ()
    sanitizer_block_wrappers: Tuple[Tuple[str, str], ...] = ()
    unclosed_block_openers: Tuple[str, ...] = ()
    excluded_comment_prefixes: Tuple[str, ...] = ()
    language_excluded_comment_prefixes: Tuple[Tuple[str, Tuple[str, ...]], ...] = ()
    sanitizer_mode: str = "wrapped"
    language_regex_patterns: Tuple[Tuple[str, Tuple[str, ...]], ...] = ()
    language_versions: Tuple[CommentLanguageVersions, ...] = ()

    def versions_for_language(self, language: str) -> Optional[CommentLanguageVersions]:
        """Return the version table for ``language``, or ``None`` if it has none."""

        normalized = language.strip().lower()
        return next(
            (table for table in self.language_versions if normalized in table.languages),
            None,
        )

    def requires_version(self, language: str) -> bool:
        """Return whether ``language`` has version-dependent comment syntax."""

        return self.versions_for_language(language) is not None

    @property
    def language_names(self) -> Tuple[str, ...]:
        """Return the canonical language key followed by all aliases."""

        return (self.canonical_name,) + self.aliases

    def regex_patterns_for_language(self, language: str) -> Tuple[str, ...]:
        """Return the regex comment patterns that apply to ``language``."""

        normalized = language.strip().lower()
        return next(
            (
                patterns
                for dialect, patterns in self.language_regex_patterns
                if dialect == normalized
            ),
            self.regex_patterns,
        )

    def excluded_comment_prefixes_for_language(self, language: str) -> Tuple[str, ...]:
        """Return family-wide and dialect-specific prefix exclusions."""

        normalized = language.strip().lower()
        dialect_prefixes = next(
            (
                prefixes
                for dialect, prefixes in self.language_excluded_comment_prefixes
                if dialect == normalized
            ),
            (),
        )
        return self.excluded_comment_prefixes + dialect_prefixes


# C11 5.1.1.2 and C++ [lex.phases]: line splicing (phase 2) precedes comment
# removal (phase 3), so a backslash-newline continues a // comment and may sit
# between the * and / of a block terminator. Trigraph replacement (phase 1)
# makes ??/ a backslash in C89-C17 and C++98-C++14. C++23 also splices a
# backslash followed by whitespace before the newline.
_SPLICE = r"\\(?:\r\n|\r|\n)"
_TRIGRAPH_SPLICE = r"(?:\\|\?\?/)(?:\r\n|\r|\n)"
_CPP23_SPLICE = r"\\[ \t\f\v]*(?:\r\n|\r|\n)"


def _c_block_pattern(splice: str) -> str:
    return r"\/\*[\S\s]*?\*(?:" + splice + r")*\/"


def _c_line_pattern(splice: str) -> str:
    return r"/{2}(?:" + splice + r"|[^\r\n])*"


_C_SPLICE_PATTERNS = (_c_block_pattern(_SPLICE), _c_line_pattern(_SPLICE))
_C_TRIGRAPH_PATTERNS = (_c_block_pattern(_TRIGRAPH_SPLICE), _c_line_pattern(_TRIGRAPH_SPLICE))
_GCC_LANG_DEFAULTS = (
    "https://github.com/gcc-mirror/gcc/blob/releases/gcc-14.2.0/libcpp/init.cc "
    "(lang_defaults: c99, trigraphs, and digit separators per standard)"
)

_C_LANGUAGE_VERSIONS = CommentLanguageVersions(
    languages=("c", "objective-c"),
    default="c23",
    notes=(
        "Objective-C comments are lexed by the C front end at the selected C "
        "edition. GCC and Clang accept // in C89 modes as an extension; the "
        "c89 version follows ISO C90, which has no // comments."
    ),
    versions=(
        CommentLanguageVersion(
            name="c89",
            aliases=("c90", "c95", "ansi", "iso9899:1990", "iso9899:199409"),
            span="ANSI X3.159-1989 / ISO C90 and the C95 amendment",
            comment_rules=(
                "Only non-nested /* */ comments; // is two division operators. "
                "Trigraph ??/ and backslash-newline splices precede comment "
                "removal; ' never separates digits."
            ),
            regex_patterns=(_c_block_pattern(_TRIGRAPH_SPLICE),),
            lexical_profile="c-without-digit-separators",
            examples=(
                CommentExample(
                    "a = b //* note */ c;\n",
                    "/* note */",
                    "C90 lexes //* as a division followed by a block comment.",
                    kind="block",
                    inline_compatible=True,
                ),
            ),
            documentation_source=("ISO/IEC 9899:1990 6.1.9 Comments; " + _GCC_LANG_DEFAULTS),
        ),
        CommentLanguageVersion(
            name="c99",
            aliases=("c11", "c17", "c18", "iso9899:1999", "iso9899:2011", "iso9899:2017"),
            span="C99, C11, and C17/C18",
            comment_rules=(
                "/* */ and // comments. Trigraph ??/ splices lines like a "
                "backslash; ' never separates digits."
            ),
            regex_patterns=_C_TRIGRAPH_PATTERNS,
            lexical_profile="c-without-digit-separators",
            examples=(
                CommentExample(
                    "x = 1; // note??/\ny = 2;\n",
                    "// note??/\ny = 2;",
                    "Before C23 the trigraph ??/ continues a // comment.",
                    kind="line",
                    inline_compatible=True,
                ),
                CommentExample(
                    "const char *s = S(1'2'/*'*/);\n",
                    "/*'*/",
                    "Before C23 '2' is a character constant, not part of 1'2.",
                    kind="block",
                    inline_compatible=True,
                ),
            ),
            documentation_source=("ISO/IEC 9899:1999 5.1.1.2 and 6.4.9; " + _GCC_LANG_DEFAULTS),
        ),
        CommentLanguageVersion(
            name="c23",
            aliases=("c2x", "iso9899:2024"),
            span="C23 (ISO/IEC 9899:2024)",
            comment_rules=(
                "/* */ and // comments with backslash-newline splicing. "
                "Trigraphs are removed and ' is a digit separator."
            ),
        ),
    ),
)

_CPP_LANGUAGE_VERSIONS = CommentLanguageVersions(
    languages=("c++", "objective_cpp", "objective_c_plus_plus", "cuda"),
    default="cpp17",
    notes=(
        "Objective-C++ and CUDA C++ are lexed by the C++ front end at the "
        "selected C++ edition. HIP keeps its reviewed HIP-Clang scanner."
    ),
    versions=(
        CommentLanguageVersion(
            name="cpp98",
            aliases=("c++98", "c++03", "cpp03"),
            span="ISO C++98 and C++03",
            comment_rules=(
                "// and non-nested /* */ comments with trigraph and backslash "
                "splices; no raw string literals or digit separators."
            ),
            regex_patterns=_C_TRIGRAPH_PATTERNS,
            lexical_profile="c-without-digit-separators",
            examples=(
                CommentExample(
                    'S(R"(a" /* note */ )");\n',
                    "/* note */",
                    'Before C++11, R"( is the identifier R and a string literal.',
                    kind="block",
                    inline_compatible=True,
                ),
            ),
            documentation_source=(
                "https://github.com/cplusplus/draft/blob/n4140/source/compatibility.tex "
                "([diff.cpp03.lex]: raw string prefixes change valid C++03 code); "
                + _GCC_LANG_DEFAULTS
            ),
        ),
        CommentLanguageVersion(
            name="cpp11",
            aliases=("c++11", "c++0x"),
            span="C++11",
            comment_rules=(
                "As cpp98 plus raw string literals, whose content is not a "
                "comment; ' never separates digits."
            ),
            regex_patterns=_C_TRIGRAPH_PATTERNS,
            lexical_profile="cpp-raw-strings-without-digit-separators",
            examples=(
                CommentExample(
                    "const char *s = S(1'2'/*'*/);\n",
                    "/*'*/",
                    "Before C++14 '2' is a character literal, not part of 1'2.",
                    kind="block",
                    inline_compatible=True,
                ),
            ),
            documentation_source=(
                "https://github.com/cplusplus/draft/blob/n4140/source/compatibility.tex "
                "([diff.cpp11.lex]: digit separators change valid C++11 code)"
            ),
        ),
        CommentLanguageVersion(
            name="cpp14",
            aliases=("c++14", "c++1y"),
            span="C++14",
            comment_rules="As cpp11 plus ' digit separators; trigraphs still apply.",
            regex_patterns=_C_TRIGRAPH_PATTERNS,
            examples=(
                CommentExample(
                    "x = 1; // note??/\ny = 2;\n",
                    "// note??/\ny = 2;",
                    "Before C++17 the trigraph ??/ continues a // comment.",
                    kind="line",
                    inline_compatible=True,
                ),
            ),
            documentation_source=(
                "https://github.com/cplusplus/draft/blob/n4659/source/compatibility.tex "
                "([diff.cpp14.lex]: trigraph removal changes comments)"
            ),
        ),
        CommentLanguageVersion(
            name="cpp17",
            aliases=("c++17", "c++1z", "c++20", "c++2a", "cpp20"),
            span="C++17 and C++20",
            comment_rules=(
                "// and non-nested /* */ comments; a backslash immediately "
                "before a newline splices; no trigraphs."
            ),
        ),
        CommentLanguageVersion(
            name="cpp23",
            aliases=("c++23", "c++2b", "c++26", "c++2c", "cpp26"),
            span="C++23 and the C++26 working draft",
            comment_rules=(
                "As cpp17, but whitespace may separate the splicing backslash from the newline."
            ),
            regex_patterns=(_c_block_pattern(_CPP23_SPLICE), _c_line_pattern(_CPP23_SPLICE)),
            examples=(
                CommentExample(
                    "x = 1; // note \\ \ny = 2;\n",
                    "// note \\ \ny = 2;",
                    "C++23 splices a backslash followed by spaces and a newline.",
                    kind="line",
                    inline_compatible=True,
                ),
            ),
            documentation_source=(
                "https://github.com/cplusplus/draft/blob/n4950/source/lex.tex "
                "([lex.phases] phase 2, P2223)"
            ),
        ),
    ),
)


_C_STYLE_BLOCK = r"\/\*[\S\s]*?\*\/"
_C_STYLE_LINE = r"/{2}[^\r\n]*"

_GLSL_LANGUAGE_VERSIONS = CommentLanguageVersions(
    languages=("glsl",),
    default="glsl110",
    notes=(
        "Shaders declare their version with a #version directive. GLSL below "
        "4.20 with GL_ARB_shading_language_420pack behaves like glsl420."
    ),
    versions=(
        CommentLanguageVersion(
            name="glsl110",
            aliases=("110", "120", "130", "140", "150", "330", "400", "410", "100", "100es"),
            span="Desktop GLSL 1.10 to 4.10 and GLSL ES 1.00",
            comment_rules=(
                "// to the end of the line and non-nested /* */; there is no line "
                "continuation, so a trailing backslash does not extend a comment."
            ),
        ),
        CommentLanguageVersion(
            name="glsl420",
            aliases=("420", "430", "440", "450", "460", "300es", "310es", "320es"),
            span="Desktop GLSL 4.20 and later, GLSL ES 3.00 and later",
            comment_rules=(
                "// and non-nested /* */ after backslash-newline continuation, so a "
                "// comment ending in a backslash includes the next line."
            ),
            regex_patterns=_C_SPLICE_PATTERNS,
            examples=(
                CommentExample(
                    "float y = x; // note \\\n    y = 2.0 * y;\n",
                    "// note \\\n    y = 2.0 * y;",
                    "GLSL 4.20 line continuation precedes comment removal.",
                    kind="line",
                    inline_compatible=True,
                ),
            ),
            documentation_source=(
                "https://github.com/KhronosGroup/OpenGL-Registry/blob/"
                "6af574a14089ccfee87efe230ebcdd8742859813/specs/gl/GLSLangSpec.4.20.pdf "
                "(3.3: line continuation precedes comments); glslang 15.0.0 "
                "ParseHelper.cpp lineContinuationCheck"
            ),
        ),
    ),
)

_HACK_LANGUAGE_VERSIONS = CommentLanguageVersions(
    languages=("hack",),
    default="hhvm4.133",
    notes="HHVM 4.81 to 4.131 could disable # comments with disallow_hash_comments.",
    versions=(
        CommentLanguageVersion(
            name="hhvm4.131",
            aliases=("hhvm3", "hhvm4.0", "hhvm4.80", "hhvm4.81"),
            release="0",
            span="Hack as shipped with HHVM 3.x through 4.131",
            comment_rules="//, # to the end of the line, and non-nested /* */.",
            regex_patterns=(_C_STYLE_BLOCK, _C_STYLE_LINE, r"#[^\r\n]*"),
            examples=(
                CommentExample(
                    "$x = 1; # note\n$y = 2;\n",
                    "# note",
                    "HHVM up to 4.131 lexes # comments as trivia.",
                    kind="line",
                    inline_compatible=True,
                    grouped_line_compatible=True,
                ),
            ),
            documentation_source=(
                "https://github.com/facebook/hhvm/blob/HHVM-4.131.0/hphp/hack/src/"
                "parser/core/lexer.rs (scan_php_trivium: scan_hash_comment)"
            ),
        ),
        CommentLanguageVersion(
            name="hhvm4.133",
            aliases=("hhvm4.134", "hhvm4.150", "current"),
            release="4.133",
            span="HHVM 4.133 and later",
            comment_rules="Only // and non-nested /* */; # is a Hash token.",
        ),
    ),
)

_STAN_LANGUAGE_VERSIONS = CommentLanguageVersions(
    languages=("stan",),
    default="2.33",
    versions=(
        CommentLanguageVersion(
            name="2.32",
            aliases=("stanc2",),
            release="0",
            span="Stan language up to 2.32 (stanc2 and stanc3 through v2.32.x)",
            comment_rules=(
                "//, non-nested /* */, and deprecated # line comments; #include is "
                "an include directive, not a comment."
            ),
            regex_patterns=(_C_STYLE_BLOCK, _C_STYLE_LINE, r"#(?!include\b)[^\r\n]*"),
            examples=(
                CommentExample(
                    "int<lower=0> N;  # note\nvector[N] y;\n",
                    "# note",
                    "Stan up to 2.32 accepts # line comments.",
                    kind="line",
                    inline_compatible=True,
                    grouped_line_compatible=True,
                ),
            ),
            documentation_source=(
                "https://github.com/stan-dev/stanc3/blob/v2.32.2/src/frontend/lexer.mll "
                "(# comment rule with deprecation warning); v2.33.0 "
                "Deprecation_removals.ml"
            ),
        ),
        CommentLanguageVersion(
            name="2.33",
            release="2.33",
            span="Stan 2.33 and later",
            comment_rules="Only // and non-nested /* */; # comments are an error.",
        ),
    ),
)

_PHP8_HTML_PATTERNS = (r"\/\*[\S\s]*?\*\/", r"/{2}.*", r"#(?!\[).*")

_SSH_CONFIG_PATTERNS = (
    r"(?m)(?<=^[ \t]*)#[^\r\n]*",
    r"(?m)(?<=[ \t])"
    r"(?<!^[ \t]*(?i:proxycommand|localcommand|remotecommand|knownhostscommand)\b[^\r\n]*)"
    r"#[^\r\n]*",
)
_ORG_COMMENT_BLOCK = r"(?ims)(?<=^[ \t]*)#\+begin_comment\b.*?^[ \t]*#\+end_comment\b[^\r\n]*"

COMMENT_SYNTAXES: Tuple[CommentSyntax, ...] = (
    CommentSyntax(
        family_name="two_dimensional_array_style",
        canonical_name="two_dimensional_array",
        aliases=("2_dimensional_array",),
        regex_patterns=(r"(?m)^[#/][^\r\n]*",),
        sanitizer_line_wrappers=(("//", ""), ("#", "")),
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
            "https://github.com/gemrb/gemrb/blob/master/gemrb/plugins/2DAImporter/2DAImporter.cpp"
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
        documentation_source=("https://apiblueprint.org/documentation/specification.html"),
        implementation_source=("https://github.com/apiaryio/api-blueprint/issues/263"),
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
        documentation_source=("https://www.ibiblio.org/apollo/assembly_language_manual.html"),
        implementation_source=("https://github.com/virtualagc/virtualagc/blob/master/yaYUL/Pass.c"),
        confidence="verified",
        notes="The yaYUL assembler treats everything following # as a comment.",
    ),
    CommentSyntax(
        family_name="arc_style",
        canonical_name="arc",
        regex_patterns=(r";[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                '(do ; note\n  (prn "hello"))',
                "; note",
                "Arc semicolon line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="https://arclanguage.github.io/tut-stable.html",
        implementation_source=(
            "https://github.com/arclanguage/anarki/blob/master/lib/tests/parser-test.arc"
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
                '<%-- note --%>\n<asp:Label runat="server" />',
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
            "https://github.com/textmate/asp.tmbundle/blob/master/Syntaxes/HTML-ASP.plist"
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
            "https://github.com/beefytech/Beef/blob/master/IDEHelper/Compiler/BfParser.cpp"
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
        documentation_source=("https://berry.readthedocs.io/en/latest/source/en/Chapter-1.html"),
        implementation_source=("https://github.com/berry-lang/berry/blob/master/src/be_lexer.c"),
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
            "https://github.com/speced/bikeshed/blob/main/bikeshed/h/parser/parser.py"
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
            "https://github.com/blitz-research/blitz3d/blob/master/compiler/toker.cpp"
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
        sanitizer_line_wrappers=(("'", ""),),
        sanitizer_block_wrappers=(("Rem", "End Rem"), ("Rem", "EndRem")),
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
                'Rem\nnote\nEnd Rem\nPrint "done"',
                "Rem\nnote\nEnd Rem",
                "BlitzMax Rem block comment.",
                kind="block",
            ),
        ),
        documentation_source="https://blitzmax.org/docs/en/language/comments/",
        implementation_source=("https://github.com/bmx-ng/bcc/blob/master/toker.bmx"),
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
            "https://github.com/B-Lang-org/bsc/blob/main/doc/BSV_ref_guide/BSV_lang.tex"
        ),
        implementation_source=(
            "https://github.com/B-Lang-org/bsc/blob/main/src/comp/SystemVerilogPreprocess.lhs"
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
        documentation_source=("https://github.com/boo-lang/boo/wiki/Language-guide%3A-comments"),
        implementation_source=(
            "https://github.com/boo-lang/boo/blob/master/src/Boo.Lang.Parser/boo.g"
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
        aliases=("daslang",),
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
                "var value:int;\n/* outer /* note */ outer */\nassume value > 0;",
                "/* outer /* note */ outer */",
                "Boogie nested block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        documentation_source=("https://boogie-docs.readthedocs.io/en/latest/LangRef.html#comments"),
        implementation_source=(
            "https://github.com/boogie-org/boogie/blob/master/Source/Core/BoogiePL.atg"
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
            "https://github.com/rokucommunity/brighterscript/blob/master/docs/readme.md"
        ),
        implementation_source=(
            "https://github.com/rokucommunity/brighterscript/blob/master/src/lexer/Lexer.ts"
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
        documentation_source=("https://developer.roku.com/dev/docs/expressions-variables-types"),
        implementation_source=(
            "https://github.com/rokucommunity/brighterscript/blob/master/src/lexer/Lexer.ts"
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
        documentation_source=("https://github.com/browserslist/browserslist#browserslistrc"),
        implementation_source=("https://github.com/browserslist/browserslist/blob/main/node.js"),
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
        implementation_source=("https://github.com/onflow/cadence/blob/master/parser/comment.go"),
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
        documentation_source=("https://cartocss.readthedocs.io/en/latest/language_elements.html"),
        implementation_source=("https://github.com/cartocss/carto/blob/master/lib/carto/parser.js"),
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
            "https://web.mit.edu/ceylon_v1.3.3/ceylon-1.3.3/doc/en/spec/html_single/#comments"
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
            "https://chapel-lang.org/docs/language/spec/lexical-structure.html#comments"
        ),
        implementation_source=(
            "https://github.com/chapel-lang/chapel/blob/main/frontend/lib/parsing/lexer-help.h"
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
                ".method public static void Main() cil managed {\n  ret // note\n}",
                "// note",
                "ILAsm slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                ".method public static void Main() cil managed {\n  /* note */\n  ret\n}",
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
            "https://github.com/dotnet/runtime/blob/main/src/coreclr/ilasm/grammar_after.cpp"
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
        documentation_source=("https://clarion.help/doku.php?id=special_characters.htm"),
        implementation_source=(
            "https://github.com/fushnisoft/SublimeClarion/blob/master/clarion.configuration.json"
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
        sanitizer_line_wrappers=(
            ("<%' ", "%>"),
            ("<%' ", ""),
            ("<%'", "%>"),
            ("<%'", ""),
            ("<% Rem ", "%>"),
            ("<% Rem ", ""),
            ("'*", ""),
            ("'", ""),
        ),
        sanitizer_block_wrappers=(("<!--", "-->"),),
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
        documentation_source=("https://clean.cs.ru.nl/download/doc/CleanLangRep.2.2.pdf"),
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
        documentation_source=("https://github.com/kohler/click/blob/master/doc/click.5"),
        implementation_source=("https://github.com/kohler/click/blob/master/lib/lexer.cc"),
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
                '(defrule example ; note\n  =>\n  (printout t "ok" crlf))',
                "; note",
                "CLIPS semicolon line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=("https://www.clipsrules.net/documentation/v642/bpg642.pdf"),
        implementation_source=("https://github.com/noxdafox/clips/blob/master/core/scanner.c"),
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
            "vue",
            "hack",
            "less",
            "groovy",
            "genie",
            "processing",
            "apex",
            "cuda",
            "scilab",
            "antlr",
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
            "cypher",
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
            "hip",
            "ispc",
            "zmodel",
            "overpassql",
            "tact",
        ),
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r"/{2}[^\r\n]*",
        ),
        language_excluded_comment_prefixes=(("c", ("/*!re2c",)),),
        # C11 5.1.1.2: line splicing (translation phase 2) precedes comment
        # removal (phase 3), so a backslash-newline continues a // comment.
        language_regex_patterns=(
            # C11 5.1.1.2: line splicing (translation phase 2) precedes comment
            # removal (phase 3), so a backslash-newline continues a // comment.
            *(
                (language, _C_SPLICE_PATTERNS)
                for language in (
                    "c",
                    "c++",
                    "cuda",
                    "objective-c",
                    "objective_c_plus_plus",
                    "objective_cpp",
                )
            ),
            # ECMA-262 12.3: LineTerminator includes U+2028 and U+2029.
            *(
                (language, (r"\/\*[\S\s]*?\*\/", r"/{2}[^\r\n\u2028\u2029]*"))
                for language in ("javascript", "jsx", "typescript", "tsx")
            ),
            # C# spec 6.3.2: new_line also includes U+0085, U+2028, and U+2029.
            *(
                (language, (r"\/\*[\S\s]*?\*\/", r"/{2}[^\r\n\x85\u2028\u2029]*"))
                for language in ("c#", "c_sharp", "csharp")
            ),
            # JLS 3.3/3.4: a \u000a or \u000d escape is a line terminator.
            (
                "java",
                (r"\/\*[\S\s]*?\*\/", r"/{2}(?:(?!\\u+000[aAdD])[^\r\n])*"),
            ),
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
        language_versions=(
            _C_LANGUAGE_VERSIONS,
            _CPP_LANGUAGE_VERSIONS,
            _GLSL_LANGUAGE_VERSIONS,
            _HACK_LANGUAGE_VERSIONS,
            _STAN_LANGUAGE_VERSIONS,
        ),
    ),
    CommentSyntax(
        family_name="kotlin_style",
        canonical_name="kotlin",
        aliases=("gradle_kotlin_dsl",),
        regex_patterns=(r"/{2}[^\r\n]*",),
        nested_delimiters=(("/*", "*/"),),
        shared_regex_examples=(
            CommentExample(
                "val value = 1 // note\nvalue",
                "// note",
                "Kotlin slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "val value = 1\n/* outer /* inner */ outer */\nvalue",
                "/* outer /* inner */ outer */",
                "Kotlin recursively nested block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://docs.gradle.org/9.6.1/userguide/kotlin_dsl.html",
        implementation_source=(
            "https://github.com/Kotlin/kotlin-spec/blob/"
            "2f7aa0524ec27e788dfacd550f144809f2e0254c/grammar/src/main/antlr/"
            "KotlinLexer.g4#L15-L22"
        ),
        confidence="verified",
        notes=(
            "Kotlin and Gradle Kotlin DSL use // line comments and recursively "
            "nested /* ... */ comments. KDoc is a block-comment subset."
        ),
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
            "CUE v0.16.1 accepts // line comments and rejects C-style /* ... */ block comments."
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
            "https://github.com/pygments/pygments/blob/2.20.0/pygments/lexers/csound.py"
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
        sanitizer_line_wrappers=(("@q", "@>"), ("//", "")),
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
        documentation_source=("https://ctan.math.illinois.edu/info/knuth/cwebman.pdf"),
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
        notes=("OpenQASM 3 supports // line comments and non-nested /* ... */ block comments."),
    ),
    CommentSyntax(
        family_name="rust_style",
        canonical_name="rust",
        aliases=("noir", "sway"),
        regex_patterns=(r"/{2}[^\r\n]*",),
        nested_delimiters=(("/*", "*/"),),
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
        ),
        shared_nested_examples=(
            CommentExample(
                "prefix\n/* outer /* nested */ tail */\nsuffix",
                "/* outer /* nested */ tail */",
                "Rust, Noir, and Sway recursively nested block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("//!", ""), ("///", ""), ("//", "")),
        sanitizer_block_wrappers=(("/*!", "*/"), ("/**", "*/"), ("/*", "*/")),
        documentation_source=("https://doc.rust-lang.org/reference/comments.html"),
        implementation_source=(
            "https://github.com/noir-lang/noir/blob/"
            "d89d99a9442295afa676633d9433291377f7d3b2/compiler/"
            "noirc_frontend/src/lexer/lexer.rs#L888-L990"
        ),
        confidence="cross-checked",
        notes=(
            "Rust, Noir, and Sway use slash line comments and recursively nested "
            "slash-star blocks. Their reviewed alias scanners preserve each "
            "language's exact line termination and literal inventory."
        ),
    ),
    CommentSyntax(
        family_name="hash_line_style",
        canonical_name="shell",
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
            "jq",
            "janet",
            "kaitai_struct",
            "kakoune_script",
            "kakounescript",
            "kvlang",
            "lookml",
            "makefile",
            "meson",
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
            "openrc_runscript",
            "open_policy_agent",
            "opentype_feature_file",
            "parrot",
            "parrot_assembly",
            "parrot_internal_representation",
            "pic",
            "protocol_buffer_text_format",
            "polar",
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
            "shellcheck_config",
            "shellsession",
            "singularity",
            "smali",
            "ssh_config",
            "sparql",
            "sed",
            "selinux_policy",
            "talon",
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
            "yasnippet",
            "zeek",
            "zimpl",
            "ragel",
            "slash",
            "edgeql",
            "hosts_file",
        ),
        regex_patterns=(r"#.*",),
        language_regex_patterns=(
            # POSIX XCU 2.3: # starts a comment only at the beginning of a word,
            # so $#, ${#x}, and a#b are not comments.
            ("shell", (r"(?<![^\s;&|()<>])#.*",)),
            # GNU make manual 3.1: a trailing backslash not escaped by another
            # backslash continues the comment across lines.
            ("makefile", (r"#(?:[^\\\r\n]|\\(?:\r?\n|[^\r\n]|\Z))*",)),
            # OpenSSH 8.7 readconf.c: argv_split ends a line at an unquoted # that
            # starts an argument; command keywords keep the raw rest of the line.
            ("ssh_config", _SSH_CONFIG_PATTERNS),
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
        language_versions=(
            CommentLanguageVersions(
                languages=("jq",),
                default="1.7",
                versions=(
                    CommentLanguageVersion(
                        name="1.7",
                        release="0",
                        span="jq 1.7.1 and earlier",
                        comment_rules="An unquoted # starts a comment to the end of the line.",
                        documentation_source=(
                            "https://github.com/jqlang/jq/blob/jq-1.7.1/src/lexer.l#L40 "
                            '("#"[^\\n]* comment rule)'
                        ),
                    ),
                    CommentLanguageVersion(
                        name="1.8",
                        aliases=("current",),
                        release="1.8",
                        span="jq 1.8.0 and later",
                        comment_rules=(
                            "An unquoted # starts a comment; an odd number of backslashes "
                            "before the line break continues it onto the next line."
                        ),
                        regex_patterns=(r"#(?:\\(?:\\|\r?\n)|\r(?!\n)|[^\r\n])*",),
                        examples=(
                            CommentExample(
                                "[\n  1,\n  # skip two \\\n  2,\n  3\n]\n",
                                "# skip two \\\n  2,",
                                "From jq 1.8, a trailing backslash continues a comment.",
                                kind="line",
                            ),
                        ),
                        documentation_source=(
                            "https://github.com/jqlang/jq/blob/jq-1.8.0/src/lexer.l#L24-L46 "
                            "(IN_COMMENT state); https://github.com/jqlang/jq/blob/jq-1.8.0/"
                            "NEWS.md (Tcl-style multiline comments)"
                        ),
                    ),
                ),
            ),
            CommentLanguageVersions(
                languages=("ssh_config",),
                default="8.7",
                notes="sshd_config command keywords such as ForceCommand are not modelled.",
                versions=(
                    CommentLanguageVersion(
                        name="8.4",
                        release="0",
                        span="OpenSSH 8.4p1 and earlier",
                        comment_rules=(
                            "Only a line whose first non-blank character is # is a "
                            "comment; a later # is an ordinary argument."
                        ),
                        regex_patterns=(r"(?m)(?<=^[ \t]*)#[^\r\n]*",),
                        examples=(
                            CommentExample(
                                "Host example # office\n# note\n",
                                "# note",
                                "Before OpenSSH 8.5, only full lines are comments.",
                                kind="line",
                                grouped_line_compatible=True,
                            ),
                        ),
                        documentation_source=(
                            "https://github.com/openssh/openssh-portable/blob/V_8_4_P1/"
                            "readconf.c#L1930-L1935 (only a keyword starting with # is "
                            "a comment)"
                        ),
                    ),
                    CommentLanguageVersion(
                        name="8.5",
                        release="8.5",
                        span="OpenSSH 8.5p1 and 8.6p1",
                        comment_rules=(
                            "Every line is cut at its first #, inside tokens, quotes, "
                            "and command values too."
                        ),
                        regex_patterns=(r"#[^\r\n]*",),
                        lexical_profile="ssh-config-8.5",
                        examples=(
                            CommentExample(
                                "Host example\n  LocalCommand echo connected # notify\n",
                                "# notify",
                                "OpenSSH 8.5 and 8.6 also cut command values at #.",
                                kind="line",
                                inline_compatible=True,
                            ),
                        ),
                        documentation_source=(
                            "https://github.com/openssh/openssh-portable/blob/V_8_5_P1/"
                            "readconf.c#L2136 (strchr(line, '#') cut)"
                        ),
                    ),
                    CommentLanguageVersion(
                        name="8.7",
                        aliases=("current",),
                        release="8.7",
                        span="OpenSSH 8.7p1 and later",
                        comment_rules=(
                            "Full-line comments, and an unquoted # at the start of an "
                            "argument; ProxyCommand, LocalCommand, RemoteCommand, and "
                            "KnownHostsCommand keep # in their value."
                        ),
                        documentation_source=(
                            "https://github.com/openssh/openssh-portable/blob/V_8_7_P1/"
                            "misc.c (argv_split terminate_on_comment); "
                            "https://github.com/openssh/openssh-portable/blob/V_8_7_P1/"
                            "readconf.c#L1319-L1333 (parse_command keeps the raw value)"
                        ),
                    ),
                ),
            ),
        ),
    ),
    CommentSyntax(
        family_name="fluent_style",
        canonical_name="fluent",
        # Fluent 1.0 EBNF CommentLine: #, ##, or ### in column 0, then a space
        # and text, or the line end.
        regex_patterns=(r"(?m)^#{1,3}(?: [^\r\n]*)?(?=\r?\n|\Z)",),
        sanitizer_line_wrappers=(("###", ""), ("##", ""), ("#", "")),
        shared_regex_examples=(
            CommentExample(
                "# note\nhello = Hello\n",
                "# note",
                "Fluent message comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "### note\nhello = Hello\n",
                "### note",
                "Fluent resource comment.",
                kind="line",
            ),
        ),
        documentation_source=(
            "https://github.com/projectfluent/fluent/blob/v1.0.0/spec/fluent.ebnf#L19"
        ),
        confidence="verified",
        notes=(
            "Comment lines start in column 0. A # inside a message value, or #word "
            "without a following space, is not a comment."
        ),
        language_versions=(
            CommentLanguageVersions(
                languages=("fluent",),
                default="1.0",
                versions=(
                    CommentLanguageVersion(
                        name="0.4",
                        release="0.3",
                        span="Fluent Syntax 0.3 and 0.4",
                        comment_rules=(
                            "Comment lines start with // in column 0; #word lines are tags."
                        ),
                        regex_patterns=(r"(?m)^//[^\r\n]*",),
                        sanitizer_line_wrappers=(("//", ""),),
                        examples=(
                            CommentExample(
                                "// note\nhello = Hello\n",
                                "// note",
                                "Fluent 0.3 and 0.4 comment lines start with //.",
                                kind="line",
                                grouped_line_compatible=True,
                            ),
                        ),
                        documentation_source=(
                            "https://github.com/projectfluent/fluent/blob/v0.4.0/spec/"
                            "fluent.ebnf#L6 (comment ::= ('//' (char - NL)* NL)+)"
                        ),
                    ),
                    CommentLanguageVersion(
                        name="1.0",
                        aliases=("current",),
                        release="0.5",
                        span="Fluent Syntax 0.5 through 1.0",
                        comment_rules=(
                            "Comment lines start in column 0 with #, ##, or ###, then a "
                            "space or the line end."
                        ),
                        documentation_source=(
                            "https://github.com/projectfluent/fluent/blob/"
                            "3dbb402ed5af6b64f5c09faeb067acff127a0f34/spec/CHANGELOG.md "
                            "(0.5.0: the comment sigil changed to #)"
                        ),
                    ),
                ),
            ),
        ),
    ),
    CommentSyntax(
        family_name="org_style",
        canonical_name="org",
        # Org manual "Comment lines": optional indentation, one # and white
        # space, and #+BEGIN_COMMENT ... #+END_COMMENT regions.
        regex_patterns=(_ORG_COMMENT_BLOCK, r"(?m)(?<=^[ \t]*)#(?=[ \t]|\r?$)[^\r\n]*"),
        shared_regex_examples=(
            CommentExample(
                "Text\n# note\nMore text\n",
                "# note",
                "Org comment line.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "Text\n  # note\nMore text\n",
                "# note",
                "Indented Org comment line.",
                kind="line",
            ),
            CommentExample(
                "Text\n#+BEGIN_COMMENT\nnote\n#+END_COMMENT\nMore text\n",
                "#+BEGIN_COMMENT\nnote\n#+END_COMMENT",
                "Org comment block.",
                kind="block",
            ),
        ),
        documentation_source=(
            "https://github.com/bzg/org-mode/blob/release_8.0/doc/org.texi#L9728-L9738"
        ),
        confidence="verified",
        notes=(
            "A # without following white space, as in Issue #42 or #+TITLE:, is not "
            "a comment. COMMENT subtrees and # lines inside source blocks are not "
            "modelled."
        ),
        language_versions=(
            CommentLanguageVersions(
                languages=("org",),
                default="8.0",
                versions=(
                    CommentLanguageVersion(
                        name="7.8",
                        release="0",
                        span="Org mode before 7.9.2",
                        comment_rules=(
                            "A line with # in column zero is a comment unless it starts "
                            "#+KEYWORD; an indented comment starts with #+ and a space. "
                            "#+BEGIN_COMMENT ... #+END_COMMENT regions are comments."
                        ),
                        regex_patterns=(
                            _ORG_COMMENT_BLOCK,
                            r"(?m)^#(?!\+\S)[^\r\n]*",
                            r"(?m)(?<=^[ \t]+)#\+[ \t][^\r\n]*",
                        ),
                        examples=(
                            CommentExample(
                                "#todo tighten wording\nText\n",
                                "#todo tighten wording",
                                "Before Org 7.9.2, # in column zero starts a comment.",
                                kind="line",
                                grouped_line_compatible=True,
                            ),
                        ),
                        documentation_source=(
                            "https://github.com/bzg/org-mode/blob/release_7.8.11/doc/"
                            "org.texi#L8985-L8995"
                        ),
                    ),
                    CommentLanguageVersion(
                        name="8.0",
                        aliases=("current",),
                        release="7.9.2",
                        span="Org mode 7.9.2 and later",
                        comment_rules=(
                            "Optional indentation, one #, and white space or the line "
                            "end; #+BEGIN_COMMENT ... #+END_COMMENT regions."
                        ),
                        documentation_source=(
                            "https://github.com/bzg/org-mode/blob/main/etc/ORG-NEWS "
                            "(Version 7.9.2: the space after # is mandatory); "
                            "https://github.com/bzg/org-mode/blob/release_8.0/doc/"
                            "org.texi#L9728-L9738"
                        ),
                    ),
                ),
            ),
        ),
    ),
    CommentSyntax(
        family_name="mcfunction_style",
        canonical_name="mcfunction",
        # A trimmed function line starting with # is a comment. From 1.20.2 a
        # trailing backslash joins the next line first, comment lines included.
        regex_patterns=(
            r"(?m)(?<=^[ \t]*)(?<!\\[ \t]*\r?\n[ \t]*)#(?:[^\r\n]*\\[ \t]*\r?\n)*[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "say hi\n# note\nsay bye\n",
                "# note",
                "Function comment line.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://github.com/SpyglassMC/Spyglass/blob/"
            "c1c7894a864c1397a1ec281227e25e71a20a8ea1/packages/mcfunction/src/"
            "parser/entry.ts#L57-L65"
        ),
        confidence="cross-checked",
        notes=(
            "A # later in a line, as in a #namespace:tag reference, is not a comment. "
            "A line continued from a line ending in a backslash is not a comment."
        ),
        language_versions=(
            CommentLanguageVersions(
                languages=("mcfunction",),
                default="1.20.2",
                versions=(
                    CommentLanguageVersion(
                        name="1.20.1",
                        release="0",
                        span="Minecraft Java Edition function files before 1.20.2",
                        comment_rules=(
                            "A trimmed line starting with # is a comment and ends at "
                            "its line break; there is no line continuation."
                        ),
                        regex_patterns=(r"(?m)(?<=^[ \t]*)#[^\r\n]*",),
                        examples=(
                            CommentExample(
                                "# note \\\nsay shown\n",
                                "# note \\",
                                "Before 1.20.2, a function comment ends at its line break.",
                                kind="line",
                            ),
                        ),
                        documentation_source=(
                            "Decompiled 1.20.1 CommandFunction.fromLines (third-party "
                            "mirror: https://github.com/Blackjack200/"
                            "minecraft_client_1_20_1, net/minecraft/commands/"
                            "CommandFunction.java#L33-L40)"
                        ),
                    ),
                    CommentLanguageVersion(
                        name="1.20.2",
                        aliases=("current",),
                        release="1.20.2",
                        span="Minecraft Java Edition 1.20.2 (23w31a) and later",
                        comment_rules=(
                            "Lines ending in a backslash are joined to the next line "
                            "before the # test, so a comment line ending in a "
                            "backslash also covers the next line."
                        ),
                        examples=(
                            CommentExample(
                                "# note \\\nsay hidden\nsay shown\n",
                                "# note \\\nsay hidden",
                                "From 1.20.2, a trailing backslash continues a comment line.",
                                kind="line",
                            ),
                        ),
                        documentation_source=(
                            "Decompiled 1.21.1 CommandFunction.fromLines (third-party "
                            "mirror: https://github.com/hackersense/OptiFine-Source/blob/"
                            "b77c5c6995874f6cf2755bc5234428906b337b75/1.21.1/net/"
                            "minecraft/commands/functions/CommandFunction.java#L37-L71)"
                        ),
                    ),
                ),
            ),
        ),
    ),
    CommentSyntax(
        family_name="picolisp_style",
        canonical_name="picolisp",
        regex_patterns=(r"#(?!\{)[^\r\n]*",),
        nested_delimiters=(("#{", "}#"),),
        shared_regex_examples=(
            CommentExample(
                "(setq X 1) # note\n(setq Y 2)",
                "# note",
                "PicoLisp line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        canonical_nested_examples=(
            CommentExample(
                "(setq X 1) #{ outer #{ inner }# outer }# (setq Y 2)",
                "#{ outer #{ inner }# outer }#",
                "Nested PicoLisp block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://github.com/pahihu/picoLisp/blob/"
            "9c68fc01bae3b8b61a25a7ac5621f30b28adf874/src/io.c#L1157-L1180"
        ),
        confidence="verified",
        notes="Block comments #{ ... }# nest from picoLisp 18.6.",
        language_versions=(
            CommentLanguageVersions(
                languages=("picolisp",),
                default="18.6",
                versions=(
                    CommentLanguageVersion(
                        name="2.3.6",
                        release="0",
                        span="picoLisp releases before 2.3.7",
                        comment_rules="# to the end of the line only; #{ has no special meaning.",
                        regex_patterns=(r"#[^\r\n]*",),
                        nested_delimiters=(),
                        examples=(
                            CommentExample(
                                "(setq X 1) #{ note }# (setq Y 2)\n",
                                "#{ note }# (setq Y 2)",
                                "Before 2.3.7, #{ starts an ordinary line comment.",
                                kind="line",
                                inline_compatible=True,
                            ),
                        ),
                        documentation_source=(
                            "https://github.com/picolisp/picolisp/blob/master/CHANGES "
                            "(30jun09 picoLisp-2.3.7: multi-line block comments)"
                        ),
                    ),
                    CommentLanguageVersion(
                        name="2.3.7",
                        release="2.3.7",
                        span="picoLisp 2.3.7 through 17.12",
                        comment_rules=(
                            "# to the end of the line and #{ ... }# block comments that "
                            "close at the first }#."
                        ),
                        regex_patterns=(r"#(?!\{)[^\r\n]*", r"#\{[\S\s]*?\}#"),
                        nested_delimiters=(),
                        sanitizer_block_wrappers=(("#{", "}#"),),
                        examples=(
                            CommentExample(
                                "#{ outer #{ inner }# outer }#\n",
                                "#{ outer #{ inner }#",
                                "Before 18.6, block comments do not nest.",
                                kind="block",
                                inline_compatible=True,
                            ),
                        ),
                        documentation_source=(
                            "https://github.com/picolisp/picolisp/blob/master/src/io.c"
                            "#L1021-L1040 (picoLisp 16.12 comment(): the first }# closes)"
                        ),
                    ),
                    CommentLanguageVersion(
                        name="18.6",
                        aliases=("pil21", "current"),
                        release="18.6",
                        span="picoLisp 18.6 and later, including pil21",
                        comment_rules="# to the end of the line and nested #{ ... }# blocks.",
                        documentation_source=(
                            "https://github.com/pahihu/picoLisp/blob/"
                            "9c68fc01bae3b8b61a25a7ac5621f30b28adf874/CHANGES "
                            "(28jun18 picoLisp-18.6: nested block comments)"
                        ),
                    ),
                ),
            ),
        ),
    ),
    CommentSyntax(
        family_name="tcl_style",
        canonical_name="tcl",
        # Tcl(n) rule [10]: # starts a comment only where Tcl expects the first
        # word of a command: at line start, or after ; [ or {.
        regex_patterns=(r"(?m)(?<=(?:^|[;\[{])[ \t]*)#.*",),
        sanitizer_line_wrappers=(("#", ""),),
        shared_regex_examples=(
            CommentExample(
                "# note\nputs ok",
                "# note",
                "Comment at the start of a command.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "set x 1 ;# note\nputs $x",
                "# note",
                "Comment after a command separator.",
                kind="line",
            ),
        ),
        documentation_source="https://www.tcl-lang.org/man/tcl/TclCmd/Tcl.htm",
        confidence="verified",
        notes=(
            "A # is a comment only where a command is expected; inside a command's "
            "arguments, as in set x #y, it is ordinary text."
        ),
    ),
    CommentSyntax(
        family_name="dockerfile_style",
        canonical_name="dockerfile",
        regex_patterns=(r"(?m)(?<=^[ \t]*)#.*",),
        shared_regex_examples=(
            CommentExample(
                "FROM alpine\n# note\nRUN true",
                "# note",
                "Dockerfile comment line.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "FROM alpine\n  # note\nRUN true",
                "# note",
                "Dockerfile comment after leading whitespace.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source="https://docs.docker.com/reference/dockerfile/#format",
        confidence="verified",
        notes=(
            "Docker treats lines that begin with # as comments, after optional "
            "leading whitespace. A # marker anywhere else in a line is passed "
            "through as an argument."
        ),
    ),
    CommentSyntax(
        family_name="ignore_list_style",
        canonical_name="ignore_list",
        # git dir.c add_patterns_from_buffer skips a UTF-8 byte order mark.
        regex_patterns=(r"(?m)(?:^|(?<=\A\ufeff))#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "# note\n*.log",
                "# note",
                "Ignore-list comment beginning at the first byte of a line.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://git-scm.com/docs/gitignore#Documentation/gitignore.txt-_PATTERN_FORMAT"
        ),
        confidence="verified",
        notes=(
            "A leading # begins a comment. Escaped hashes, indented hashes, "
            "and hashes later in a pattern are pattern data."
        ),
    ),
    CommentSyntax(
        family_name="slash_line_style",
        canonical_name="qsharp",
        aliases=(
            "q_sharp",
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
            "hare",
            "kerboscript",
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
        family_name="go_directive_file_style",
        canonical_name="go_module",
        aliases=("go_workspace",),
        regex_patterns=(r"/{2}[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "go 1.25\n// note\nuse ./module",
                "// note",
                "Go module and workspace line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://github.com/golang/mod/blob/"
            "792ac169a90372d88fb14e712cb793061ba0c104/modfile/work.go#L31-L45"
        ),
        implementation_source=(
            "https://github.com/golang/mod/blob/"
            "792ac169a90372d88fb14e712cb793061ba0c104/modfile/read.go#L510-L552"
        ),
        confidence="verified",
        notes=(
            "go.mod and go.work share the modfile lexer. It accepts // comments "
            "and explicitly rejects /* ... */ comments."
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
            r"#(?:[^\r\n]|\r(?!\n))*",
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
        # IEEE 1076-2008 15.9: VHDL-2008 adds delimited /* */ comments.
        language_regex_patterns=(("vhdl", (r"--.*", r"\/\*[\S\s]*?\*\/")),),
        sanitizer_block_wrappers=(("/*", "*/"),),
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
        aliases=(
            "elm",
            "frege",
            "grammatical_framework",
            "literate_agda",
            "untyped_plutus_core",
        ),
        regex_patterns=(r"--.*",),
        nested_delimiters=(("{-", "-}"),),
        sanitizer_line_wrappers=(("--", ""),),
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
                "(program 1.1.0 -- uplc note\n  (lam x x))",
                "-- uplc note",
                "Untyped Plutus Core unconditional dash comment.",
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
            CommentExample(
                "(program 1.1.0 {- outer {- uplc note -} tail -} (lam x x))",
                "{- outer {- uplc note -} tail -}",
                "Untyped Plutus Core nested whitespace comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        notes=(
            "The Untyped Plutus Core alias is pinned to Plutus commit "
            "3e257708aea5705074ae5a9687e0d97d66a954f2, whose shared parser "
            "uses unconditional -- comments and nested {- -} comments."
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
            "dune",
            "firrtl",
            "pact",
            "pddl",
        ),
        regex_patterns=(r";[^\r\n]*",),
        # R7RS 2.2: #; comments out the next datum.
        language_regex_patterns=(
            (
                "scheme",
                (
                    r";[^\r\n]*",
                    r'#;\s*(?P<d>(?:[\'`,]|,@)*(?:\((?:[^()\[\]"\\;]|"(?:\\[\s\S]|[^"\\])*"|\\[\s\S]|;[^\r\n]*|(?&d))*\)|\[(?:[^()\[\]"\\;]|"(?:\\[\s\S]|[^"\\])*"|\\[\s\S]|;[^\r\n]*|(?&d))*\]|"(?:\\[\s\S]|[^"\\])*"|[^\s()\[\]";]+))',
                ),
            ),
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
        ),
    ),
    CommentSyntax(
        family_name="module_management_system_style",
        canonical_name="module_management_system",
        regex_patterns=(r"(?m)(?<!\S)[#!][^\r\n]*",),
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
        sanitizer_line_wrappers=((";", ""),),
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
            "https://ltwiki.org/LTspiceHelp/LTspiceHelp/A_General_Structure_and_Conventions.htm"
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
        documentation_source=("https://docs.netlify.com/manage/routing/redirects/overview/"),
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
            "https://github.com/antlr/stringtemplate4/blob/master/doc/cheatsheet.md"
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
        sanitizer_line_wrappers=(
            (";/*++", ""),
            (";/*--", ""),
            (";--*/", ""),
            ("; //", ""),
            (";//", ""),
            (";", "*/"),
            (";/*", ""),
            (";*/", ""),
            (";", ""),
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
            "https://learn.microsoft.com/en-us/windows/win32/eventlog/message-text-files"
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
        sanitizer_line_wrappers=(("#", ""),),
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
        sanitizer_line_wrappers=((".!", ""), (".;", ""), ("!", "")),
        shared_regex_examples=(
            CommentExample(
                ".LEFT MARGIN 0.RIGHT MARGIN 60!note;.SKIP",
                "!note",
                "RUNOFF inline comment flag.",
                kind="line",
                inline_compatible=True,
            ),
            CommentExample(
                ".!note\n.LEFT MARGIN 0",
                ".!note",
                "RUNOFF control/comment flag pair at line start.",
                kind="directive",
            ),
        ),
        documentation_source=(
            "https://docs.vmssoftware.com/digital-standard-runoff-reference-manual/"
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
        sanitizer_line_wrappers=(("!", ""),),
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
            "https://xorg.freedesktop.org/archive/X11R7.5/doc/man/man1/mkfontdir.1.html"
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
        aliases=("ocaml", "rocq", "rocq_prover"),
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
        canonical_nested_examples=(
            CommentExample(
                '(* outer "quoted "" *) still quoted" tail *)',
                '(* outer "quoted "" *) still quoted" tail *)',
                "Coq/Rocq quoted span shielding inside a nested comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://github.com/github-linguist/linguist/commit/"
            "4b9ec2834bd069758bb2ec766997bb2070fe61d2"
        ),
        implementation_source=(
            "https://github.com/rocq-prover/rocq/blob/"
            "d3971a897c7e578afd920eac4c1fcbb666c67ead/"
            "parsing/cLexer.ml#L402-L436"
        ),
        confidence="verified",
        notes=(
            "Rocq Prover is the current Stack label for Coq and retains its "
            "nested (* ... *) comments. Coq/Rocq quoted spans shield delimiters "
            "inside comments; OCaml lexes its string, character, and quoted "
            "string literals inside comments."
        ),
        language_versions=(
            CommentLanguageVersions(
                languages=("ocaml",),
                default="4.11",
                versions=(
                    CommentLanguageVersion(
                        name="4.01",
                        release="0",
                        span="OCaml 4.01 and earlier",
                        comment_rules=(
                            "Nested (* *) comments; string and character literals are "
                            "lexed inside comments, and {| has no meaning."
                        ),
                        nested_delimiters=(),
                        contextual_extractor="ocaml_401_comments",
                        sanitizer_block_wrappers=(("(*", "*)"),),
                        examples=(
                            CommentExample(
                                "(* {| *) let x = 1 (* |} *)\n",
                                "(* {| *)",
                                "Before OCaml 4.02, {| inside a comment is ordinary text.",
                                kind="block",
                                inline_compatible=True,
                            ),
                        ),
                        documentation_source=(
                            "https://github.com/ocaml/ocaml/blob/4.01.0/parsing/lexer.mll "
                            "(the comment rule lexes strings but has no { rule)"
                        ),
                    ),
                    CommentLanguageVersion(
                        name="4.02",
                        release="4.02",
                        span="OCaml 4.02 through 4.10",
                        comment_rules=(
                            "As 4.01, plus quoted strings {id|...|id} lexed in and "
                            "outside comments."
                        ),
                        nested_delimiters=(),
                        contextual_extractor="ocaml_402_comments",
                        sanitizer_block_wrappers=(("(*", "*)"),),
                        examples=(
                            CommentExample(
                                "(* {%ext| *) let y = 2 (* |} *)\n",
                                "(* {%ext| *)",
                                "Before OCaml 4.11, {%ext| inside a comment is ordinary text.",
                                kind="block",
                                inline_compatible=True,
                            ),
                        ),
                        documentation_source=(
                            "https://github.com/ocaml/ocaml/blob/4.02.0/parsing/lexer.mll "
                            '(comment rule: "{" lowercase* "|" starts a quoted string)'
                        ),
                    ),
                    CommentLanguageVersion(
                        name="4.11",
                        aliases=("5.x", "current"),
                        release="4.11",
                        span="OCaml 4.11 and later, including 5.x",
                        comment_rules=(
                            "As 4.02, plus quoted extensions {%ext|...|} and {%%ext id|...|id}."
                        ),
                        examples=(
                            CommentExample(
                                "(* {%ext| *) let y = 2 (* |} *)\n",
                                "(* {%ext| *) let y = 2 (* |} *)",
                                "From OCaml 4.11, a quoted extension is lexed inside a comment.",
                                kind="nested",
                                inline_compatible=True,
                            ),
                        ),
                        documentation_source=(
                            "https://github.com/ocaml/ocaml/blob/4.11.0/parsing/lexer.mll "
                            "(comment rule: quoted extensions)"
                        ),
                    ),
                ),
            ),
        ),
    ),
    CommentSyntax(
        family_name="d_style",
        canonical_name="d",
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r"\/\/[^\r\n]*",
        ),
        nested_delimiters=(("/+", "+/"),),
        shared_regex_examples=(
            CommentExample(
                "prefix\n// note\nsuffix",
                "// note",
                "Line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "prefix\n/// note\nsuffix",
                "/// note",
                "Triple-slash doc comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "prefix\n/* note */\nsuffix",
                "/* note */",
                "Non-nesting block comment.",
                kind="block",
                inline_compatible=True,
            ),
            CommentExample(
                "prefix\n/** note */\nsuffix",
                "/** note */",
                "Block doc comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "before /+ outer /+ inner +/ outer +/ after",
                "/+ outer /+ inner +/ outer +/",
                "Nesting block comment.",
                kind="nested",
                inline_compatible=True,
            ),
            CommentExample(
                "prefix\n/++ note +/\nsuffix",
                "/++ note +/",
                "Plus-delimited doc comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://dlang.org/spec/lex.html#comment",
        confidence="verified",
        notes=(
            "D has // line comments, non-nesting /* */ block comments, and "
            "nesting /+ +/ block comments; doc comments are subsets of each."
        ),
    ),
    CommentSyntax(
        family_name="pascal_style",
        canonical_name="pascal",
        aliases=("oxygene",),
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
        family_name="portugol_style",
        canonical_name="portugol",
        regex_patterns=(
            r"/\*[\S\s]*?\*/",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "programa {\n  // note\n  funcao inicio() {}\n}",
                "// note",
                "Portugol Studio line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "programa {\n  /* note */\n  funcao inicio() {}\n}",
                "/* note */",
                "Portugol Studio block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://github.com/UNIVALI-LITE/Portugol-Studio/wiki/A-Linguagem-Portugol#comentários"
        ),
        implementation_source=("https://github.com/UNIVALI-LITE/Portugol-Studio"),
        confidence="cross-checked",
        notes=(
            "Portugol Studio uses // and /* ... */ comments. Program bodies use "
            "braces, so Portugol must not inherit Pascal brace comments."
        ),
    ),
    CommentSyntax(
        family_name="percent_style",
        canonical_name="erlang",
        aliases=("bibtex", "bibtex_style", "charity", "postscript", "tex"),
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
        aliases=("f*",),
        contextual_extractor="f_star_comments",
        shared_contextual_examples=(
            CommentExample(
                "let x = 1 // note\nin x",
                "// note",
                "F* line comment outside literals and compatibility markers.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "let x = 1\n(* outer (* inner *) outer *)\nin x",
                "(* outer (* inner *) outer *)",
                "F* nested block comment.",
                kind="nested",
                inline_compatible=True,
            ),
            CommentExample(
                "let x = 1\n(* accepted through EOF",
                "(* accepted through EOF",
                "F* lexer-accepted EOF block comment.",
                kind="nested",
                inline_compatible=True,
                consumes_eof=True,
            ),
        ),
        sanitizer_line_wrappers=(("//", ""),),
        sanitizer_block_wrappers=(("(*", "*)"),),
        unclosed_block_openers=("(*",),
        documentation_source=(
            "https://fstar-lang.org/tutorial/book/part1/part1_getting_off_the_ground.html"
        ),
        implementation_source=(
            "https://github.com/FStarLang/FStar/blob/"
            "42b45f6df687397cbb1b905c4066ff2435d5080f/"
            "src/ml/FStarC_Parser_LexFStar.ml#L573-L581"
        ),
        confidence="verified",
        notes=(
            "F* supports four line terminators and nested (* ... *) comments. "
            "The lexer accepts an unterminated block at EOF and resumes lexing "
            "after the exact // IN F*: compatibility prefix."
        ),
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
        language_versions=(
            CommentLanguageVersions(
                languages=("julia",),
                default="0.3",
                versions=(
                    CommentLanguageVersion(
                        name="0.2",
                        release="0",
                        span="Julia releases before 0.3",
                        comment_rules="# to the end of the line only; #= has no special meaning.",
                        regex_patterns=(r"#[^\r\n]*",),
                        nested_delimiters=(),
                        examples=(
                            CommentExample(
                                "x = 1 #= note =# + 2\n",
                                "#= note =# + 2",
                                "Before Julia 0.3, #= starts an ordinary line comment.",
                                kind="line",
                                inline_compatible=True,
                            ),
                        ),
                        documentation_source=(
                            "https://github.com/JuliaLang/julia/blob/v0.2.0/src/"
                            "julia-parser.scm#L323 (# skips to the end of the line)"
                        ),
                    ),
                    CommentLanguageVersion(
                        name="0.3",
                        aliases=("1.x", "current"),
                        release="0.3",
                        span="Julia 0.3 and later, including 1.x",
                        comment_rules="# to the end of the line and nested #= =# blocks.",
                        documentation_source=(
                            "https://github.com/JuliaLang/julia/blob/v1.10.0/HISTORY.md "
                            "(Julia v0.3.0 release notes: multi-line comments #= =#)"
                        ),
                    ),
                ),
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
            "ecmarkup",
        ),
        # WHATWG HTML 13.2.5.43-52 and CommonMark 6.6: <!--> and <!---> are empty
        # comments, and --!> also closes a comment.
        regex_patterns=(r"<!--(?:-?>|[\S\s]*?--!?>)",),
        shared_regex_examples=(
            CommentExample(
                "prefix\n<!-- note -->\nsuffix",
                "<!-- note -->",
                "Markup block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        language_versions=(
            CommentLanguageVersions(
                languages=("markdown",),
                default="commonmark-0.31",
                notes="GFM 0.29 keeps the 0.30 inline rule.",
                versions=(
                    CommentLanguageVersion(
                        name="commonmark-0.30",
                        aliases=("0.30", "gfm", "gfm-0.29"),
                        span="CommonMark 0.30 and earlier, and GFM 0.29",
                        comment_rules=(
                            "A line starting with <!-- opens an HTML block comment. An "
                            "inline comment's text must not start with > or ->, end "
                            "with -, or contain --."
                        ),
                        regex_patterns=(
                            r"(?m)(?<=^[ ]{0,3})<!--(?:-?>|[\S\s]*?--!?>)",
                            r"<!--(?!>|->)(?:(?!--)[\S\s])*-->",
                        ),
                        examples=(
                            CommentExample(
                                "foo <!-- a -- b -->\n<!-- note -- here -->\n",
                                "<!-- note -- here -->",
                                "CommonMark 0.30 HTML block comment; the inline one is text.",
                                kind="block",
                            ),
                        ),
                        documentation_source=(
                            "https://github.com/commonmark/commonmark-spec/blob/0.30/"
                            "spec.txt#L8983 (HTML comment text rules) and #L2386 (HTML "
                            "block type 2)"
                        ),
                    ),
                    CommentLanguageVersion(
                        name="commonmark-0.31",
                        aliases=("0.31", "0.31.2", "current"),
                        span="CommonMark 0.31 and later",
                        comment_rules=(
                            "<!-->, <!--->, or <!-- and any text up to the first --> "
                            "is an HTML comment, inline or as a block."
                        ),
                        documentation_source=(
                            "https://github.com/commonmark/commonmark-spec/blob/0.31.2/"
                            "spec.txt#L8994"
                        ),
                    ),
                ),
            ),
        ),
    ),
    CommentSyntax(
        family_name="lua_style",
        canonical_name="lua",
        aliases=("luau", "moonscript", "terra", "xmake"),
        regex_patterns=(
            r"--\[(=*)\[[\s\S]*?\]\1\]",
            r"--(?!\[[=]*\[)[^\n]*",
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
                "prefix\n--[=[ long note ]=]\nsuffix",
                "--[=[ long note ]=]",
                "Equal-level Lua-family long block comment.",
                kind="block",
                inline_compatible=True,
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
        language_excluded_comment_prefixes=(("luau", ("--!",)),),
        language_versions=(
            CommentLanguageVersions(
                languages=("lua",),
                default="5.1",
                versions=(
                    CommentLanguageVersion(
                        name="4.0",
                        aliases=("lua4",),
                        release="0",
                        span="Lua 4.0 and earlier",
                        comment_rules="Only -- comments to the end of the line.",
                        regex_patterns=(r"--[^\n]*",),
                        lexical_profile="lua-5.0",
                        examples=(
                            CommentExample(
                                "--[[ a ]] y = 2\n",
                                "--[[ a ]] y = 2",
                                "Lua 4.0 has no long comments.",
                                kind="line",
                                inline_compatible=True,
                            ),
                        ),
                        documentation_source=(
                            "https://github.com/lua/lua/blob/v4.0/llex.c (after -- the "
                            "lexer skips to the end of the line)"
                        ),
                    ),
                    CommentLanguageVersion(
                        name="5.0",
                        aliases=("lua5.0",),
                        release="5.0",
                        span="Lua 5.0",
                        comment_rules=(
                            "--[[ opens a long comment closed by the matching ]], "
                            "counting nested [[ ]]; any other -- runs to the end of "
                            "the line."
                        ),
                        regex_patterns=(
                            r"--(\[\[(?:(?!\[\[|\]\])[\s\S]|(?1))*\]\])",
                            r"--(?!\[\[)[^\n]*",
                        ),
                        lexical_profile="lua-5.0",
                        examples=(
                            CommentExample(
                                "--[[ a [[ b ]] c ]] x = 1\n",
                                "--[[ a [[ b ]] c ]]",
                                "Lua 5.0 long comments nest [[ ]] pairs.",
                                kind="block",
                                inline_compatible=True,
                            ),
                            CommentExample(
                                "--[==[ b ]==] z = 3\n",
                                "--[==[ b ]==] z = 3",
                                "Lua 5.0 has no leveled long brackets.",
                                kind="line",
                                inline_compatible=True,
                            ),
                        ),
                        documentation_source=(
                            "https://github.com/lua/lua/blob/v5.0/llex.c (--[[ calls "
                            "read_long_string, which counts nested [[ ]])"
                        ),
                    ),
                    CommentLanguageVersion(
                        name="5.1",
                        aliases=("lua5.1", "lua5.4", "current"),
                        release="5.1",
                        span="Lua 5.1 through 5.4",
                        comment_rules=(
                            "-- followed by [=*[ opens a long comment closed by ]=*] "
                            "with the same level; long comments do not nest."
                        ),
                        documentation_source=(
                            "https://github.com/lua/lua/blob/v5.4.6/llex.c (long "
                            "comment when skip_sep finds a leveled bracket)"
                        ),
                    ),
                ),
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
        # Every member nests (* *) comments: Mathematica, SML, Modula-2/3,
        # Component Pascal, Isabelle, Ur/Web, Augeas, and ISO 14977 EBNF.
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
        family_name="matlab_style",
        canonical_name="matlab",
        aliases=("lilypond", "turing", "txl"),
        # MATLAB 'Comments': %{ and %} open and close a block only alone on
        # their lines, and block comments nest; otherwise % starts a line comment.
        language_regex_patterns=(
            (
                "matlab",
                (
                    r"(?m)(?<=^[ \t]*)(?P<b>%\{[ \t]*\r?$"
                    r"(?:\r?\n(?:[ \t]*(?&b)[ \t]*\r?$|(?![ \t]*%[{}][ \t]*\r?$)[^\r\n]*))*"
                    r"\r?\n[ \t]*%\})(?=[ \t]*\r?$)",
                    r"(?m)%(?!(?<=^[ \t]*%)[{}][ \t]*\r?$)[^\r\n]*",
                ),
            ),
        ),
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
                "x = 1;\n%{\nnote\n%}\ny = 2;",
                "%{\nnote\n%}",
                "MATLAB block comment with %{ and %} alone on their lines.",
                kind="block",
            ),
        ),
    ),
    CommentSyntax(
        family_name="perl_style",
        canonical_name="perl",
        regex_patterns=(
            # perlpod: any =command paragraph (=pod, =head1, =over, ...) begins Pod.
            r"(?ms)^[ \t]*=(?!cut\b)[A-Za-z]\w*\b[\s\S]*?^[ \t]*=cut\b[ \t]*$",
            # perldata: $#array and $#{expr} are last-index expressions.
            r"(?<!\$)#.*",
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
            r"#(?:[^\r\n]|\r(?!\n))*",
            # Ruby embedded documents end at =end followed by whitespace or
            # EOL; the rest of that line belongs to the comment.
            r"(?ms)^[ \t]*=begin\b[\s\S]*?^[ \t]*=end(?=[ \t\r\n]|\Z)[^\r\n]*",
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
        aliases=("hiveql", "piglatin", "plsql", "sqlpl"),
        regex_patterns=(
            r"\/\*[\s\S]*?\*\/",
            r"--(?:[^\r\n]|\r(?!\n))*",
        ),
        language_excluded_comment_prefixes=(("sql", ("/*!",)),),
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
        regex_patterns=(
            # A leading @ only suppresses command echo; @REM is still REM.
            r"(?mi)^[ \t]*(?:@?rem\b.*|::.*)$",
            # cmd /?: &, &&, ||, and ( start a new command, which may be REM.
            r"(?i)(?<=(?:&|\||\()[ \t]*@?)rem\b[^\r\n]*",
        ),
        sanitizer_line_wrappers=(("::", ""), ("@REM", ""), ("REM", "")),
        shared_regex_examples=(
            CommentExample(
                "REM note\nafter",
                "REM note",
                "Batch REM comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "echo ok & rem note\nafter",
                "rem note",
                "REM command after a command separator.",
                kind="line",
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
            "vb6",
            "vbscript",
            "visual_basic",
            "visual_basic_6_0",
            "xojo",
        ),
        regex_patterns=(r"'[^\r\n]*",),
        sanitizer_line_wrappers=(("REM", ""), ("'", "")),
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
        documentation_source=(
            "https://github.com/MicrosoftDocs/VBA-Docs/blob/"
            "b2cda886ea91e36c62eb1cb177133ad024ecd345/Language/Reference/"
            "User-Interface-Help/rem-statement.md#L15-L34"
        ),
        implementation_source="src/ml4setk/Parsing/Comments/contextual.py",
        confidence="verified",
        notes=(
            "Visual Basic apostrophe comments run through newline. A "
            "case-insensitive Rem comment must begin a statement, either at the "
            "start of a line or after a colon."
        ),
        contextual_extractor="visual_basic_rem_comments",
        shared_contextual_examples=(
            CommentExample(
                "Rem note\nvalue = 1",
                "Rem note",
                "Visual Basic line-start Rem statement.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "value = 1: Rem note\nvalue = 2",
                "Rem note",
                "Visual Basic colon-separated Rem statement.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
    ),
    CommentSyntax(
        family_name="quote_line_style",
        canonical_name="vim_script",
        aliases=("viml",),
        # Vim :help :comment: " starts a comment where a command is expected, or
        # after a command when no closing quote follows on the line; a quoted
        # argument such as echo "text" is a string.
        regex_patterns=(r"(?m)(?<=^[ \t:]*)\".*", r"(?m)\"[^\"\r\n]*(?=\r?$)"),
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
        language_versions=(
            CommentLanguageVersions(
                languages=("vim_script", "viml"),
                default="legacy",
                notes=(
                    "Vim 9 applies Vim9 rules only after a leading vim9script command "
                    "and inside :def functions; choose vim9 for such files."
                ),
                versions=(
                    CommentLanguageVersion(
                        name="legacy",
                        aliases=("vim8", "neovim", "nvim"),
                        span=(
                            "Legacy Vim script: Vim up to 8.2, Vim 9 files without "
                            "vim9script, and Neovim"
                        ),
                        comment_rules=(
                            '" starts a comment where a command is expected, or after a '
                            "command when no closing quote follows on the line; # is "
                            "not a comment."
                        ),
                    ),
                    CommentLanguageVersion(
                        name="vim9",
                        aliases=("vim9script",),
                        span="Vim9 script: files starting with vim9script and :def bodies",
                        comment_rules=(
                            '# at the line start or after white space starts a comment; " '
                            "starts a string. A comment may not start with #{ unless it "
                            "starts with #{{."
                        ),
                        regex_patterns=(r"(?m)(?:^|(?<=[ \t]))#(?!\{(?!\{))[^\r\n]*",),
                        lexical_profile="vim9",
                        sanitizer_line_wrappers=(("#", ""),),
                        examples=(
                            CommentExample(
                                "vim9script\n# header note\nvar total = 0  # running total\n",
                                "# running total",
                                "Vim9 script # comment after white space.",
                                kind="line",
                                inline_compatible=True,
                                grouped_line_compatible=True,
                            ),
                            CommentExample(
                                'vim9script\necho "a # b" # note\n',
                                "# note",
                                'In Vim9 script, " opens a string, not a comment.',
                                kind="line",
                                inline_compatible=True,
                            ),
                        ),
                        documentation_source=(
                            "https://github.com/vim/vim/blob/v9.0.0000/runtime/doc/"
                            "vim9.txt#L120-L146 (comments start with #, white space "
                            "is required before #, and #{ is an error)"
                        ),
                    ),
                ),
            ),
        ),
    ),
    CommentSyntax(
        family_name="smalltalk_style",
        canonical_name="smalltalk",
        regex_patterns=(r'"[\S\s]*?"',),
        sanitizer_block_wrappers=(('"', '"'),),
        shared_regex_examples=(
            CommentExample(
                'before\n"note"\nafter',
                '"note"',
                "Smalltalk paired double-quote comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://www.gnu.org/software/smalltalk/manual/html_node/Smalltalk-syntax.html"
        ),
        confidence="verified",
        notes=(
            "Smalltalk comments are paired double-quoted regions and may span "
            "physical lines. This is distinct from Vim's one-sided quote syntax."
        ),
    ),
    CommentSyntax(
        family_name="editorconfig_style",
        canonical_name="editorconfig",
        regex_patterns=(r"(?m)^[ \t]*[;#].*$",),
        sanitizer_line_wrappers=(("#", ""), (";", "")),
        shared_regex_examples=(
            CommentExample(
                "# note\nafter",
                "# note",
                "Start-of-line EditorConfig comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        language_versions=(
            CommentLanguageVersions(
                languages=("editorconfig",),
                default="0.15",
                versions=(
                    CommentLanguageVersion(
                        name="pre-0.15",
                        release="0",
                        span="EditorConfig specification before 0.15.0 (core-c 0.12.x)",
                        comment_rules=(
                            "A line whose first non-blank character is ; or # is a "
                            "comment, and a ; or # after white space starts an inline "
                            "comment to the end of the line."
                        ),
                        regex_patterns=(r"(?m)^[ \t]*[;#].*$", r"(?<=[ \t])[;#][^\r\n]*"),
                        lexical_profile="editorconfig-pre-0.15",
                        examples=(
                            CommentExample(
                                "[*.py]\nindent_style = space ; use spaces\n",
                                "; use spaces",
                                "Before 0.15, ; after white space starts an inline comment.",
                                kind="line",
                                inline_compatible=True,
                            ),
                        ),
                        documentation_source=(
                            "https://github.com/editorconfig/editorconfig-core-c/blob/"
                            "v0.12.5/src/lib/ini.c#L64-L75 (find_char_or_comment stops "
                            "at ; or # after white space)"
                        ),
                    ),
                    CommentLanguageVersion(
                        name="0.15",
                        aliases=("current",),
                        release="0.15",
                        span="EditorConfig specification 0.15.0 and later",
                        comment_rules=(
                            "Only full-line comments; ; or # elsewhere is part of the "
                            "section name or value."
                        ),
                        documentation_source=(
                            "https://github.com/editorconfig/specification/blob/v0.15.1/"
                            "index.rst#L97-L100 (no inline comments, versionchanged 0.15.0)"
                        ),
                    ),
                ),
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
        sanitizer_line_wrappers=(("#", ""), (";", "")),
        sanitizer_block_wrappers=(("/*", "*/"),),
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
            r"(?!\A#!)#[^\r\n]*",
            r"--[^\r\n]*",
        ),
        sanitizer_line_wrappers=(("--", ""), ("#", "")),
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
        regex_patterns=(r";[^\r\n]*",),
        # Racket reference 1.3.9: #; comments out the next datum.
        language_regex_patterns=(
            (
                "racket",
                (
                    r";[^\r\n]*",
                    r'#;\s*(?P<d>(?:[\'`,]|,@)*(?:\((?:[^()\[\]"\\;]|"(?:\\[\s\S]|[^"\\])*"|\\[\s\S]|;[^\r\n]*|(?&d))*\)|\[(?:[^()\[\]"\\;]|"(?:\\[\s\S]|[^"\\])*"|\\[\s\S]|;[^\r\n]*|(?&d))*\]|"(?:\\[\s\S]|[^"\\])*"|[^\s()\[\]";]+))',
                ),
            ),
        ),
        sanitizer_line_wrappers=(("#;", ""),),
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
                '(message "before") ; note\n(message "after")',
                "; note",
                "Emacs Lisp semicolon line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://www.gnu.org/software/emacs/manual/html_node/elisp/Comment-Tips.html"
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
        sanitizer_line_wrappers=(("REM", ""), ("'", "")),
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
        language_regex_patterns=(
            # PHP 8.0 scanner: #[ is the T_ATTRIBUTE token, not a # comment.
            ("html_php", _PHP8_HTML_PATTERNS),
            ("html_plus_php", _PHP8_HTML_PATTERNS),
        ),
        language_versions=(
            CommentLanguageVersions(
                languages=("html_php", "html_plus_php"),
                default="php8.0",
                versions=(
                    CommentLanguageVersion(
                        name="php7.4",
                        aliases=("php5", "php7", "php7.0", "php7.1", "php7.2", "php7.3"),
                        release="0",
                        span="PHP 7.4 and earlier",
                        comment_rules="#, //, and non-nested /* */; #[ is an ordinary # comment.",
                        regex_patterns=(r"\/\*[\S\s]*?\*\/", r"/{2}.*", r"#.*"),
                        examples=(
                            CommentExample(
                                "<?php\n#[Pure]\nfunction f() {} # tail\n",
                                "#[Pure]",
                                "Before PHP 8.0, #[ starts an ordinary # line comment.",
                                kind="line",
                                inline_compatible=True,
                                grouped_line_compatible=True,
                            ),
                        ),
                        documentation_source=(
                            "https://github.com/php/php-src/blob/php-7.4.0/Zend/"
                            "zend_language_scanner.l#L2147 (# and // comment rule, no #[ rule)"
                        ),
                    ),
                    CommentLanguageVersion(
                        name="php8.0",
                        aliases=("php8", "php8.1", "php8.2", "php8.3", "php8.4", "current"),
                        release="8.0",
                        span="PHP 8.0 and later",
                        comment_rules=(
                            "#, //, and non-nested /* */; #[ opens an attribute and is "
                            "not a comment."
                        ),
                        documentation_source=(
                            "https://github.com/php/php-src/blob/php-8.0.0/Zend/"
                            "zend_language_scanner.l#L1409-L1412 (#[ returns "
                            "T_ATTRIBUTE ahead of the # comment rule)"
                        ),
                    ),
                ),
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
                'service {\n  // note\n  host = "localhost"\n}',
                "// note",
                "HOCON slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                'service {\n  # note\n  host = "localhost"\n}',
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
        sanitizer_block_wrappers=(
            ("(::", "::)"),
            ("(:~", ":)"),
        ),
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
        documentation_source=("https://cmake.org/cmake/help/latest/manual/cmake-language.7.html"),
        implementation_source="https://gitlab.kitware.com/cmake/cmake",
        confidence="verified",
        notes=(
            "CMake bracket comments use the same equal-delimited bracket "
            "syntax as bracket arguments, and bracket arguments do not nest."
        ),
        language_versions=(
            CommentLanguageVersions(
                languages=("cmake",),
                default="3.0",
                versions=(
                    CommentLanguageVersion(
                        name="2.8",
                        aliases=("pre-3.0", "2.6", "2.8.12"),
                        release="0",
                        span="CMake releases before 3.0",
                        comment_rules=(
                            "# comments run to the end of the line; #[[ and #[=[ have "
                            "no special meaning, and [[...]] is not a bracket argument."
                        ),
                        regex_patterns=(r"#[^\r\n]*",),
                        lexical_profile="cmake-2.8",
                        examples=(
                            CommentExample(
                                "#[[ note ]] set(x 1)\nset(y 2)",
                                "#[[ note ]] set(x 1)",
                                "Before 3.0, #[[ starts an ordinary line comment.",
                                kind="line",
                                inline_compatible=True,
                            ),
                            CommentExample(
                                "set(x [[ a ]]) # note\n",
                                "# note",
                                "Before 3.0, [[ is not a bracket argument.",
                                kind="line",
                                inline_compatible=True,
                            ),
                            CommentExample(
                                "set(x [[ # note ]])\n",
                                "# note ]])",
                                "Before 3.0, # inside [[ ]] starts a comment.",
                                kind="line",
                                inline_compatible=True,
                            ),
                        ),
                        documentation_source=(
                            "https://cmake.org/cmake/help/v3.0/release/3.0.0.html "
                            "(bracket comments and arguments are new and change the "
                            "meaning of #[[ lines)"
                        ),
                    ),
                    CommentLanguageVersion(
                        name="3.0",
                        aliases=("3.x", "4.x"),
                        release="3.0",
                        span="CMake 3.0.0 and later",
                        comment_rules=(
                            "# line comments plus #[[...]] and #[=[...]=] bracket "
                            "comments; [[...]] bracket arguments protect their content."
                        ),
                    ),
                ),
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
        sanitizer_line_wrappers=(("*", ";"), ("*", "")),
        sanitizer_block_wrappers=(("/*", "*/"),),
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
        # Haskell 2010 Report 2.3: dashes that form part of an operator lexeme
        # (for example --> , --+ , or |--) do not begin a comment.
        regex_patterns=(
            r"(?<![!#$%&*+./<=>?@\\^|~:])--+(?![!#$%&*+./<=>?@\\^|~:])"
            r"(?:[^\r\n]|\r(?!\n))*",
        ),
        excluded_comment_prefixes=("-->",),
        # GHC and Curry {-# ... #-} pragmas are compiler directives. Dhall,
        # Idris, and PureScript have no such pragmas, so {-# is a comment there.
        language_excluded_comment_prefixes=(
            ("haskell", ("{-#",)),
            ("literate_haskell", ("{-#",)),
            ("c2hs_haskell", ("{-#",)),
            ("curry", ("{-#",)),
        ),
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
        sanitizer_line_wrappers=(
            ('*"*"', ""),
            ("***", ""),
            ("**", ""),
            ('"*', ""),
            ('"!', ""),
            ('*"', ""),
            ("*&", ""),
            ('"', ""),
            ("*", ""),
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
        regex_patterns=(r"(?im)\bcomment\b[^\r\n]*",),
        sanitizer_line_wrappers=(("Comment", ""),),
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
        aliases=("dm", "dylan", "jflex", "koka", "powerbuilder", "v"),
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
        family_name="php_style",
        canonical_name="php",
        # PHP manual "Comments": one-line comments end at the line end or at
        # the ?> close tag, whichever comes first. PHP 8 #[ starts an attribute.
        regex_patterns=(
            r"\/\*[\S\s]*?\*\/",
            r"/{2}(?:(?!\?>)[^\r\n])*",
            r"#(?!\[)(?:(?!\?>)[^\r\n])*",
        ),
        sanitizer_line_wrappers=(("//", ""), ("#", "")),
        shared_regex_examples=(
            CommentExample(
                "<?php\n// note\n$x = 1;",
                "// note",
                "Slash one-line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "<?php\n# note\n$x = 1;",
                "# note",
                "Shell-style one-line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "<?php\n/* note */\n$x = 1;",
                "/* note */",
                "Block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://www.php.net/manual/en/language.basic-syntax.comments.php",
        confidence="verified",
        notes=(
            "PHP supports //, #, and /* */ comments. One-line comments stop "
            "before ?>. #[ begins a PHP 8 attribute, not a comment."
        ),
        language_versions=(
            CommentLanguageVersions(
                languages=("php",),
                default="php8.0",
                versions=(
                    CommentLanguageVersion(
                        name="php7.2",
                        aliases=("php5", "php7.0", "php7.1"),
                        release="0",
                        span="PHP 7.2 and earlier",
                        comment_rules=(
                            "#, // to the end of the line or before ?>, and non-nested "
                            "/* */; #[ is an ordinary # comment. A heredoc or nowdoc "
                            "closes only at its label in column 0, followed by an "
                            "optional ; and a line break."
                        ),
                        regex_patterns=(
                            r"\/\*[\S\s]*?\*\/",
                            r"/{2}(?:(?!\?>)[^\r\n])*",
                            r"#(?:(?!\?>)[^\r\n])*",
                        ),
                        lexical_profile="php-7.2",
                        examples=(
                            CommentExample(
                                "<?php\n#[Pure]\nfunction f() {}\n",
                                "#[Pure]",
                                "Before PHP 8.0, #[ starts an ordinary # line comment.",
                                kind="line",
                                inline_compatible=True,
                                grouped_line_compatible=True,
                            ),
                            CommentExample(
                                "<?php\n$s = <<<EOT\n  EOT; # text\nEOT; # note\n",
                                "# note",
                                "Before PHP 7.3, an indented label does not close a heredoc.",
                                kind="line",
                                inline_compatible=True,
                            ),
                        ),
                        documentation_source=(
                            "https://github.com/php/php-src/blob/php-7.3.0/UPGRADING "
                            "(flexible heredoc and nowdoc: before 7.3 the closing label "
                            "had to start its line); https://github.com/php/php-src/blob/"
                            "php-7.4.0/Zend/zend_language_scanner.l#L2147 (no #[ rule)"
                        ),
                    ),
                    CommentLanguageVersion(
                        name="php7.3",
                        aliases=("php7.4",),
                        release="7.3",
                        span="PHP 7.3 and 7.4",
                        comment_rules=(
                            "As PHP 7.2, but a heredoc or nowdoc closes at an indented "
                            "label, so the rest of that line is code or a comment."
                        ),
                        regex_patterns=(
                            r"\/\*[\S\s]*?\*\/",
                            r"/{2}(?:(?!\?>)[^\r\n])*",
                            r"#(?:(?!\?>)[^\r\n])*",
                        ),
                        examples=(
                            CommentExample(
                                "<?php\n#[Pure]\nfunction f() {}\n",
                                "#[Pure]",
                                "Before PHP 8.0, #[ starts an ordinary # line comment.",
                                kind="line",
                                inline_compatible=True,
                                grouped_line_compatible=True,
                            ),
                        ),
                        documentation_source=(
                            "https://github.com/php/php-src/blob/php-7.4.0/Zend/"
                            "zend_language_scanner.l#L2147 (# and // comment rule, no #[ "
                            "rule); https://github.com/php/php-src/blob/php-7.3.0/UPGRADING "
                            "(flexible heredoc and nowdoc closing labels)"
                        ),
                    ),
                    CommentLanguageVersion(
                        name="php8.0",
                        aliases=("php8", "php8.1", "php8.2", "php8.3", "php8.4", "current"),
                        release="8.0",
                        span="PHP 8.0 and later",
                        comment_rules=(
                            "#, // to the end of the line or before ?>, and non-nested "
                            "/* */; #[ opens an attribute and is not a comment."
                        ),
                        documentation_source=(
                            "https://github.com/php/php-src/blob/php-8.0.0/UPGRADING "
                            "(#[ is no longer a comment)"
                        ),
                    ),
                ),
            ),
        ),
    ),
    CommentSyntax(
        family_name="nested_block_c_style",
        canonical_name="scala",
        aliases=("dart", "swift"),
        regex_patterns=(r"/{2}[^\r\n]*",),
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
        documentation_source=(
            "https://scala-lang.org/files/archive/spec/2.13/01-lexical-syntax.html#comments; "
            "https://docs.swift.org/swift-book/documentation/the-swift-programming-language/"
            "lexicalstructure/#Comments; https://spec.dart.dev/DartLangSpecDraft.pdf"
        ),
        confidence="verified",
        notes=(
            "Scala, Swift, and Dart block comments nest, unlike C. Line comments end at CR or LF."
        ),
    ),
    CommentSyntax(
        family_name="sql_nested_style",
        canonical_name="plpgsql",
        aliases=("tsql",),
        regex_patterns=(r"--(?:[^\r\n]|\r(?!\n))*",),
        nested_delimiters=(("/*", "*/"),),
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
                "SELECT 1 /* outer /* inner */ outer */ FROM t",
                "/* outer /* inner */ outer */",
                "Nested bracketed comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://www.postgresql.org/docs/current/sql-syntax-lexical.html"
            "#SQL-SYNTAX-COMMENTS; https://learn.microsoft.com/sql/t-sql/language-"
            "elements/slash-star-comment-transact-sql"
        ),
        confidence="verified",
        notes=(
            "PostgreSQL and SQL Server nest block comments as the SQL standard "
            "specifies. MySQL and SQLite do not, so the generic sql key keeps "
            "non-nesting blocks."
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
            "https://github.com/eclipse-archived/golo-lang/blob/master/doc/basics.adoc"
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
        unclosed_block_openers=("/",),
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
        sanitizer_block_wrappers=(
            ("{{!----", "----}}"),
            ("{{!--", "--}}"),
            ("{{!", "}}"),
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
        aliases=("lean4", "lean_4"),
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
            CommentExample(
                "/-- block note -/\ndef value := 1",
                "/-- block note -/",
                "Lean declaration documentation comment.",
                kind="block",
            ),
            CommentExample(
                "/-! block note -/\ndef value := 1",
                "/-! block note -/",
                "Lean module documentation comment.",
                kind="block",
            ),
        ),
        sanitizer_line_wrappers=(("--", ""),),
        sanitizer_block_wrappers=(("/--", "-/"), ("/-!", "-/"), ("/-", "-/")),
        documentation_source=(
            "https://github.com/leanprover/lean4/blob/"
            "4b7a61dfa4ff3f29f07f0ae8ce428fbe39babd6f/"
            "src/Lean/Parser/Basic.lean#L536-L587"
        ),
        implementation_source=(
            "https://github.com/leanprover/lean4/blob/"
            "4b7a61dfa4ff3f29f07f0ae8ce428fbe39babd6f/"
            "src/Lean/Parser/Basic.lean#L536-L587"
        ),
        confidence="verified",
        notes=(
            "Lean 4 preserves Lean's -- line comments and recursively nested "
            "/- ... -/ block comments, including documentation variants."
        ),
    ),
    CommentSyntax(
        family_name="liquid_style",
        canonical_name="liquid",
        regex_patterns=(
            r"\{%-?\s*comment\s*-?%\}[\S\s]*?\{%-?\s*endcomment\s*-?%\}",
            r"\{%-?\s*(?:#[^\r\n]*(?:\r?\n\s*#[^\r\n]*)*)\s*-?%\}",
        ),
        sanitizer_block_wrappers=(
            ("{%- comment -%}", "{%- endcomment -%}"),
            ("{% comment -%}", "{% endcomment -%}"),
            ("{% comment %}", "{% endcomment %}"),
            ("{%comment %}", "{%endcomment%}"),
            ("{%comment%}", "{%endcomment%}"),
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
        sanitizer_block_wrappers=(
            ("{{!----", "----}}"),
            ("{{!--", "--}}"),
            ("{{!", "}}"),
        ),
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
        sanitizer_line_wrappers=(("//-", ""), ("//", "")),
        unclosed_block_openers=("//-", "//"),
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
        sanitizer_line_wrappers=(("/L/", ""), ("/F/", ""), ("/", "")),
        sanitizer_block_wrappers=(("/\n", "\n\\"),),
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
        documentation_source=(
            "https://github.com/github-linguist/linguist/commit/"
            "a45d988963768e54352ae40792cf5e5350a19f89"
        ),
        implementation_source=(
            "https://github.com/FourjsGenero/GeneroFgl.tmbundle/tree/"
            "dedc0c5df4235a3c63969eb15a24c7d10f67b686/Syntaxes"
        ),
        confidence="verified",
        notes=(
            "The legacy canonical and Genero Forms mappings remain supported. "
            "The raw Stack labels Genero 4gl and Genero per are intentionally "
            "deferred because their reviewed dialect contracts conflict with "
            "this shared syntax."
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
            # Ruby embedded documents end at =end followed by whitespace or
            # EOL; the rest of that line belongs to the comment.
            r"(?ms)^[ \t]*=begin\b[\s\S]*?^[ \t]*=end(?=[ \t\r\n]|\Z)[^\r\n]*",
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
        sanitizer_line_wrappers=(("/!", ""), ("/", "")),
        unclosed_block_openers=("/!", "/"),
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
            "https://github.com/pygments/pygments/blob/2.20.0/pygments/lexers/esoteric.py"
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
        sanitizer_line_wrappers=(("shh", ""),),
        sanitizer_block_wrappers=(("quiet", "loud"),),
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
        documentation_source=("https://github.com/dogescript/dogescript/blob/master/LANGUAGE.md"),
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
            "https://learn.microsoft.com/en-us/aspnet/core/test/http-files?view=aspnetcore-10.0"
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
        documentation_source=("https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html"),
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
            "https://github.com/pygments/pygments/blob/2.20.0/pygments/lexers/templates.py"
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
            "https://www.ncl.ucar.edu/Document/Manuals/Ref_Manual/NclStatements.shtml"
        ),
        implementation_source=(
            "https://github.com/pygments/pygments/blob/2.20.0/pygments/lexers/ncl.py"
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
            "https://github.com/pygments/pygments/blob/2.20.0/pygments/lexers/lisp.py"
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
            "https://github.com/pygments/pygments/blob/2.20.0/pygments/lexers/templates.py"
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
        sanitizer_line_wrappers=(("@comment", ""), ("@c", "")),
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
        documentation_source=(
            "https://www.gnu.org/software/texinfo/manual/texinfo/html_node/Comments.html"
        ),
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
                'Print "Hello" \' note\nEnd',
                "' note",
                "Monkey apostrophe line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                'Print "before"\n#Rem\nnote\n#End\nPrint "after"',
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
        sanitizer_block_wrappers=(("/*", "*/"),),
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
            CommentExample(
                "DEFINE_PROGRAM\n/* note */\nWAIT 10 {}",
                "/* note */",
                "NetLinx slash-star block comment.",
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
                'MESSAGE "before".\n/* note */\nMESSAGE "after".',
                "/* note */",
                "OpenEdge ABL block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://docs.progress.com/bundle/openedge-abl-basic-guided-journey/page/Comments.html"
        ),
        confidence="verified",
        notes="OpenEdge ABL documents /* ... */ comments.",
    ),
    CommentSyntax(
        family_name="maxscript_style",
        canonical_name="maxscript",
        regex_patterns=(
            r"/\*[\S\s]*?\*/",
            r"--[^\r\n]*",
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
        documentation_source=("https://help.autodesk.com/cloudhelp/2026/ENU/MAXScript-Help/"),
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
        language_excluded_comment_prefixes=(
            ("reason", ("/*!re2c",)),
            ("reasonml", ("/*!re2c",)),
        ),
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
        language_versions=(
            CommentLanguageVersions(
                languages=("supercollider",),
                default="3.9",
                versions=(
                    CommentLanguageVersion(
                        name="3.8",
                        release="0",
                        span="SuperCollider 3.8 and earlier",
                        comment_rules=(
                            "// line comments and nested /* */ comments whose "
                            "delimiters overlap, so */*/ closes, reopens, and closes."
                        ),
                        regex_patterns=(),
                        nested_delimiters=(),
                        contextual_extractor="supercollider_38_comments",
                        sanitizer_block_wrappers=(("/*", "*/"),),
                        examples=(
                            CommentExample(
                                "x = 1; /* a /* b */*/ y = 2; // */\n",
                                "/* a /* b */*/ y = 2; // */",
                                "Before 3.9, */*/ reopens the nested comment.",
                                kind="block",
                                inline_compatible=True,
                            ),
                        ),
                        documentation_source=(
                            "https://github.com/supercollider/supercollider/blob/"
                            "Version-3.8.0/lang/LangSource/PyrLexer.cpp#L840-L852"
                        ),
                    ),
                    CommentLanguageVersion(
                        name="3.9",
                        aliases=("current",),
                        release="3.9",
                        span="SuperCollider 3.9 and later",
                        comment_rules=(
                            "// line comments and nested /* */ comments; each "
                            "delimiter consumes both of its characters."
                        ),
                        documentation_source=(
                            "https://github.com/supercollider/supercollider/blob/"
                            "Version-3.9.0/CHANGELOG.md (sclang: nestable comment fix, "
                            "#2625)"
                        ),
                    ),
                ),
            ),
        ),
    ),
    CommentSyntax(
        family_name="propeller_spin_style",
        canonical_name="propeller_spin",
        regex_patterns=(
            r"\{\{[\S\s]*?\}\}",
            r"\{[\S\s]*?\}",
            r"'{1,2}[^\r\n]*",
        ),
        sanitizer_block_wrappers=(("{{", "}}"), ("{", "}")),
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
            "https://forums.parallax.com/discussion/download/85706/Propeller_Tutorial_1.01.pdf"
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
        sanitizer_line_wrappers=(
            ("NOTE", ""),
            ("&&", ""),
            ("**", ""),
            ("//", ""),
            ("*", ""),
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
        regex_patterns=(r";[^\r\n]*",),
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
        regex_patterns=(r";[^\r\n]*",),
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
        language_versions=(
            CommentLanguageVersions(
                languages=("macaulay2",),
                default="1.13",
                versions=(
                    CommentLanguageVersion(
                        name="1.10",
                        release="0",
                        span="Macaulay2 1.0 through 1.10",
                        comment_rules="-- line comments and non-nested {* *} block comments.",
                        regex_patterns=(r"\{\*[\S\s]*?\*\}", r"--.*"),
                        sanitizer_block_wrappers=(("{*", "*}"),),
                        examples=(
                            CommentExample(
                                "x = 1\ny = {* note *} 2",
                                "{* note *}",
                                "Before 1.11, {* *} encloses a block comment.",
                                kind="block",
                                inline_compatible=True,
                            ),
                        ),
                        documentation_source=(
                            "https://github.com/Macaulay2/M2/blob/master/M2/Macaulay2/"
                            "packages/Macaulay2Doc/changes.m2 (changes, 1.0 and 1.1: "
                            "{* ... *} block comments)"
                        ),
                    ),
                    CommentLanguageVersion(
                        name="1.11",
                        aliases=("1.12",),
                        release="1.11",
                        span="Macaulay2 1.11 and 1.12",
                        comment_rules=(
                            "-- line comments, non-nested -* *- block comments, and the "
                            "deprecated {* *} block comments."
                        ),
                        regex_patterns=(r"-\*[\S\s]*?\*-", r"\{\*[\S\s]*?\*\}", r"--.*"),
                        sanitizer_block_wrappers=(("{*", "*}"),),
                        examples=(
                            CommentExample(
                                "x = 1\ny = {* note *} 2",
                                "{* note *}",
                                "Macaulay2 1.11 and 1.12 still accept {* *} block comments.",
                                kind="block",
                                inline_compatible=True,
                            ),
                        ),
                        documentation_source=(
                            "https://github.com/Macaulay2/M2/blob/master/M2/Macaulay2/"
                            "packages/Macaulay2Doc/changes.m2 (changes, 1.11: -* ... *- "
                            "replaces {* ... *}, which is still recognized)"
                        ),
                    ),
                    CommentLanguageVersion(
                        name="1.13",
                        aliases=("current",),
                        release="1.13",
                        span="Macaulay2 1.13 and later",
                        comment_rules="-- line comments and non-nested -* *- block comments.",
                        documentation_source=(
                            "https://github.com/Macaulay2/M2/blob/master/M2/Macaulay2/"
                            "packages/Macaulay2Doc/changes.m2 (changes, 1.13: the old "
                            "block comment syntax is disabled)"
                        ),
                    ),
                ),
            ),
        ),
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
    CommentSyntax(
        family_name="gnu_checksum_manifest_style",
        canonical_name="checksums",
        regex_patterns=(r"(?m)^#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "# note\ne3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  empty",
                "# note",
                "GNU Coreutils checksum checker column-zero comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=("https://www.gnu.org/software/coreutils/manual/html_node/cksum.html"),
        implementation_source=(
            "https://github.com/coreutils/coreutils/blob/"
            "6e812858bb8b5cc1a4c91b16502a3092ead1d72f/src/cksum.c#L1414-L1416"
        ),
        confidence="verified",
        notes=(
            "GNU Coreutils checksum check-file dialect only. # must be the "
            "first byte of the physical line; indented hashes and hashes in "
            "filenames are data."
        ),
    ),
    CommentSyntax(
        family_name="ecere_econ_style",
        canonical_name="ecere_projects",
        regex_patterns=(
            r"/\*[\S\s]*?\*/",
            r"//[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                '{\n  // note\n  "Version": 0.2\n}',
                "// note",
                "Ecere .epj ECON line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                '{ /* note */ "Version": 0.2 }',
                "/* note */",
                "Ecere .epj ECON non-nested block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source=(
            "https://github.com/ecere/ecere-sdk/blob/"
            "cca43ca73c12aba5a152a8dba909483eef494faf/"
            "ecere/src/sys/JSON.ec#L317-L339"
        ),
        implementation_source=(
            "https://github.com/ecere/ecere-sdk/blob/"
            "cca43ca73c12aba5a152a8dba909483eef494faf/"
            "ide/src/project/Project.ec#L4912-L4923"
        ),
        confidence="verified",
        notes=(
            ".epj projects use Ecere Object Notation rather than strict JSON. "
            "Its reader accepts // and non-nested /* ... */ comments outside "
            "double-quoted strings."
        ),
    ),
    CommentSyntax(
        family_name="figlet_counted_header_style",
        canonical_name="figlet_font",
        contextual_extractor="figlet_header_comments",
        canonical_contextual_examples=(
            CommentExample(
                "flf2a$ 1 1 1 0 2\n"
                "FIGlet font attribution\n"
                "  leading space is content\n"
                "@ glyph sentinel\n",
                "FIGlet font attribution\n  leading space is content",
                "FIGfont header-declared comment lines.",
                kind="contextual",
            ),
        ),
        sanitizer_mode="raw",
        documentation_source=("https://sources.debian.org/data/main/f/figlet/2.2.5-3/figfont.txt"),
        implementation_source=(
            "https://github.com/cmatsuoka/figlet/blob/"
            "202a0a8110650a943f1125f536b3bb455cf72ee1/figlet.c"
        ),
        confidence="verified",
        notes=(
            "The byte-oriented FIGfont header requires a single-byte hardblank "
            "and C whitespace between numeric fields. The fifth numeric field is "
            "Comment_Lines. Exactly that many following physical lines are "
            "comments; they have no lexical wrapper."
        ),
    ),
    CommentSyntax(
        family_name="visual_studio_solution_style",
        canonical_name="microsoft_visual_studio_solution",
        regex_patterns=(r"(?:\A|(?<=[\r\n]))[^\S\r\n]*#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "Microsoft Visual Studio Solution File, Format Version 12.00\n"
                "# note\n"
                "Global\nEndGlobal\n",
                "# note",
                "MSBuild .sln full-line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://learn.microsoft.com/en-us/visualstudio/extensibility/"
            "internals/solution-dot-sln-file"
        ),
        implementation_source=(
            "https://github.com/dotnet/msbuild/blob/"
            "fecd32cb8181813b4d9fd2ffea6691746461fabd/"
            "src/Build/Construction/Solution/SolutionFile.cs"
        ),
        confidence="verified",
        notes=(
            "MSBuild trims solution lines and ignores a line whose first "
            "non-whitespace character is #. It does not define inline or block "
            "comments."
        ),
    ),
    CommentSyntax(
        family_name="ampl_nl_style",
        canonical_name="nl",
        regex_patterns=(r"(?m)^(?![ \t]*#)[^#\r\n]*\S[ \t]*\K#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "g3 0 1 0\t# note\n0 0\n",
                "# note",
                "AMPL text .nl record annotation.",
                kind="line",
                inline_compatible=True,
                standalone_compatible=False,
            ),
        ),
        documentation_source="https://ampl.github.io/nlwrite.pdf",
        implementation_source=(
            "https://github.com/ampl/mp/blob/"
            "3521b072f65527bf3b810ca3e47c79fc80a28256/"
            "include/mp/nl-reader.h"
        ),
        confidence="verified",
        notes=(
            "Text .nl comments begin with # after a record and run to EOL. "
            "The query masks h<N>: raw-string records using C whitespace and "
            "the binary payload after a complete ten-line b-format header; "
            "standalone # lines are not records."
        ),
    ),
    CommentSyntax(
        family_name="omgrofl_style",
        canonical_name="omgrofl",
        regex_patterns=(
            r"(?i)(?:\A|(?<=[\r\n\u0085\u2028\u2029]))"
            r"[ \t\x0b\f\x1c-\x1f\u1680\u2000-\u2006\u2008-\u200a\u205f\u3000]*"
            r"w00t"
            r"(?=[ \t\x0b\f\x1c-\x1f\u1680\u2000-\u2006\u2008-\u200a\u205f"
            r"\u3000\r\n\u0085\u2028\u2029]|\Z)"
            r"[^\r\n\u0085\u2028\u2029]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "w00t note\nlol iz 71\n",
                "w00t note",
                "Omgrofl whole-line w00t comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "\tW00T note\nlol iz 71\n",
                "\tW00T note",
                "Omgrofl comment operator is case-insensitive.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        documentation_source=(
            "https://github.com/OlegSmelov/omgrofl-interpreter/blob/"
            "6c621627b913771f3896c75ea8a27f06e34f2e65/README.md"
        ),
        implementation_source=(
            "https://github.com/OlegSmelov/omgrofl-interpreter/blob/"
            "6c621627b913771f3896c75ea8a27f06e34f2e65/"
            "src/omgrofl/interpreter/ScriptParser.java"
        ),
        confidence="verified",
        notes=(
            "w00t must be the first complete token under Java Scanner's default "
            "whitespace and line-separator rules. The parser ignores that "
            "physical line case-insensitively; there is no inline or block form."
        ),
    ),
    CommentSyntax(
        family_name="pogoscript_style",
        canonical_name="pogoscript",
        regex_patterns=(
            r"/\*[\S\s]*?(?:\*/|\Z)",
            r"//[^\r\n]*",
        ),
        unclosed_block_openers=("/*",),
        shared_regex_examples=(
            CommentExample(
                "value = 1 // note\nnext = 2",
                "// note",
                "PogoScript line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "a = 1 /* block note */ b = 2",
                "/* block note */",
                "PogoScript non-nested block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        documentation_source="https://featurist.github.io/pogoscript/cheatsheet.html",
        implementation_source=(
            "https://github.com/featurist/pogoscript/blob/"
            "51ab449cd05e3ed30386fae816569514416039ff/"
            "lib/parser/grammar.pogo"
        ),
        confidence="verified",
        notes=(
            "The lexer accepts // comments and non-nested /* ... */ comments, "
            "including an unterminated block through EOF. PogoScript's "
            "multiline strings are masked before comment matching."
        ),
    ),
    CommentSyntax(
        family_name="aiken_style",
        canonical_name="aiken",
        regex_patterns=(r"/{2}[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "const timeout = 60 // note\n",
                "// note",
                "Aiken ordinary line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/// note\nconst timeout = 60",
                "/// note",
                "Aiken documentation line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "//// note\nconst timeout = 60",
                "//// note",
                "Aiken module documentation line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("////", ""), ("///", ""), ("//", "")),
        documentation_source=(
            "https://github.com/aiken-lang/site/blob/"
            "20b105bcdf4842f31f24e36a2b9b8013670765ff/"
            "src/pages/language-tour/functions.mdx"
        ),
        implementation_source=(
            "https://github.com/aiken-lang/aiken/blob/"
            "6aa51055f6d54b57f508d8ddcb2c33612c96dee4/"
            "crates/aiken-lang/src/parser/lexer.rs#L270-L353"
        ),
        confidence="verified",
        notes=(
            "The Aiken lexer distinguishes //, ///, and //// tokens. Extraction "
            "uses their shared range shape while cleaning removes the complete "
            "longest introducer."
        ),
    ),
    CommentSyntax(
        family_name="answer_set_programming_style",
        canonical_name="answer_set_programming",
        contextual_extractor="answer_set_programming_comments",
        shared_contextual_examples=(
            CommentExample(
                "chosen(X). % note\nnext(X).",
                "% note",
                "clingo percent line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "#! note\nchosen(a).",
                "#! note",
                "clingo hash-bang line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "before %* block note %* inner *% outer *% after",
                "%* block note %* inner *% outer *%",
                "clingo nested block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("#!", ""), ("%", "")),
        sanitizer_block_wrappers=(("%*", "*%"),),
        documentation_source=(
            "https://github.com/potassco/guide/blob/"
            "26fba894654e88aa511c2a547e69afe1ae0f23fa/"
            "language.tex#L1692-L1709"
        ),
        implementation_source=(
            "https://github.com/potassco/clingo/blob/"
            "920d06bcda7dd420814ce50953feff260a60fd8b/"
            "libgringo/src/input/nongroundlexer.xch#L149-L217"
        ),
        confidence="cross-checked",
        notes=(
            "Implements clingo host-language modes, including nested blocks and "
            "#! comments. Embedded #script bodies are protected through #end."
        ),
    ),
    CommentSyntax(
        family_name="b4x_style",
        canonical_name="b4x",
        regex_patterns=(r"'[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "Dim value = 1 ' note\nLog(value)",
                "' note",
                "B4X apostrophe line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("'", ""),),
        documentation_source="https://www.b4x.com/guides/B4XGettingStarted.html",
        implementation_source=(
            "https://www.b4x.com/android/forum/threads/coments-as.37729/#post-222534"
        ),
        confidence="cross-checked",
        notes=(
            "B4X uses apostrophe comments, not VB Rem comments. Ordinary doubled-"
            "quote strings and multiline smart strings are masked before matching."
        ),
    ),
    CommentSyntax(
        family_name="bluespec_bh_style",
        canonical_name="bluespec_bh",
        contextual_extractor="bluespec_bh_comments",
        shared_contextual_examples=(
            CommentExample(
                "value\n--- note\nnext",
                "--- note",
                "BH maximal-dash line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "before {- block note {- inner -} outer -} after",
                "{- block note {- inner -} outer -}",
                "BH nested block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("--", ""),),
        sanitizer_block_wrappers=(("{-", "-}"),),
        documentation_source=(
            "https://github.com/B-Lang-org/bsc/blob/"
            "941eecfe1bf583ce717a10965a0bcb6f6b3b8773/"
            "doc/BH_ref_guide/BH_lang.tex#L510-L534"
        ),
        implementation_source=(
            "https://github.com/B-Lang-org/bsc/blob/"
            "941eecfe1bf583ce717a10965a0bcb6f6b3b8773/"
            "src/comp/Lex.hs#L198-L231"
        ),
        confidence="verified",
        notes=(
            "BH line comments require the lexer dash-run boundary and a physical "
            "LF. Nested {- -} comments exclude {-# #-} compiler pragmas."
        ),
    ),
    CommentSyntax(
        family_name="bqn_style",
        canonical_name="bqn",
        contextual_extractor="bqn_comments",
        shared_contextual_examples=(
            CommentExample(
                "value # note\nnext",
                "# note",
                "BQN hash line comment outside literals.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("#", ""),),
        documentation_source=(
            "https://github.com/mlochbaum/BQN/blob/"
            "1d43de0a8d66010c55f26fafb967c648d2fefade/"
            "spec/token.md#L3-L23"
        ),
        implementation_source=(
            "https://github.com/mlochbaum/BQN/blob/"
            "1d43de0a8d66010c55f26fafb967c648d2fefade/"
            "spec/token.md#L3-L23"
        ),
        confidence="verified",
        notes=(
            "BQN double-quoted strings may span lines and escape a quote by "
            "doubling it; single-code-point character literals are protected."
        ),
    ),
    CommentSyntax(
        family_name="yaml_style",
        canonical_name="yaml",
        aliases=("buildstream", "oasv2_yaml", "oasv3_yaml"),
        contextual_extractor="yaml_comments",
        shared_contextual_examples=(
            CommentExample(
                "kind: manual  # note\ndepends: []",
                "# note",
                "YAML separation-space hash comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("#", ""),),
        documentation_source=(
            "https://github.com/yaml/yaml-spec/blob/"
            "1b1a1be43bd6e0cfec45caf0e40af3b5d2bb7f8a/"
            "spec/1.2.2/spec.md#L2791-L2868"
        ),
        implementation_source=(
            "https://github.com/apache/buildstream/blob/"
            "ad6b437d760df8b3a8cdb151bd3da93ca3a77006/"
            "src/buildstream/_yaml.pyx#L244-L325"
        ),
        confidence="cross-checked",
        notes=(
            "BuildStream consumes YAML. Comments require a separation boundary; "
            "quoted scalars and literal or folded block-scalar bodies are protected."
        ),
    ),
    CommentSyntax(
        family_name="caddyfile_style",
        canonical_name="caddyfile",
        contextual_extractor="caddyfile_comments",
        shared_contextual_examples=(
            CommentExample(
                "reverse_proxy localhost:9000 # note\n",
                "# note",
                "Caddyfile hash comment at a token boundary.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("#", ""),),
        documentation_source="https://caddyserver.com/docs/caddyfile/concepts#comments",
        implementation_source=(
            "https://github.com/caddyserver/caddy/blob/"
            "e096ca9503188f057c69a049f709fdade6077631/"
            "caddyconfig/caddyfile/lexer.go#L71-L238"
        ),
        confidence="verified",
        notes=(
            "A hash starts a comment only at the beginning of a lexer token. "
            "Quoted tokens, backticks, heredocs, and escaped newlines are protected."
        ),
        language_versions=(
            CommentLanguageVersions(
                languages=("caddyfile",),
                default="2.1",
                versions=(
                    CommentLanguageVersion(
                        name="2.0",
                        aliases=("v1",),
                        release="0",
                        span="Caddy 1.x and 2.0",
                        comment_rules=(
                            "An unquoted # anywhere, even inside a token, starts a comment to the "
                            "end of the line."
                        ),
                        contextual_extractor="caddyfile_20_comments",
                        examples=(
                            CommentExample(
                                "redir /help https://example.com/docs#install\n",
                                "#install",
                                "Before Caddy 2.1, a # inside a token starts a comment.",
                                kind="line",
                            ),
                        ),
                        documentation_source=(
                            "https://github.com/caddyserver/caddy/blob/v2.0.0/caddyconfig/"
                            "caddyfile/lexer.go#L141-L146"
                        ),
                    ),
                    CommentLanguageVersion(
                        name="2.1",
                        aliases=("current",),
                        release="2.1",
                        span="Caddy 2.1 and later",
                        comment_rules=(
                            "# starts a comment only at the start of a token; quotes, backticks, "
                            "and heredocs protect it."
                        ),
                        documentation_source=(
                            "https://github.com/caddyserver/caddy/blob/v2.1.0/caddyconfig/"
                            "caddyfile/lexer.go#L144"
                        ),
                    ),
                ),
            ),
        ),
    ),
    CommentSyntax(
        family_name="cairo_zero_style",
        canonical_name="cairo_zero",
        contextual_extractor="cairo_zero_comments",
        shared_contextual_examples=(
            CommentExample(
                "let value = 1; // note\nret;",
                "// note",
                "Cairo Zero slash line comment outside hints.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("//", ""),),
        documentation_source=(
            "https://github.com/starkware-libs/cairo-lang/blob/"
            "cf9bf972bede402a125e8638bb258e77563ae933/"
            "src/starkware/cairo/lang/compiler/cairo.ebnf#L141-L183"
        ),
        implementation_source=(
            "https://github.com/starkware-libs/cairo-lang/blob/"
            "cf9bf972bede402a125e8638bb258e77563ae933/"
            "src/starkware/cairo/lang/compiler/cairo.ebnf#L1-L10"
        ),
        confidence="verified",
        notes=(
            "Cairo Zero %{ %} hint bodies and quoted literals take precedence "
            "over // comment recognition."
        ),
        language_versions=(
            CommentLanguageVersions(
                languages=("cairo_zero",),
                default="0.10",
                versions=(
                    CommentLanguageVersion(
                        name="0.9",
                        aliases=("cairo0.9",),
                        release="0",
                        span="cairo-lang Cairo 0 releases before 0.10.0",
                        comment_rules=(
                            "# starts a comment to the end of the line; // is not a "
                            "comment. Hint bodies and quoted literals are protected."
                        ),
                        contextual_extractor="cairo_zero_09_comments",
                        sanitizer_line_wrappers=(("#", ""),),
                        examples=(
                            CommentExample(
                                "const SIZE = 3  # cells\nret;",
                                "# cells",
                                "Before cairo-lang 0.10, # starts a line comment.",
                                kind="line",
                                inline_compatible=True,
                                grouped_line_compatible=True,
                            ),
                        ),
                        documentation_source=(
                            "https://github.com/starkware-libs/cairo-lang/blob/v0.9.1/"
                            "src/starkware/cairo/lang/compiler/cairo.ebnf#L143 "
                            "(COMMENT: /#.*/)"
                        ),
                    ),
                    CommentLanguageVersion(
                        name="0.10",
                        aliases=("cairo0.10", "current"),
                        release="0.10",
                        span="cairo-lang Cairo 0 releases 0.10.0 and later",
                        comment_rules=(
                            "// starts a comment to the end of the line; # is not a "
                            "comment. Hint bodies and quoted literals are protected."
                        ),
                        documentation_source=(
                            "https://github.com/starkware-libs/cairo-lang/blob/v0.10.0/"
                            "src/starkware/cairo/lang/compiler/cairo.ebnf#L143 "
                            "(COMMENT: /\\/\\/.*/)"
                        ),
                    ),
                ),
            ),
        ),
    ),
    CommentSyntax(
        family_name="carbon_style",
        canonical_name="carbon",
        regex_patterns=(r"(?<!/)//(?=[ \t\n]|\Z)[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "var value: i32 = 1; // note\nreturn value;",
                "// note",
                "Carbon whitespace-delimited line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("//", ""),),
        documentation_source=(
            "https://github.com/carbon-language/carbon-lang/blob/"
            "46b5482bb4723a51b9f6870f4644d7de6af29f07/"
            "docs/design/lexical_conventions/comments.md"
        ),
        implementation_source=(
            "https://github.com/carbon-language/carbon-lang/blob/"
            "46b5482bb4723a51b9f6870f4644d7de6af29f07/toolchain/lex/lex.cpp"
        ),
        confidence="verified",
        notes=(
            "The byte after // must be ASCII space, tab, LF, or EOF. Carbon "
            "simple, raw, and block literals are masked before matching."
        ),
    ),
    CommentSyntax(
        family_name="circom_style",
        canonical_name="circom",
        regex_patterns=(
            r"/\*[\S\s]*?\*/",
            r"/{2}[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "signal input value; // note\nvalue === 1;",
                "// note",
                "Circom line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "signal input value; /* block note */ value === 1;",
                "/* block note */",
                "Circom first-close block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("//", ""),),
        sanitizer_block_wrappers=(("/*", "*/"),),
        documentation_source=(
            "https://github.com/iden3/circom/blob/"
            "a100faedb1c62d4d3e1463f8a3f88342d82351cd/"
            "mkdocs/docs/circom-language/comment-lines.md"
        ),
        implementation_source=(
            "https://github.com/iden3/circom/blob/"
            "a100faedb1c62d4d3e1463f8a3f88342d82351cd/"
            "parser/src/parser_logic.rs#L9-L85"
        ),
        confidence="verified",
        notes=(
            "Circom preprocessing recognizes // and first-close /* */ markers "
            "without maintaining quoted-string state. Unclosed blocks are not "
            "reported as complete comments."
        ),
    ),
    CommentSyntax(
        family_name="clue_style",
        canonical_name="clue",
        contextual_extractor="clue_comments",
        shared_contextual_examples=(
            CommentExample(
                "local value = 1 // note\nprint(value)",
                "// note",
                "Clue line comment outside strings.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "local value = 1 /* block note */ print(value)",
                "/* block note */",
                "Clue first-close block comment.",
                kind="block",
                inline_compatible=True,
            ),
            CommentExample(
                "local value = 1 /* block note",
                "/* block note",
                "Clue EOF-terminated block comment.",
                kind="block",
                inline_compatible=True,
                consumes_eof=True,
            ),
        ),
        sanitizer_line_wrappers=(("//", ""),),
        sanitizer_block_wrappers=(("/*", "*/"),),
        unclosed_block_openers=("/*",),
        documentation_source=(
            "https://github.com/ClueLang/Clue/blob/"
            "78ce10c1d7a985b294ce7d08ef03565cc956e3c1/README.md#general-syntax-differences"
        ),
        implementation_source=(
            "https://github.com/ClueLang/Clue/blob/"
            "78ce10c1d7a985b294ce7d08ef03565cc956e3c1/"
            "core/src/preprocessor.rs#L97-L231"
        ),
        confidence="verified",
        notes=(
            "Clue protects single, double, and backtick strings. Its pinned "
            "preprocessor accepts an unclosed /* block through EOF."
        ),
    ),
    CommentSyntax(
        family_name="crontab_style",
        canonical_name="crontab",
        regex_patterns=(r"(?m)^[ \t]*#[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "  # note\n0 0 * * * rotate",
                "  # note",
                "Cronie full-line comment after ASCII indentation.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("#", ""),),
        documentation_source=(
            "https://github.com/cronie-crond/cronie/blob/"
            "5f9f16b5663becefdd0dd70df31c0ef5ac36f943/man/crontab.5#L25-L43"
        ),
        implementation_source=(
            "https://github.com/cronie-crond/cronie/blob/"
            "5f9f16b5663becefdd0dd70df31c0ef5ac36f943/src/misc.c#L416-L455"
        ),
        confidence="verified",
        notes=(
            "Only a # that is the first non-space/tab byte starts a Cronie "
            "comment. Hashes on active schedule or assignment lines are data."
        ),
    ),
    CommentSyntax(
        family_name="cylc_style",
        canonical_name="cylc",
        contextual_extractor="cylc_comments",
        shared_contextual_examples=(
            CommentExample(
                "[runtime] # note\n    script = true",
                "# note",
                "Cylc native trailing comment outside quoted values.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("#", ""),),
        documentation_source=(
            "https://cylc.github.io/cylc-doc/stable/html/reference/config/file-format.html"
        ),
        implementation_source=(
            "https://github.com/cylc/cylc-flow/blob/"
            "4ae32d5218fdfa87f26f200ca3659e1e1ade4276/"
            "cylc/flow/parsec/fileparse.py#L69-L121"
        ),
        confidence="cross-checked",
        notes=(
            "Native # comments are extracted outside single, double, and "
            "triple-quoted values. #!jinja2 and Jinja comment regions are excluded."
        ),
    ),
    CommentSyntax(
        family_name="d2_style",
        canonical_name="d2",
        contextual_extractor="d2_comments",
        shared_contextual_examples=(
            CommentExample(
                "client -> server # note\nserver: ok",
                "# note",
                "D2 hash comment outside scalar values.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                '""" block note """\nclient -> server',
                '""" block note """',
                "D2 block comment at a map-node position.",
                kind="block",
            ),
        ),
        sanitizer_line_wrappers=(("#", ""),),
        sanitizer_block_wrappers=(('"""', '"""'),),
        documentation_source="https://d2lang.com/tour/comments/",
        implementation_source=(
            "https://github.com/terrastruct/d2/blob/"
            "2446e247b6d7d5b9395a1ae8ad1e9c2641231035/"
            "d2parser/parse.go#L466-L633"
        ),
        confidence="verified",
        notes=(
            "Triple-quote blocks are comments only where the official parser "
            "begins a map node. Quoted and |...| block-string values are protected."
        ),
    ),
    CommentSyntax(
        family_name="dotenv_style",
        canonical_name="dotenv",
        contextual_extractor="dotenv_comments",
        shared_contextual_examples=(
            CommentExample(
                "TOKEN=value# note\nNEXT=ok",
                "# note",
                "Node dotenv inline comment in an unquoted value.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("#", ""),),
        documentation_source=(
            "https://github.com/motdotla/dotenv/blob/"
            "c0e32b8267b69a438bc0cc31345f73b5e2f037db/README.md#comments"
        ),
        implementation_source=(
            "https://github.com/motdotla/dotenv/blob/"
            "c0e32b8267b69a438bc0cc31345f73b5e2f037db/lib/main.js#L12-L215"
        ),
        confidence="verified",
        notes=(
            "Implements Node dotenv >=15 assignment, quote, multiline, and "
            "unclosed-quote fallback behavior. Invalid assignment lines are ignored."
        ),
        language_versions=(
            CommentLanguageVersions(
                languages=("dotenv",),
                default="16",
                versions=(
                    CommentLanguageVersion(
                        name="13",
                        release="0",
                        span="Node dotenv 13 and earlier",
                        comment_rules=(
                            "Only lines whose first non-blank character is # are comments; # in a "
                            "value is literal."
                        ),
                        contextual_extractor="dotenv_13_comments",
                        examples=(
                            CommentExample(
                                "# note\nSECRET=abc # rotate\n",
                                "# note",
                                "Before 14.0, dotenv has no inline comments.",
                                kind="line",
                            ),
                        ),
                        documentation_source=(
                            "https://github.com/motdotla/dotenv/blob/v13.0.1/lib/main.js "
                            "(RE_INI_KEY_VAL)"
                        ),
                    ),
                    CommentLanguageVersion(
                        name="14.0",
                        release="14.0",
                        span="Node dotenv 14.0.0 through 14.3.1",
                        comment_rules=(
                            "The first # after an unquoted value starts a comment; single-line "
                            "quotes protect #."
                        ),
                        contextual_extractor="dotenv_14_0_comments",
                        examples=(
                            CommentExample(
                                "TOKEN=`x#y`\n",
                                "#y`",
                                "Node dotenv 14.0 does not treat backticks as quotes.",
                                kind="line",
                            ),
                        ),
                        documentation_source=(
                            "https://github.com/motdotla/dotenv/blob/v14.0.0/lib/main.js "
                            "(RE_INI_KEY_VAL)"
                        ),
                    ),
                    CommentLanguageVersion(
                        name="14.3.2",
                        release="14.3.2",
                        span="Node dotenv 14.3.2",
                        comment_rules=(
                            "Only a # after white space starts an inline comment; values are "
                            "single-line."
                        ),
                        contextual_extractor="dotenv_14_3_2_comments",
                        examples=(
                            CommentExample(
                                'KEY="a\n# b\nc"\n',
                                "# b",
                                "Node dotenv 14 splits lines before parsing quoted values.",
                                kind="line",
                            ),
                        ),
                        documentation_source=(
                            "https://github.com/motdotla/dotenv/blob/v14.3.2/lib/main.js "
                            "(RE_INI_KEY_VAL)"
                        ),
                    ),
                    CommentLanguageVersion(
                        name="15",
                        release="15",
                        span="Node dotenv 15",
                        comment_rules=(
                            "Any unquoted # starts a comment; single- and double-quoted values may "
                            "span lines."
                        ),
                        contextual_extractor="dotenv_15_comments",
                        examples=(
                            CommentExample(
                                "TOKEN=`x#y`\n",
                                "#y`",
                                "Node dotenv 15 does not treat backticks as quotes.",
                                kind="line",
                            ),
                        ),
                        documentation_source=(
                            "https://github.com/motdotla/dotenv/blob/v15.0.0/lib/main.js (LINE)"
                        ),
                    ),
                    CommentLanguageVersion(
                        name="16",
                        aliases=(
                            "17",
                            "current",
                        ),
                        release="16",
                        span="Node dotenv 16 and later",
                        comment_rules="As 15, plus backtick-quoted values that may span lines.",
                        documentation_source=(
                            "https://github.com/motdotla/dotenv/blob/v16.0.0/lib/main.js (LINE)"
                        ),
                    ),
                ),
            ),
        ),
    ),
    CommentSyntax(
        family_name="edge_style",
        canonical_name="edge",
        contextual_extractor="edge_comments",
        shared_contextual_examples=(
            CommentExample(
                "<p>{{-- note --}} {{ value }}</p>",
                "{{-- note --}}",
                "Edge raw-template comment.",
                kind="block",
                inline_compatible=True,
            ),
            CommentExample(
                "{{-- outer {{-- inner --}} tail --}}",
                "{{-- outer {{-- inner --}} tail --}}",
                "Brace-balanced nested-looking Edge comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        sanitizer_block_wrappers=(("{{--", "--}}"),),
        documentation_source="https://edgejs.dev/docs/syntax_specification#comments",
        implementation_source=(
            "https://github.com/edge-js/lexer/blob/"
            "730f916e350498c2eb93817e490eb4bfd52edef4/src/tokenizer.ts#L299-L420"
        ),
        confidence="verified",
        notes=(
            "Edge comments are recognized only in raw template mode. Their "
            "closing marker is eligible only when ordinary brace depth is zero."
        ),
    ),
    CommentSyntax(
        family_name="gdshader_style",
        canonical_name="gdshader",
        contextual_extractor="gdshader_comments",
        shared_contextual_examples=(
            CommentExample(
                "uniform vec4 tint; // material note\n",
                "// material note",
                "GDShader LF-terminated line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/** inspector note */\nuniform float strength;",
                "/** inspector note */",
                "GDShader documentation block comment.",
                kind="block",
                inline_compatible=True,
            ),
            CommentExample(
                "shader_type spatial;\n/* accepted through EOF",
                "/* accepted through EOF",
                "GDShader lexer-accepted EOF block comment.",
                kind="block",
                inline_compatible=True,
                consumes_eof=True,
            ),
        ),
        sanitizer_line_wrappers=(("//", ""),),
        sanitizer_block_wrappers=(("/**", "*/"), ("/*", "*/")),
        unclosed_block_openers=("/*",),
        documentation_source=(
            "https://github.com/godotengine/godot-docs/blob/"
            "cc147ca70ba721db8b5dcf5864f211d9687f8f85/tutorials/shaders/"
            "shader_reference/shading_language.rst#comments"
        ),
        implementation_source=(
            "https://github.com/godotengine/godot/blob/"
            "eda2a482e9ce82e4056cfffae0ea98c1954605a1/servers/rendering/"
            "shader_language.cpp#L418-L480"
        ),
        confidence="verified",
        notes=(
            "Line comments terminate only at LF, so a bare CR remains comment "
            "content. Non-nested block comments are accepted through EOF."
        ),
    ),
    CommentSyntax(
        family_name="glimmer_js_style",
        canonical_name="glimmer_js",
        contextual_extractor="glimmer_comments",
        shared_contextual_examples=(
            CommentExample(
                "// host note\n<template><p>ok</p></template>",
                "// host note",
                "Glimmer JS host-language line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/* block note */\n<template><p>ok</p></template>",
                "/* block note */",
                "Glimmer JS host-language block comment.",
                kind="block",
                inline_compatible=True,
            ),
            CommentExample(
                "<template>{{!-- template note --}}</template>",
                "{{!-- template note --}}",
                "Glimmer long Handlebars comment inside a content tag.",
                kind="block",
                inline_compatible=True,
                standalone_compatible=False,
            ),
            CommentExample(
                "<template><!-- markup note --></template>",
                "<!-- markup note -->",
                "Glimmer HTML comment inside a content tag.",
                kind="block",
                inline_compatible=True,
                standalone_compatible=False,
            ),
        ),
        sanitizer_line_wrappers=(("//", ""),),
        sanitizer_block_wrappers=(
            ("{{~!--", "--~}}"),
            ("{{~!--", "--}}"),
            ("{{!--", "--~}}"),
            ("{{!--", "--}}"),
            ("{{~!", "~}}"),
            ("{{~!", "}}"),
            ("{{!", "~}}"),
            ("{{!", "}}"),
            ("<!--", "-->"),
            ("/*", "*/"),
        ),
        documentation_source=(
            "https://github.com/emberjs/rfcs/blob/"
            "227ec9b21ed0bdecc01713d3637e79d509e7d553/text/0779-first-class-"
            "component-templates.md"
        ),
        implementation_source=(
            "https://github.com/embroider-build/content-tag/blob/"
            "b0426e5dadc1348d57a80ad95229e42e9556207f/src/locate.rs#L33-L88"
        ),
        confidence="cross-checked",
        notes=(
            "JavaScript comments are active outside parser-recognized content "
            "tags; Handlebars and HTML comments are active only inside them."
        ),
    ),
    CommentSyntax(
        family_name="glimmer_ts_style",
        canonical_name="glimmer_ts",
        contextual_extractor="glimmer_comments",
        shared_contextual_examples=(
            CommentExample(
                "/* block note */\n<template><p>ok</p></template>",
                "/* block note */",
                "Glimmer TS host-language block comment.",
                kind="block",
                inline_compatible=True,
            ),
            CommentExample(
                "<template><button {{! attr note }}>ok</button></template>",
                "{{! attr note }}",
                "Glimmer short comment between attributes.",
                kind="block",
                inline_compatible=True,
                standalone_compatible=False,
            ),
        ),
        sanitizer_line_wrappers=(("//", ""),),
        sanitizer_block_wrappers=(
            ("{{~!--", "--~}}"),
            ("{{~!--", "--}}"),
            ("{{!--", "--~}}"),
            ("{{!--", "--}}"),
            ("{{~!", "~}}"),
            ("{{~!", "}}"),
            ("{{!", "~}}"),
            ("{{!", "}}"),
            ("<!--", "-->"),
            ("/*", "*/"),
        ),
        documentation_source=("https://guides.emberjs.com/v6.8.0/components/template-tag-format/"),
        implementation_source=(
            "https://github.com/embroider-build/content-tag/blob/"
            "b0426e5dadc1348d57a80ad95229e42e9556207f/src/locate.rs"
        ),
        confidence="cross-checked",
        notes=(
            "TypeScript comments are active outside parser-recognized content "
            "tags; Glimmer comments are active only inside those ranges."
        ),
    ),
    CommentSyntax(
        family_name="godot_resource_style",
        canonical_name="godot_resource",
        contextual_extractor="godot_resource_comments",
        shared_contextual_examples=(
            CommentExample(
                '[node name="Demo"] ; scene note\ncolor = #ff00ff',
                "; scene note",
                "Godot resource semicolon comment outside a Variant string.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=((";", ""),),
        documentation_source=(
            "https://docs.godotengine.org/en/4.6/engine_details/file_formats/tscn.html"
        ),
        implementation_source=(
            "https://github.com/godotengine/godot/blob/"
            "35e80b3a8822a9df9be390814b62f44c0a9c69e8/core/variant/"
            "variant_parser.cpp#L162-L415"
        ),
        confidence="cross-checked",
        notes=(
            "Semicolons start comments outside Variant strings. Hash-prefixed "
            "Color values are source data, not GDScript comments."
        ),
    ),
    CommentSyntax(
        family_name="imba_style",
        canonical_name="imba",
        contextual_extractor="imba_comments",
        shared_contextual_examples=(
            CommentExample(
                "tag App\n# component note\n",
                "# component note",
                "Imba whitespace-qualified hash line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "### block note ###",
                "### block note ###",
                "Version-common Imba triple-hash block comment.",
                kind="block",
                inline_compatible=True,
            ),
            CommentExample(
                "### accepted through EOF",
                "### accepted through EOF",
                "Nonempty Imba triple-hash block accepted at EOF.",
                kind="block",
                inline_compatible=True,
                consumes_eof=True,
            ),
        ),
        sanitizer_line_wrappers=(("#", ""),),
        sanitizer_block_wrappers=(("###", "###"),),
        unclosed_block_openers=("###",),
        documentation_source=(
            "https://github.com/imba/imba/blob/"
            "9eaa35332461a3dde4342e67cd1f1e40fb16400e/apps/imba.io/content/docs/"
            "basic-syntax.md#L650-L668"
        ),
        implementation_source=(
            "https://github.com/imba/imba/blob/"
            "9eaa35332461a3dde4342e67cd1f1e40fb16400e/packages/imba/src/compiler/"
            "lexer.mjs#L204-L240"
        ),
        confidence="cross-checked",
        notes=(
            "Only hash forms shared by Imba 1 and 2 are enabled. Unversioned "
            "source does not enable Imba-2-only slash comments."
        ),
        language_versions=(
            CommentLanguageVersions(
                languages=("imba",),
                default="imba1",
                notes=(
                    "Imba 2 is published as alpha and documents only # and ### comments, so imba1 "
                    "stays the default."
                ),
                versions=(
                    CommentLanguageVersion(
                        name="imba1",
                        aliases=(
                            "1",
                            "1.5",
                        ),
                        release="",
                        span="Imba 1.x",
                        comment_rules=(
                            "# followed by white space or !, or at the line end, and ### ... ### "
                            "blocks."
                        ),
                        documentation_source=(
                            "https://github.com/imba/imba/blob/v1.5.2/src/compiler/"
                            "lexer.imba#L143-L145"
                        ),
                    ),
                    CommentLanguageVersion(
                        name="imba2",
                        aliases=("2",),
                        release="",
                        span="Imba 2 (2.0.0 alpha series)",
                        comment_rules=(
                            "The Imba 1 forms plus // (not ///) line comments and /* */ blocks."
                        ),
                        contextual_extractor="imba2_comments",
                        sanitizer_line_wrappers=(("//", ""),),
                        sanitizer_block_wrappers=(("/*", "*/"),),
                        examples=(
                            CommentExample(
                                "let x = 1 // note\n",
                                "// note",
                                "Imba 2 accepts // line comments.",
                                kind="line",
                            ),
                        ),
                        documentation_source=(
                            "https://github.com/imba/imba/blob/"
                            "9eaa35332461a3dde4342e67cd1f1e40fb16400e/packages/imba/src/compiler/"
                            "lexer.mjs#L215-L217"
                        ),
                    ),
                ),
            ),
        ),
    ),
    CommentSyntax(
        family_name="ink_style",
        canonical_name="ink",
        contextual_extractor="ink_comments",
        shared_contextual_examples=(
            CommentExample(
                "Hello. // author note\nNext.",
                "// author note",
                "Ink raw-prepass line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/* multiline\n   author note */\nStory text",
                "/* multiline\n   author note */",
                "Ink non-nested block comment.",
                kind="block",
                inline_compatible=True,
            ),
            CommentExample(
                "/* accepted through EOF",
                "/* accepted through EOF",
                "Nonempty Ink block comment accepted through EOF.",
                kind="block",
                inline_compatible=True,
                consumes_eof=True,
            ),
        ),
        sanitizer_line_wrappers=(("//", ""),),
        sanitizer_block_wrappers=(("/*", "*/"),),
        unclosed_block_openers=("/*",),
        documentation_source=(
            "https://github.com/inkle/ink/blob/"
            "35c63e52f1d36060930dc7ed3cfba38ea224b528/Documentation/"
            "WritingWithInk.md#L77-L96"
        ),
        implementation_source=(
            "https://github.com/inkle/ink/blob/"
            "35c63e52f1d36060930dc7ed3cfba38ea224b528/compiler/InkParser/"
            "CommentEliminator.cs"
        ),
        confidence="verified",
        notes=(
            "Ink eliminates comments before parsing, so quoted prose and URLs "
            "do not protect markers. A nonempty unclosed block reaches EOF."
        ),
    ),
    CommentSyntax(
        family_name="vento_style",
        canonical_name="vento",
        regex_patterns=(r"\{\{#[\S\s]*?#\}\}",),
        shared_regex_examples=(
            CommentExample(
                "<h1>{{#- block note -#}}{{ title }}</h1>",
                "{{#- block note -#}}",
                "Vento template comment with whitespace trim controls.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        sanitizer_block_wrappers=(
            ("{{#-", "-#}}"),
            ("{{#-", "#}}"),
            ("{{#", "-#}}"),
            ("{{#", "#}}"),
        ),
        documentation_source=(
            "https://github.com/ventojs/vento/blob/"
            "90a135acbaabb031382278e0903eea0e2c34857f/docs/4.syntax/8.comments.md#L1-L24"
        ),
        implementation_source=(
            "https://github.com/ventojs/vento/blob/"
            "90a135acbaabb031382278e0903eea0e2c34857f/core/tokenizer.ts#L11-L42"
        ),
        confidence="verified",
        notes=(
            "Vento comments use the first #}} closer and do not nest. A missing "
            "closer is a compile error and is not returned as a complete comment."
        ),
    ),
    CommentSyntax(
        family_name="webassembly_interface_type_style",
        canonical_name="webassembly_interface_type",
        aliases=("wit",),
        regex_patterns=(r"/{2}[^\r\n]*",),
        nested_delimiters=(("/*", "*/"),),
        shared_regex_examples=(
            CommentExample(
                "package demo:api;\n/// note\ninterface api {}",
                "/// note",
                "WIT documentation line comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "interface api { /* outer /* rationale */ outer */ run: func(); }",
                "/* outer /* rationale */ outer */",
                "WIT recursively nested block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("//", ""),),
        sanitizer_block_wrappers=(("/*", "*/"),),
        documentation_source=(
            "https://github.com/WebAssembly/component-model/blob/"
            "73b7ad51d3b5d6f1ef53c923d8c585e28b242bcc/design/mvp/WIT.md#L1017-L1039"
        ),
        implementation_source=(
            "https://github.com/bytecodealliance/wasm-tools/blob/"
            "606b4cc5503015ce539e6d6a7ec39a774710e114/crates/wit-parser/"
            "src/ast/lex.rs#L246-L285"
        ),
        confidence="verified",
        notes=(
            "WIT uses slash line comments and recursively nested slash-star "
            "blocks. Core WebAssembly ;; and (; ;) forms are intentionally excluded."
        ),
    ),
    CommentSyntax(
        family_name="wgsl_style",
        canonical_name="wgsl",
        regex_patterns=(r"/{2}[^\n\v\f\r\u0085\u2028\u2029]*",),
        nested_delimiters=(("/*", "*/"),),
        shared_regex_examples=(
            CommentExample(
                "let value = 1; // shader note\u2028let next = 2;",
                "// shader note",
                "WGSL line comment terminated by a Unicode line separator.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        shared_nested_examples=(
            CommentExample(
                "let value = 1; /* outer /* rationale */ outer */",
                "/* outer /* rationale */ outer */",
                "WGSL recursively nested block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("//", ""),),
        sanitizer_block_wrappers=(("/*", "*/"),),
        documentation_source=(
            "https://github.com/gpuweb/gpuweb/blob/"
            "d390da5f80f18e82d9535a40c6f2f1f65e6884ae/wgsl/index.bs#L1059-L1094"
        ),
        implementation_source=(
            "https://github.com/gpuweb/tree-sitter-wgsl/blob/"
            "52e3c620a9c316cc8c1d504dd1908eb8cebe255b/src/scanner.c#L655-L677"
        ),
        confidence="verified",
        notes=(
            "WGSL line comments recognize the complete normative line-break set, "
            "and slash-star comments nest recursively. Unclosed blocks are invalid."
        ),
    ),
    CommentSyntax(
        family_name="kdl_style",
        canonical_name="kdl",
        contextual_extractor="kdl_comments",
        shared_contextual_examples=(
            CommentExample(
                'server host="localhost" // note\n',
                "// note",
                "KDL line comment outside quoted and raw strings.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "server /* outer /* block note */ outer */ port=8080",
                "/* outer /* block note */ outer */",
                "KDL recursively nested block comment.",
                kind="nested",
                inline_compatible=True,
            ),
            CommentExample(
                '/- legacy host="old.example" {\n  child value=1\n}\nkept value=2',
                '/- legacy host="old.example" {\n  child value=1\n}',
                "KDL slashdash comment spanning one complete node.",
                kind="contextual",
            ),
        ),
        sanitizer_line_wrappers=(("//", ""), ("/-", "")),
        sanitizer_block_wrappers=(("/*", "*/"),),
        documentation_source=(
            "https://github.com/kdl-org/kdl/blob/"
            "b8570137b6d3486a6b0cd64706f749c624ffd0ad/"
            "draft-marchan-kdl2.md#L870-L901"
        ),
        implementation_source=(
            "https://github.com/kdl-org/kdl/blob/"
            "b8570137b6d3486a6b0cd64706f749c624ffd0ad/"
            "draft-marchan-kdl2.md#L1008-L1065"
        ),
        confidence="verified",
        notes=(
            "Implements the KDL v1/v2 common lexical forms and grammar-scoped "
            "slashdash nodes, arguments, properties, and child blocks. The "
            "kdl-version marker and incomplete components are excluded."
        ),
    ),
    CommentSyntax(
        family_name="kickstart_style",
        canonical_name="kickstart",
        contextual_extractor="kickstart_comments",
        shared_contextual_examples=(
            CommentExample(
                "  # note\nreboot",
                "# note",
                "Indented pykickstart host comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                'url --url="https://host/tree#fragment" # note\nreboot',
                "# note",
                "Unquoted inline hash comment in command state.",
                kind="line",
                inline_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("#", ""),),
        documentation_source=(
            "https://github.com/rhinstaller/pykickstart/blob/"
            "15c401010c5bb8984deca9a4d132f99f938bffc3/"
            "docs/kickstart-docs.rst#L52-L97"
        ),
        implementation_source=(
            "https://github.com/rhinstaller/pykickstart/blob/"
            "15c401010c5bb8984deca9a4d132f99f938bffc3/"
            "pykickstart/parser.py#L649-L784"
        ),
        confidence="cross-checked",
        notes=(
            "Tracks command, ordinary section, and pykickstart all-lines states. "
            "Raw script/certificate bodies and semantic #platform= records are "
            "not returned as host comments."
        ),
    ),
    CommentSyntax(
        family_name="java_template_engine_style",
        canonical_name="java_template_engine",
        aliases=("jte",),
        contextual_extractor="java_template_engine_comments",
        shared_contextual_examples=(
            CommentExample(
                "Hello <%-- block note --%> world",
                "<%-- block note --%>",
                "Native JTE comment in template text mode.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        sanitizer_block_wrappers=(("<%--", "--%>"),),
        documentation_source=(
            "https://github.com/casid/jte/blob/"
            "5b2f6983f6eb3d804ddb3cf4a5dea4876dc1e60d/docs/syntax.md#L184-L194"
        ),
        implementation_source=(
            "https://github.com/casid/jte/blob/"
            "5b2f6983f6eb3d804ddb3cf4a5dea4876dc1e60d/jte/src/main/java/"
            "gg/jte/compiler/TemplateParser.java#L121-L170"
        ),
        confidence="verified",
        notes=(
            "Only native <%-- ... --%> comments in Text mode are enabled. Java "
            "expressions, @raw bodies, output-language comments, and unclosed "
            "native comments are excluded."
        ),
    ),
    CommentSyntax(
        family_name="jcl_style",
        canonical_name="jcl",
        contextual_extractor="jcl_comments",
        shared_contextual_examples=(
            CommentExample(
                "//* note\n//STEP EXEC PGM=IEFBR14",
                "//* note",
                "Base JCL comment statement in columns one through three.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "//STEP EXEC PGM=IEFBR14  compatibility note",
                "compatibility note",
                "Grammar-delimited JCL trailing comment field.",
                kind="contextual",
                inline_compatible=True,
                standalone_compatible=False,
            ),
        ),
        sanitizer_line_wrappers=(("//*", ""),),
        documentation_source=(
            "https://www.ibm.com/docs/en/zos/3.2.0?topic=statements-jcl-statement-fields"
        ),
        implementation_source=("https://www.ibm.com/docs/en/zos/3.2.0?topic=statement-parameter"),
        confidence="cross-checked",
        notes=(
            "Implements base z/OS JCL comment statements and conservative trailing "
            "fields through column 71. DD *, DD DATA, and custom DLM payload state "
            "prevents embedded records from being reclassified."
        ),
    ),
    CommentSyntax(
        family_name="just_style",
        canonical_name="just",
        contextual_extractor="just_comments",
        shared_contextual_examples=(
            CommentExample(
                "# note\nbuild:\n  echo ok",
                "# note",
                "Native top-level Just documentation comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "build: # note\n  echo ok # recipe text",
                "# note",
                "Native trailing comment on a Just recipe header.",
                kind="line",
                inline_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("#", ""),),
        documentation_source=(
            "https://github.com/casey/just/blob/"
            "13bf03f642f4cec7799c19f1f8f039e1cb3b095d/README.md#L1516-L1556"
        ),
        implementation_source=(
            "https://github.com/casey/just/blob/"
            "13bf03f642f4cec7799c19f1f8f039e1cb3b095d/src/lexer.rs#L474-L817"
        ),
        confidence="verified",
        notes=(
            "Returns hash comments only in the normal lexer mode. Indented shell, "
            "shebang, and script recipe bodies remain source text regardless of "
            "the ignore-comments setting."
        ),
    ),
    CommentSyntax(
        family_name="leo_style",
        canonical_name="leo",
        regex_patterns=(
            r"//[^\r\n\u202a-\u202e\u2066-\u2069]*",
            r"/\*[^\u202a-\u202e\u2066-\u2069]*?\*/",
        ),
        shared_regex_examples=(
            CommentExample(
                "let amount = 1u64; // range note\nreturn amount;",
                "// range note",
                "Leo line comment outside a static string.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "transition mint() { /* block note */ return; }",
                "/* block note */",
                "Leo non-nested block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("//", ""),),
        sanitizer_block_wrappers=(("/*", "*/"),),
        documentation_source=(
            "https://github.com/ProvableHQ/leo/blob/"
            "320a595caae5804cf02762902db768d51611237a/crates/parser-rowan/"
            "src/lexer.rs#L56-L105"
        ),
        implementation_source=(
            "https://github.com/ProvableHQ/leo/blob/"
            "320a595caae5804cf02762902db768d51611237a/crates/parser-rowan/"
            "src/lexer.rs#L1105-L1129"
        ),
        confidence="verified",
        notes=(
            "Bidi controls terminate Leo line-comment tokens and invalidate block "
            "comments. Blocks close at the first */; malformed EOF blocks are excluded."
        ),
    ),
    CommentSyntax(
        family_name="linear_programming_style",
        canonical_name="linear_programming",
        regex_patterns=(r"\\[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "Minimize\n cost: 4 x + 2 y \\ objective note\nEnd",
                "\\ objective note",
                "Common Gurobi and GLPK LP line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("\\", ""),),
        documentation_source=(
            "https://docs.gurobi.com/projects/optimizer/en/13.0/reference/"
            "fileformats/modelformats.html#lp-format"
        ),
        implementation_source="https://ftp.gnu.org/gnu/glpk/glpk-5.0.tar.gz",
        confidence="cross-checked",
        notes=(
            "Implements the unconditional backslash-to-physical-line-end rule "
            "shared by Gurobi LP and GLPK's CPLEX LP reader."
        ),
    ),
    CommentSyntax(
        family_name="livecode_script_style",
        canonical_name="livecode_script",
        regex_patterns=(
            r"/\*[\s\S]*?\*/",
            r"//[^\r\n]*",
            r"--[^\r\n]*",
            r"#[^\r\n]*",
        ),
        shared_regex_examples=(
            CommentExample(
                "put 1 into value # hash note\nreturn value",
                "# hash note",
                "LiveCode hash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "put 1 into value -- dash note\nreturn value",
                "-- dash note",
                "LiveCode dash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "put 1 into value // slash note\nreturn value",
                "// slash note",
                "LiveCode slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "put 1 into value /* block note */\nreturn value",
                "/* block note */",
                "LiveCode non-nested block comment.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("#", ""), ("--", ""), ("//", "")),
        sanitizer_block_wrappers=(("/*", "*/"),),
        documentation_source=(
            "https://docs.livecode.com/docs/LiveCode%20Script/Keywords/singleline%20comment/"
        ),
        implementation_source=(
            "https://github.com/livecode/livecode/blob/"
            "4606a10ea10b16d5071d0f9f263ccdd7ede8b31d/engine/src/"
            "scriptpt.cpp#L856-L926"
        ),
        confidence="verified",
        notes=(
            "The engine recognizes #, --, //, and first-close /* ... */ forms "
            "between tokens. Quoted string contents are protected."
        ),
    ),
    CommentSyntax(
        family_name="mdsvex_style",
        canonical_name="mdsvex",
        contextual_extractor="mdsvex_comments",
        shared_contextual_examples=(
            CommentExample(
                "# Heading\n\n<!-- block note -->\n\nText",
                "<!-- block note -->",
                "MDsveX host HTML comment outside embedded and code regions.",
                kind="block",
                inline_compatible=True,
            ),
        ),
        sanitizer_block_wrappers=(("<!--", "-->"),),
        documentation_source=(
            "https://github.com/pngwn/MDsveX/blob/"
            "6cd89be39d2e506d408d832175884b74689e2126/packages/mdsvex/"
            "test/_fixtures/markdown/input/html-comments.md#L1-L8"
        ),
        implementation_source=(
            "https://github.com/pngwn/MDsveX/blob/"
            "6cd89be39d2e506d408d832175884b74689e2126/packages/mdsvex/"
            "src/parsers/html_block.ts#L11-L114"
        ),
        confidence="cross-checked",
        notes=(
            "Only ordinary host HTML nodes are returned. Front matter, code, raw "
            "script/style/pre regions, Svelte expressions, and svelte-ignore "
            "directives are preserved."
        ),
    ),
    CommentSyntax(
        family_name="mdx_style",
        canonical_name="mdx",
        contextual_extractor="mdx_comments",
        shared_contextual_examples=(
            CommentExample(
                "Before {/* block note */} after",
                "/* block note */",
                "MDX JavaScript block comment in a content expression.",
                kind="block",
                inline_compatible=True,
                standalone_compatible=False,
            ),
        ),
        sanitizer_line_wrappers=(("//", ""),),
        sanitizer_block_wrappers=(("/*", "*/"),),
        documentation_source=(
            "https://github.com/mdx-js/mdx/blob/"
            "685627a819567c0788eadb85f5f57065bcc81c2c/docs/docs/"
            "what-is-mdx.mdx#L161-L171"
        ),
        implementation_source=(
            "https://github.com/micromark/micromark-extension-mdx-expression/blob/"
            "2891b75ff9e985c6df208a47348e76ced05dbfed/test/index.js#L635-L684"
        ),
        confidence="verified",
        notes=(
            "Returns JavaScript comment token ranges only from MDX expressions, "
            "valid JSX expression slots, and top-level ESM regions."
        ),
        language_versions=(
            CommentLanguageVersions(
                languages=("mdx",),
                default="mdx2",
                versions=(
                    CommentLanguageVersion(
                        name="mdx1",
                        aliases=("1",),
                        release="0",
                        span="MDX 1.x",
                        comment_rules=(
                            "HTML <!-- --> comments outside code; JavaScript comments only in ESM "
                            "and JSX tag expressions."
                        ),
                        contextual_extractor="mdx1_comments",
                        sanitizer_block_wrappers=(("<!--", "-->"),),
                        examples=(
                            CommentExample(
                                "# Title\n\n<!-- draft note -->\n",
                                "<!-- draft note -->",
                                "MDX 1 compiles HTML comments to JSX comments.",
                                kind="block",
                            ),
                        ),
                        documentation_source=(
                            "https://github.com/mdx-js/mdx/blob/v1.6.22/packages/mdx/test/"
                            "index.test.js#L141"
                        ),
                    ),
                    CommentLanguageVersion(
                        name="mdx2",
                        aliases=(
                            "mdx3",
                            "current",
                        ),
                        release="2",
                        span="MDX 2 and 3",
                        comment_rules=(
                            "JavaScript // and /* */ comments inside {...} expressions and ESM; "
                            "<!-- is an error."
                        ),
                        documentation_source=(
                            "https://github.com/mdx-js/mdx/blob/"
                            "685627a819567c0788eadb85f5f57065bcc81c2c/docs/docs/"
                            "what-is-mdx.mdx#L166-L169"
                        ),
                    ),
                ),
            ),
        ),
    ),
    CommentSyntax(
        family_name="mermaid_style",
        canonical_name="mermaid",
        contextual_extractor="mermaid_comments",
        shared_contextual_examples=(
            CommentExample(
                "sequenceDiagram\n  %% retry note\n  Client->>Server: request",
                "%% retry note",
                "Portable Mermaid own-line comment after indentation.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("%%", ""),),
        documentation_source=(
            "https://github.com/mermaid-js/mermaid/blob/"
            "19563d81ebbfd6cb7b97e285bafd986ed40df130/packages/mermaid/"
            "src/docs/syntax/classDiagram.md#L502-L511"
        ),
        implementation_source=(
            "https://github.com/mermaid-js/mermaid/blob/"
            "19563d81ebbfd6cb7b97e285bafd986ed40df130/packages/mermaid/"
            "src/diagram-api/comments.ts#L1-L8"
        ),
        confidence="verified",
        notes=(
            "Implements the portable global own-line %% form only. Directives, "
            "front matter, bare markers, and diagram-specific inline forms are excluded."
        ),
        language_versions=(
            CommentLanguageVersions(
                languages=("mermaid",),
                default="10.1",
                notes=(
                    "Before 10.1 each diagram grammar defined its own %% rules; the flowchart "
                    "rules are modelled."
                ),
                versions=(
                    CommentLanguageVersion(
                        name="10.0",
                        release="0",
                        span="Mermaid before 10.1.0",
                        comment_rules=(
                            "%% not followed by { starts a comment to the end of the line outside "
                            "quoted labels, also after code."
                        ),
                        contextual_extractor="mermaid_10_0_comments",
                        examples=(
                            CommentExample(
                                "flowchart LR\n  A --> B %% trailing\n",
                                "%% trailing",
                                "Before 10.1, the flowchart lexer skips a trailing %% comment.",
                                kind="line",
                            ),
                        ),
                        documentation_source=(
                            "https://github.com/mermaid-js/mermaid/blob/v10.0.2/packages/mermaid/"
                            "src/diagrams/flowchart/parser/flow.jison#L30-L31"
                        ),
                    ),
                    CommentLanguageVersion(
                        name="10.1",
                        aliases=(
                            "11",
                            "current",
                        ),
                        release="10.1",
                        span="Mermaid 10.1.0 and later",
                        comment_rules=(
                            "Own-line %% comments are removed before parsing; a trailing %% after "
                            "flowchart code is not a comment."
                        ),
                        documentation_source=(
                            "https://github.com/mermaid-js/mermaid/blob/v10.1.0/packages/mermaid/"
                            "src/diagram-api/comments.ts "
                            "(cleanupComments)"
                        ),
                    ),
                ),
            ),
        ),
    ),
    CommentSyntax(
        family_name="minizinc_style",
        canonical_name="minizinc",
        aliases=("minizinc_data",),
        regex_patterns=(
            r"%[^\n]*",
            r"/\*[\s\S]*?(?:\*/|\Z)",
        ),
        shared_regex_examples=(
            CommentExample(
                "int: workers; % worker note\nsolve satisfy;",
                "% worker note",
                "MiniZinc percent comment ending only at LF.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/** block note */\nint: workers;",
                "/** block note */",
                "MiniZinc documentation block comment.",
                kind="block",
            ),
            CommentExample(
                "/*** file documentation */\nint: workers;",
                "/*** file documentation */",
                "MiniZinc file-documentation block comment.",
                kind="block",
            ),
            CommentExample(
                "constraint true; /* accepted through EOF",
                "/* accepted through EOF",
                "MiniZinc block comment accepted through EOF by the pinned lexer.",
                kind="block",
                inline_compatible=True,
                consumes_eof=True,
            ),
        ),
        sanitizer_line_wrappers=(("%", ""),),
        sanitizer_block_wrappers=(
            ("/***", "*/"),
            ("/**", "*/"),
            ("/*", "*/"),
        ),
        unclosed_block_openers=("/***", "/**", "/*"),
        documentation_source=(
            "https://github.com/MiniZinc/libminizinc/blob/"
            "c9f9b649b2a251a40aa427a84d7cce73a8807fea/docs/en/spec.rst#L300-L320"
        ),
        implementation_source=(
            "https://github.com/MiniZinc/libminizinc/blob/"
            "c9f9b649b2a251a40aa427a84d7cce73a8807fea/lib/lexer.lxx#L155-L202"
        ),
        confidence="verified",
        notes=(
            "Percent comments end only at LF, retaining a preceding CR. Ordinary, "
            "documentation, and file-documentation blocks close first or consume EOF."
        ),
    ),
    CommentSyntax(
        family_name="mojo_style",
        canonical_name="mojo",
        contextual_extractor="mojo_comments",
        shared_contextual_examples=(
            CommentExample(
                "var value = 1 # inline note\nreturn value",
                "# inline note",
                "Mojo hash comment outside quoted and triple-quoted strings.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("#", ""),),
        documentation_source=(
            "https://github.com/modular/modular/blob/"
            "83bacbc5121ef488bbc44f412703a70c97739a99/mojo/docs/manual/"
            "basics.mdx#L140-L175"
        ),
        implementation_source="official Mojo compiler 0.26.2.0 (d627decc)",
        confidence="cross-checked",
        notes=(
            "Only source hash comments are returned; ordinary, raw, interpolated, "
            "and triple-quoted literals are protected."
        ),
    ),
    CommentSyntax(
        family_name="moonbit_style",
        canonical_name="moonbit",
        contextual_extractor="moonbit_comments",
        shared_contextual_examples=(
            CommentExample(
                "fn value() -> Int { 1 } /// documentation note\n",
                "/// documentation note",
                "MoonBit documentation comment outside literal-line forms.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("///|", ""), ("///", ""), ("//", "")),
        documentation_source=(
            "https://github.com/moonbitlang/moonbit-docs/blob/"
            "24f6b9a0b9ac997119ecd3069825edf65d3473fe/next/language/docs.md#L1-L96"
        ),
        implementation_source=(
            "https://github.com/moonbitlang/moonbit-compiler/blob/"
            "d4ada10d212b5376f7f8bf49cd2fbaa275a395df/src/lex_unicode_lex.ml#L1955-L1977"
        ),
        confidence="verified",
        notes=(
            "Line, documentation, and literate documentation forms are returned. "
            "File directives, recognized doc pragmas, strings, and #|/$| literal "
            "lines are protected."
        ),
    ),
    CommentSyntax(
        family_name="nmodl_style",
        canonical_name="nmodl",
        contextual_extractor="nmodl_comments",
        shared_contextual_examples=(
            CommentExample(
                "SUFFIX demo : suffix note\n",
                ": suffix note",
                "NMODL colon line comment outside an ontology identifier.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "COMMENT\nblock note\nENDCOMMENT\n",
                "COMMENT\nblock note\nENDCOMMENT",
                "NMODL exact COMMENT copy-mode block.",
                kind="block",
            ),
        ),
        sanitizer_line_wrappers=((":", ""), ("?", "")),
        sanitizer_block_wrappers=(("COMMENT", "ENDCOMMENT"),),
        documentation_source=(
            "https://github.com/BlueBrain/nmodl/blob/"
            "06132d23125bf6d65b0cc7b7136754ed378969d9/docs/language.rst#L89-L149"
        ),
        implementation_source=(
            "https://github.com/BlueBrain/nmodl/blob/"
            "06132d23125bf6d65b0cc7b7136754ed378969d9/src/lexer/nmodl.ll#L137-L151"
        ),
        confidence="verified",
        notes=(
            "Colon and question-mark comments terminate at CR, LF, or EOF. "
            "COMMENT blocks are non-nested and must close; VERBATIM copy mode, "
            "quoted strings, and ontology identifiers are protected."
        ),
    ),
    CommentSyntax(
        family_name="nushell_style",
        canonical_name="nushell",
        contextual_extractor="nushell_comments",
        shared_contextual_examples=(
            CommentExample(
                "let value = 1 # inline note\n$value",
                "# inline note",
                "Nushell hash comment at an item boundary.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("#", ""),),
        documentation_source=(
            "https://github.com/nushell/nushell.github.io/blob/"
            "bef55b50ba8cdf93a576dd142971294253cb4d98/book/custom_commands.md#L856-L936"
        ),
        implementation_source=(
            "https://github.com/nushell/nushell/blob/"
            "4c6dcc59d6ea3f42ce434cfd0da3d422deb776c9/crates/nu-parser/src/lex.rs#L87-L260"
        ),
        confidence="verified",
        notes=(
            "Boundary-qualified hash comments use the lexer's distinct top-level "
            "and compound CR rules. A byte-zero shebang and hashes inside literals "
            "or bare items are excluded. This is not the separate Nu language."
        ),
        language_versions=(
            CommentLanguageVersions(
                languages=("nushell",),
                default="0.94",
                versions=(
                    CommentLanguageVersion(
                        name="0.76",
                        release="0",
                        span="Nushell 0.76 and earlier",
                        comment_rules=(
                            "# outside quotes starts a comment to the end of the line, even inside "
                            "a bare word."
                        ),
                        contextual_extractor="nushell_076_comments",
                        examples=(
                            CommentExample(
                                "http get https://example.com/docs#intro\n",
                                "#intro",
                                "Before 0.77, # ends a bare word and starts a comment.",
                                kind="line",
                            ),
                        ),
                        documentation_source=(
                            "https://github.com/nushell/nushell/blob/0.76.0/crates/nu-parser/src/"
                            "lex.rs#L62 "
                            "(is_item_terminator includes #)"
                        ),
                    ),
                    CommentLanguageVersion(
                        name="0.77",
                        release="0.77",
                        span="Nushell 0.77 through 0.93",
                        comment_rules=(
                            "# starts a comment only at the start of an item; there are no raw "
                            "strings."
                        ),
                        contextual_extractor="nushell_077_comments",
                        examples=(
                            CommentExample(
                                "echo r#'a #b'#\n",
                                "#b'#",
                                "Before 0.94, r#'...'# is not a raw string.",
                                kind="line",
                            ),
                        ),
                        documentation_source=(
                            "https://github.com/nushell/nushell/blob/0.77.0/crates/nu-parser/src/"
                            "lex.rs#L49-L63 "
                            "(# is no longer an item terminator)"
                        ),
                    ),
                    CommentLanguageVersion(
                        name="0.94",
                        aliases=("current",),
                        release="0.94",
                        span="Nushell 0.94 and later",
                        comment_rules=(
                            "# starts a comment at the start of an item; raw strings r#'...'# "
                            "protect #."
                        ),
                        documentation_source=(
                            "https://github.com/nushell/nushell/blob/0.94.0/crates/nu-parser/src/"
                            "lex.rs#L228 "
                            "(lex_raw_string)"
                        ),
                    ),
                ),
            ),
        ),
    ),
    CommentSyntax(
        family_name="omnet_plus_plus_msg_style",
        canonical_name="omnet_plus_plus_msg",
        contextual_extractor="omnet_msg_comments",
        shared_contextual_examples=(
            CommentExample(
                "int sequence; // field note\n",
                "// field note",
                "OMNeT++ MSG host comment outside lexer-exclusive states.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("//", ""),),
        documentation_source=(
            "https://github.com/omnetpp/omnetpp/blob/"
            "820d04e7bb0ef53acaf6a41858ee7ea29f2754ca/doc/src/manual/"
            "ch-message-definitions.tex#L636-L648"
        ),
        implementation_source=(
            "https://github.com/omnetpp/omnetpp/blob/"
            "820d04e7bb0ef53acaf6a41858ee7ea29f2754ca/src/nedxml/msg2.lex#L58-L144"
        ),
        confidence="verified",
        notes=(
            "Only host-state // comments are returned. Strings, balanced property "
            "values, embedded cplusplus bodies, and malformed protected states "
            "consume or protect their remaining source."
        ),
    ),
    CommentSyntax(
        family_name="omnet_plus_plus_ned_style",
        canonical_name="omnet_plus_plus_ned",
        contextual_extractor="omnet_ned_comments",
        shared_contextual_examples=(
            CommentExample(
                "network Demo {} // network note\n",
                "// network note",
                "OMNeT++ NED host comment outside lexer-exclusive states.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("//", ""),),
        documentation_source=(
            "https://github.com/omnetpp/omnetpp/blob/"
            "820d04e7bb0ef53acaf6a41858ee7ea29f2754ca/doc/src/manual/"
            "appendix-ned-ref.tex#L113-L119"
        ),
        implementation_source=(
            "https://github.com/omnetpp/omnetpp/blob/"
            "820d04e7bb0ef53acaf6a41858ee7ea29f2754ca/src/nedxml/ned2.lex#L58-L182"
        ),
        confidence="verified",
        notes=(
            "Only host-state // comments are returned. Single/double strings and "
            "balanced or malformed property-value states are protected."
        ),
    ),
    CommentSyntax(
        family_name="pip_requirements_style",
        canonical_name="pip_requirements",
        contextual_extractor="pip_requirements_comments",
        shared_contextual_examples=(
            CommentExample(
                "package==1 # pinned version note\n",
                "# pinned version note",
                "pip requirement comment after a whitespace boundary.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("#", ""),),
        documentation_source=(
            "https://github.com/pypa/pip/blob/"
            "6236392d41f0623476b9dbca2f1c55b832ee7e43/docs/html/reference/"
            "requirements-file-format.md#L57-L75"
        ),
        implementation_source=(
            "https://github.com/pypa/pip/blob/"
            "6236392d41f0623476b9dbca2f1c55b832ee7e43/src/pip/_internal/"
            "req/req_file.py#L496-L533"
        ),
        confidence="verified",
        notes=(
            "A hash begins a comment only at physical/logical line start or after "
            "whitespace. URL fragments remain data, and physical ranges are retained "
            "after continuation joining."
        ),
    ),
    CommentSyntax(
        family_name="praat_style",
        canonical_name="praat",
        contextual_extractor="praat_comments",
        shared_contextual_examples=(
            CommentExample(
                "value = 1 ; verified note\n",
                "; verified note",
                "Praat quote-aware inline semicolon comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("#", ""), (";", ""), ("!", "")),
        documentation_source=(
            "https://github.com/praat/praat/blob/"
            "5d452fe3490bdc8d0edd12196a74127795b6a20a/fon/"
            "manual_scripting.cpp#L942-L975"
        ),
        implementation_source=(
            "https://github.com/praat/praat/blob/"
            "5d452fe3490bdc8d0edd12196a74127795b6a20a/sys/Interpreter.cpp#L369-L381"
        ),
        confidence="cross-checked",
        notes=(
            "Leading #, ;, and ! lines are comments. Only semicolon begins an "
            "inline comment; straight doubled-quote and curly strings protect it, "
            "and malformed string state protects the remainder."
        ),
    ),
    CommentSyntax(
        family_name="pyret_style",
        canonical_name="pyret",
        contextual_extractor="pyret_comments",
        shared_contextual_examples=(
            CommentExample(
                "value = 1 # line note\nvalue",
                "# line note",
                "Pyret hash line comment outside strings.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "#| outer #| inner |# block note |#\nvalue",
                "#| outer #| inner |# block note |#",
                "Recursively nested Pyret hash-pipe block.",
                kind="nested",
            ),
        ),
        sanitizer_line_wrappers=(("#", ""),),
        sanitizer_block_wrappers=(("#|", "|#"),),
        documentation_source="https://pyret.org/docs/latest/s_comments.html",
        implementation_source=(
            "https://github.com/brownplt/pyret-lang/blob/"
            "817b85eba62ef35d345c10fb02c9f7add94f1e54/src/js/base/"
            "pyret-tokenizer.js#L524-L563"
        ),
        confidence="verified",
        notes=(
            "Hash-pipe wins over the hash line prefix and nests recursively. "
            "Quoted bytes inside comments do not shield nested delimiters; "
            "unclosed blocks are excluded."
        ),
    ),
    CommentSyntax(
        family_name="rez_style",
        canonical_name="rez",
        contextual_extractor="rez_comments",
        shared_contextual_examples=(
            CommentExample(
                "resource 'STR ' (128) { \"Ready\" }; // status note\n",
                "// status note",
                "Contemporary Apple Rez line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/* resource block note */\n#define kStatus 128",
                "/* resource block note */",
                "Non-nested Rez block comment.",
                kind="block",
            ),
        ),
        sanitizer_line_wrappers=(("//", ""),),
        sanitizer_block_wrappers=(("/*", "*/"),),
        documentation_source=(
            "https://ftpmirror.your.org/pub/misc/bitsavers/pdf/apple/mac/developer/"
            "MPW_2.0_Reference_1987.pdf"
        ),
        implementation_source=(
            "https://github.com/autc04/Retro68/blob/"
            "f99ecb5aeb6fbb004c647518ea760daba2b1f6bb/Rez/RezLexer.cc#L71-L89"
        ),
        confidence="cross-checked",
        notes=(
            "Implements the contemporary Apple Rez C-preprocessor contract, "
            "including escaped physical line removal, quoted resource literals, "
            "first-close blocks, and complete-only malformed handling."
        ),
    ),
    CommentSyntax(
        family_name="roc_style",
        canonical_name="roc",
        contextual_extractor="roc_comments",
        shared_contextual_examples=(
            CommentExample(
                "answer = 42 # chosen note\n",
                "# chosen note",
                "Roc hash line comment outside literals.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("#", ""),),
        documentation_source=(
            "https://github.com/roc-lang/roc/blob/"
            "a892c9f42c528ba13c1ac9e61cc4c3226f1be918/docs/langref/"
            "comments-and-docs.md#L1-L41"
        ),
        implementation_source=(
            "https://github.com/roc-lang/roc/blob/"
            "a892c9f42c528ba13c1ac9e61cc4c3226f1be918/src/parse/tokenize.zig#L757-L785"
        ),
        confidence="verified",
        notes=(
            "Roc has only hash line comments. Strings, multiline strings, and "
            "code-point literals protect marker bytes; shebangs remain comments."
        ),
    ),
    CommentSyntax(
        family_name="rbs_style",
        canonical_name="rbs",
        contextual_extractor="rbs_comments",
        shared_contextual_examples=(
            CommentExample(
                "type path = %a{route#fragment} # trailing note\n",
                "# trailing note",
                "Standalone RBS hash comment after an annotation.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("#", ""),),
        documentation_source=(
            "https://github.com/ruby/rbs/blob/"
            "7534c7e8a5f6c83bc28cc057cc4f84d881125c33/docs/syntax.md#L912-L924"
        ),
        implementation_source=(
            "https://github.com/ruby/rbs/blob/"
            "7534c7e8a5f6c83bc28cc057cc4f84d881125c33/src/lexer.re#L19-L66"
        ),
        confidence="verified",
        notes=(
            "LF alone terminates an RBS comment, so CR is retained as payload. "
            "All five %a annotation delimiters and quoted tokens protect hashes; "
            "malformed annotation payloads are conservatively shielded."
        ),
    ),
    CommentSyntax(
        family_name="ron_style",
        canonical_name="ron",
        contextual_extractor="ron_comments",
        shared_contextual_examples=(
            CommentExample(
                '(name: "Ada", // display note\n active: true)',
                "// display note",
                "LF-terminated RON line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/* outer /* nested */ block note */\n(value: 1)",
                "/* outer /* nested */ block note */",
                "Recursively nested RON block comment.",
                kind="nested",
            ),
        ),
        sanitizer_line_wrappers=(("//", ""),),
        sanitizer_block_wrappers=(("/*", "*/"),),
        documentation_source=(
            "https://github.com/ron-rs/ron/blob/"
            "31529b8b8d8c44ebf6ef91975da6cb14ae76a505/docs/grammar.md#L16-L23"
        ),
        implementation_source=(
            "https://github.com/ron-rs/ron/blob/"
            "31529b8b8d8c44ebf6ef91975da6cb14ae76a505/src/parse.rs#L1396-L1438"
        ),
        confidence="verified",
        notes=(
            "RON line comments require LF and blocks require complete recursive "
            "closure. Rust-style normal, byte, character, and raw values shield "
            "comment markers."
        ),
    ),
    CommentSyntax(
        family_name="sail_style",
        canonical_name="sail",
        contextual_extractor="sail_comments",
        shared_contextual_examples=(
            CommentExample(
                "function f(x) = x // function note\n",
                "// function note",
                "LF-terminated Sail line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/*! outer /* nested */ block note */\nfunction f(x) = x",
                "/*! outer /* nested */ block note */",
                "Nested Sail documentation block.",
                kind="nested",
            ),
        ),
        sanitizer_line_wrappers=(("///", ""), ("//", "")),
        sanitizer_block_wrappers=(("/*!", "*/"), ("/*", "*/")),
        documentation_source=(
            "https://github.com/rems-project/sail/blob/"
            "19f73e47ef094732749828d578cfa3a9e3e43fa9/doc/asciidoc/modules.adoc#L80-L92"
        ),
        implementation_source=(
            "https://github.com/rems-project/sail/blob/"
            "19f73e47ef094732749828d578cfa3a9e3e43fa9/src/lib/lexer.mll#L315-L360"
        ),
        confidence="verified",
        notes=(
            "Ordinary and documentation lines require LF; blocks nest. Strings "
            "and $[...] attributes protect markers, while simple pragmas allow "
            "only their lexer's terminal line or block comment placements."
        ),
    ),
    CommentSyntax(
        family_name="scenic_style",
        canonical_name="scenic",
        contextual_extractor="scenic_comments",
        shared_contextual_examples=(
            CommentExample(
                "ego = new Object at 0@0 # position note\n",
                "# position note",
                "Python-tokenized Scenic comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("#", ""),),
        documentation_source=(
            "https://github.com/BerkeleyLearnVerify/Scenic/blob/"
            "2fc163437ef1d3a47f109419c89b33295e26186d/docs/syntax_guide.rst#L1-L10"
        ),
        implementation_source=(
            "https://github.com/BerkeleyLearnVerify/Scenic/blob/"
            "2fc163437ef1d3a47f109419c89b33295e26186d/src/scenic/syntax/"
            "scenic.gram#L59-L89"
        ),
        confidence="verified",
        notes=(
            "Scenic delegates lexical comments to Python tokenization. All valid "
            "Python string forms remain literals, including triple and formatted "
            "strings; malformed quote states are conservative."
        ),
    ),
    CommentSyntax(
        family_name="simple_file_verification_style",
        canonical_name="simple_file_verification",
        aliases=("sfv",),
        regex_patterns=(r"(?m)^;[^\r\n]*",),
        shared_regex_examples=(
            CommentExample(
                "; Generated manifest note\narchive.bin DEADBEEF",
                "; Generated manifest note",
                "Column-zero SFV metadata record.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=((";", ""),),
        documentation_source="https://zakalwe.fi/~shd/foss/cksfv/",
        implementation_source=(
            "https://gitlab.com/heikkiorsila/cksfv/-/blob/"
            "25fc8bd369887fc6f1feccdf035db64f50d5f1a4/src/readsfv.c#L90-L100"
        ),
        confidence="cross-checked",
        notes=(
            "Only a semicolon at byte zero of an SFV record is a comment. "
            "Indented and inline semicolons remain checksum-record data."
        ),
    ),
    CommentSyntax(
        family_name="slang_style",
        canonical_name="slang",
        contextual_extractor="slang_comments",
        shared_contextual_examples=(
            CommentExample(
                "float gain = 1.0; // calibration note\n",
                "// calibration note",
                "Slang logical-line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/* shader block note */\nfloat enabled = 1;",
                "/* shader block note */",
                "Non-nested Slang block comment.",
                kind="block",
            ),
            CommentExample(
                "// spliced note\\\ncontinued\nfloat value = 1;",
                "// spliced note\\\ncontinued",
                "Slang comment spanning an escaped physical LF.",
                kind="line",
            ),
        ),
        sanitizer_line_wrappers=(("//", ""),),
        sanitizer_block_wrappers=(("/*", "*/"),),
        documentation_source=(
            "https://github.com/shader-slang/slang/blob/"
            "7c58a326b1f3812411a204b19cb01e323d8f6010/docs/language-reference/"
            "lexical-structure.md#comments"
        ),
        implementation_source=(
            "https://github.com/shader-slang/slang/blob/"
            "7c58a326b1f3812411a204b19cb01e323d8f6010/source/compiler-core/"
            "slang-lexer.cpp#L405-L455"
        ),
        confidence="verified",
        notes=(
            "Escaped physical line breaks are removed before comment recognition. "
            "C++ raw and ordinary literals protect markers; blocks close at the "
            "first terminator and malformed blocks are excluded."
        ),
    ),
    CommentSyntax(
        family_name="slint_style",
        canonical_name="slint",
        contextual_extractor="slint_comments",
        shared_contextual_examples=(
            CommentExample(
                "width: 100px; // design note\n",
                "// design note",
                "Slint line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/* outer /* inner */ block note */\ncomponent Demo {}",
                "/* outer /* inner */ block note */",
                "Recursively nested Slint block.",
                kind="nested",
            ),
        ),
        sanitizer_line_wrappers=(("//", ""),),
        sanitizer_block_wrappers=(("/*", "*/"),),
        documentation_source=(
            "https://docs.slint.dev/latest/docs/slint/guide/language/coding/file/#comments"
        ),
        implementation_source=(
            "https://github.com/slint-ui/slint/blob/"
            "cf62c975c311e7036d599ed8ed0b7e6a8386a934/internal/compiler/lexer.rs#L51-L123"
        ),
        confidence="verified",
        notes=(
            "Slint blocks nest and lines end at CR, LF, or EOF. String text "
            "protects markers while \\{...} interpolation re-enters comment-aware "
            "code mode."
        ),
    ),
    CommentSyntax(
        family_name="smithy_style",
        canonical_name="smithy",
        contextual_extractor="smithy_comments",
        shared_contextual_examples=(
            CommentExample(
                "string Name // public note\n",
                "// public note",
                "Smithy ordinary line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/// documentation note\nstring Name",
                "/// documentation note",
                "Smithy documentation slash-run subset.",
                kind="line",
                grouped_line_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("//", ""),),
        documentation_source="https://smithy.io/2.0/spec/idl.html#comments",
        implementation_source=(
            "https://github.com/smithy-lang/smithy/blob/"
            "bc9f0babd071d4ab818d5c4ea582f0e6f71f251e/smithy-model/src/main/java/"
            "software/amazon/smithy/model/loader/DefaultTokenizer.java#L299-L329"
        ),
        confidence="cross-checked",
        notes=(
            "Smithy slash comments terminate at CR, LF, or EOF in the pinned "
            "tokenizer. Quoted strings and triple-quoted text blocks protect "
            "markers; block syntax is unsupported."
        ),
    ),
    CommentSyntax(
        family_name="snakemake_style",
        canonical_name="snakemake",
        contextual_extractor="snakemake_comments",
        shared_contextual_examples=(
            CommentExample(
                'output: "result.txt" # artifact note\n',
                "# artifact note",
                "Python-tokenized Snakemake comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("#", ""),),
        documentation_source="https://snakemake.readthedocs.io/en/v9.24.0/snakefiles/rules.html",
        implementation_source=(
            "https://github.com/snakemake/snakemake/blob/"
            "e7f10a512bfe8c25ecfaa1062f60f282f427edd0/src/snakemake/parser.py#L1351-L1361"
        ),
        confidence="verified",
        notes=(
            "Snakemake consumes Python COMMENT tokens. Python and shell-directive "
            "string contents, including multiline/raw/bytes/formatted forms, are "
            "not host comments."
        ),
    ),
    CommentSyntax(
        family_name="survex_data_style",
        canonical_name="survex_data",
        contextual_extractor="survex_data_comments",
        shared_contextual_examples=(
            CommentExample(
                "A B 10 90 0 ; survey note\n",
                "; survey note",
                "Default Survex semicolon comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "*set comment %\nA B 10 90 0 % note\n",
                "% note",
                "Survex comment after a translation-map replacement.",
                kind="line",
                inline_compatible=True,
                standalone_compatible=False,
            ),
        ),
        sanitizer_line_wrappers=(("%", ""), ("!", ""), (";", "")),
        documentation_source="https://survex.com/docs/manual/datafile.htm",
        implementation_source=(
            "https://deb.debian.org/debian/pool/main/s/survex/survex_1.4.22.orig.tar.gz"
        ),
        confidence="verified",
        notes=(
            "Tracks scoped *begin/*end translation maps for comment, EOL, and "
            "quote character classes. Dynamic xHH markers and logical comments "
            "spanning physical newlines retain exact source slices."
        ),
    ),
    CommentSyntax(
        family_name="templ_style",
        canonical_name="templ",
        contextual_extractor="templ_comments",
        shared_contextual_examples=(
            CommentExample(
                "// top-level Go note\ntempl render() { <p>Ready</p> }",
                "// top-level Go note",
                "Top-level templ Go comment.",
                kind="line",
                grouped_line_compatible=True,
            ),
            CommentExample(
                "templ render() { <!-- rendered block note --> }",
                "<!-- rendered block note -->",
                "templ HTML comment node.",
                kind="block",
                inline_compatible=True,
                standalone_compatible=False,
            ),
            CommentExample(
                "templ render() {\n  /* Go block note */\n}",
                "/* Go block note */",
                "Go block comment in a template-node position.",
                kind="block",
                standalone_compatible=False,
            ),
        ),
        sanitizer_line_wrappers=(("//", ""),),
        sanitizer_block_wrappers=(("<!--", "-->"), ("/*", "*/")),
        documentation_source=(
            "https://github.com/a-h/templ/blob/"
            "09d6b02946f54492f3d3dcb9729f5b792f220b40/docs/docs/"
            "03-syntax-and-usage/14-comments.md"
        ),
        implementation_source=(
            "https://github.com/a-h/templ/blob/"
            "09d6b02946f54492f3d3dcb9729f5b792f220b40/parser/v2/"
            "templateparser.go#L61-L84"
        ),
        confidence="verified",
        notes=(
            "Returns parser-recognized Go line/block and HTML block nodes. Plain "
            "template text and raw script/style bodies remain protected target "
            "language content."
        ),
        language_versions=(
            CommentLanguageVersions(
                languages=("templ",),
                default="0.2.408",
                versions=(
                    CommentLanguageVersion(
                        name="0.2.364",
                        release="0",
                        span="templ v0.2.364 and earlier",
                        comment_rules=(
                            "Inside component bodies only <!-- --> comments exist; // and /* */ "
                            "there are template text."
                        ),
                        contextual_extractor="templ_0_2_364_comments",
                        examples=(
                            CommentExample(
                                "// note\ntempl hello() {\n\t// shown\n\t<p>Hi</p>\n}\n",
                                "// note",
                                "Before v0.2.408, only Go code outside components has // comments.",
                                kind="line",
                            ),
                        ),
                        documentation_source=(
                            "https://github.com/a-h/templ/blob/v0.2.364/parser/v2/"
                            "templateparser.go#L63 "
                            "(HTML comments only)"
                        ),
                    ),
                    CommentLanguageVersion(
                        name="0.2.408",
                        aliases=("current",),
                        release="0.2.408",
                        span="templ v0.2.408 and later",
                        comment_rules=(
                            "Go // and /* */ comments are also recognized inside component bodies."
                        ),
                        documentation_source=(
                            "https://github.com/a-h/templ/blob/v0.2.408/parser/v2/"
                            "templateparser.go#L96-L116 "
                            "(goComment)"
                        ),
                    ),
                ),
            ),
        ),
    ),
    CommentSyntax(
        family_name="terraform_template_style",
        canonical_name="terraform_template",
        contextual_extractor="terraform_template_comments",
        shared_contextual_examples=(
            CommentExample(
                "${\n  # expression note\n  var.name\n}",
                "# expression note",
                "HCL hash comment in template interpolation mode.",
                kind="line",
                standalone_compatible=False,
            ),
            CommentExample(
                "${var.name /* block note */}",
                "/* block note */",
                "HCL block comment in template interpolation mode.",
                kind="block",
                inline_compatible=True,
                standalone_compatible=False,
            ),
        ),
        sanitizer_line_wrappers=(("//", ""), ("#", "")),
        sanitizer_block_wrappers=(("/*", "*/"),),
        documentation_source=(
            "https://github.com/hashicorp/hcl/blob/"
            "6b5068090eef06b1f127f61529db5ba0be7ed343/hclsyntax/spec.md#comments-and-whitespace"
        ),
        implementation_source=(
            "https://github.com/hashicorp/hcl/blob/"
            "6b5068090eef06b1f127f61529db5ba0be7ed343/hclsyntax/scan_tokens.rl#L249-L291"
        ),
        confidence="verified",
        notes=(
            "Bare template text never recognizes HCL comments. Hash, slash-line, "
            "and first-close slash-star forms are returned only from complete "
            "${...} or %{...} code modes; escaped openers remain literal."
        ),
    ),
    CommentSyntax(
        family_name="textgrid_style",
        canonical_name="textgrid",
        contextual_extractor="textgrid_comments",
        shared_contextual_examples=(
            CommentExample(
                '0 2.3 ! time note\n"Mary ! literal"',
                "! time note",
                "Praat TextGrid explicit comment outside a quoted value.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("!", ""),),
        documentation_source=(
            "https://github.com/praat/praat/blob/"
            "5d452fe3490bdc8d0edd12196a74127795b6a20a/docs/"
            "manual/TextGrid_file_formats.html"
        ),
        implementation_source=("src/ml4setk/Parsing/Comments/stack_v3_batch_10_contextual.py"),
        confidence="verified",
        notes=(
            "Only explicit ! suffixes are comments. Doubled double quotes shield "
            "marker text; full-format field scaffolding remains data."
        ),
    ),
    CommentSyntax(
        family_name="toit_style",
        canonical_name="toit",
        contextual_extractor="toit_comments",
        shared_contextual_examples=(
            CommentExample(
                "value := 1 // line note\nvalue++",
                "// line note",
                "Toit slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "/* outer /* block note */ tail */",
                "/* outer /* block note */ tail */",
                "Toit escape-aware nested block comment.",
                kind="nested",
                inline_compatible=True,
            ),
            CommentExample(
                'text := "literal // $(1 /* expression note */) tail"',
                "/* expression note */",
                "Toit comment inside a parenthesized string interpolation.",
                kind="block",
                inline_compatible=True,
                standalone_compatible=False,
            ),
        ),
        sanitizer_line_wrappers=(("//", ""),),
        sanitizer_block_wrappers=(("/*", "*/"),),
        documentation_source="https://docs.toit.io/language",
        implementation_source=(
            "https://github.com/toitlang/toit/blob/"
            "0d46acd86c2637c448157f6b1d6c7845252c685e/src/compiler/"
            "scanner.cc#L843-L897"
        ),
        confidence="verified",
        notes=(
            "Nested blocks honor backslash escapes and require balance. Literal "
            "string spans are protected while $(...) expressions re-enter code."
        ),
    ),
    CommentSyntax(
        family_name="tor_config_style",
        canonical_name="tor_config",
        aliases=("torrc",),
        contextual_extractor="tor_config_comments",
        shared_contextual_examples=(
            CommentExample(
                "Nickname escaped\\#value # line note\n",
                "# line note",
                "Tor configuration hash comment outside an escaped value.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("#", ""),),
        documentation_source=(
            "https://gitlab.torproject.org/tpo/core/tor/-/blob/"
            "2fbdc52d625c02a9787c9215cd5d1818dd575e4d/doc/torrc_format.txt"
        ),
        implementation_source=("src/ml4setk/Parsing/Comments/stack_v3_batch_10_contextual.py"),
        confidence="verified",
        notes=(
            "Quoted and backslash-escaped hashes remain values. LF ends comments; "
            "a bare CR is retained as comment or value content."
        ),
    ),
    CommentSyntax(
        family_name="tree_sitter_query_style",
        canonical_name="tree_sitter_query",
        contextual_extractor="tree_sitter_query_comments",
        shared_contextual_examples=(
            CommentExample(
                '(identifier) @name ; query note\n"; literal"',
                "; query note",
                "Tree-sitter query semicolon comment outside a string.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=((";", ""),),
        documentation_source=(
            "https://tree-sitter.github.io/tree-sitter/using-parsers/queries/1-syntax.html"
        ),
        implementation_source=(
            "https://github.com/tree-sitter/tree-sitter/blob/"
            "963b5a5a971021359cf091a63d4f1286bc319643/lib/src/query.c#L404-L417"
        ),
        confidence="verified",
        notes=(
            "Double-quoted query strings shield semicolons. LF terminates a "
            "comment, so a bare CR remains part of its exact source range."
        ),
    ),
    CommentSyntax(
        family_name="typespec_style",
        canonical_name="typespec",
        contextual_extractor="typespec_comments",
        shared_contextual_examples=(
            CommentExample(
                "model Widget { id: string; // line note\n}",
                "// line note",
                "TypeSpec slash line comment.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                'const value = "literal ${name /* block note */} tail";',
                "/* block note */",
                "TypeSpec comment inside a template expression.",
                kind="block",
                inline_compatible=True,
                standalone_compatible=False,
            ),
        ),
        sanitizer_line_wrappers=(("//", ""),),
        sanitizer_block_wrappers=(("/*", "*/"),),
        documentation_source=("https://typespec.io/docs/language-basics/documentation/"),
        implementation_source=(
            "https://github.com/microsoft/typespec/blob/"
            "961e5aa200584a4e969e886d92d207c13986e3ef/packages/compiler/"
            "src/core/scanner.ts#L728-L742"
        ),
        confidence="verified",
        notes=(
            "Ordinary and triple strings are protected, except that ${...} "
            "template expressions re-enter code. Blocks are non-nested and must close."
        ),
    ),
    CommentSyntax(
        family_name="typst_style",
        canonical_name="typst",
        contextual_extractor="typst_comments",
        shared_contextual_examples=(
            CommentExample(
                "Text // line note\nNext",
                "// line note",
                "Typst line comment in markup mode.",
                kind="line",
                inline_compatible=True,
                grouped_line_compatible=True,
            ),
            CommentExample(
                "Text /* outer /* block note */ tail */ Next",
                "/* outer /* block note */ tail */",
                "Typst recursively nested block comment.",
                kind="nested",
                inline_compatible=True,
            ),
        ),
        sanitizer_line_wrappers=(("//", ""),),
        sanitizer_block_wrappers=(("/*", "*/"),),
        unclosed_block_openers=("/*",),
        documentation_source="https://www.typst.app/docs/reference/syntax/#comments",
        implementation_source=(
            "https://github.com/typst/typst/blob/"
            "32fd4cc3861e0ab99f4c42ca6bea281482ba9f51/crates/"
            "typst-syntax/src/lexer.rs#L91-L183"
        ),
        confidence="verified",
        notes=(
            "Raw text, strings, markup escapes, URLs, and the byte-zero shebang "
            "are protected. Nested blocks are accepted through EOF when unclosed."
        ),
    ),
)


_RELEASE_PATTERN = re.compile(r"[0-9]+(?:\.[0-9]+)*")


def _normalize_version_label(version: str) -> str:
    """Return a lookup key for a user- or registry-provided version label."""

    normalized = re.sub(r"\s+", "", str(version).strip().lower())
    if re.fullmatch(r"v[0-9][0-9.]*", normalized):
        normalized = normalized[1:]
    return normalized


def _release_key(release: str) -> Tuple[int, ...]:
    """Return a comparable tuple for a dotted numeric release such as ``3.0``."""

    parts = [int(part) for part in release.split(".")]
    while len(parts) > 1 and parts[-1] == 0:
        parts.pop()
    return tuple(parts)


def _validate_language_versions(syntax: CommentSyntax) -> None:
    """Reject malformed version tables for one registry family."""

    family = syntax.family_name
    seen_languages = set()
    for table in syntax.language_versions:
        if not table.languages:
            raise ValueError("Version tables must name at least one language: " + family)
        for language in table.languages:
            if language not in syntax.language_names:
                raise ValueError(f"Version table language {language!r} is not in family: " + family)
            if language in seen_languages:
                raise ValueError(f"Language {language!r} has more than one version table")
            seen_languages.add(language)
        if len(table.versions) < 2:
            raise ValueError("Version tables need at least two versions: " + family)
        labels = [_normalize_version_label(label) for v in table.versions for label in v.labels]
        if any(not label for label in labels):
            raise ValueError("Version names and aliases must not be empty: " + family)
        if len(labels) != len(set(labels)):
            raise ValueError("Version names and aliases must be unique: " + family)
        if any(version.name != version.name.lower() for version in table.versions):
            raise ValueError("Version names must be lowercase: " + family)
        if table.default not in table.version_names:
            raise ValueError(f"Default version {table.default!r} is not declared: " + family)
        default = table.version(table.default)
        if default.has_overlay:
            raise ValueError(
                "The default version is the registry entry and must not overlay it: " + family
            )
        releases = [version.release for version in table.versions]
        if any(releases):
            if not all(_RELEASE_PATTERN.fullmatch(release) for release in releases):
                raise ValueError("Every version release must be a dotted number: " + family)
            keys = [_release_key(release) for release in releases]
            if keys != sorted(keys) or len(keys) != len(set(keys)):
                raise ValueError("Version releases must increase strictly: " + family)
        for version in table.versions:
            if version.name == table.default:
                continue
            if not version.has_overlay:
                raise ValueError(
                    f"Version {version.name!r} must change extraction behavior: " + family
                )
            if not version.examples:
                raise ValueError(f"Version {version.name!r} needs seeded examples: " + family)
            if version.regex_patterns is not None:
                for pattern in version.regex_patterns:
                    # Compile with the query engine's regex module.
                    regex.compile(pattern)
            if (
                version.contextual_extractor
                and version.contextual_extractor not in SUPPORTED_CONTEXTUAL_EXTRACTORS
            ):
                raise ValueError(
                    f"Unknown contextual extractor {version.contextual_extractor!r}: " + family
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

        contextual_examples = (
            syntax.shared_contextual_examples or syntax.canonical_contextual_examples
        )
        if syntax.contextual_extractor and not contextual_examples:
            raise ValueError(
                "Registry entries with contextual extractors must provide "
                "seeded contextual examples: " + syntax.family_name
            )
        if contextual_examples and not syntax.contextual_extractor:
            raise ValueError(
                "Contextual examples require a contextual extractor: " + syntax.family_name
            )
        if (
            syntax.contextual_extractor
            and syntax.contextual_extractor not in SUPPORTED_CONTEXTUAL_EXTRACTORS
        ):
            raise ValueError(
                "Unknown contextual extractor "
                f"{syntax.contextual_extractor!r}: {syntax.family_name}"
            )
        if syntax.sanitizer_mode not in {"wrapped", "raw"}:
            raise ValueError(
                f"Unknown sanitizer mode {syntax.sanitizer_mode!r}: " + syntax.family_name
            )
        if any(
            not open_token
            for open_token, _ in (
                *syntax.sanitizer_line_wrappers,
                *syntax.sanitizer_block_wrappers,
            )
        ):
            raise ValueError(
                "Explicit sanitizer wrapper openers must not be empty: " + syntax.family_name
            )
        if any(not close_token for _, close_token in syntax.sanitizer_block_wrappers):
            raise ValueError(
                "Explicit sanitizer block closers must not be empty: " + syntax.family_name
            )
        if syntax.sanitizer_mode == "raw" and (
            syntax.sanitizer_line_wrappers or syntax.sanitizer_block_wrappers
        ):
            raise ValueError(
                "Raw sanitizers cannot declare explicit wrappers: " + syntax.family_name
            )
        if any(not opener for opener in syntax.unclosed_block_openers):
            raise ValueError("Unclosed block openers must not be empty: " + syntax.family_name)
        if syntax.sanitizer_mode == "raw" and syntax.unclosed_block_openers:
            raise ValueError(
                "Raw sanitizers cannot declare unclosed block openers: " + syntax.family_name
            )
        if syntax.unclosed_block_openers and not (
            syntax.regex_patterns or syntax.contextual_extractor
        ):
            raise ValueError(
                "Unclosed block openers require extractable syntax: " + syntax.family_name
            )
        if any(not prefix for prefix in syntax.excluded_comment_prefixes):
            raise ValueError("Excluded comment prefixes must not be empty: " + syntax.family_name)
        if syntax.excluded_comment_prefixes and not (
            syntax.regex_patterns or syntax.nested_delimiters
        ):
            raise ValueError(
                "Excluded comment prefixes require extractable syntax: " + syntax.family_name
            )
        dialect_exclusions = syntax.language_excluded_comment_prefixes
        excluded_dialects = [language for language, _ in dialect_exclusions]
        if len(excluded_dialects) != len(set(excluded_dialects)):
            raise ValueError(
                "Language-specific excluded comment prefixes must use unique "
                "languages: " + syntax.family_name
            )
        if any(language not in syntax.language_names for language in excluded_dialects):
            raise ValueError(
                "Language-specific excluded comment prefixes require a family "
                "language: " + syntax.family_name
            )
        if any(
            not prefixes or any(not prefix for prefix in prefixes)
            for _, prefixes in dialect_exclusions
        ):
            raise ValueError(
                "Language-specific excluded comment prefixes must not be empty: "
                + syntax.family_name
            )
        if dialect_exclusions and not (syntax.regex_patterns or syntax.nested_delimiters):
            raise ValueError(
                "Language-specific excluded comment prefixes require extractable "
                "syntax: " + syntax.family_name
            )

        regex_dialects = [language for language, _ in syntax.language_regex_patterns]
        if len(regex_dialects) != len(set(regex_dialects)):
            raise ValueError(
                "Language-specific regex patterns must use unique languages: " + syntax.family_name
            )
        if any(language not in syntax.language_names for language in regex_dialects):
            raise ValueError(
                "Language-specific regex patterns require a family language: " + syntax.family_name
            )
        if any(not patterns for _, patterns in syntax.language_regex_patterns):
            raise ValueError(
                "Language-specific regex patterns must not be empty: " + syntax.family_name
            )
        if syntax.language_regex_patterns and not syntax.regex_patterns:
            raise ValueError(
                "Language-specific regex patterns require family regex patterns: "
                + syntax.family_name
            )

        _validate_language_versions(syntax)

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


def _resolve_comment_language_key(language: str) -> str:
    """Return the exact registered key selected by normalized lookup."""

    for key in _language_lookup_candidates(language):
        if key in LANGUAGE_SYNTAX:
            return key
    raise NotImplementedError(f"Unsupported language: {language}")


class UnsupportedCommentLanguageVersionError(NotImplementedError, ValueError):
    """Raised when a version is unknown for a language or the language has none.

    Attributes:
        language: Language label passed by the caller.
        version: Version label passed by the caller.
        supported_versions: Canonical version names the language supports, in
            chronological order; empty when the language is not versioned.
    """

    def __init__(self, language: str, version: str, supported_versions: Tuple[str, ...]):
        self.language = language
        self.version = version
        self.supported_versions = supported_versions
        key = _resolve_comment_language_key(language)
        table = LANGUAGE_SYNTAX[key].versions_for_language(key)
        if table is None:
            message = (
                f"Language {language!r} has no version-dependent comment syntax; "
                f"omit version (got {version!r})."
            )
        else:
            message = (
                f"Unsupported version {version!r} for language {language!r}. "
                f"Supported versions: {_describe_versions(table)}."
            )
        super().__init__(message)


class CommentLanguageVersionWarning(UserWarning):
    """Warns that a version-dependent language was used without a version."""


_WARNED_DEFAULT_VERSIONS = set()


def _describe_versions(table: CommentLanguageVersions) -> str:
    """Return a readable list of a table's versions, aliases, and default."""

    described = []
    for index, version in enumerate(table.versions):
        details = []
        if version.name == table.default:
            details.append("default")
        if version.release and index == 0 and _release_key(version.release) == (0,):
            details.append(f"releases before {table.versions[1].release}")
        elif version.release:
            details.append(f"releases from {version.release}")
        if version.aliases:
            details.append("aliases: " + ", ".join(version.aliases))
        described.append(version.name + (f" ({'; '.join(details)})" if details else ""))
    return ", ".join(described)


def _version_table(language: str) -> Tuple[str, Optional[CommentLanguageVersions]]:
    """Return the resolved registry key and its version table, if any."""

    key = _resolve_comment_language_key(language)
    return key, LANGUAGE_SYNTAX[key].versions_for_language(key)


def resolve_comment_language_version(language: str, version: Optional[str]) -> Optional[str]:
    """Return the canonical version name selected by ``version``.

    Args:
        language: Registry key or alias.
        version: Version name, alias, or dotted release number. ``None``
            selects the default version of a version-dependent language.

    Returns:
        The canonical version name, or ``None`` when the language has no
        version-dependent comment syntax and no version was requested.

    Raises:
        NotImplementedError: If the language is not in the registry.
        UnsupportedCommentLanguageVersionError: If ``version`` is not a
            supported version of the language, or the language has no versions.
    """

    key, table = _version_table(language)
    if version is None:
        return None if table is None else table.default
    if not isinstance(version, str):
        raise TypeError("version must be a string or None")
    if table is None:
        raise UnsupportedCommentLanguageVersionError(language, version, ())
    label = _normalize_version_label(version)
    for candidate in table.versions:
        if label in (_normalize_version_label(name) for name in candidate.labels):
            return candidate.name
    if _RELEASE_PATTERN.fullmatch(label) and all(v.release for v in table.versions):
        requested = _release_key(label)
        selected = None
        for candidate in table.versions:
            if _release_key(candidate.release) <= requested:
                selected = candidate.name
        if selected is not None:
            return selected
    raise UnsupportedCommentLanguageVersionError(language, version, table.version_names)


def warn_default_comment_language_version(language: str) -> None:
    """Warn once per language that its default comment version was assumed."""

    key, table = _version_table(language)
    if table is None or key in _WARNED_DEFAULT_VERSIONS:
        return
    _WARNED_DEFAULT_VERSIONS.add(key)
    warnings.warn(
        f"Comment syntax for {language!r} depends on the language version; assuming "
        f"{table.default!r}. Pass version= to choose one of: {_describe_versions(table)}.",
        CommentLanguageVersionWarning,
        stacklevel=_caller_stacklevel(),
    )


_PACKAGE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _caller_stacklevel() -> int:
    """Return the ``warnings.warn`` stacklevel of the first frame outside ml4setk."""

    frame = sys._getframe(1)
    level = 1
    while frame is not None:
        if not os.path.abspath(frame.f_code.co_filename).startswith(_PACKAGE_DIR + os.sep):
            return level
        frame = frame.f_back
        level += 1
    return 1


def resolve_query_language_version(language: str, version: Optional[str]) -> Optional[str]:
    """Resolve a query's version, warning once when a needed version is omitted."""

    resolved = resolve_comment_language_version(language, version)
    if version is None and resolved is not None:
        warn_default_comment_language_version(language)
    return resolved


@lru_cache(maxsize=None)
def _versioned_comment_syntax(key: str, version_name: str) -> CommentSyntax:
    """Return ``key``'s syntax with a non-default version overlay applied."""

    base = LANGUAGE_SYNTAX[key]
    table = base.versions_for_language(key)
    version = table.version(version_name)

    def pick(value, default):
        return default if value is None else value

    return replace(
        base,
        regex_patterns=pick(version.regex_patterns, base.regex_patterns_for_language(key)),
        language_regex_patterns=(),
        nested_delimiters=pick(version.nested_delimiters, base.nested_delimiters),
        excluded_comment_prefixes=pick(
            version.excluded_comment_prefixes, base.excluded_comment_prefixes_for_language(key)
        ),
        language_excluded_comment_prefixes=(),
        contextual_extractor=pick(version.contextual_extractor, base.contextual_extractor),
        unclosed_block_openers=pick(version.unclosed_block_openers, base.unclosed_block_openers),
        sanitizer_line_wrappers=base.sanitizer_line_wrappers + version.sanitizer_line_wrappers,
        sanitizer_block_wrappers=base.sanitizer_block_wrappers + version.sanitizer_block_wrappers,
        canonical_regex_examples=base.canonical_regex_examples
        + tuple(example for example in version.examples if example.kind != "nested"),
        canonical_nested_examples=base.canonical_nested_examples
        + tuple(example for example in version.examples if example.kind == "nested"),
    )


def get_comment_syntax(language: str, version: Optional[str] = None) -> CommentSyntax:
    """Return syntax metadata for one supported language.

    Args:
        language: Registry key or alias. Lookup is case-insensitive.
        version: Optional language version name, alias, or release number.
            ``None`` and the default version return the registry entry itself;
            another version returns a copy with that version's overlay applied.

    Returns:
        The matching ``CommentSyntax`` entry.

    Raises:
        NotImplementedError: If the language is not in the registry.
        UnsupportedCommentLanguageVersionError: If ``version`` is not
            supported for the language.
    """

    key = _resolve_comment_language_key(language)
    if version is None:
        return LANGUAGE_SYNTAX[key]
    version_name = resolve_comment_language_version(key, version)
    if version_name == LANGUAGE_SYNTAX[key].versions_for_language(key).default:
        return LANGUAGE_SYNTAX[key]
    return _versioned_comment_syntax(key, version_name)


def get_comment_language_version(
    language: str, version: Optional[str] = None
) -> Optional[CommentLanguageVersion]:
    """Return version metadata, using the default version when ``version`` is ``None``."""

    key, table = _version_table(language)
    name = resolve_comment_language_version(key, version)
    return None if name is None else table.version(name)


def get_comment_language_versions(language: str) -> Tuple[str, ...]:
    """Return a language's supported comment versions in chronological order.

    The tuple is empty for languages whose comment syntax does not depend on
    the language version.
    """

    _, table = _version_table(language)
    return () if table is None else table.version_names


def get_default_comment_language_version(language: str) -> Optional[str]:
    """Return the version assumed when none is given, or ``None`` if unversioned."""

    _, table = _version_table(language)
    return None if table is None else table.default


def comment_language_requires_version(language: str) -> bool:
    """Return whether ``language`` has version-dependent comment syntax."""

    _, table = _version_table(language)
    return table is not None


VERSIONED_COMMENT_LANGUAGES = tuple(
    language for language in SUPPORTED_LANGUAGES if comment_language_requires_version(language)
)


def iter_comment_syntaxes() -> Iterable[CommentSyntax]:
    """Return all canonical syntax-family entries in registry order."""

    return COMMENT_SYNTAXES
