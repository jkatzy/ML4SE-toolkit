# imports
from datasets import load_from_disk
import matplotlib.pyplot as plt
from tqdm import tqdm
from collections import Counter
import pandas as pd
import os
import re

# Load local dataset
language = 'Java'
ds = load_from_disk(f"/scratch/lcwitte/satd-annotate/{language.lower()}/satd-1m")
print(len(ds))

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

# Ensure the directory exists
output_dir = "/scratch/lcwitte/results/presence-100k"
os.makedirs(output_dir, exist_ok=True)

satd_counts = ds["satd_count"]
loc_counts = ds["total_lines"]

average_satd = sum(satd_counts) / len(satd_counts)
median_satd = sorted(satd_counts)[len(satd_counts) // 2] if satd_counts else 0
max_satd = max(satd_counts)

# Calculate the percentage of files with at least one SATD
files_with_satd = sum(1 for count in satd_counts if count > 0)
percentage_with_satd = (files_with_satd / len(satd_counts)) * 100
satd_per_kloc = sum(satd_counts) / (sum(loc_counts) / 1000) if sum(loc_counts) > 0 else 0

# Print the results
print(f"Total number of SATD comments: {sum(satd_counts)}")
print(f"Average SATD count per file: {average_satd:.2f}")
print(f"Median SATD count per file: {median_satd}")
print(f"Maximum SATD count in a single file: {max_satd}")
print(f"Percentage of files with at least one SATD: {percentage_with_satd:.2f}%")
print(f"SATD comments per KLOC: {satd_per_kloc:.2f}")

# Plot the histogram
plt.figure(figsize=(10, 6))
plt.hist(satd_counts, bins=range(1, max(satd_counts) + 2), edgecolor='black', alpha=0.7, log=True)
plt.title('Histogram of SATD Comments per File')
plt.xlabel('Number of SATD Comments')
plt.ylabel('Number of Files')
plt.grid(axis='y', linestyle='--', alpha=0.7)
# save plt as pdf
plt.savefig(os.path.join(output_dir, "satd_histogram.pdf"), format='pdf')


COMMENT_PREFIX_RE = re.compile(r'^/\*+\s*')   # For /* or /** start
COMMENT_SUFFIX_RE = re.compile(r'\s*\*/$')    # For */ end
LEADING_STAR_RE = re.compile(r'^\s*\*\s?')    # For each line in block/Javadoc

def strip_java_comment_syntax_bulk(comments: list[str]) -> list[str]:
    cleaned = []

    for comment in comments:
        c = comment.strip()

        if c.startswith("//"):
            cleaned.append(c[2:].lower().split())
        elif c.startswith("/*"):
            c = COMMENT_PREFIX_RE.sub('', c)
            c = COMMENT_SUFFIX_RE.sub('', c)

            if '\n' in c:
                lines = c.splitlines()
                lines = [LEADING_STAR_RE.sub('', line) for line in lines]
                c = "\n".join(lines)

            cleaned.append(c.lower().split())
        else:
            cleaned.append(c.lower().split())

    return cleaned


satd_comments = []

for file in tqdm(ds, desc="Extracting SATD comments"):
    spans = decode_bitmask_string(file["bitmask_satd"])
    for span in spans:
        start = span[0]
        end = span[1]
        satd_comments.append(file["content"][start:end])

cleaned_comments = strip_java_comment_syntax_bulk(satd_comments)

def generate_n_grams(words, n):
    return [" ".join(words[i:i+n]) for i in range(len(words)-n+1)]

for n in range(1, 7):
    n_grams = []
    for comment in cleaned_comments:
        n_grams.extend(generate_n_grams(comment, n))
    if n == 1:
        n_grams = [gram for gram in n_grams if len(gram) > 2]  # Filter out single characters and short words
    n_gram_counts = Counter(n_grams)
    n_gram_df = pd.DataFrame(n_gram_counts.items(), columns=["N-Gram", "Count"])
    n_gram_df = n_gram_df.sort_values(by="Count", ascending=False).reset_index(drop=True)
    n_gram_df["Rank"] = n_gram_df.index + 1

    # Save only the top 100 rows to the CSV file
    top_100_df = n_gram_df.head(100)
    top_100_df.to_csv(os.path.join(output_dir, f"satd_n_grams_top_100_{n}.csv"), index=False)
    print(f"Top 10 {n}-grams:")
    print(n_gram_df.head(10))