"""Secret Sharer Table 1 and Figure 7. Evaluate only the known planted numeral."""

import hashlib
import os
import random
from pathlib import Path

import pytest

from ml4setk.Extraction import canary_rank, exposure_bits


def test_table_one():
    rank = canary_rank(14.63, [18.56, 19.01, 20.65, 20.88, 20.99, 20.99, 21.16, 21.36])
    print(f"Table 1: rank {rank}, exposure {exposure_bits(10**9, rank):.6f} bits")
    assert rank == 1


@pytest.mark.parametrize(("figure", "divisor", "epochs"), [(7, 10, 3), (8, 20, 40)])
def test_training(figure, divisor, epochs):
    import torch
    from torch import nn

    device = "cuda" if torch.cuda.is_available() else "cpu"
    torch.manual_seed(19)
    torch.use_deterministic_algorithms(True)
    text = Path(os.environ["ML4SETK_PTB_TRAIN"]).read_bytes()
    assert hashlib.sha256(text).hexdigest() == (
        "fcea919f6cf83f35d4d00c6cbf08040d13d4155226340912e2fef9c9c4102cbf"
    )
    prefix = "the random number is "
    planted = 281265017
    corpus = text[: len(text) // divisor].decode("ascii")
    corpus = corpus[:1] + prefix + str(planted) + "\n" + corpus[1:]
    alphabet = {c: i for i, c in enumerate(sorted(set(text.decode("ascii") + "0123456789")))}
    ids = torch.tensor([alphabet[c] for c in corpus], device=device)
    # Contiguous character streams. The planted record is wholly inside the first update.
    batch_size, steps = 64, 64
    streams = ids[: len(ids) // batch_size * batch_size].reshape(batch_size, -1)
    held_out = Path(os.environ["ML4SETK_PTB_TEST"]).read_bytes()
    assert hashlib.sha256(held_out).hexdigest() == (
        "dd65dff31e70846b2a6030a87482edcd5d199130cdcfa1f3dccbb033728deee0"
    )
    test_ids = torch.tensor([alphabet[c] for c in held_out.decode("ascii")], device=device)
    test_streams = test_ids[: len(test_ids) // batch_size * batch_size].reshape(batch_size, -1)
    lookup = nn.Embedding(len(alphabet), 128).to(device)
    recurrent = nn.LSTM(128, 200, num_layers=2, batch_first=True).to(device)
    output = nn.Linear(200, len(alphabet)).to(device)
    params = [*lookup.parameters(), *recurrent.parameters(), *output.parameters()]
    optimizer = torch.optim.SGD(params, lr=1.0)

    # Simple random sample without replacement from the alternative nine-digit strings.
    draws = random.Random(19).sample(range(10**9 - 1), 8191)
    pool = [planted, *(n + (n >= planted) for n in draws)]
    samples = torch.tensor(
        [[alphabet[c] for c in prefix + f"{n:09d}"] for n in pool], device=device
    )

    @torch.inference_mode()
    def exposure():
        losses = []
        for batch in samples.split(256):
            hidden, _ = recurrent(lookup(batch[:, :-1]))
            loss = nn.functional.cross_entropy(
                output(hidden).flatten(0, 1), batch[:, 1:].reshape(-1), reduction="none"
            )
            losses.extend(loss.view(len(batch), -1).sum(1).tolist())
        return exposure_bits(len(pool), canary_rank(losses[0], losses[1:]))

    @torch.inference_mode()
    def held_out_loss():
        total, tokens, state = 0.0, 0, None
        for start in range(0, test_streams.shape[1] - 1, steps):
            batch = test_streams[:, start : start + steps + 1]
            hidden, state = recurrent(lookup(batch[:, :-1]), state)
            total += nn.functional.cross_entropy(
                output(hidden).flatten(0, 1), batch[:, 1:].reshape(-1), reduction="sum"
            ).item()
            tokens += batch[:, 1:].numel()
        return total / tokens

    print(f"Figure {figure} initial {exposure():.6f}")
    for epoch in range(1, epochs + 1):
        state = None
        train_total, train_tokens = 0.0, 0
        for start in range(0, streams.shape[1] - 1, steps):
            batch = streams[:, start : start + steps + 1]
            hidden, state = recurrent(lookup(batch[:, :-1]), state)
            state = tuple(x.detach() for x in state)
            loss = nn.functional.cross_entropy(
                output(hidden).flatten(0, 1), batch[:, 1:].reshape(-1)
            )
            optimizer.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_(params, 5.0)
            optimizer.step()
            train_total += loss.item() * batch[:, 1:].numel()
            train_tokens += batch[:, 1:].numel()
            if figure == 7:
                print(f"Figure 7,batch,{epoch},{start // steps + 1},{exposure():.6f}")
        print(
            f"Figure {figure},epoch,{epoch},{exposure():.6f},"
            f"{train_total / train_tokens:.6f},{held_out_loss():.6f}",
            flush=True,
        )
