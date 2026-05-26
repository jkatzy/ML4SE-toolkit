# Stack v2 Comment Judge Validation Ledger

This development-only ledger records which real-corpus Stack v2 LLM judge buckets have already run for a committed comment extraction and sanitization code version. The JSON block is the source of truth for tooling; edit entries through the judge workflow whenever possible.

<!-- STACK_V2_COMMENT_JUDGE_LEDGER_START
{
  "entries": [
    {
      "case_ids": [
        "coffeescript-block-17359e6ef386d172",
        "coffeescript-block-482ff653923e3881",
        "coffeescript-block-7aee95a5a4c2008c",
        "coffeescript-block-9b697b817c9af82b",
        "coffeescript-block-9ecdd6d538a2f578",
        "coffeescript-block-df6dd44a35af1255",
        "coffeescript-block-e439c649077b41c4",
        "coffeescript-block-f16697df59988f2a",
        "coffeescript-block-f6df8fbed4a2878f",
        "coffeescript-block-fdca33d96e459c7f"
      ],
      "cases": 10,
      "code_fingerprint": "ec077eb7f98575982060a21a3cefa8a9f2fac3d900dc46104680483a7fb48b60",
      "comment_kind": "block",
      "failure_type": "",
      "git_commit": "d6c976e35d6f32b8a07bdbebd1687936fa91c302",
      "judge_model": "gpt-5.4-mini",
      "language": "coffeescript",
      "manifest": "tmp/stack_v2_comment_judge_coffeescript_500/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-05-26T09:02:42+00:00"
    },
    {
      "case_ids": [
        "coffeescript-block-17359e6ef386d172",
        "coffeescript-block-482ff653923e3881",
        "coffeescript-block-7aee95a5a4c2008c",
        "coffeescript-block-9b697b817c9af82b",
        "coffeescript-block-9ecdd6d538a2f578",
        "coffeescript-block-df6dd44a35af1255",
        "coffeescript-block-e439c649077b41c4",
        "coffeescript-block-f16697df59988f2a",
        "coffeescript-block-f6df8fbed4a2878f",
        "coffeescript-block-fdca33d96e459c7f"
      ],
      "cases": 10,
      "code_fingerprint": "a430f45c87973398e17f2a950c11ab81c3a53dd5f1e22b3550485512f823056f",
      "comment_kind": "block",
      "failure_type": "",
      "git_commit": "fc9ab5301c6d38455c6315bffa3280385f7a8798",
      "judge_model": "gpt-5.4-mini",
      "language": "coffeescript",
      "manifest": "tmp/stack_v2_comment_judge_coffeescript_500/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-05-26T09:28:37+00:00"
    },
    {
      "case_ids": [
        "coffeescript-line-0481051cf5484f20",
        "coffeescript-line-4272213270525f9f",
        "coffeescript-line-48f4c6e968ec5872",
        "coffeescript-line-5c355f721c9182dc",
        "coffeescript-line-811768a0e3ef5e86",
        "coffeescript-line-a29f8c480ec90e94",
        "coffeescript-line-bb0ac30543946d97",
        "coffeescript-line-ca4f140ec4c62ee5",
        "coffeescript-line-e292edba142a9270",
        "coffeescript-line-f95ac4e150bec1b9"
      ],
      "cases": 10,
      "code_fingerprint": "ec077eb7f98575982060a21a3cefa8a9f2fac3d900dc46104680483a7fb48b60",
      "comment_kind": "line",
      "failure_type": "",
      "git_commit": "d6c976e35d6f32b8a07bdbebd1687936fa91c302",
      "judge_model": "gpt-5.4-mini",
      "language": "coffeescript",
      "manifest": "tmp/stack_v2_comment_judge_coffeescript_500/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-05-26T09:01:00+00:00"
    },
    {
      "case_ids": [
        "coffeescript-line-0481051cf5484f20",
        "coffeescript-line-4272213270525f9f",
        "coffeescript-line-48f4c6e968ec5872",
        "coffeescript-line-5c355f721c9182dc",
        "coffeescript-line-811768a0e3ef5e86",
        "coffeescript-line-a29f8c480ec90e94",
        "coffeescript-line-bb0ac30543946d97",
        "coffeescript-line-ca4f140ec4c62ee5",
        "coffeescript-line-e292edba142a9270",
        "coffeescript-line-f95ac4e150bec1b9"
      ],
      "cases": 10,
      "code_fingerprint": "a430f45c87973398e17f2a950c11ab81c3a53dd5f1e22b3550485512f823056f",
      "comment_kind": "line",
      "failure_type": "",
      "git_commit": "fc9ab5301c6d38455c6315bffa3280385f7a8798",
      "judge_model": "gpt-5.4-mini",
      "language": "coffeescript",
      "manifest": "tmp/stack_v2_comment_judge_coffeescript_500/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-05-26T09:27:30+00:00"
    }
  ],
  "schema_version": 1
}
STACK_V2_COMMENT_JUDGE_LEDGER_END -->

## Passed Coverage

| Language | Kind | Status | Cases | Model | Commit | Fingerprint | Report | Updated |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| coffeescript | block | passed | 10 | gpt-5.4-mini | `d6c976e35d6f` | `ec077eb7f985` |  | 2026-05-26T09:02:42+00:00 |
| coffeescript | block | passed | 10 | gpt-5.4-mini | `fc9ab5301c6d` | `a430f45c8797` |  | 2026-05-26T09:28:37+00:00 |
| coffeescript | line | passed | 10 | gpt-5.4-mini | `d6c976e35d6f` | `ec077eb7f985` |  | 2026-05-26T09:01:00+00:00 |
| coffeescript | line | passed | 10 | gpt-5.4-mini | `fc9ab5301c6d` | `a430f45c8797` |  | 2026-05-26T09:27:30+00:00 |

## Failed Coverage

| Language | Kind | Status | Cases | Model | Commit | Fingerprint | Report | Updated |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| _none_ |  |  |  |  |  |  |  |  |
