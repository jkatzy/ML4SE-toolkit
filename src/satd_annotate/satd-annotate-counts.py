from datasets import load_from_disk

# Load local dataset
language = 'Java'
ds = load_from_disk(f"/scratch/lcwitte/satd-annotate/{language.lower()}/satd-all")
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

def add_satd_count_batch(batch):
    return {"satd_count": [len(decode_bitmask_string(b)) for b in batch["bitmask_satd"]]}

ds_counts = ds.map(add_satd_count_batch, batched=True, batch_size=100000)

# Save the dataset with counts
ds_counts.save_to_disk(f"/scratch/lcwitte/satd-annotate/{language.lower()}/satd-all-counts")

print(f"Total SATD comments: {sum(ds_counts['satd_count'])}")
