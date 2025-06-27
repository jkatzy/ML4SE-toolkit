from tree_sitter_languages import get_language, get_parser
from ..Query import Query

class TreeSitterQuery(Query):
    def __init__(self, language):
        self.language = get_language(language)
        self.parser = get_parser(language)

    def contains(self, text, rule):
        return len(self.parse(text, rule)) > 0


    def parse(self, text, rule):
        encoded_text = text.encode()
        tree = self.parser.parse(encoded_text)
        node = tree.root_node

        query = self.language.query(rule)
        matches = query.captures(node)

        results = []
        for capture_node, _ in matches:
            byte_start = capture_node.start_byte
            byte_end = capture_node.end_byte

            # Convert byte offsets to character offsets
            char_start = len(encoded_text[:byte_start].decode('utf-8', errors='ignore'))
            char_end = len(encoded_text[:byte_end].decode('utf-8', errors='ignore'))

            match_text = text[char_start:char_end]
            prefix_len = char_start
            suffix_len = len(text) - char_end

            results.append((prefix_len, suffix_len, match_text))

        return results
