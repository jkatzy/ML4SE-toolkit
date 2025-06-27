# Imports
from datasets import load_from_disk
from ml4setk.Parsing.Code.TreeSitterQuery import TreeSitterQuery
import re
import SATDDetector

language = 'Java'

ds = load_from_disk(f"/scratch/lcwitte/the_heap/HeapJava")

print(len(ds))

def preprocess_comments(comments):
    """
    Preprocess comments to:
    1. Merge consecutive single-line comments into a single block.
    2. Exclude license comments at the beginning of the file that do not contain task annotations.
    3. Exclude commented-out code.
    4. Exclude Javadoc comments that do not contain task annotations.
    """
    processed_comments = []

    # Rule 1: Merge consecutive single-line comments
    # comments = merge_single_line_comments(comments)

    # Rule 2: Exclude license comments at the beginning of the file
    if comments and is_license_comment(comments[0][2]) and not contains_task_annotation(comments[0][2]):
        comments = comments[1:]  # Remove the first comment if it's a license comment

    for prefix, suffix, comment in comments:
        has_task_annotation = contains_task_annotation(comment)

        # Rule 3: Exclude commented-out code
        if is_commented_out_code(comment) and not has_task_annotation:
            continue

        # Rule 4: Exclude Javadoc comments without task annotations
        if is_javadoc_comment(comment) and not has_task_annotation:
            continue

        # Add the processed comment to the list
        processed_comments.append((prefix, suffix, comment))

    return processed_comments


TASK_PATTERN = re.compile(r'\b(?:todo|fixme|xxx)\b', re.IGNORECASE)
LICENSE_PATTERN = re.compile(r'\b(?:copyright|license|all rights reserved|permission|redistribution)\b', re.IGNORECASE)
SOURCE_CODE_REGEX = re.compile(
    r"else\s*\{|" +
    r"try\s*\{|" +
    r"do\s*\{|" +
    r"finally\s*\{|" +
    r"if\s*\(|" +
    r"for\s*\(|" +
    r"while\s*\(|" +
    r"switch\s*\(|" +
    r"(?:Long|Byte|Double|Float|Integer|Short|BigDecimal|BigInteger|Character|Boolean|String)\s*\(|" +
    r"assert\s*\(|" +
    r"System\.out\.|" +
    r"public\s+void|" +
    r"private\s+static\s+final|" +
    r"catch\s*\("
)

def contains_task_annotation(comment):
    return bool(TASK_PATTERN.search(comment))

def is_license_comment(comment):
    return bool(LICENSE_PATTERN.search(comment))

def is_commented_out_code(comment):
    return bool(SOURCE_CODE_REGEX.search(comment))

def is_javadoc_comment(comment):
    return comment.lstrip().startswith("/**")

def encode_bitmask_string(code_len: int, spans: list[tuple[int, int]]) -> str:
    mask = ['0'] * code_len
    for start, end in spans:
        mask[start:end] = ['1'] * (end - start)
    return ''.join(mask)

def decode_bitmask_string(mask: str) -> list[tuple[int, int]]:
    spans = []
    start = None
    for i, bit in enumerate(mask):
        if bit == '1':
            if start is None:
                start = i
        else:
            if start is not None:
                spans.append((start, i))
                start = None
    if start is not None:
        spans.append((start, len(mask)))
    return spans

# Function to classify SATD for a batch of rows
def classify_satd(batch):
    java_tree_query = TreeSitterQuery('java')
    detector = SATDDetector.SATDDetector()
    batch_bitmasks = []

    for content in batch["content"]:
        spans = []
        comments = java_tree_query.parse(content, '(line_comment) @comment (block_comment) @comment')
        preprocessed_comments = preprocess_comments(comments)
        for (prefix, suffix, comment) in preprocessed_comments:
            clean_comment = " ".join(comment.split())
            if detector.classify(clean_comment) == ">SATD":
                start = prefix
                end = len(content) - suffix
                spans.append((start, end))

        batch_bitmasks.append(encode_bitmask_string(len(content), spans))

    detector.close()
    return {"bitmask_satd": batch_bitmasks}


ds_satd = ds.map(
    classify_satd,
    batched=True,
    batch_size=100000,
)

# Save the dataset with bitmask
ds_satd.save_to_disk(f"/scratch/lcwitte/satd-annotate/{language.lower()}/satd-all")

# count SATD
satd_count = 0
for file in ds_satd:
    spans = decode_bitmask_string(file["bitmask_satd"])
    satd_count += len(spans)
print(f"Total SATD comments: {satd_count}")
