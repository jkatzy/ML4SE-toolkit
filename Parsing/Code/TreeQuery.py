import torch
from tree_sitter import Language, Parser
from tree_sitter_languages import get_language, get_parser
import os
import random
from random import choices, randint

from Parsing.Code.LanguageParser import getLanguage, getParser


def getQuery(name, lang):
    treesitter = {"identifiers", "string_literals", "boolean_literals", "numeric_literals", "function_call", "function_name"}
    #regex = {"closing_bracket", "stop", "eol", "keywords", "mathematical_operators", "boolean_operators", "assignment_operators"}
    if name in treesitter:
        return TreeSitterQuery(name, lang)

    else:
        raise ValueError("Query type not known " + name)


def getQueryString(lang, name):
    if name =='random':
        return ""
    if lang == 'java':
        return getJavaQuery(name)
    else:
        raise ValueError("Language not implemented")

def getQueryString(lang, name):
    if name =='random':
        return ""
    if lang == 'java':
        return getJavaQuery(name)
    else:
        raise ValueError("Language not implemented")

def getJavaQuery(name):
    if name == 'identifiers':
        return """
                (identifier) @id
               """
    elif name == 'string_literals':
        return """
                (string_literal) @String_literal
                (character_literal) @String_literal
               """
    elif name =="boolean_literals":
        return """
               (true) @boolean
               (false) @boolean
               """
    elif name == "numeric_literals":
        return """
               (decimal_integer_literal) @number
               (decimal_floating_point_literal) @number
               (hex_integer_literal) @number
               (binary_integer_literal) @number

               """
    elif name == "function_call":
        return """
                (method_invocation
                    name: (identifier) @func_call
                )
               """
    elif name == "function_name":
        return """
                   (method_declaration
                       name: (identifier) @func_name
                   )

               """
    elif name == "closing_bracket":
        return "}|\)|]"
    elif name == "eol":
        return ";\n"
    elif name == "keywords":
        return "abstract|assert|break|case|catch|continue|default|do|else|enum|exports|extends|final|finally|for|if|implements|import|instanceof|interface|module|native|new|package|private|protected|public|requires|return|static|super|switch|synchronized|this|throws|throw|transient|try|void|volatile|while"
    elif name == "mathematical_operators":
        return "\+|-|\*|/|>|<|>=|<=|%|\+\+|--"
    elif name == "boolean_operators":
        return "!|&&|\|\|==|!="
    elif name =="assignment_operators":
        return "\+=|-=|\*=|/=|%=|&=|\|=|\^=|>>=|<<="
    elif name == "stop":
        return "\."
    else:
        raise ValueError("Query not implemented: " + str(name))

class Query():
    def __init__(self, query_name, query_string, lang):
        self.query_name = query_name
        self.query_string = query_string
        self.lang = lang
        #self.tokenizer = tokenizer

    def get_span(self, content):
        raise Exception("Not implemented")

    # def tokenize(self, content, label):
    #     input = self.tokenizer(content, return_tensors = 'pt')
    #     label = self.tokenizer(label, return_tensors = 'pt')
    #
    #     return {"input": input, "label": label}
    def untokenize(self, content, label):

        return {"input": content, "label": label}

class TreeSitterQuery(Query):
    def __init__(self, query_name, lang):
        super(TreeSitterQuery).__init__()
        self.lang = lang
        self.query = getLanguage(self.lang).query(getQueryString(self.lang, query_name))
        self.parser = getParser(self.lang)


    def get_span(self, content):
        content = bytes(content, "UTF-8")
        tree = self.parser.parse(content)
        captures = self.query.captures(tree.root_node)

        try:
            capture = random.sample(captures, 1)[0]
        except ValueError:
            raise ValueError("No matches detected in sample")
        start = capture[0].start_byte
        finish = capture[0].end_byte

        target = content[start:finish]
        context = content[:start] + b"<fim_suffix>" + content[finish:]

        context = context.decode("UTF-8")
        target = target.decode("UTF-8")


        return self.untokenize(*(context, target))