"""Redraw the Extraction reports from their checked-in aggregate measurements."""

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[3] / "docs/reproduction_reports/ml4setk/Extraction"


def read(module, filename):
    with (ROOT / module / filename).open() as f:
        return list(csv.DictReader(f))


def exposure():
    runs = read("exposure", "ptb_epochs.csv")
    batch = read("exposure", "ptb_batches.csv")
    steps = max(int(r["batch"]) for r in batch)
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.1), layout="constrained")
    axes[0].plot(
        [int(r["epoch"]) - 1 + int(r["batch"]) / steps for r in batch],
        [float(r["measured_bits"]) for r in batch],
        color="#28677d",
        lw=1,
        label="ML4SETK",
    )
    axes[0].scatter([1, 3], [3, 8], marker="D", color="#ac4c27", label="Paper, §7.1", zorder=3)
    axes[0].set(title="Figure 7 · 10% of PTB", ylabel="Estimated exposure (bits)", xlabel="Epoch")
    runs = [r for r in runs if r["figure"] == "8"]
    axes[1].plot(
        [int(r["epoch"]) for r in runs],
        [float(r["measured_bits"]) for r in runs],
        color="#28677d",
        label="ML4SETK",
    )
    axes[1].axvline(10, color="#ac4c27", lw=1.3, ls="--", label="Paper peak epoch")
    axes[1].set(title="Figure 8 · 5% of PTB", xlabel="Epoch", ylabel="Estimated exposure (bits)")
    for ax in axes:
        ax.legend(frameon=False)
        ax.grid(axis="y", alpha=0.2)
    fig.savefig(ROOT / "exposure" / "ptb.png", dpi=150)
    plt.close(fig)


def predictable():
    data = read("predictable", "pythia_comparisons.csv")
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.1), layout="constrained", sharey=True)
    for ax, suite, title in zip(axes, ["duped", "deduped"], ["Original Pile", "Deduplicated Pile"]):
        rows = [r for r in data if r["suite"] == suite and r["comparison"] == "scale"]
        for metric, color in [("precision", "#28677d"), ("recall", "#ac4c27")]:
            sizes = [r["condition"].upper() for r in rows]
            ax.plot(
                sizes,
                [float(r[f"ml4setk_{metric}"]) for r in rows],
                color=color,
                label=f"{metric.title()} · ML4SETK",
            )
            ax.scatter(
                sizes,
                [float(r[f"paper_{metric}"]) for r in rows],
                marker="o",
                facecolors="white",
                edgecolors=color,
                zorder=3,
                label=f"{metric.title()} · paper",
            )
        ax.set(title=title, xlabel="Pythia predictor size", ylim=(0, 1.02))
        ax.grid(axis="y", alpha=0.2)
        ax.tick_params(axis="x", labelsize=8)
    axes[0].set_ylabel("Precision or recall")
    axes[1].legend(loc="lower right", frameon=False, fontsize=8)
    fig.savefig(ROOT / "predictable" / "pythia.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    exposure()
    predictable()
