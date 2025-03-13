from ..Query import Query
import regex as re

class LineCommentQuery(Query):
    def __init__(self, language):
        self.language = language
        self.regexes = self.get_regex(language)

    def contains(self, string):
        contains = False
        for r in self.regexes:
            if(re.search(r, string)):
                return True
        return False

    def parse(self, text):
        matches = []
        for r in self.regexes:
            for m in re.finditer(r, text):
                prefix = text[:m.start()]
                match = m.group()
                suffix = text[m.end():]
                matches.append((prefix, suffix, match))
        return matches

    def get_regex(self, language):
        lang = language.lower()
        if lang in ['java', 'c', 'c++', 'c#', 'javascript', 'typescript', 'objective-c', 'go', 'kotlin', 'vue', 'scala', 'dart', 'rust', 'hack', 'less', 'groovy', 'processing', 'apex', 'cuda', 'scilab', 'antlr', 'swift', 'php']:      
            regex = self.get_regex_java()    
        elif lang in ['python', 'r', 'elixir', 'nix', 'starlark', 'graphql', 'crystal']: 
            regex = self.get_regex_python()  
        elif lang in ['ada']:
            regex = self.get_regex_ada()     
        elif lang in ['agda', 'elm']:       
            regex = self.get_regex_agda()    
        elif lang in ['assembly', 'netlogo', 'scheme']:
            regex = self.get_regex_assembly()
        elif lang in ['cobol']:
            regex = self.get_regex_cobol()   
        elif lang in ['coq', 'ocaml']:      
            regex = self.get_regex_coq()     
        elif lang in ['d']:
            regex = self.get_regex_d()       
        elif lang in ['erlang']:            
            regex = self.get_regex_erlang()  
        elif lang in ['f#']:
            regex = self.get_regex_fsharp()  
        elif lang in ['forth']:
            regex = self.get_regex_forth()   
        elif lang in ['fortran']:           
            regex = self.get_regex_fortran() 
        elif lang in ['julia']:
            regex = self.get_regex_julia()   
        elif lang in ['lisp']:
            regex = self.get_regex_lisp()    
        elif lang in ['lua']:
            regex = self.get_regex_lua()     
        elif lang in ['mathematica']:       
            regex = self.get_regex_mathematica()
        elif lang in ['matlab']:            
            regex = self.get_regex_matlab()  
        elif lang in ['perl']:
            regex = self.get_regex_perl()    
        elif lang in ['prolog']:            
            regex = self.get_regex_prolog()  
        elif lang in ['raku']:
            regex = self.get_regex_raku()    
        elif lang in ['ruby']:
            regex = self.get_regex_ruby()    
        elif lang in ['sql']:
            regex = self.get_regex_sql()     
        elif lang in ['webassembly']:       
            regex = self.get_regex_webassembly()
        elif lang in ['haskell']:           
            regex = self.get_regex_haskell() 
        else:
            raise NotImplemented        
        return regex

    def get_regex_java(self):
        return [
            r"\/\*[\S\s]*?\*\/",
            r"/{2}.*.*"
        ]
 
    def get_regex_python(self):
        return [
            r"#.*",
            r"\"{3}([\S\s]*?)\"{3}"
        ]

    def get_regex_erlang(self):
        return [
            r"%.*"
        ]
        
    def get_regex_julia(self):
        return [
            r"#=([\S\s]*?)=#",
            r"#.*"
        ] 
        
    def get_regex_lisp(self):
        return [
            r";.*"
        ]
        
    def get_regex_fortran(self):
        return [
            r"!.*"
        ]
        
    def get_regex_cobol(self):
        return [
            r"(^|\n).{6}(\*|/).*",
            r"\*>.*"
        ]
        
    def get_regex_html(self):
        return [
            r"<!--([\S\s]*?)-->"
        ]
        
    def get_regex_matlab(self):
        return [
            r"%{([\S\s]*?)%}",
            r"%.*"
        ]
        
    def get_regex_webassembly(self):
        return [
            r"\(;([\S\s]*?);\)",
            r";;.*"
        ]
        
    def get_regex_assembly(self):
        return [
            r";.*"
        ]

    def get_regex_ruby(self):
        return [
            r"#.*",
            r"=begin([\S\s]*?)=end"
        ]
        
    def get_regex_ada(self):
        return [
            r"--.*"
        ]

    def get_regex_d(self):
        return [
            r"\/\*\*[\S\s]*?\*\/",
            r"\/\+\+[\S\s]*?\+\/",
            r"\/\/\/.*"
        ]
        
    def get_regex_forth(self):
        return [
            r"\\\s.*",
            r"\(\s[\s\S]*?\s\)"
        ]
        
    def get_regex_lua(self):
        return [
            r"--\[\[[\s\S]*?\]\]",
            r"--.*"
        ]
        
    def get_regex_perl(self):
        return [
            r"=[\s\S]*?=cut",
            r"#.*"
        ]
        
    def get_regex_prolog(self):
        return [
            r"%.*",
            r"\/\*[\s\S]*?\*\/"
        ]
        
    def get_regex_raku(self):
        return [
            r"#'\([\s\S]*?\)",
            r"#'\{[\s\S]*?\}",
            r"#'\[[\s\S]*?\]",
            r"#'\<[\s\S]*?\>",
            r"#.*"
        ]
        
    def get_regex_sql(self):
        return [
            r"\/\*[\s\S]*?\*\/",
            r"--.*"
        ] 

    def get_regex_agda(self):
        return [
            r"--.*"
        ]

    def get_regex_fsharp(self):
        return [
            r"\/\/.*"
        ]

    def get_regex_haskell(self):
        return [
            r"--.*"
        ]

    def get_regex_mathematica(self):
        return []

    def get_regex_coq(self):
        return []

class NestedCommentQuery(Query):
    def __init__(self, language):
        self.language = language
        self.delimeters = self.get_delimeters(language)

    def contains(self, string):
        contains = False
        for d in self.delimeters:
            r = d[0] + "[\s\S]*" + d[1]
            if(re.search(r, string)):
                return True
        return False

    def parse(self, text):
        matches = []
        for d in self.delimeters:
            for m in self.parse_nested(d[0], d[1], text):
                matches.append(m)
        return matches

    def parse_nested(open_delim, close_delim, text):
        """Extracts only top-level delimited text (including delimiters) 
           and returns it with full surrounding text."""
        
        result = []
        stack = []
        top_level_ranges = []
        
        open_len = len(open_delim)
        close_len = len(close_delim)
        i = 0

        while i < len(text):
            if text[i:i+open_len] == open_delim:
                if not stack:  # Mark start of a top-level section
                    top_level_ranges.append([i, None])
                stack.append(i)
                i += open_len - 1  # Move past the opening delimiter
            elif text[i:i+close_len] == close_delim and stack:
                start = stack.pop()
                if not stack:  # Mark end of a top-level section
                    top_level_ranges[-1][1] = i + close_len - 1
                i += close_len - 1  # Move past the closing delimiter
            i += 1

        # Process each top-level section
        for start, end in top_level_ranges:
            inner_text = text[start:end + 1]  # Keep delimiters
            before_text = text[:start]
            after_text = text[end + 1:]
            result.append((inner_text, before_text, after_text))

        return result

    def get_delimeters(self, language):
        lang = language.lower()
        if lang in ['java', 'c', 'c++', 'c#', 'javascript', 'typescript', 'objective-c', 'go', 'kotlin', 'vue', 'scala', 'dart', 'rust', 'hack', 'less', 'groovy', 'processing', 'apex', 'cuda', 'scilab', 'antlr', 'swift', 'php', 'python', 'r', 'elixir', 'nix', 'starlark', 'graphql', 'crystal', 'ada', 'assembly', 'netlogo', 'scheme', 'cobol', 'd', 'erlang', 'forth', 'fortran', 'julia', 'lisp', 'lua', 'matlab', 'perl', 'prolog', 'raku', 'ruby', 'sql', 'webassembly']:
            delimeter = self.get_delimeter_null()
        elif lang in ['agda', 'elm']:
            delimeter = self.get_delimeter_agda()
        elif lang in ['coq', 'ocaml']:
            delimeter = self.get_delimeter_coq()
        elif lang in ['f#']:
            delimeter = self.get_delimeter_fsharp()
        elif lang in ['mathematica']:
            delimeter = self.get_delimeter_mathematica()
        elif lang in ['haskell']:
            delimeter = self.get_delimeter_haskell()
        else:
            raise NotImplemented
        return delimeter

    def get_delimeter_null(self):
        return []

    def get_delimeter_mathematica(self):
        return [
            ("(*", "*)")
        ]
       
    def get_delimeter_agda(self):
        return [
            ('{-', '-}')
        ]
        
    def get_delimeter_coq(self):
        return [
            ("(*", " *)")
        ]
        
    def get_delimeter_fsharp(self):
        return [
            ("(*", "*)")
        ]
        
    def get_delimeter_haskell(self):
        return [
            ("{-", "-}")
        ]
 
class CommentQuery(Query):

    def __init__(self, language):
        self.language = language
        self.line_comments = LineCommentQuery(language)
        self.nested_comments = NestedCommentQuery(language)

    def contains(self, text):
        if self.nested_comments.contains(text):
            return True
        elif self.line_comments.contains(text):
            return True
        return False
    
    def parse(self, text):
        comments = []
        comments.extend(self.nested_comments.parse(text))
        comments.extend(self.line_comments.parse(text))
        return comments
