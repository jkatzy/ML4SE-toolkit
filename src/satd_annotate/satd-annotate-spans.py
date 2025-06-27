from datasets import load_from_disk
import os

# Load local dataset
language = 'Java'
ds_dir = f"/scratch/lcwitte/satd-annotate/{language.lower()}"
ds = load_from_disk(f"{ds_dir}/satd-all-counts")
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

def add_satd_spans_batch(batch):
    return {"satd_spans": [decode_bitmask_string(b) for b in batch["bitmask_satd"]]}

ds_spans = ds.map(add_satd_spans_batch, batched=True, batch_size=100000)

# Save the dataset with spans
print(f"Saving spans to disk...")
output_dir = f"{ds_dir}/satd-all-counts-spans"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
ds_spans.save_to_disk(output_dir)

print(f"Total SATD comments: {sum(len(spans) for spans in ds_spans['satd_spans'])}")
