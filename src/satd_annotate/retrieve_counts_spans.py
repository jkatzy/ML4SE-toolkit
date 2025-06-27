from datasets import load_from_disk
import json

language = 'Java'
ds = load_from_disk(f"/scratch/lcwitte/satd-annotate/{language.lower()}/satd-all-counts-spans")

annotations = []
for file in ds:
    annotations.append({
        "satd_spans": file["satd_spans"],
        "satd_count": file["satd_count"],
    })

# Save to JSONL (newline-delimited JSON)
print(f"Saving annotations to /scratch/lcwitte/satd-annotate/{language.lower()}/satd_count_spans_annotations.jsonl")
with open(f"/scratch/lcwitte/satd-annotate/{language.lower()}/satd_count_spans_annotations.jsonl", "w") as f:
    for entry in annotations:
        f.write(json.dumps(entry) + "\n")
