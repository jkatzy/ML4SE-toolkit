"""Recompute summary arithmetic and check example provenance in Ye et al. (ACL 2024)."""

import argparse
import json
import re
import subprocess
import unicodedata
from pathlib import Path


def table1(text):
    header = "WikiMIA StackMIAsub\nPPL Zlib"
    rows = text.split(header, 1)[1].split("\nMean\n", 1)[1].split("Table 1:", 1)[0]
    values = re.findall(r"0\.\d{3}(?:↑\d+(?:\.\d+)?%)?", rows)
    assert len(values) == 28
    for start, form, dataset in [
        (0, "original", "WikiMIA"),
        (7, "original", "StackMIAsub"),
        (14, "rewritten", "WikiMIA"),
        (21, "rewritten", "StackMIAsub"),
    ]:
        baseline = max(float(cell) for cell in values[start : start + 6])
        pac, published_gain = values[start + 6].split("↑")
        gain = 100 * (float(pac) / baseline - 1)
        print(f"Table 1 {dataset} {form}: paper {published_gain}, from mean AUCs {gain:.2f}%")


def table4(text):
    rows = text.split("Rate Total Rate Total Rate Total\n", 1)[1].split("Table 4:", 1)[0]
    assert len(rows.splitlines()) == 4
    for row in rows.splitlines():
        model, *cells = row.split()
        rates = [float(token.rstrip("%")) for token in cells[:-1:2]]
        sizes = [int(token) for token in cells[1:-1:2]]
        average = sum(rate * size for rate, size in zip(rates, sizes)) / sum(sizes)
        print(f"Table 4 {model}: paper {cells[-1]}, from rates and sizes {average:.2f}%")
        assert f"{average:.1f}%" == cells[-1]


def normalized(text):
    # PDF extraction can turn a quote next to a vowel into a combining diaeresis.
    return "".join(c for c in unicodedata.normalize("NFKD", text).casefold() if c.isalnum())


def table7(text, dataset):
    appendix = text.rsplit("Figure 8:", 1)[1].split("Table 7:", 1)[0]
    originals = re.findall(r"(?:\n|\f)ori (.+?)\nsyn ", appendix, flags=re.DOTALL)
    with dataset.open(encoding="utf-8") as source:
        rows = [json.loads(line) for line in source]
    members = {
        normalized(row["snippet"])
        for row in rows
        if row["label"] == 1 and 32 < len(row["snippet"].split()) <= 64
    }
    keys = [normalized(original) for original in originals]
    assert len(keys) == 5 and len(set(keys)) == 4 and set(keys) <= members
    print(
        "Table 7: all 5 printed original examples found, 4 distinct, in the 33–64 word member group"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paper", type=Path, help="Final ACL Anthology PDF")
    parser.add_argument("stackmia", type=Path, help="Pinned StackMIAsub.jsonl")
    args = parser.parse_args()
    paper = subprocess.check_output(["pdftotext", "-raw", args.paper, "-"], encoding="utf-8")
    table1(paper)
    table4(paper)
    table7(paper, args.stackmia)
