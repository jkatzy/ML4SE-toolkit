from tree_sitter_languages import get_language, get_parser

def getParser(language):
    parser = get_parser(language)
    parser.set_language(get_language(language))
    return parser

def getLanguage(lang):
    return get_language(lang)
