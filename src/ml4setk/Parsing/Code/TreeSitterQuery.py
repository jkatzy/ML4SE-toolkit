from ..Query import Query, QueryMatch

try:
    from tree_sitter_languages import get_language, get_parser
except ModuleNotFoundError as exc:
    get_language = None
    get_parser = None
    _TREE_SITTER_IMPORT_ERROR = exc
else:
    _TREE_SITTER_IMPORT_ERROR = None

class TreeSitterQuery(Query):
    def __init__(self, language):
        if get_language is None or get_parser is None:
            raise ModuleNotFoundError(
                "TreeSitterQuery requires the optional dependency "
                "`tree_sitter_languages`. Install it with "
                "`uv sync --group dev --extra treesitter`."
            ) from _TREE_SITTER_IMPORT_ERROR

        self.language_name = language
        self.language = get_language(language)
        self.parser = get_parser(language)

    def contains(self, text, rule):
        return len(self.parse(text, rule)) > 0


    def parse(self, text, rule):
        tree = self.parser.parse(text.encode())
        node = tree.root_node

        query = self.language.query(rule)
        matches = query.captures(node)

        tuples = [
            QueryMatch(
                text[:node.start_byte],
                text[node.end_byte:],
                text[node.start_byte:node.end_byte],
            )
            for node, _ in matches
        ]
        return tuples
