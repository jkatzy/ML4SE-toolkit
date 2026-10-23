"""Unwrapping regressions found by judging real comments.

Each case is a minimized comment from a public project's source, cleaned by
``sanitize_comment``. The project and file are named above each case. The
link definition, prompt, indented example, and two-pipe cases already passed
before the fix; they guard the new rules against reaching too far.
"""

import pytest

from ml4setk import unwrap_comment

pytestmark = pytest.mark.unit

KEEPS = {
    # haskell/containers Data/Map/Internal.hs: bird-track examples.
    "haskell_bird_tracks": (
        '> lookupIndex 2 (fromList [(5,"a"), (3,"b")])   == Nothing\n'
        '> fromJust (lookupIndex 3 (fromList [(5,"a"), (3,"b")])) == 0'
    ),
    # haskell/containers Data/Map/Internal.hs: a signature after prose.
    "haskell_signature": (
        "Delete the value at the key. If it is absent the result is Nothing.\n"
        "mustDelete :: Ord k => k -> Map k a -> Maybe (Map k a)\n"
        "mustDelete = alterF (Nothing <$)"
    ),
    # rails/rails activesupport/lib/active_support/cache.rb.
    "ruby_result_comments": (
        "  cache.write('city', \"Duckburgh\") # => true\n  cache.read('city')   # => \"Duckburgh\""
    ),
    # rails/rails activerecord/lib/active_record/associations.rb.
    "ruby_table_rows": (
        "  other                             |     X      |      X       |    X\n"
        "  other=(other)                     |     X      |      X       |    X"
    ),
    "ruby_trailing_comments": (
        "  project.milestones.size        # uses the milestone counter cache\n"
        "  project.milestones.empty?      # uses the milestone counter cache"
    ),
    # scala/scala src/library/scala/Option.scala.
    "scala_match_arms": (
        "  case Some(x) if p(x) => Some(x)  // keeps the value from the option\n"
        "  case _               => None"
    ),
    # lodash/lodash lodash.js.
    "javascript_declarations": (
        "var matchesFunc = _.overSome([{ 'a': 1 }, { 'a': 2 }])\n"
        "var matchesPropertyFunc = _.overSome([['a', 1], ['a', 2]])"
    ),
    # apache/commons-lang StringUtils.java.
    "java_call_results": (
        'StringUtils.appendIfMissing("abcXYZ", "xyz", "mno") = "abcXYZxyz"\n'
        'StringUtils.appendIfMissing("abcMNO", "xyz", "mno") = "abcMNOxyz"'
    ),
    # python/cpython Lib/argparse.py: a call split over lines.
    "python_open_call": (
        "parser = argparse.ArgumentParser(\n    description='sum the integers at the command line')"
    ),
    # rust-lang/rust library/alloc/src/vec/mod.rs: link definitions.
    "markdown_link_definitions": (
        "[`Layout`]: crate::alloc::Layout\n[`Layout::array::<T>(cap)`]: crate::alloc::Layout::array"
    ),
    # erlang/otp lib/stdlib/src/gen_server.erl: a diagram in columns.
    "column_diagram": (
        "    start            ----->             start\n    init             <-----              ."
    ),
    # elixir-lang/elixir lib/elixir/lib/enum.ex: a prompt and its result.
    "iex_prompt_result": (
        "Maps and sums the given `enumerable` in one pass.\n"
        "\n"
        "    iex> Enum.sum_by([%{count: 1}, %{count: 2}, %{count: 3}], fn x -> x.count end)\n"
        "    6"
    ),
    # rails/rails activerecord/lib/active_record/associations.rb: an
    # indented example with no punctuation that marks it as code.
    "ruby_indented_example": (
        "Consider the following loop using the class above, which prints a post:\n"
        "\n"
        "  Post.all.each do |post|\n"
        '    puts "Post:            " + post.title\n'
        '    puts "Written by:      " + post.author.name\n'
        '    puts "Last comment on: " + post.comments.first.created_on\n'
        "  end\n"
        "\n"
        "To iterate over these one hundred posts, we'll generate 201 database queries."
    ),
    "ruby_indented_class": (
        "Specifies a many-to-many relationship with another class, as follows:\n"
        "\n"
        "  class CreateDevelopersProjectsJoinTable < ActiveRecord::Migration[8.2]\n"
        "    def change\n"
        "      create_join_table :developers, :projects\n"
        "    end\n"
        "  end"
    ),
    # pandas-dev/pandas pandas/core/frame.py: numpydoc parameter rows.
    "numpydoc_fields": (
        "other : scalar, sequence, Series, dict or DataFrame\n"
        "func : arithmetic or comparison operator"
    ),
    # sqlite/sqlite src/btree.c: items numbered in parentheses.
    "parenthesized_items": (
        "(1) We found one or more cells (cntNew[0])>0), or\n"
        "(2) pPage is a virtual root page.  A virtual root page is when"
    ),
    # python/cpython Lib/difflib.py: doctest output after a prompt.
    "doctest_output": (
        ">>> for block in s.get_matching_blocks():\n"
        '...     print("a[%d] and b[%d] match for %d elements" % block)\n'
        "a[0] and b[0] match for 8 elements\n"
        "a[8] and b[17] match for 21 elements"
    ),
    # dotnet/fsharp src/FSharp.Core/list.fsi: a lone <code> line after prose.
    "fsharp_code_tag_line": (
        "Using the identity function <c>id</c> (is defined like <c>fun x -> x</c>):\n"
        '<code lang="fsharp">\n'
        "let input1 = [ Some 1; None; Some 3; None ]"
    ),
    # dotnet/fsharp src/FSharp.Core/list.fsi: a type definition in an example.
    "fsharp_type_definition": (
        '<code lang="fsharp">Count the number of times the coins match:\n'
        "type CoinToss = Head | Tails"
    ),
    # rust-lang/rust bootstrap.example.toml: items numbered with a dash.
    "numbered_dash_items": (
        "0 - Set the number of threads according to the detected number of threads of the "
        "host system\n"
        "1 - Use a single thread for compilation of Rust code (the default)\n"
        "N - Number of threads used for compilation of Rust code"
    ),
    # rails/rails activerecord/lib/active_record/associations.rb: calls with
    # a symbol argument.
    "ruby_symbol_calls": (
        '  belongs_to :person, primary_key: "name", foreign_key: "person_name"\n'
        '  belongs_to :author, class_name: "Person", foreign_key: "author_id"\n'
        '  belongs_to :valid_coupon, ->(o) { where "discounts > ?", o.payments_count },\n'
        "  belongs_to :attachable, polymorphic: true"
    ),
    # lowRISC/ibex rtl/ibex_core.sv: a Verilog macro call after prose.
    "verilog_macro_call": (
        "If the ID stage signals its ready the mult/div FSMs must be idle in the following cycle\n"
        "`ASSERT(MultDivFSMIdleOnIdReady, id_in_ready |=> ex_block_i.sva_multdiv_fsm_idle)"
    ),
}

JOINS = {
    # openjdk/jdk java/util/HashMap.java: lines that start with {@code x}.
    "javadoc_inline_tag_lines": (
        "operations ({@code get} and {@code put}), assuming the hash function\n"
        "disperses the elements properly among the buckets.  Iteration over\n"
        'collection views requires time proportional to the "capacity" of the\n'
        "{@code HashMap} instance (the number of buckets) plus its size (the number\n"
        "of key-value mappings).",
        "operations ({@code get} and {@code put}), assuming the hash function "
        "disperses the elements properly among the buckets.  Iteration over "
        'collection views requires time proportional to the "capacity" of the '
        "{@code HashMap} instance (the number of buckets) plus its size (the number "
        "of key-value mappings).",
    ),
    # sqlite/sqlite src/pager.c: indented prose that starts and ends with calls.
    "indented_prose_with_calls": (
        "Variable dbFileSize.\n"
        "\n"
        "  The only reason the dbFileSize variable is required is to suppress\n"
        "  unnecessary calls to xTruncate() after committing a transaction. If,\n"
        "  when a transaction is committed, the dbFileSize variable indicates\n"
        "  that the database file is larger than the database image (Pager.dbSize),\n"
        "  pager_truncate() is called. The pager_truncate() call uses xFilesize()\n"
        "  to measure the database file on disk, and then truncates it if required.",
        "Variable dbFileSize.\n"
        "\n"
        "  The only reason the dbFileSize variable is required is to suppress "
        "unnecessary calls to xTruncate() after committing a transaction. If, "
        "when a transaction is committed, the dbFileSize variable indicates "
        "that the database file is larger than the database image (Pager.dbSize), "
        "pager_truncate() is called. The pager_truncate() call uses xFilesize() "
        "to measure the database file on disk, and then truncates it if required.",
    ),
    # dotnet/fsharp src/FSharp.Core/list.fsi: XML doc text after its tag.
    "xml_doc_summary": (
        "<summary>Returns a new list that contains the elements of the first list\n"
        "followed by elements of the second list.</summary>",
        "<summary>Returns a new list that contains the elements of the first list "
        "followed by elements of the second list.</summary>",
    ),
    # google/guava ImmutableList.java: a paragraph opened by <p>.
    "javadoc_paragraph_tag": (
        "<p>It is not specified if any performance benefits apply if {@code expectedSize} is\n"
        "close to, but not exactly, the number of elements added to the builder.",
        "<p>It is not specified if any performance benefits apply if {@code expectedSize} is "
        "close to, but not exactly, the number of elements added to the builder.",
    ),
    # redis/redis src/t_list.c: prose that starts with a label.
    "label_then_prose": (
        "In-place rotation: the length is unchanged, so there is no key\n"
        "creation/deletion and no histogram change. Fire the push notification\n"
        "before the pop notification, matching LMOVE and the distinct-key path.",
        "In-place rotation: the length is unchanged, so there is no key "
        "creation/deletion and no histogram change. Fire the push notification "
        "before the pop notification, matching LMOVE and the distinct-key path.",
    ),
    # rust-lang/rust library/alloc/src/vec/mod.rs.
    "safety_label": (
        "SAFETY: Because of the invariant, read_ptr, prev_ptr and write_ptr\n"
        "are always in-bounds and read_ptr never aliases prev_ptr",
        "SAFETY: Because of the invariant, read_ptr, prev_ptr and write_ptr "
        "are always in-bounds and read_ptr never aliases prev_ptr",
    ),
    # elixir-lang/elixir lib/elixir/lib/enum.ex: a sentence ending in a colon.
    "lowercase_line_ending_in_colon": (
        "Finally, if you don't want to raise on empty enumerables, you can pass\n"
        "the empty fallback:",
        "Finally, if you don't want to raise on empty enumerables, you can pass "
        "the empty fallback:",
    ),
    # lodash/lodash lodash.js.
    "lowercase_word_and_colon": (
        "Iterates over elements of `collection`. The predicate is invoked with three\n"
        "arguments: (value, index, array).",
        "Iterates over elements of `collection`. The predicate is invoked with three "
        "arguments: (value, index, array).",
    ),
    # scala/scala src/library/scala/collection/immutable/List.scala.
    "tag_with_hanging_indent": (
        "@return  a list which contains `x` as first element and\n"
        "          which continues with this list.",
        "@return  a list which contains `x` as first element and which continues with this list.",
    ),
    # python/cpython Lib/argparse.py: a list item with a deeper hanging indent.
    "list_item_with_hanging_indent": (
        "- nargs -- The number of command-line arguments that should be\n"
        "      consumed. By default, one argument will be consumed and a single\n"
        "      value will be produced.",
        "- nargs -- The number of command-line arguments that should be "
        "consumed. By default, one argument will be consumed and a single "
        "value will be produced.",
    ),
    # golang/go src/net/http/server.go: a line ending in a semicolon.
    "prose_semicolon": (
        "Once Shutdown has been called on a server, it may not be reused;\n"
        "future calls to methods such as Serve will return ErrServerClosed.",
        "Once Shutdown has been called on a server, it may not be reused; "
        "future calls to methods such as Serve will return ErrServerClosed.",
    ),
    # elixir-lang/elixir lib/elixir/lib/gen_server.ex: a type with two pipes.
    "prose_with_two_pipes": (
        "Returning `{:noreply, new_state, timeout | :hibernate | {:continue, arg}}`\n"
        "is similar to `{:noreply, new_state}` except a timeout or continue occurs.",
        "Returning `{:noreply, new_state, timeout | :hibernate | {:continue, arg}}` "
        "is similar to `{:noreply, new_state}` except a timeout or continue occurs.",
    ),
    # haskell/text src/Data/Text.hs: a line that opens with /O(n)/ emphasis.
    "haddock_emphasis": (
        "/O(n)/ 'dropWhileEnd' @p@ @t@ returns the prefix remaining after\n"
        "dropping characters that satisfy the predicate @p@ from the end of\n"
        "@t@.",
        "/O(n)/ 'dropWhileEnd' @p@ @t@ returns the prefix remaining after "
        "dropping characters that satisfy the predicate @p@ from the end of\n"
        "@t@.",
    ),
    # WordPress/WordPress wp-includes/post.php: a deep hanging indent.
    "phpdoc_aligned_description": (
        "@type bool|string $label        A descriptive name for the post status marked\n"
        "                                for translation. Defaults to value of $post_status.",
        "@type bool|string $label        A descriptive name for the post status marked "
        "for translation. Defaults to value of $post_status.",
    ),
    # pandas-dev/pandas pandas/core/frame.py: an autolink on its own line.
    "rst_autolink": (
        "This method returns a new object using a lazy copy. See the `user guide\n"
        "<https://pandas.pydata.org/docs/dev/user_guide/migration.html>`__\n"
        "for more details.",
        "This method returns a new object using a lazy copy. See the `user guide "
        "<https://pandas.pydata.org/docs/dev/user_guide/migration.html>`__ "
        "for more details.",
    ),
}


@pytest.mark.parametrize("text", KEEPS.values(), ids=KEEPS.keys())
def test_keeps_breaks_in_examples_and_tables(text):
    assert unwrap_comment(text) == text


@pytest.mark.parametrize(("text", "expected"), JOINS.values(), ids=JOINS.keys())
def test_joins_prose_after_labels_tags_and_semicolons(text, expected):
    assert unwrap_comment(text) == expected


def test_joins_indented_prose_with_inline_markup():
    # rails/rails activesupport/lib/active_support/cache.rb: option text is
    # indented under its label and its lines start with inline <tt> tags.
    text = (
        "[+:coder+]\n"
        "  The coder for serializing and (optionally) compressing cache entries.\n"
        "\n"
        "  If the store can handle cache entries directly, you may also specify\n"
        "  <tt>coder: nil</tt> to omit the serializer, compressor, and coder. For\n"
        "  example, if you are using ActiveSupport::Cache::MemoryStore and can\n"
        "  guarantee that cache values will not be mutated."
    )
    assert unwrap_comment(text) == (
        "[+:coder+]\n"
        "  The coder for serializing and (optionally) compressing cache entries.\n"
        "\n"
        "  If the store can handle cache entries directly, you may also specify "
        "<tt>coder: nil</tt> to omit the serializer, compressor, and coder. For "
        "example, if you are using ActiveSupport::Cache::MemoryStore and can "
        "guarantee that cache values will not be mutated."
    )
