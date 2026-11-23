"""Read the published vector curves in Figures 7 and 8 of the ACL proceedings PDF."""

import argparse

import pymupdf


def points(path):
    segments = path["items"]
    return [segments[0][1], *(segment[2] for segment in segments)]


def compare_figures(page):
    # Both figures have eight panels, six coloured lines per panel, and five x positions.
    paths = [
        path
        for path in page.get_drawings()
        if len(path["items"]) == 4
        and all(item[0] == "l" for item in path["items"])
        and abs(path["rect"].width - 79.226) < 0.015
    ]
    left = [path for path in paths if path["rect"].x0 < page.rect.width / 2]
    right = [path for path in paths if path["rect"].x0 > page.rect.width / 2]
    assert len(left) == len(right) == 48
    offset = points(right[0])[0].x - points(left[0])[0].x
    for first, second in zip(left, right):
        assert first["color"] == second["color"]
        for a, b in zip(points(first), points(second)):
            assert abs(b.x - a.x - offset) < 0.001 and abs(b.y - a.y) < 0.001
    print("Figures 7 and 8: all 240 plotted vertices coincide after horizontal translation")

    # Confirm that both figures also label the panels, tick marks, and legends alike.
    # The plot region ends before the captions, which name different datasets.
    words = [w for w in page.get_text("words") if w[1] < 570 and w[1] > 225]
    left_words = sorted((round(w[1], 2), w[4]) for w in words if w[0] < page.rect.width / 2)
    right_words = sorted((round(w[1], 2), w[4]) for w in words if w[0] > page.rect.width / 2)
    assert left_words and left_words == right_words
    print("Both panels use the same axis, model, and legend labels")
    return left


def print_gpt_neo(left):
    # Series colours come from the PPL and Ours legend strokes. Tick positions
    # are in PDF points, measured downwards from the top of the published page.
    palette = {(243, 114, 44): "Perplexity", (87, 117, 144): "PAC"}
    methods = set()
    for path in left:
        vertices = points(path)
        x, y = vertices[0]
        if abs(x - 204.671) > 0.01 or not 335 < y < 392:
            continue
        rgb = tuple(round(255 * c) for c in path["color"])
        if rgb in palette:
            method = palette[rgb]
            methods.add(method)
            for length, point in zip((32, 64, 128, 256, "pooled"), vertices):
                auc = 0.575 + (384.819427 - point.y) * 0.125 / (384.819427 - 337.927551)
                print(f"Figure 7 GPT-Neo {method}, {length}: {auc:.3f}")
    assert methods == set(palette.values())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paper", help="Final ACL Anthology PDF")
    args = parser.parse_args()
    with pymupdf.open(args.paper) as document:
        page = document[15]
        assert "Figure 7:" in page.get_text() and "Figure 8:" in page.get_text()
        print_gpt_neo(compare_figures(page))
