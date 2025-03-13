from tree_sitter_languages import get_language, get_parser
from ..Query import Query

class TreeSitterQuery(Query):
    def __init__(self, language):
        self.language = get_language('python')
        self.parser = get_parser('python')

    def contains(self, text, rule):
        return len(self.parse(text, rule)) > 0


    def parse(self, text, rule):
        tree = self.parser.parse(text.encode())
        node = tree.root_node

        query = self.language.query(rule)
        matches = query.captures(node)

        tuples = [
            (text[:node.start_byte],  # Prefix (before node)
             text[node.end_byte:],    # Suffix (after node)
             text[node.start_byte:node.end_byte])  # Node text
            for node, _ in matches
        ]
        return tuples
