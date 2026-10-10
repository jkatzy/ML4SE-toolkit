import json
import tempfile
from pathlib import Path

from ml4setk import ChunkedIterator, CommentQuery

QUERY = CommentQuery("python")


def comments(row):
    return [{"id": row["id"], "comment": match.match} for match in QUERY.parse(row["content"])]


def main():
    root = Path(tempfile.mkdtemp())
    for chunk in range(3):
        rows = [{"id": f"{chunk}-{i}", "content": f"x = {i}  # set x to {i}\n"} for i in range(2)]
        lines = "".join(json.dumps(row) + "\n" for row in rows)
        (root / f"part-{chunk}.jsonl").write_text(lines, encoding="utf-8")

    def start_worker():
        return ChunkedIterator(str(root / "part-*.jsonl"), comments, "demo", root / "runs")

    # Process one chunk, then stop as if the worker had been interrupted.
    for result in start_worker():
        print("first worker finished", result.chunk)
        break

    # A restarted worker skips the finished chunk and does the rest.
    iterator = start_worker()
    for result in iterator:
        print("second worker finished", result.chunk)

    print(iterator.status())
    for path in iterator.output_files():
        print(path.name, path.read_text(encoding="utf-8").splitlines())


if __name__ == "__main__":
    main()
