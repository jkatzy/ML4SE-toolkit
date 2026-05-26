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
    },
    {
      "case_ids": [
        "forth-block-1c05f048c7f6960f",
        "forth-block-56851f1b77ce0bac",
        "forth-block-6a928c66dbe4f506",
        "forth-block-7b8c9fbd613042f4",
        "forth-block-9db0aa18f4fad411",
        "forth-block-ae4c1a13cb6e2f3a",
        "forth-block-b4e7169686576cff",
        "forth-block-d96f261df4fbf0e7",
        "forth-block-e44d3e446eaea330",
        "forth-block-f96bcc6986f94875"
      ],
      "cases": 10,
      "code_fingerprint": "a430f45c87973398e17f2a950c11ab81c3a53dd5f1e22b3550485512f823056f",
      "comment_kind": "block",
      "failure_type": "",
      "git_commit": "84de62b2af13cb5ca8ce788cfb2de65259646810",
      "judge_model": "gpt-5.4-mini",
      "language": "forth",
      "manifest": "tmp/stack_v2_comment_judge_less_known_500/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-05-26T10:04:16+00:00"
    },
    {
      "case_ids": [
        "forth-line-ce83fb3b8d1fb2ca"
      ],
      "cases": 10,
      "code_fingerprint": "a430f45c87973398e17f2a950c11ab81c3a53dd5f1e22b3550485512f823056f",
      "comment_kind": "line",
      "failure_type": "extraction",
      "git_commit": "84de62b2af13cb5ca8ce788cfb2de65259646810",
      "judge_model": "gpt-5.4-mini",
      "language": "forth",
      "manifest": "tmp/stack_v2_comment_judge_less_known_500/manifest.jsonl",
      "rationale": "The extracted raw comment is not the sampled standalone backslash comment; it absorbs additional source text, and the cleaned output incorrectly preserves the comment syntax instead of returning an empty string.",
      "report": "tmp/stack_v2_comment_judge_less_known_500/reports/forth-line-ce83fb3b8d1fb2ca-forth-line-extraction-6570f987.md",
      "status": "failed",
      "updated_at": "2026-05-26T10:02:51+00:00"
    },
    {
      "case_ids": [
        "haskell-line-22b13e1f340510d9",
        "haskell-line-2a4eb687493ff97a",
        "haskell-line-38ce4851bca81d5e",
        "haskell-line-46f27a62307c021b",
        "haskell-line-56caba1b3cdbe7eb",
        "haskell-line-87255a5510328a64",
        "haskell-line-91a91f39ef4b9f74",
        "haskell-line-b9c12b34b03c22ea",
        "haskell-line-da4324c8ad03c652",
        "haskell-line-e7af8a3737f2be86"
      ],
      "cases": 10,
      "code_fingerprint": "a430f45c87973398e17f2a950c11ab81c3a53dd5f1e22b3550485512f823056f",
      "comment_kind": "line",
      "failure_type": "",
      "git_commit": "84de62b2af13cb5ca8ce788cfb2de65259646810",
      "judge_model": "gpt-5.4-mini",
      "language": "haskell",
      "manifest": "tmp/stack_v2_comment_judge_less_known_500/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-05-26T10:00:40+00:00"
    },
    {
      "case_ids": [
        "haskell-nested-2397807d3c794ca2",
        "haskell-nested-70c42c5f3948ea5a",
        "haskell-nested-71cee9896e3b4252",
        "haskell-nested-80f457008cbf1b96",
        "haskell-nested-965de0402473031b",
        "haskell-nested-96c553de69db4d87",
        "haskell-nested-ae97f74ccc20a22a",
        "haskell-nested-b5849a0fd90ece32",
        "haskell-nested-d12644b377252ebc",
        "haskell-nested-e112dcfb08e442b1"
      ],
      "cases": 10,
      "code_fingerprint": "a430f45c87973398e17f2a950c11ab81c3a53dd5f1e22b3550485512f823056f",
      "comment_kind": "nested",
      "failure_type": "",
      "git_commit": "84de62b2af13cb5ca8ce788cfb2de65259646810",
      "judge_model": "gpt-5.4-mini",
      "language": "haskell",
      "manifest": "tmp/stack_v2_comment_judge_less_known_500/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-05-26T10:01:49+00:00"
    },
    {
      "case_ids": [
        "julia-line-42ab9ac760f76d4c",
        "julia-line-480f272591628d79",
        "julia-line-6d028044f97e28b3",
        "julia-line-7b250f83a519b65e",
        "julia-line-8237aa019e795413",
        "julia-line-97964882bbf07f50",
        "julia-line-9d64ed5421117a84",
        "julia-line-a05e8ced4aa1d1ed",
        "julia-line-a70975941a340f48",
        "julia-line-cdb4661ee9e0833a"
      ],
      "cases": 10,
      "code_fingerprint": "a430f45c87973398e17f2a950c11ab81c3a53dd5f1e22b3550485512f823056f",
      "comment_kind": "line",
      "failure_type": "",
      "git_commit": "84de62b2af13cb5ca8ce788cfb2de65259646810",
      "judge_model": "gpt-5.4-mini",
      "language": "julia",
      "manifest": "tmp/stack_v2_comment_judge_less_known_500/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-05-26T09:58:11+00:00"
    },
    {
      "case_ids": [
        "julia-nested-3b057e50c61620e3",
        "julia-nested-5b1910d59d901419",
        "julia-nested-6eec1cd9b56888cd",
        "julia-nested-76a27759bc627cf6",
        "julia-nested-83332a73b2529950",
        "julia-nested-abed76dc4b032ada",
        "julia-nested-b21f62b8a1dbd6cf",
        "julia-nested-bdb1d0cd6f964354",
        "julia-nested-c90afa751d11a20a",
        "julia-nested-e11534d80d7e0eaa"
      ],
      "cases": 10,
      "code_fingerprint": "a430f45c87973398e17f2a950c11ab81c3a53dd5f1e22b3550485512f823056f",
      "comment_kind": "nested",
      "failure_type": "",
      "git_commit": "84de62b2af13cb5ca8ce788cfb2de65259646810",
      "judge_model": "gpt-5.4-mini",
      "language": "julia",
      "manifest": "tmp/stack_v2_comment_judge_less_known_500/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-05-26T09:59:14+00:00"
    },
    {
      "case_ids": [
        "mathematica-nested-09e49b55b24e72eb",
        "mathematica-nested-0e76e1e184594796",
        "mathematica-nested-28823f4ca56a37c8",
        "mathematica-nested-3248c6016956a958",
        "mathematica-nested-39875d95fadc86ea",
        "mathematica-nested-3a45432dd95bb637",
        "mathematica-nested-6be95217b086b931",
        "mathematica-nested-c3f3415c58687568",
        "mathematica-nested-d7c30a85561883d1",
        "mathematica-nested-f5074af42bda75ab"
      ],
      "cases": 10,
      "code_fingerprint": "a430f45c87973398e17f2a950c11ab81c3a53dd5f1e22b3550485512f823056f",
      "comment_kind": "nested",
      "failure_type": "",
      "git_commit": "84de62b2af13cb5ca8ce788cfb2de65259646810",
      "judge_model": "gpt-5.4-mini",
      "language": "mathematica",
      "manifest": "tmp/stack_v2_comment_judge_less_known_500/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-05-26T10:05:36+00:00"
    },
    {
      "case_ids": [
        "nim-line-14d09557691df3a6",
        "nim-line-210a2aac9045a71b",
        "nim-line-21a78f69fd0dbeef",
        "nim-line-4553e8d4427f0b28",
        "nim-line-5b23ee242a8d67fa",
        "nim-line-6e5f1d49c4cdaadb",
        "nim-line-6f825dfde1c6a2d7",
        "nim-line-b910c8011d589e33",
        "nim-line-be7bfafa048646f9",
        "nim-line-e093f6a139f2090a"
      ],
      "cases": 10,
      "code_fingerprint": "a430f45c87973398e17f2a950c11ab81c3a53dd5f1e22b3550485512f823056f",
      "comment_kind": "line",
      "failure_type": "",
      "git_commit": "84de62b2af13cb5ca8ce788cfb2de65259646810",
      "judge_model": "gpt-5.4-mini",
      "language": "nim",
      "manifest": "tmp/stack_v2_comment_judge_less_known_500/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-05-26T09:54:04+00:00"
    },
    {
      "case_ids": [
        "nim-nested-19343231cf04c878",
        "nim-nested-364bc495ed34935a",
        "nim-nested-3ee808a87647fc70",
        "nim-nested-52fedabc50fb54b5",
        "nim-nested-6869c30fd78ed4bd",
        "nim-nested-726ec0d40dae0d7f",
        "nim-nested-750624e1e32b5be4",
        "nim-nested-75f83c6a47a8f2f2",
        "nim-nested-cf27800025c728e2",
        "nim-nested-e19b61514e9e36c9"
      ],
      "cases": 10,
      "code_fingerprint": "a430f45c87973398e17f2a950c11ab81c3a53dd5f1e22b3550485512f823056f",
      "comment_kind": "nested",
      "failure_type": "",
      "git_commit": "84de62b2af13cb5ca8ce788cfb2de65259646810",
      "judge_model": "gpt-5.4-mini",
      "language": "nim",
      "manifest": "tmp/stack_v2_comment_judge_less_known_500/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-05-26T09:55:13+00:00"
    },
    {
      "case_ids": [],
      "cases": 1,
      "code_fingerprint": "a430f45c87973398e17f2a950c11ab81c3a53dd5f1e22b3550485512f823056f",
      "comment_kind": "block",
      "failure_type": "manifest_generation",
      "git_commit": "84de62b2af13cb5ca8ce788cfb2de65259646810",
      "judge_model": "manifest-generator",
      "language": "raku",
      "manifest": "tmp/stack_v2_comment_judge_less_known_500/manifest.jsonl",
      "rationale": "Only found 1/10 block comment case(s) for raku after scanning 500 record(s).",
      "report": "tmp/stack_v2_comment_judge_less_known_500/reports/manifest-raku-block-manifest_generation-33917390.md",
      "status": "failed",
      "updated_at": "2026-05-26T09:52:49+00:00"
    },
    {
      "case_ids": [],
      "cases": 1,
      "code_fingerprint": "3c1b3dc4e34b1b3d25d9471ea4183eda028e135c28192720c8ef00933f6b3f4f",
      "comment_kind": "block",
      "failure_type": "manifest_generation",
      "git_commit": "8fe681219afadf26cf3c52ea1ec6788151dd9e8e",
      "judge_model": "manifest-generator",
      "language": "raku",
      "manifest": "tmp/stack_v2_comment_judge_raku_forth_fix/manifest.jsonl",
      "rationale": "Only found 1/10 block comment case(s) for raku after scanning 500 record(s).",
      "report": "tmp/stack_v2_comment_judge_raku_forth_fix/reports/manifest-raku-block-manifest_generation-33917390.md",
      "status": "failed",
      "updated_at": "2026-05-26T11:22:12+00:00"
    },
    {
      "case_ids": [
        "raku-line-38ec331a469cb043",
        "raku-line-55383897eca7895d",
        "raku-line-55e9074c7c07ecbd",
        "raku-line-63de5a54bfb75c84",
        "raku-line-964e0215882485f1",
        "raku-line-9eb683429726c060",
        "raku-line-a673064d4753e5f3",
        "raku-line-bf4e431e940d7486",
        "raku-line-eb1dc1bf222f83a8",
        "raku-line-f488f4874683e251"
      ],
      "cases": 10,
      "code_fingerprint": "a430f45c87973398e17f2a950c11ab81c3a53dd5f1e22b3550485512f823056f",
      "comment_kind": "line",
      "failure_type": "",
      "git_commit": "84de62b2af13cb5ca8ce788cfb2de65259646810",
      "judge_model": "gpt-5.4-mini",
      "language": "raku",
      "manifest": "tmp/stack_v2_comment_judge_less_known_500/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-05-26T09:57:13+00:00"
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
| forth | block | passed | 10 | gpt-5.4-mini | `84de62b2af13` | `a430f45c8797` |  | 2026-05-26T10:04:16+00:00 |
| haskell | line | passed | 10 | gpt-5.4-mini | `84de62b2af13` | `a430f45c8797` |  | 2026-05-26T10:00:40+00:00 |
| haskell | nested | passed | 10 | gpt-5.4-mini | `84de62b2af13` | `a430f45c8797` |  | 2026-05-26T10:01:49+00:00 |
| julia | line | passed | 10 | gpt-5.4-mini | `84de62b2af13` | `a430f45c8797` |  | 2026-05-26T09:58:11+00:00 |
| julia | nested | passed | 10 | gpt-5.4-mini | `84de62b2af13` | `a430f45c8797` |  | 2026-05-26T09:59:14+00:00 |
| mathematica | nested | passed | 10 | gpt-5.4-mini | `84de62b2af13` | `a430f45c8797` |  | 2026-05-26T10:05:36+00:00 |
| nim | line | passed | 10 | gpt-5.4-mini | `84de62b2af13` | `a430f45c8797` |  | 2026-05-26T09:54:04+00:00 |
| nim | nested | passed | 10 | gpt-5.4-mini | `84de62b2af13` | `a430f45c8797` |  | 2026-05-26T09:55:13+00:00 |
| raku | line | passed | 10 | gpt-5.4-mini | `84de62b2af13` | `a430f45c8797` |  | 2026-05-26T09:57:13+00:00 |

## Failed Coverage

| Language | Kind | Status | Cases | Model | Commit | Fingerprint | Report | Updated |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| forth | line | failed | 10 | gpt-5.4-mini | `84de62b2af13` | `a430f45c8797` | [forth-line-ce83fb3b8d1fb2ca-forth-line-extraction-6570f987.md](tmp/stack_v2_comment_judge_less_known_500/reports/forth-line-ce83fb3b8d1fb2ca-forth-line-extraction-6570f987.md) | 2026-05-26T10:02:51+00:00 |
| raku | block | failed | 1 | manifest-generator | `84de62b2af13` | `a430f45c8797` | [manifest-raku-block-manifest_generation-33917390.md](tmp/stack_v2_comment_judge_less_known_500/reports/manifest-raku-block-manifest_generation-33917390.md) | 2026-05-26T09:52:49+00:00 |
| raku | block | failed | 1 | manifest-generator | `8fe681219afa` | `3c1b3dc4e34b` | [manifest-raku-block-manifest_generation-33917390.md](tmp/stack_v2_comment_judge_raku_forth_fix/reports/manifest-raku-block-manifest_generation-33917390.md) | 2026-05-26T11:22:12+00:00 |
