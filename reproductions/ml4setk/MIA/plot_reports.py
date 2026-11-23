"""Redraw the three original-study figures from the aggregate tables in the documentation."""

import csv
from math import erf, sqrt
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

REPORTS = Path(__file__).resolve().parents[3] / "docs/reproduction_reports/ml4setk/MIA"
PAPER = "#214567"
REPRODUCED = "#ad4826"
GRID = "#dbe2e5"


def rows(module, filename):
    with (REPORTS / module / "data" / filename).open(encoding="utf-8") as source:
        return list(csv.DictReader(source))


def save(figure, module, name):
    target = REPORTS / module / "figures"
    target.mkdir(exist_ok=True)
    figure.savefig(target / name, dpi=160, bbox_inches="tight", pad_inches=0.18)
    plt.close(figure)


def loss():
    data = rows("loss", "loss_figure2b.csv")
    fig, ax = plt.subplots(figsize=(7.3, 3.2), layout="constrained")
    ratios = [1 + i / 50 for i in range(351)]
    curve = [erf(1 / sqrt(2)) - erf(1 / (r * sqrt(2))) for r in ratios]
    ax.plot(ratios, curve, color=PAPER, lw=2, label="Yeom et al. · theoretical curve")
    ax.scatter(
        [int(r["sigma_ratio"]) for r in data],
        [float(r["reproduced"]) for r in data],
        color=REPRODUCED,
        edgecolor="white",
        s=65,
        zorder=3,
        label="ML4SETK · evaluated points",
    )
    ax.set(
        xlabel="Population / training standard deviation",
        ylabel="Membership advantage",
        xticks=[1, 2, 4, 6, 8],
        ylim=(-0.035, 0.65),
    )
    ax.grid(axis="y", color=GRID)
    ax.legend(loc="lower right", frameon=False)
    save(fig, "loss", "loss_figure2b.png")


def pac():
    data = {r["method"]: r for r in rows("pac", "pac_table1.csv")}
    fig, ax = plt.subplots(figsize=(7.3, 2.55), layout="constrained")
    for y, field in enumerate(["reproduced_roc_auc", "paper_roc_auc"]):
        a, b = (float(data[m][field]) for m in ("Perplexity", "PAC"))
        ax.plot([a, b], [y, y], color=GRID, lw=3, zorder=1)
        for x, name, marker, color in [(a, "Perplexity", "o", PAPER), (b, "PAC", "D", REPRODUCED)]:
            ax.scatter(
                x, y, marker=marker, color=color, s=54, zorder=2, label=name if y == 1 else None
            )
            ax.annotate(f"{x:.4f}", (x, y), xytext=(0, 9), textcoords="offset points", ha="center")
    ax.set(
        yticks=[0, 1],
        yticklabels=["ML4SETK", "Ye et al."],
        ylim=(-0.5, 1.6),
        xlim=(0.605, 0.677),
        xlabel="ROC-AUC",
    )
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.24), ncol=2, frameon=False)
    ax.grid(axis="x", color=GRID, alpha=0.7)
    save(fig, "pac", "pac_table1.png")


def pac_by_length():
    data = rows("pac", "pac_figure7_gpt_neo.csv")
    fig, axes = plt.subplots(1, 2, figsize=(8.2, 3.1), layout="constrained", sharey=True)
    for ax, method in zip(axes, ["Perplexity", "PAC"]):
        series = [r for r in data if r["method"] == method]
        lengths = [r["length"] for r in series]
        for field, label, color, marker in [
            ("paper_roc_auc", "Paper (digitized)", PAPER, "o"),
            ("reproduced_roc_auc", "ML4SETK", REPRODUCED, "x"),
        ]:
            ax.plot(
                lengths, [float(r[field]) for r in series], marker=marker, color=color, label=label
            )
        ax.set(title=method, xlabel="WikiMIA length group")
        ax.grid(axis="y", color=GRID)
    axes[0].set_ylabel("ROC-AUC")
    axes[1].legend(loc="lower right", frameon=False)
    save(fig, "pac", "pac_figure7_gpt_neo.png")


def ast_pac():
    data = rows("ast_pac", "ast_pac_fixed_pilot.csv")
    fig, axes = plt.subplots(1, 2, figsize=(8.8, 3.0), sharey=True, sharex=True)
    fig.subplots_adjust(left=0.19, right=0.98, bottom=0.16, top=0.76, wspace=0.14)
    for ax, metric in zip(axes, ["ROC-AUC", "PR-AUC"]):
        subset = [r for r in data if r["metric"] == metric]
        for index, row in enumerate(subset):
            y = len(subset) - 1 - index
            ax.hlines(
                y + 0.1,
                float(row["reference_ci_lower"]),
                float(row["reference_ci_upper"]),
                color=PAPER,
                lw=1.5,
            )
            ax.plot(
                float(row["reference"]),
                y + 0.1,
                "o",
                color=PAPER,
                mfc="white",
                mew=1.8,
                label="FSE companion table (95% interval)" if index == 0 else None,
            )
            ax.plot(
                float(row["reproduced"]),
                y - 0.1,
                "D",
                color=REPRODUCED,
                ms=5,
                label="ML4SETK" if index == 0 else None,
            )
        ax.set(
            yticks=range(len(subset)),
            yticklabels=[r["model"] for r in reversed(subset)],
            title=metric,
            ylim=(-0.45, 3.45),
            xlim=(0.485, 0.82),
        )
        ax.xaxis.set_major_locator(MaxNLocator(4))
        ax.grid(axis="x", color=GRID)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=2, frameon=False)
    save(fig, "ast_pac", "ast_pac_fixed_pilot.png")


def fse_strata():
    fig, axes = plt.subplots(
        2, 3, figsize=(9.2, 5.8), sharex=True, sharey=True, layout="constrained"
    )
    values = []
    for col, (name, title, section) in enumerate(
        [("loss", "Loss", "RQ2"), ("pac", "PAC", "RQ2"), ("ast_pac", "AST-PAC", "RQ3")]
    ):
        data = rows("ast_pac", f"{name}_fse.csv")
        for row, metric in enumerate(["ROC-AUC", "PR-AUC"]):
            ax = axes[row, col]
            pairs = [
                r
                for r in data
                if r["reference_source"] == f"{section} companion table" and r["metric"] == metric
            ]
            assert len(pairs) == 144
            ax.axline((0.5, 0.5), slope=1, color=PAPER, lw=1, linestyle="--", zorder=1)
            reference = [float(r["reference"]) for r in pairs]
            reproduced = [float(r["reproduced"]) for r in pairs]
            values.extend(reference)
            values.extend(reproduced)
            ax.scatter(
                reference,
                reproduced,
                color=REPRODUCED,
                s=13,
                alpha=0.6,
                linewidths=0,
                zorder=2,
            )
            ax.set_aspect("equal", adjustable="box")
            ax.set(xticks=[0.4, 0.6, 0.8], yticks=[0.4, 0.6, 0.8])
            if row == 0:
                ax.set_title(title)
            if col == 0:
                ax.set_ylabel(f"ML4SETK {metric}")
            if row == 1:
                ax.set_xlabel("FSE companion table")
    limits = (min(values) - 0.02, max(values) + 0.02)
    axes[0, 0].set(xlim=limits, ylim=limits)
    save(fig, "ast_pac", "fse_strata.png")


if __name__ == "__main__":
    plt.rcParams.update(
        {
            "font.size": 10,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.edgecolor": "#a9b6bd",
            "axes.axisbelow": True,
        }
    )
    loss()
    pac()
    pac_by_length()
    ast_pac()
    fse_strata()
