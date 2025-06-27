# Imports
from ml4setk.Parsing.Code.TreeSitterQuery import TreeSitterQuery
import re
from transformers import StoppingCriteria
import torch
import Levenshtein
from collections import Counter
import os
import json
import gzip

class StopOnSubstrings(StoppingCriteria):
    def __init__(self, stop_strings, tokenizer, start_len):
        self.stop_strings = stop_strings
        self.tokenizer = tokenizer
        self.start_len = start_len  # used to slice out only the generated part

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        # Decode only the newly generated part
        generated_ids = input_ids[0][self.start_len:]
        decoded = self.tokenizer.decode(generated_ids, skip_special_tokens=True)
        
        return any(stop in decoded for stop in self.stop_strings)
    
class StopOnMethodTreeSitter(StoppingCriteria):
    def __init__(self, tree_query: TreeSitterQuery, tokenizer, start_len):
        self.tree_query = tree_query
        self.tokenizer = tokenizer
        self.start_len = start_len
        self.open_bracket = False

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        last_token_id = input_ids[0, -1].item()
        last_token = self.tokenizer.decode([last_token_id])

        if not self.open_bracket:
            # Check if the last token is an opening brace, which indicates a multi-line method declaration
            if "{" in last_token:
                self.open_bracket = True
        
        # Only check when a closing brace is generated
        if "}" not in last_token and (self.open_bracket or ";" not in last_token):
            return False
        
        generated_ids = input_ids[0][self.start_len:]
        decoded = self.tokenizer.decode(generated_ids, skip_special_tokens=True)
        
        # Parse the generated code to check for method declarations
        methods = self.tree_query.parse(decoded, '(method_declaration) @method')

        # Only stop if a complete method is found and it ends with a closing brace
        if methods and ((decoded.strip().endswith("}") and methods[0][2].count("{") == methods[0][2].count("}")) or (not self.open_bracket and decoded.strip().endswith(";"))):
            return True
        
        return False
    
class LineRepetitionStoppingCriteria(StoppingCriteria):
    def __init__(self, tokenizer, start_len: int, filename: str, repeat_threshold: int = 5, min_line_length_ed: int = 20, edit_distance_threshold: int = 4):
        self.tokenizer = tokenizer
        self.start_len = start_len
        self.filename = filename
        self.repeat_threshold = repeat_threshold
        self.repeat_threshold_shortline = 20
        self.min_line_length_ed = min_line_length_ed
        self.edit_distance_threshold = edit_distance_threshold
        self.min_line_length_prefix = 40
        self.repeated_white_space_re = re.compile(r"\s{40,}")

    def is_similar(self, line1: str, line2: str) -> bool:
        return Levenshtein.distance(line1, line2) <= self.edit_distance_threshold
    
    def is_structurally_repetitive(self, prev_line: str, current_line: str) -> bool:
        # Check if one line is a prefix or suffix of another (ignoring whitespace and trailing punctuation)
        def clean(line: str) -> str:
            return line.strip().rstrip(";")

        p, c = clean(prev_line), clean(current_line)
        if len(c) < self.min_line_length_prefix or len(p) < self.min_line_length_prefix:
            return False
        if c.startswith(p) or p.startswith(c) or c.endswith(p) or p.endswith(c):
            return True
        return self.is_similar(p, c)  # Fall back to edit distance

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        # Only check when the last generated token is a newline
        last_token_id = input_ids[0, -1].item()
        last_token = self.tokenizer.decode([last_token_id])

        if "\n" not in last_token:
            return False  # Skip unless a new line was generated

        # Decode only the generated text
        generated_ids = input_ids[0][self.start_len:]
        text = self.tokenizer.decode(generated_ids, skip_special_tokens=True)

        if self.repeated_white_space_re.search(text):
            print(f"Stopping in file:{self.filename} due to excessive whitespace")
            return True

        lines = [line.strip() for line in text.split("\n") if line.strip()]

        if len(lines) < self.repeat_threshold:
            return False

        last_line = lines[-1]

        # If the last line is too short, check for short line repetition
        if len(last_line) < self.min_line_length_ed:
            if len(lines) < self.repeat_threshold_shortline:
                return False
            else:
                same_count = sum(1 for line in lines[:-1] if line == last_line)
                if same_count + 1 >= self.repeat_threshold_shortline:
                    print(f"Stopping in file:{self.filename} due to short line repetition: '{last_line}' repeated {same_count + 1} times")
                    return True
            return False
        
        else:
            similar_count_ed = sum(1 for line in lines[:-1] if self.is_similar(line, last_line))
            if similar_count_ed + 1 >= self.repeat_threshold:
                print(f"Stopping in file:{self.filename} due to line repetition: '{last_line}' repeated {similar_count_ed + 1} times")
                return True
            
            similar_count_prefix = sum(1 for line in lines[:-1] if self.is_structurally_repetitive(line, last_line))
            if similar_count_prefix + 1 >= self.repeat_threshold:
                print(f"Stopping in file:{self.filename} due to structural line repetition: '{last_line}' repeated {similar_count_prefix + 1} times")
                return True
        
        return False
    
class RepetitionInLongSingleLine(StoppingCriteria):
    def __init__(self, tokenizer, start_len: int, filename: str, min_repeat_len=4, max_repeat_len=20, threshold=40):
        self.tokenizer = tokenizer
        self.start_len = start_len
        self.filename = filename
        self.min_repeat_len = min_repeat_len
        self.max_repeat_len = max_repeat_len
        self.threshold = threshold
        self.long_line_threshold = 250

    def has_repeating_hallucination(self, line: str):
        for size in range(self.min_repeat_len, self.max_repeat_len + 1):
            for i in range(0, len(line) - size * self.threshold + 1):
                unit = line[i:i+size]
                if all(line[i + j*size:i + (j+1)*size] == unit for j in range(self.threshold)):
                    return True
        return False
    
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        generated_ids = input_ids[0][self.start_len:]
        text = self.tokenizer.decode(generated_ids, skip_special_tokens=True)

        lines = [line.strip() for line in text.split("\n") if line.strip()]
        if not lines:
            return False
        last_line = lines[-1]

        # Only check if the last line is long enough
        if len(last_line) > self.long_line_threshold:
            if self.has_repeating_hallucination(last_line):
                print(f"Stopping in file:{self.filename} due to hallucination in long line: '{last_line}'")
                return True
            else:
                self.long_line_threshold = self.long_line_threshold + 250  # Increase threshold for next checks
        return False

class RepetitionInSingleLineComment(StoppingCriteria):
    def __init__(self, tokenizer, start_len: int, filename: str, repeated_word_threshold: int = 30, long_digit_or_punct_threshold: int = 60,):
        self.tokenizer = tokenizer
        self.start_len = start_len
        self.filename = filename
        self.repeated_word_threshold = repeated_word_threshold
        self.long_digit_or_punct_threshold = long_digit_or_punct_threshold
        self.digits_or_delim_re = re.compile(rf"[\d.,]{{{self.long_digit_or_punct_threshold},}}")
        self.punct_re = re.compile(rf"([^\w\s])\1{{{self.long_digit_or_punct_threshold - 1},}}")
        self.repeated_number_punct_re = re.compile(rf"(?:\b\d+[\.\)]?\s+){{{self.repeated_word_threshold - 1},}}")
        self.repeated_white_space_re = re.compile(rf"\s{{{self.long_digit_or_punct_threshold - 1},}}")

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        generated_ids = input_ids[0][self.start_len:]
        text = self.tokenizer.decode(generated_ids, skip_special_tokens=True)

        # Only check if the generated text is long enough
        if len(text) < self.long_digit_or_punct_threshold:
            return False

        # Check 1: Long digit + punctuation sequences, Match N+ digits or digits with delimiters. EX: 1.1.1.1.1.1.1.
        # Check 2: Match N+ identical punctuation characters (excluding letters/numbers/whitespace). EX: #############
        # Check 3: Long repeated sequences of numbers or punctuation. EX: 1. 2. 3. 4. 5.
        # Check 4: Long repeated whitespace sequences. EX: "    "
        if self.digits_or_delim_re.search(text) or self.punct_re.search(text) or self.repeated_number_punct_re.search(text) or self.repeated_white_space_re.search(text):
            print(f"Stopping in file:{self.filename} due to repetition")
            return True

        # Check 4: Repeated words in the generated text
        words = text.split()
        word_counts = Counter(words)
        if any(count >= self.repeated_word_threshold for count in word_counts.values()):
            print(f"Stopping in file:{self.filename} due to repeated words: {word_counts.most_common(1)[0][0]} repeated {word_counts.most_common(1)[0][1]} times")
            return True

        return False
    

def load_threshold(filepath):
    output_dir_tresholds = "../../../data/thresholds/mean-2std-all" # Careful adjust this path if you change the thresholds
    with open(os.path.join(output_dir_tresholds, filepath), "r") as f:
        data = json.load(f)
    return data

def load_jsonl_gz(path):
    with gzip.open(path, 'rt', encoding='utf-8') as f:
        return [json.loads(line) for line in f]
    
def get_fim_input_ids(tokenizer, prefix, suffix, available_context, filename):
    """
    Constructs the FiM input IDs based on the prefix and suffix, ensuring they fit within the available token limit.
    """
    FIM_PREFIX = "<fim_prefix>"
    FIM_MIDDLE = "<fim_middle>"
    FIM_SUFFIX = "<fim_suffix>"

    # Tokenize prefix and suffix separately
    prefix_ids = tokenizer(prefix, return_tensors="pt", truncation=False)["input_ids"][0]
    suffix_ids = tokenizer(suffix, return_tensors="pt", truncation=False)["input_ids"][0]

    available = available_context - 3  # 3 for FIM_PREFIX, FIM_MIDDLE, FIM_SUFFIX

    total_len = len(prefix_ids) + len(suffix_ids)
    if total_len <= available:
        # No truncation needed
        prefix_final = prefix_ids
        suffix_final = suffix_ids
    else:
        # Truncate to keep tokens closest to the target
        half = available // 2

        if len(prefix_ids) > half and len(suffix_ids) > half:
            prefix_final = prefix_ids[-half:]
            suffix_final = suffix_ids[:half]
        elif len(prefix_ids) <= half:
            prefix_final = prefix_ids
            suffix_final = suffix_ids[: available - len(prefix_ids)]
        else:  # len(suffix_ids) <= half
            suffix_final = suffix_ids
            prefix_final = prefix_ids[-(available - len(suffix_ids)):]
        print(f"Input truncated to fit within available context, file: {filename}")

    # Reconstruct FiM input
    fim_input_ids = torch.cat([
        tokenizer(FIM_PREFIX, return_tensors="pt")["input_ids"][0],
        prefix_final,
        tokenizer(FIM_SUFFIX, return_tensors="pt")["input_ids"][0],
        suffix_final,
        tokenizer(FIM_MIDDLE, return_tensors="pt")["input_ids"][0],
    ]).unsqueeze(0)

    return fim_input_ids
    
