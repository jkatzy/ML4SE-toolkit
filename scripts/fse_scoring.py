"""ML4SETK scoring routines for the fixed, labeled FSE benchmark."""

import random
from statistics import mean

import numpy as np
import torch

from ml4setk.MIA import MembershipScorer
from ml4setk.MIA.pac import _polarized_distance


def polarized_gap(values):
    length = len(values)
    low, high = min(30, length), min(5, length)
    scale = min(1.0, length / (low + high))
    return _polarized_distance(
        values.tolist(), low_count=max(1, int(low * scale)), high_count=max(1, int(high * scale))
    )


def token_neighbors(source, tokenizer, seed):
    # The artifact samples two distinct indices per swap. Sampling from a range
    # avoids materializing a file-length index list for each swap.
    rng = random.Random(seed)
    original = tokenizer.encode(source, add_special_tokens=False, verbose=False)
    positions = range(len(original))
    neighbors = []
    for _ in range(5):
        tokens = original.copy()
        for _ in range(int(0.3 * len(tokens))):
            left, right = rng.sample(positions, 2)
            tokens[left], tokens[right] = tokens[right], tokens[left]
        neighbors.append(tokenizer.decode(tokens, skip_special_tokens=True))
    return neighbors


@torch.inference_mode()
def fse_statistics(text, tokenizer, model, device):
    # Match the deposit's forward arguments, including the attention mask.
    inputs = tokenizer(text, truncation=True, max_length=8192, return_tensors="pt").to(device)
    ids = inputs.input_ids
    if ids.shape[1] < 2:
        raise ValueError("Missing next-token targets")
    output = model(**inputs, labels=ids)
    targets = ids[0, 1:, None]
    logs = []
    for logits, labels in zip(output.logits[0, :-1].split(256), targets.split(256)):
        logs.append(logits.log_softmax(-1).gather(1, labels).flatten().cpu().numpy())
    return -output.loss.item(), polarized_gap(np.concatenate(logs))


class BenchmarkScorer(MembershipScorer):
    """Experiment adapter over the explicitly labeled FSE benchmark sources."""

    def __init__(self, method, neighbors, tokenizer, device, original_stats=None):
        self.method = method
        self.neighbors = neighbors
        self.tokenizer = tokenizer
        self.device = device
        self.original_stats = original_stats

    def score(self, model, source):
        variants = self.neighbors[source]
        if self.original_stats is None:
            log_likelihood, gap = fse_statistics(source, self.tokenizer, model, self.device)
        else:
            if source not in self.original_stats:
                self.original_stats[source] = fse_statistics(
                    source, self.tokenizer, model, self.device
                )
            log_likelihood, gap = self.original_stats[source]
        if self.method == "loss":
            return log_likelihood
        gaps = {source: gap}
        for neighbor in variants:
            if neighbor not in gaps:
                _, gaps[neighbor] = fse_statistics(neighbor, self.tokenizer, model, self.device)
        # The joint API requires higher scores for members. The FSE raw PAC
        # columns use the opposite sign.
        return mean(gaps[text] for text in variants) - gap
