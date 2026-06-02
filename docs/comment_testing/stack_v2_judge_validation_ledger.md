# Stack v2 Comment Judge Validation Ledger

This development-only ledger records which real-corpus Stack v2 LLM judge buckets have already run for a committed comment extraction and sanitization code version. The JSON block is the source of truth for tooling; edit entries through the judge workflow whenever possible.

<!-- STACK_V2_COMMENT_JUDGE_LEDGER_START
{
  "entries": [
    {
      "case_ids": [
        "ada-line-2f38ee9633ece9b5",
        "ada-line-5862350576cba12c",
        "ada-line-b10f63834ce7be75",
        "ada-line-e5f5d985968cc0da",
        "ada-line-ee7adf03ecbd1dc6"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "ada",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T14:28:08+00:00"
    },
    {
      "case_ids": [
        "agda-line-15b97faee34f4277",
        "agda-line-49e08e1c96b3ea6a",
        "agda-line-667d864755c1f98d",
        "agda-line-a1812f479784b164",
        "agda-line-eae575bca07263ed"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "agda",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T14:29:43+00:00"
    },
    {
      "case_ids": [
        "agda-nested-03faa6dcc370e48b",
        "agda-nested-2f7fb9dc70711dfb",
        "agda-nested-6650e5c492cf1da8",
        "agda-nested-7e36ffdc16f09ede",
        "agda-nested-b6a3c7614f819f58"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "nested",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "agda",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T14:31:00+00:00"
    },
    {
      "case_ids": [
        "ampl-block-1e473f612e34fba2",
        "ampl-block-a5356e3a01a0d98b",
        "ampl-block-a80acb0512e64931"
      ],
      "cases": 3,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "block",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "ampl",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T14:21:58+00:00"
    },
    {
      "case_ids": [
        "ampl-line-a09c059c9b9b91dc",
        "ampl-line-a7a8fa814a0eb779",
        "ampl-line-c64db495a8b8a77a",
        "ampl-line-d6fb0b519817dfd0",
        "ampl-line-ee4099dc2d8a814d"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "ampl",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T14:19:16+00:00"
    },
    {
      "case_ids": [
        "antlers-block-4433910e9c24e892",
        "antlers-block-50f6465ecee682d0",
        "antlers-block-64c9bcf28ff3587e",
        "antlers-block-88b0065507f76ac6",
        "antlers-block-be8eeacaf9923a1d"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "block",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "antlers",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T16:10:47+00:00"
    },
    {
      "case_ids": [
        "applescript-line-18aa6b0bc4d10010",
        "applescript-line-231d10f93453be6a",
        "applescript-line-786d8eac879a84a0",
        "applescript-line-dce8cff283acade4",
        "applescript-line-f60c1600b063db85"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "applescript",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T15:50:57+00:00"
    },
    {
      "case_ids": [
        "applescript-nested-6a68aed98d1faa39",
        "applescript-nested-82a54226045c54c7",
        "applescript-nested-8c33d7f4cd882482",
        "applescript-nested-926d606f95cc1deb",
        "applescript-nested-aac72218ae063ad6"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "nested",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "applescript",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T15:52:47+00:00"
    },
    {
      "case_ids": [
        "assembly-line-541f69482a2f9304",
        "assembly-line-7f13c78f3559268e",
        "assembly-line-a74efe8398bf13c2",
        "assembly-line-c6a94c53f11ba070",
        "assembly-line-c72a97433b805ce2"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "assembly",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T14:32:35+00:00"
    },
    {
      "case_ids": [
        "autohotkey-block-25f0ffa547aa2fc3",
        "autohotkey-block-2fd9e44d172a456f",
        "autohotkey-block-5fd9b2ec933ea54b",
        "autohotkey-block-9f0768b2dadf324b",
        "autohotkey-block-fe3493d608e66bbc"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "block",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "autohotkey",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T15:43:29+00:00"
    },
    {
      "case_ids": [
        "autohotkey-line-09df99f2c2ac27f4"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "extraction",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "autohotkey",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "The parser has incorrectly extracted a massive block of executable source code as part of a single comment. In AutoHotkey, ';' is a line comment delimiter; it should only extract the text from the semicolon to the end of the line. The actual output includes dozens of lines of code (e.g., 'CapsLock & F1:: Return') that are not comments.",
      "report": "tmp/stack_v2_comment_judge/reports/autohotkey-line-09df99f2c2ac27f4-autohotkey-line-extraction-43195474.md",
      "status": "failed",
      "updated_at": "2026-06-01T15:40:41+00:00"
    },
    {
      "case_ids": [
        "autoit-block-a9f015b2e27d4208"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "block",
      "failure_type": "sanitation",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "autoit",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "The sampled raw comment and the actual extracted raw comment differ in the number of dashes in the header line, indicating a mismatch in the source data provided to the judge. However, focusing on the cleaning process: the cleaned comment preserves the decorative dash gutter/header, which should be removed according to the instructions ('removes only comment syntax scaffolding, decorative gutters...').",
      "report": "tmp/stack_v2_comment_judge/reports/autoit-block-a9f015b2e27d4208-autoit-block-sanitation-61d4e931.md",
      "status": "failed",
      "updated_at": "2026-06-01T15:47:46+00:00"
    },
    {
      "case_ids": [
        "autoit-line-063c58fc5737bd85",
        "autoit-line-1e469f832b78103a",
        "autoit-line-26e167eb820510dd",
        "autoit-line-91ba71b04459ae90",
        "autoit-line-e42966fc14eb9e1b"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "autoit",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T15:44:31+00:00"
    },
    {
      "case_ids": [
        "batchfile-line-8b32a688fe90f6d9",
        "batchfile-line-91a7cfada4499f3c",
        "batchfile-line-a1e6dea0dd419927",
        "batchfile-line-e11f1044f786b466",
        "batchfile-line-ef085743ea409b4b"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "batchfile",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T15:32:37+00:00"
    },
    {
      "case_ids": [
        "blade-block-254eee632b2bce70",
        "blade-block-55966e1f7c02a2f7",
        "blade-block-cd3f3e23b48a9258",
        "blade-block-dc2dce08e7d9ffd7",
        "blade-block-e53f30d444040c2e"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "block",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "blade",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T16:13:01+00:00"
    },
    {
      "case_ids": [
        "cmake-line-4a4380c7e47ed330"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "sanitation",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "cmake",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "The cleaned comment preserves a large block of decorative hash characters, which should be removed as decorative gutters/scaffolding according to the cleaning criteria.",
      "report": "tmp/stack_v2_comment_judge/reports/cmake-line-4a4380c7e47ed330-cmake-line-sanitation-adfa732e.md",
      "status": "failed",
      "updated_at": "2026-06-01T16:09:09+00:00"
    },
    {
      "case_ids": [
        "cmake-nested-a0c7aa64a08f8dbc"
      ],
      "cases": 1,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "nested",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "cmake",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T16:09:32+00:00"
    },
    {
      "case_ids": [
        "cobol-line-d428778855caa91f"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "judge_command",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "cobol",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "judge command failed with exit code 1",
      "report": "tmp/stack_v2_comment_judge/reports/cobol-line-d428778855caa91f-cobol-line-judge_command-cd269bdf.md",
      "status": "failed",
      "updated_at": "2026-06-01T14:41:00+00:00"
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
        "coq-nested-12ea7d139c02e287",
        "coq-nested-68c2d0f6c6942c94",
        "coq-nested-8fad0fcc2d7eaf36",
        "coq-nested-cc1db5bf437a5038",
        "coq-nested-e12dea7577a10a07"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "nested",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "coq",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T14:42:08+00:00"
    },
    {
      "case_ids": [
        "css-block-0cd6db928431f566",
        "css-block-1cae6e3a2addf690",
        "css-block-419c53d5f4c39939",
        "css-block-d442b0a33a7f1bdc",
        "css-block-e345e63a38ed4cf2"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "block",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "css",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T14:18:24+00:00"
    },
    {
      "case_ids": [
        "d-block-0e5cabc335f730a0",
        "d-block-4893acbbd5179cfc",
        "d-block-7ecc2d611d4da627",
        "d-block-9c75fc3d693b4acf",
        "d-block-f2fa32e87529f7d3"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "block",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "d",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T14:44:23+00:00"
    },
    {
      "case_ids": [
        "d-line-695baf7d4001e436"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "extraction",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "d",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "The extracted raw comment contains a typo in the delimiter ('/ //' instead of '///'), which does not match the sampled raw comment.",
      "report": "tmp/stack_v2_comment_judge/reports/d-line-695baf7d4001e436-d-line-extraction-49334352.md",
      "status": "failed",
      "updated_at": "2026-06-01T14:42:42+00:00"
    },
    {
      "case_ids": [
        "dockerfile-line-0612b0e63741c474",
        "dockerfile-line-0f62c5eeae3523ec",
        "dockerfile-line-2a7745982db78e06",
        "dockerfile-line-44ddd22c4417f174",
        "dockerfile-line-f251feb42a10a8a2"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "dockerfile",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T14:17:29+00:00"
    },
    {
      "case_ids": [
        "e_mail-nested-438da2fb63bd7494",
        "e_mail-nested-87ce34d12da48e0b",
        "e_mail-nested-91fff8eb6e543ce0",
        "e_mail-nested-a0aac0036d86b611",
        "e_mail-nested-f4cbdd5d78509a25"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "nested",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "e_mail",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T16:08:29+00:00"
    },
    {
      "case_ids": [
        "editorconfig-line-1fea8d2f2be0a551",
        "editorconfig-line-45493a57f12fd129",
        "editorconfig-line-68fbd0cf662097e3",
        "editorconfig-line-73b1d65eee741a0b",
        "editorconfig-line-95c49112495c8d27"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "editorconfig",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T15:34:49+00:00"
    },
    {
      "case_ids": [
        "ejs-block-027f955302abad01",
        "ejs-block-061a23099ab9a20f",
        "ejs-block-7063a3bb2aa5c252",
        "ejs-block-95fdb3987cd38346",
        "ejs-block-a867a9231358b331"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "block",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "ejs",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T16:14:02+00:00"
    },
    {
      "case_ids": [
        "erlang-line-d377a7a07c46ba63"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "extraction",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "erlang",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "The extracted raw comment differs from the sampled raw comment (different dash patterns/lengths), and the cleaned comment fails to remove the decorative gutter/border lines, which should be removed according to the cleaning rules.",
      "report": "tmp/stack_v2_comment_judge/reports/erlang-line-d377a7a07c46ba63-erlang-line-extraction-c4d10ed3.md",
      "status": "failed",
      "updated_at": "2026-06-01T14:52:54+00:00"
    },
    {
      "case_ids": [
        "f-line-2dc31d1f987f8240",
        "f-line-2df12a9adb3067f3",
        "f-line-392bac180db43614",
        "f-line-60813fbb264a55ff",
        "f-line-6c32f026f9afcf5a"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "f#",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T14:54:23+00:00"
    },
    {
      "case_ids": [
        "f-nested-00bdd9d244221610",
        "f-nested-0cf7b8a1c55daa5a",
        "f-nested-1416792a8946f19a",
        "f-nested-3b26c5e3a0f6ce02",
        "f-nested-63c5a67d545ffa56"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "nested",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "f#",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T14:55:23+00:00"
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
        "forth-block-1c05f048c7f6960f",
        "forth-block-4fe9efaa57419499",
        "forth-block-56851f1b77ce0bac",
        "forth-block-6a928c66dbe4f506",
        "forth-block-7b8c9fbd613042f4",
        "forth-block-9db0aa18f4fad411",
        "forth-block-ae4c1a13cb6e2f3a",
        "forth-block-b4e7169686576cff",
        "forth-block-d96f261df4fbf0e7",
        "forth-block-f96bcc6986f94875"
      ],
      "cases": 10,
      "code_fingerprint": "3c1b3dc4e34b1b3d25d9471ea4183eda028e135c28192720c8ef00933f6b3f4f",
      "comment_kind": "block",
      "failure_type": "",
      "git_commit": "052d2e20a11ee561aff276ed6c47c8cbf9548715",
      "judge_model": "gpt-5.4-mini",
      "language": "forth",
      "manifest": "tmp/stack_v2_comment_judge_raku_forth_fix/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-05-26T12:20:43+00:00"
    },
    {
      "case_ids": [
        "forth-block-1c05f048c7f6960f",
        "forth-block-4fe9efaa57419499",
        "forth-block-56851f1b77ce0bac",
        "forth-block-6a928c66dbe4f506",
        "forth-block-7b8c9fbd613042f4",
        "forth-block-9db0aa18f4fad411",
        "forth-block-ae4c1a13cb6e2f3a",
        "forth-block-b4e7169686576cff",
        "forth-block-d96f261df4fbf0e7",
        "forth-block-f96bcc6986f94875"
      ],
      "cases": 10,
      "code_fingerprint": "e7950d34cf30a02a9ce8d447048815125bd45534763686935461e37a8f3a34a6",
      "comment_kind": "block",
      "failure_type": "",
      "git_commit": "1a3eca563cecbdac23f6e7fa97a9b6fa07bf1c03",
      "judge_model": "gpt-5.4-mini",
      "language": "forth",
      "manifest": "tmp/stack_v2_comment_judge_raku_forth_fix/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-05-26T13:53:37+00:00"
    },
    {
      "case_ids": [
        "forth-block-1c05f048c7f6960f",
        "forth-block-56851f1b77ce0bac",
        "forth-block-6a928c66dbe4f506",
        "forth-block-7b8c9fbd613042f4",
        "forth-block-f96bcc6986f94875"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "block",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "forth",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T14:57:30+00:00"
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
        "forth-line-ce83fb3b8d1fb2ca"
      ],
      "cases": 10,
      "code_fingerprint": "3c1b3dc4e34b1b3d25d9471ea4183eda028e135c28192720c8ef00933f6b3f4f",
      "comment_kind": "line",
      "failure_type": "extraction",
      "git_commit": "052d2e20a11ee561aff276ed6c47c8cbf9548715",
      "judge_model": "gpt-5.4-mini",
      "language": "forth",
      "manifest": "tmp/stack_v2_comment_judge_raku_forth_fix/manifest.jsonl",
      "rationale": "The raw comment is missing the sampled trailing carriage return, so extraction is not an exact match; the cleaned comment matches the expected empty string.",
      "report": "tmp/stack_v2_comment_judge_raku_forth_fix/reports/forth-line-ce83fb3b8d1fb2ca-forth-line-extraction-6570f987.md",
      "status": "failed",
      "updated_at": "2026-05-26T12:19:29+00:00"
    },
    {
      "case_ids": [
        "forth-line-20d57babac5d01b5",
        "forth-line-363ac4279c697770",
        "forth-line-7da007a36d6ab8f9",
        "forth-line-8479f1e2976c8b5a",
        "forth-line-aa17df9c781b537f",
        "forth-line-b605539e7b725776",
        "forth-line-bc9c8b9ea3a2f1d2",
        "forth-line-bcc7006650ded0a8",
        "forth-line-ce83fb3b8d1fb2ca",
        "forth-line-e1507099f124996a"
      ],
      "cases": 10,
      "code_fingerprint": "e7950d34cf30a02a9ce8d447048815125bd45534763686935461e37a8f3a34a6",
      "comment_kind": "line",
      "failure_type": "",
      "git_commit": "1a3eca563cecbdac23f6e7fa97a9b6fa07bf1c03",
      "judge_model": "gpt-5.4-mini",
      "language": "forth",
      "manifest": "tmp/stack_v2_comment_judge_raku_forth_fix/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-05-26T13:52:36+00:00"
    },
    {
      "case_ids": [
        "forth-line-7da007a36d6ab8f9",
        "forth-line-aa17df9c781b537f",
        "forth-line-b605539e7b725776",
        "forth-line-bc9c8b9ea3a2f1d2",
        "forth-line-bcc7006650ded0a8"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "forth",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T14:56:30+00:00"
    },
    {
      "case_ids": [
        "fortran-line-5d4096b01df90d1e"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "extraction",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "fortran",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "The actual extracted raw comment differs from the sampled raw comment in the distribution of dashes in the header lines (lines 1 and 3), indicating a failure in raw extraction accuracy.",
      "report": "tmp/stack_v2_comment_judge/reports/fortran-line-5d4096b01df90d1e-fortran-line-extraction-77e7d085.md",
      "status": "failed",
      "updated_at": "2026-06-01T14:59:12+00:00"
    },
    {
      "case_ids": [
        "freebasic-block-1b91a5c028c83577",
        "freebasic-block-78d0af76dc6d204f",
        "freebasic-block-96c5ec6487cc5e25",
        "freebasic-block-bfc2fc633900d57d",
        "freebasic-block-e5926a7b8d092087"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "block",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "freebasic",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T16:03:26+00:00"
    },
    {
      "case_ids": [
        "freebasic-line-0139b31bf2164fd9",
        "freebasic-line-01f15d6095b10e87",
        "freebasic-line-1e6739fd7777f204",
        "freebasic-line-2d1cb45c4b4f2b3e",
        "freebasic-line-8ad3839cc967180d"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "freebasic",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T16:01:35+00:00"
    },
    {
      "case_ids": [
        "freemarker-block-040df8949b9d5924",
        "freemarker-block-53a7352adb8e066b",
        "freemarker-block-6173bd5893189f08",
        "freemarker-block-676d3fd094c2020c",
        "freemarker-block-f2f35d7f1a096f81"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "block",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "freemarker",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T16:17:00+00:00"
    },
    {
      "case_ids": [
        "git_config-line-03c9667e384cb4b8",
        "git_config-line-450cbb4d324f6e28",
        "git_config-line-5c4ca36ec2d02240",
        "git_config-line-5dbf3ae16832edcf",
        "git_config-line-fa2194423e041a25"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "git_config",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T15:35:51+00:00"
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
        "html-block-4a602add2ec84d7b",
        "html-block-5d0e7baf952261a6",
        "html-block-b2d61e64e53491de",
        "html-block-ba90ce8e7a5cfcd0",
        "html-block-d7143693d3754101"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "block",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "html",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T15:02:29+00:00"
    },
    {
      "case_ids": [
        "java-block-70ffc9894f18a01e",
        "java-block-7c27e65575fef29d",
        "java-block-92d431cca1e5a6d3",
        "java-block-a09e6c24cf452618",
        "java-block-d94e5579c8d74057"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "block",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "java",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T14:16:39+00:00"
    },
    {
      "case_ids": [
        "java-line-002d34c7bdd945a1",
        "java-line-0a94003a6a42c040",
        "java-line-19d748708879ddde",
        "java-line-b50d40731ad02b4d",
        "java-line-ddb7881fde344a72"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "java",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T14:15:03+00:00"
    },
    {
      "case_ids": [
        "java_properties-line-807704924180f31a"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "judge_command",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "java_properties",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "judge command failed with exit code 1",
      "report": "tmp/stack_v2_comment_judge/reports/java_properties-line-807704924180f31a-java_properties-line-judge_command-98f0f87d.md",
      "status": "failed",
      "updated_at": "2026-06-01T15:39:25+00:00"
    },
    {
      "case_ids": [
        "jsonnet-block-00f5a39dbfdf519b",
        "jsonnet-block-313bf815d096ee0e",
        "jsonnet-block-41cf8b1f8004afd9",
        "jsonnet-block-954f9c2d80730dbe",
        "jsonnet-block-f7b39692b9da5526"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "block",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "jsonnet",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T16:05:36+00:00"
    },
    {
      "case_ids": [
        "jsonnet-line-964fe9b53dc103d7",
        "jsonnet-line-9fecfaf3f7035c2e",
        "jsonnet-line-b0c0f659ff7cd5a6",
        "jsonnet-line-d5cc8ada460c5ad4",
        "jsonnet-line-e047f4ba3f70b141"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "jsonnet",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T16:04:31+00:00"
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
        "julia-line-42ab9ac760f76d4c",
        "julia-line-6d028044f97e28b3",
        "julia-line-7b250f83a519b65e",
        "julia-line-8237aa019e795413",
        "julia-line-9d64ed5421117a84"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "julia",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T15:00:05+00:00"
    },
    {
      "case_ids": [
        "julia-nested-5b1910d59d901419"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "nested",
      "failure_type": "sanitation",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "julia",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "The cleaned comment contains a trailing '#' character, which is part of the comment syntax scaffolding/delimiter and should have been removed during cleaning.",
      "report": "tmp/stack_v2_comment_judge/reports/julia-nested-5b1910d59d901419-julia-nested-sanitation-477d0198.md",
      "status": "failed",
      "updated_at": "2026-06-01T15:01:33+00:00"
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
        "lua-block-5c53f090f50ebfbc",
        "lua-block-7933125e00209098",
        "lua-block-91f23ef127dd5c1a",
        "lua-block-c8e08f5f1f6082a3",
        "lua-block-d5c302c36e704f3a"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "block",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "lua",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T15:06:14+00:00"
    },
    {
      "case_ids": [
        "lua-line-a2ff8eca29a389c8"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "extraction",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "lua",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "The actual extracted raw comment differs from the sampled raw comment (different number of leading/trailing dashes), and the cleaned comment also differs from the expected cleaned comment.",
      "report": "tmp/stack_v2_comment_judge/reports/lua-line-a2ff8eca29a389c8-lua-line-extraction-70b7851f.md",
      "status": "failed",
      "updated_at": "2026-06-01T15:04:43+00:00"
    },
    {
      "case_ids": [
        "mathematica-nested-3248c6016956a958"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "nested",
      "failure_type": "extraction",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "mathematica",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "The actual extracted comments do not match the sampled raw comment content. The sampled raw comment has 80 asterisks, while the actual extracted comments have different counts of asterisks.",
      "report": "tmp/stack_v2_comment_judge/reports/mathematica-nested-3248c6016956a958-mathematica-nested-extraction-23f9eabc.md",
      "status": "failed",
      "updated_at": "2026-06-01T15:06:58+00:00"
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
        "matlab-block-1da5f23428e0bdd7",
        "matlab-block-4e5a29eb4f87ae4b",
        "matlab-block-73b8f0ecdfed8567",
        "matlab-block-80dd25eeaa22f6f1",
        "matlab-block-aba57f550d7add18"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "block",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "matlab",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T15:10:05+00:00"
    },
    {
      "case_ids": [
        "matlab-line-110098629111a5f9",
        "matlab-line-6460634f002c406c",
        "matlab-line-c0cd3d4766aab623",
        "matlab-line-ef442d6c5404e345",
        "matlab-line-f79d2437f511259a"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "matlab",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T15:08:35+00:00"
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
        "nim-line-210a2aac9045a71b",
        "nim-line-4553e8d4427f0b28",
        "nim-line-6f825dfde1c6a2d7",
        "nim-line-b910c8011d589e33",
        "nim-line-be7bfafa048646f9"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "nim",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T15:56:37+00:00"
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
      "case_ids": [
        "nim-nested-364bc495ed34935a",
        "nim-nested-3ee808a87647fc70",
        "nim-nested-6869c30fd78ed4bd",
        "nim-nested-cf27800025c728e2",
        "nim-nested-e19b61514e9e36c9"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "nested",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "nim",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T15:58:33+00:00"
    },
    {
      "case_ids": [
        "nsis-block-0e8bd06b46192018",
        "nsis-block-674009874a72be64",
        "nsis-block-ac3a282bf5857fa3",
        "nsis-block-f88d3de343f03edc",
        "nsis-block-fa0341a9efe767fb"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "block",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "nsis",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T15:50:03+00:00"
    },
    {
      "case_ids": [
        "nsis-line-165c027a508aa40e",
        "nsis-line-2aa19458f5561cc9",
        "nsis-line-43e2afc885b9b88f",
        "nsis-line-7d681f7d1332a77d",
        "nsis-line-a818c998478c5f16"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "nsis",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T15:48:49+00:00"
    },
    {
      "case_ids": [
        "pascal-block-2f9135e5e95a6991"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "block",
      "failure_type": "sanitation",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "pascal",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "The cleaned_comment in the actual output differs significantly in the number of asterisks in the decorative gutters compared to the sampled_cleaned_comment, indicating an inconsistent or incorrect cleaning process for the decorative borders.",
      "report": "tmp/stack_v2_comment_judge/reports/pascal-block-2f9135e5e95a6991-pascal-block-sanitation-9d073262.md",
      "status": "failed",
      "updated_at": "2026-06-01T14:48:53+00:00"
    },
    {
      "case_ids": [
        "pascal-line-dbf2d3aed438e1ac"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "sanitation",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "pascal",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "The cleaned comment in the actual output differs from the sampled expected cleaned comment in the number of hash characters in the first and last lines, and the fourth line's trailing hashes also differ.",
      "report": "tmp/stack_v2_comment_judge/reports/pascal-line-dbf2d3aed438e1ac-pascal-line-sanitation-f657c720.md",
      "status": "failed",
      "updated_at": "2026-06-01T14:45:51+00:00"
    },
    {
      "case_ids": [
        "pascal-nested-427307de52131b12",
        "pascal-nested-479055a84a47ce68",
        "pascal-nested-904bb39088e95e1c",
        "pascal-nested-bf84127451f559df",
        "pascal-nested-ea91009a21b3ce2f"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "nested",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "pascal",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T14:52:14+00:00"
    },
    {
      "case_ids": [
        "perl-block-07725327bb7ded5c",
        "perl-block-0ea8d92b18d35a69",
        "perl-block-86a282199ca6840b",
        "perl-block-c5f52a84bb5eb3db",
        "perl-block-d09b69672d171b50"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "block",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "perl",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T15:14:57+00:00"
    },
    {
      "case_ids": [
        "perl-line-2e0ac65ffbe158ff",
        "perl-line-37a5408552335230",
        "perl-line-4fabd792109ada53",
        "perl-line-51d61a34d99d3ca2",
        "perl-line-b98b5c53b5fdff87"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "perl",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T15:13:31+00:00"
    },
    {
      "case_ids": [
        "powershell-block-2473a890dff65a6e"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "block",
      "failure_type": "sanitation",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "powershell",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "The cleaned comment in the actual output differs from the sampled expected cleaned comment in the number of trailing dashes, indicating a mismatch in the expected vs actual cleaning result.",
      "report": "tmp/stack_v2_comment_judge/reports/powershell-block-2473a890dff65a6e-powershell-block-sanitation-d164e6c9.md",
      "status": "failed",
      "updated_at": "2026-06-01T16:00:36+00:00"
    },
    {
      "case_ids": [
        "powershell-line-192d12de1b767ad1",
        "powershell-line-3992dc99c5d473f9",
        "powershell-line-960668480397c448",
        "powershell-line-a119156d4fecff61",
        "powershell-line-b9195706aa0b32ba"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "powershell",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T15:59:28+00:00"
    },
    {
      "case_ids": [
        "prolog-block-07ba3d9e4c7348b2",
        "prolog-block-233f5570965514ab",
        "prolog-block-5992aad7ef3ec471",
        "prolog-block-b8f82322a4e01274",
        "prolog-block-d96673155409f6da"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "block",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "prolog",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T15:17:37+00:00"
    },
    {
      "case_ids": [
        "prolog-line-e2f275d8bf1721c1"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "extraction",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "prolog",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "The actual extracted comments do not match the sampled raw comment content. Additionally, the cleaned comments contain random sequences of percent signs that do not correspond to the sampled cleaned comment.",
      "report": "tmp/stack_v2_comment_judge/reports/prolog-line-e2f275d8bf1721c1-prolog-line-extraction-0fffc022.md",
      "status": "failed",
      "updated_at": "2026-06-01T15:16:19+00:00"
    },
    {
      "case_ids": [
        "python-block-053d4c993afee5c5",
        "python-block-11225d39574c503c",
        "python-block-26bce9c9fda7e226",
        "python-block-6ec950e0817359e2",
        "python-block-72b4fee4fd0eb70e"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "block",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "python",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T14:24:52+00:00"
    },
    {
      "case_ids": [
        "python-line-bb8043e742591e01"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "sanitation",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "python",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "The cleaning process failed to remove the decorative gutter of '#' characters at the top of the comment and the leading '#' characters on each line. Instead, it merely reduced the number of '#' characters, which is incorrect as decorative gutters and comment syntax scaffolding should be removed.",
      "report": "tmp/stack_v2_comment_judge/reports/python-line-bb8043e742591e01-python-line-sanitation-3b584de2.md",
      "status": "failed",
      "updated_at": "2026-06-01T14:23:24+00:00"
    },
    {
      "case_ids": [
        "racket-line-37a2a0443d81ff6d",
        "racket-line-420fcf3084f0d843",
        "racket-line-68bec95d02cb9d4e",
        "racket-line-d0d28ffab9ceb5fe",
        "racket-line-d754080000757fb6"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "racket",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T15:53:53+00:00"
    },
    {
      "case_ids": [
        "racket-nested-0c08c1bdd3a4efd6",
        "racket-nested-1c34f918072521a1",
        "racket-nested-21e638cd703f829d",
        "racket-nested-4cb455cd5ecf6b97",
        "racket-nested-c6d6d6652cfe2e29"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "nested",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "racket",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T15:55:37+00:00"
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
      "git_commit": "052d2e20a11ee561aff276ed6c47c8cbf9548715",
      "judge_model": "manifest-generator",
      "language": "raku",
      "manifest": "tmp/stack_v2_comment_judge_raku_forth_fix/manifest.jsonl",
      "rationale": "Only found 1/10 block comment case(s) for raku after scanning 500 record(s).",
      "report": "tmp/stack_v2_comment_judge_raku_forth_fix/reports/manifest-raku-block-manifest_generation-33917390.md",
      "status": "failed",
      "updated_at": "2026-05-26T12:16:10+00:00"
    },
    {
      "case_ids": [],
      "cases": 1,
      "code_fingerprint": "e7950d34cf30a02a9ce8d447048815125bd45534763686935461e37a8f3a34a6",
      "comment_kind": "block",
      "failure_type": "manifest_generation",
      "git_commit": "1a3eca563cecbdac23f6e7fa97a9b6fa07bf1c03",
      "judge_model": "manifest-generator",
      "language": "raku",
      "manifest": "tmp/stack_v2_comment_judge_raku_forth_fix/manifest.jsonl",
      "rationale": "Only found 1/10 block comment case(s) for raku after scanning 500 record(s).",
      "report": "tmp/stack_v2_comment_judge_raku_forth_fix/reports/manifest-raku-block-manifest_generation-33917390.md",
      "status": "failed",
      "updated_at": "2026-05-26T13:50:11+00:00"
    },
    {
      "case_ids": [
        "raku-block-14cf7b970314d041"
      ],
      "cases": 1,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "block",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "raku",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T15:18:49+00:00"
    },
    {
      "case_ids": [
        "raku-line-55e9074c7c07ecbd"
      ],
      "cases": 10,
      "code_fingerprint": "3c1b3dc4e34b1b3d25d9471ea4183eda028e135c28192720c8ef00933f6b3f4f",
      "comment_kind": "line",
      "failure_type": "extraction",
      "git_commit": "052d2e20a11ee561aff276ed6c47c8cbf9548715",
      "judge_model": "gpt-5.4-mini",
      "language": "raku",
      "manifest": "tmp/stack_v2_comment_judge_raku_forth_fix/manifest.jsonl",
      "rationale": "The cleaned text matches the sample, but the raw extraction drops the trailing carriage return from the sampled comment, so it does not fully preserve the sampled raw comment content.",
      "report": "tmp/stack_v2_comment_judge_raku_forth_fix/reports/raku-line-55e9074c7c07ecbd-raku-line-extraction-f9ce1915.md",
      "status": "failed",
      "updated_at": "2026-05-26T12:17:06+00:00"
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
      "code_fingerprint": "e7950d34cf30a02a9ce8d447048815125bd45534763686935461e37a8f3a34a6",
      "comment_kind": "line",
      "failure_type": "",
      "git_commit": "1a3eca563cecbdac23f6e7fa97a9b6fa07bf1c03",
      "judge_model": "gpt-5.4-mini",
      "language": "raku",
      "manifest": "tmp/stack_v2_comment_judge_raku_forth_fix/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-05-26T13:51:28+00:00"
    },
    {
      "case_ids": [
        "raku-line-38ec331a469cb043",
        "raku-line-964e0215882485f1",
        "raku-line-a673064d4753e5f3",
        "raku-line-eb1dc1bf222f83a8",
        "raku-line-f488f4874683e251"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "raku",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T15:18:32+00:00"
    },
    {
      "case_ids": [
        "ruby-block-4836d637c39f8196",
        "ruby-block-638cd6de0da9c598",
        "ruby-block-6724209d1ed70109",
        "ruby-block-c4e26407d372cc00",
        "ruby-block-c9b50dd8fa54f25c"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "block",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "ruby",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T15:21:04+00:00"
    },
    {
      "case_ids": [
        "ruby-line-34dfd2692edf9a3a",
        "ruby-line-3af9702f83a1e221",
        "ruby-line-72eedb0abb85911d",
        "ruby-line-9f4f96f1f9f28445",
        "ruby-line-c1821d0dd9ed1197"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "ruby",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T15:19:41+00:00"
    },
    {
      "case_ids": [
        "sql-block-04567b3be73aaa5f",
        "sql-block-1faf4a9d24b4f433",
        "sql-block-a0ef8e4562b9188d",
        "sql-block-bc4c15e6d68497ec",
        "sql-block-f844495c758f842f"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "block",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "sql",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T15:23:21+00:00"
    },
    {
      "case_ids": [
        "sql-line-b589a5032878bc5b"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "sanitation",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "sql",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "The sampled_cleaned_comment contains leading/trailing dashes that should have been removed as decorative gutters, but the actual_extracted_comments' cleaned_comment also retains them. However, the sampled_cleaned_comment itself is inconsistent with the raw comment (it has a leading '--' on the last line), and the actual cleaning result is more consistent with the raw input but still fails to remove decorative gutters as required by the cleaning definition.",
      "report": "tmp/stack_v2_comment_judge/reports/sql-line-b589a5032878bc5b-sql-line-sanitation-11105a2b.md",
      "status": "failed",
      "updated_at": "2026-06-01T15:22:05+00:00"
    },
    {
      "case_ids": [
        "vim_script-line-7c3784ed30ef209d",
        "vim_script-line-b28e6594c7dfff01",
        "vim_script-line-b78b07e10692cb1e",
        "vim_script-line-bbfd1ed80d7d08c5",
        "vim_script-line-e27bee0ccc046e70"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "vim_script",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T15:33:53+00:00"
    },
    {
      "case_ids": [
        "webassembly-line-d9340259efa788c9"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "line",
      "failure_type": "judge_command",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "webassembly",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "judge command failed with exit code 1",
      "report": "tmp/stack_v2_comment_judge/reports/webassembly-line-d9340259efa788c9-webassembly-line-judge_command-b77de502.md",
      "status": "failed",
      "updated_at": "2026-06-01T15:27:31+00:00"
    },
    {
      "case_ids": [
        "webassembly-nested-358a86f42eab8f52"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "nested",
      "failure_type": "judge_command",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "webassembly",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "judge command failed with exit code 1",
      "report": "tmp/stack_v2_comment_judge/reports/webassembly-nested-358a86f42eab8f52-webassembly-nested-judge_command-7f306909.md",
      "status": "failed",
      "updated_at": "2026-06-01T15:30:32+00:00"
    },
    {
      "case_ids": [
        "xquery-nested-46c1d65495e2a761",
        "xquery-nested-63180765e27ae268",
        "xquery-nested-7798212c33a4fbc6",
        "xquery-nested-796c55b6769e8735",
        "xquery-nested-896a59ed3a6dbda2"
      ],
      "cases": 5,
      "code_fingerprint": "ff933e980c015b926f38431cc7739373ad9601e28f0f4ae96f330f271a8de12a",
      "comment_kind": "nested",
      "failure_type": "",
      "git_commit": "5110a544cdbd0a86f47279bef453a89f478c5a7c",
      "judge_model": "ollama:gemma4:31b",
      "language": "xquery",
      "manifest": "tmp/stack_v2_comment_judge/manifest.jsonl",
      "rationale": "",
      "report": "",
      "status": "passed",
      "updated_at": "2026-06-01T16:07:28+00:00"
    }
  ],
  "schema_version": 1
}
STACK_V2_COMMENT_JUDGE_LEDGER_END -->

## Passed Coverage

| Language | Kind | Status | Cases | Model | Commit | Fingerprint | Report | Updated |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| ada | line | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T14:28:08+00:00 |
| agda | line | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T14:29:43+00:00 |
| agda | nested | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T14:31:00+00:00 |
| ampl | block | passed | 3 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T14:21:58+00:00 |
| ampl | line | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T14:19:16+00:00 |
| antlers | block | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T16:10:47+00:00 |
| applescript | line | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T15:50:57+00:00 |
| applescript | nested | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T15:52:47+00:00 |
| assembly | line | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T14:32:35+00:00 |
| autohotkey | block | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T15:43:29+00:00 |
| autoit | line | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T15:44:31+00:00 |
| batchfile | line | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T15:32:37+00:00 |
| blade | block | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T16:13:01+00:00 |
| cmake | nested | passed | 1 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T16:09:32+00:00 |
| coffeescript | block | passed | 10 | gpt-5.4-mini | `d6c976e35d6f` | `ec077eb7f985` |  | 2026-05-26T09:02:42+00:00 |
| coffeescript | block | passed | 10 | gpt-5.4-mini | `fc9ab5301c6d` | `a430f45c8797` |  | 2026-05-26T09:28:37+00:00 |
| coffeescript | line | passed | 10 | gpt-5.4-mini | `d6c976e35d6f` | `ec077eb7f985` |  | 2026-05-26T09:01:00+00:00 |
| coffeescript | line | passed | 10 | gpt-5.4-mini | `fc9ab5301c6d` | `a430f45c8797` |  | 2026-05-26T09:27:30+00:00 |
| coq | nested | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T14:42:08+00:00 |
| css | block | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T14:18:24+00:00 |
| d | block | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T14:44:23+00:00 |
| dockerfile | line | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T14:17:29+00:00 |
| e_mail | nested | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T16:08:29+00:00 |
| editorconfig | line | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T15:34:49+00:00 |
| ejs | block | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T16:14:02+00:00 |
| f# | line | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T14:54:23+00:00 |
| f# | nested | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T14:55:23+00:00 |
| forth | block | passed | 10 | gpt-5.4-mini | `84de62b2af13` | `a430f45c8797` |  | 2026-05-26T10:04:16+00:00 |
| forth | block | passed | 10 | gpt-5.4-mini | `052d2e20a11e` | `3c1b3dc4e34b` |  | 2026-05-26T12:20:43+00:00 |
| forth | block | passed | 10 | gpt-5.4-mini | `1a3eca563cec` | `e7950d34cf30` |  | 2026-05-26T13:53:37+00:00 |
| forth | block | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T14:57:30+00:00 |
| forth | line | passed | 10 | gpt-5.4-mini | `1a3eca563cec` | `e7950d34cf30` |  | 2026-05-26T13:52:36+00:00 |
| forth | line | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T14:56:30+00:00 |
| freebasic | block | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T16:03:26+00:00 |
| freebasic | line | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T16:01:35+00:00 |
| freemarker | block | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T16:17:00+00:00 |
| git_config | line | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T15:35:51+00:00 |
| haskell | line | passed | 10 | gpt-5.4-mini | `84de62b2af13` | `a430f45c8797` |  | 2026-05-26T10:00:40+00:00 |
| haskell | nested | passed | 10 | gpt-5.4-mini | `84de62b2af13` | `a430f45c8797` |  | 2026-05-26T10:01:49+00:00 |
| html | block | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T15:02:29+00:00 |
| java | block | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T14:16:39+00:00 |
| java | line | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T14:15:03+00:00 |
| jsonnet | block | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T16:05:36+00:00 |
| jsonnet | line | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T16:04:31+00:00 |
| julia | line | passed | 10 | gpt-5.4-mini | `84de62b2af13` | `a430f45c8797` |  | 2026-05-26T09:58:11+00:00 |
| julia | line | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T15:00:05+00:00 |
| julia | nested | passed | 10 | gpt-5.4-mini | `84de62b2af13` | `a430f45c8797` |  | 2026-05-26T09:59:14+00:00 |
| lua | block | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T15:06:14+00:00 |
| mathematica | nested | passed | 10 | gpt-5.4-mini | `84de62b2af13` | `a430f45c8797` |  | 2026-05-26T10:05:36+00:00 |
| matlab | block | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T15:10:05+00:00 |
| matlab | line | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T15:08:35+00:00 |
| nim | line | passed | 10 | gpt-5.4-mini | `84de62b2af13` | `a430f45c8797` |  | 2026-05-26T09:54:04+00:00 |
| nim | line | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T15:56:37+00:00 |
| nim | nested | passed | 10 | gpt-5.4-mini | `84de62b2af13` | `a430f45c8797` |  | 2026-05-26T09:55:13+00:00 |
| nim | nested | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T15:58:33+00:00 |
| nsis | block | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T15:50:03+00:00 |
| nsis | line | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T15:48:49+00:00 |
| pascal | nested | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T14:52:14+00:00 |
| perl | block | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T15:14:57+00:00 |
| perl | line | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T15:13:31+00:00 |
| powershell | line | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T15:59:28+00:00 |
| prolog | block | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T15:17:37+00:00 |
| python | block | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T14:24:52+00:00 |
| racket | line | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T15:53:53+00:00 |
| racket | nested | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T15:55:37+00:00 |
| raku | block | passed | 1 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T15:18:49+00:00 |
| raku | line | passed | 10 | gpt-5.4-mini | `84de62b2af13` | `a430f45c8797` |  | 2026-05-26T09:57:13+00:00 |
| raku | line | passed | 10 | gpt-5.4-mini | `1a3eca563cec` | `e7950d34cf30` |  | 2026-05-26T13:51:28+00:00 |
| raku | line | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T15:18:32+00:00 |
| ruby | block | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T15:21:04+00:00 |
| ruby | line | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T15:19:41+00:00 |
| sql | block | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T15:23:21+00:00 |
| vim_script | line | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T15:33:53+00:00 |
| xquery | nested | passed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` |  | 2026-06-01T16:07:28+00:00 |

## Failed Coverage

| Language | Kind | Status | Cases | Model | Commit | Fingerprint | Report | Updated |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| autohotkey | line | failed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` | [autohotkey-line-09df99f2c2ac27f4-autohotkey-line-extraction-43195474.md](tmp/stack_v2_comment_judge/reports/autohotkey-line-09df99f2c2ac27f4-autohotkey-line-extraction-43195474.md) | 2026-06-01T15:40:41+00:00 |
| autoit | block | failed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` | [autoit-block-a9f015b2e27d4208-autoit-block-sanitation-61d4e931.md](tmp/stack_v2_comment_judge/reports/autoit-block-a9f015b2e27d4208-autoit-block-sanitation-61d4e931.md) | 2026-06-01T15:47:46+00:00 |
| cmake | line | failed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` | [cmake-line-4a4380c7e47ed330-cmake-line-sanitation-adfa732e.md](tmp/stack_v2_comment_judge/reports/cmake-line-4a4380c7e47ed330-cmake-line-sanitation-adfa732e.md) | 2026-06-01T16:09:09+00:00 |
| cobol | line | failed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` | [cobol-line-d428778855caa91f-cobol-line-judge_command-cd269bdf.md](tmp/stack_v2_comment_judge/reports/cobol-line-d428778855caa91f-cobol-line-judge_command-cd269bdf.md) | 2026-06-01T14:41:00+00:00 |
| d | line | failed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` | [d-line-695baf7d4001e436-d-line-extraction-49334352.md](tmp/stack_v2_comment_judge/reports/d-line-695baf7d4001e436-d-line-extraction-49334352.md) | 2026-06-01T14:42:42+00:00 |
| erlang | line | failed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` | [erlang-line-d377a7a07c46ba63-erlang-line-extraction-c4d10ed3.md](tmp/stack_v2_comment_judge/reports/erlang-line-d377a7a07c46ba63-erlang-line-extraction-c4d10ed3.md) | 2026-06-01T14:52:54+00:00 |
| forth | line | failed | 10 | gpt-5.4-mini | `84de62b2af13` | `a430f45c8797` | [forth-line-ce83fb3b8d1fb2ca-forth-line-extraction-6570f987.md](tmp/stack_v2_comment_judge_less_known_500/reports/forth-line-ce83fb3b8d1fb2ca-forth-line-extraction-6570f987.md) | 2026-05-26T10:02:51+00:00 |
| forth | line | failed | 10 | gpt-5.4-mini | `052d2e20a11e` | `3c1b3dc4e34b` | [forth-line-ce83fb3b8d1fb2ca-forth-line-extraction-6570f987.md](tmp/stack_v2_comment_judge_raku_forth_fix/reports/forth-line-ce83fb3b8d1fb2ca-forth-line-extraction-6570f987.md) | 2026-05-26T12:19:29+00:00 |
| fortran | line | failed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` | [fortran-line-5d4096b01df90d1e-fortran-line-extraction-77e7d085.md](tmp/stack_v2_comment_judge/reports/fortran-line-5d4096b01df90d1e-fortran-line-extraction-77e7d085.md) | 2026-06-01T14:59:12+00:00 |
| java_properties | line | failed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` | [java_properties-line-807704924180f31a-java_properties-line-judge_command-98f0f87d.md](tmp/stack_v2_comment_judge/reports/java_properties-line-807704924180f31a-java_properties-line-judge_command-98f0f87d.md) | 2026-06-01T15:39:25+00:00 |
| julia | nested | failed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` | [julia-nested-5b1910d59d901419-julia-nested-sanitation-477d0198.md](tmp/stack_v2_comment_judge/reports/julia-nested-5b1910d59d901419-julia-nested-sanitation-477d0198.md) | 2026-06-01T15:01:33+00:00 |
| lua | line | failed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` | [lua-line-a2ff8eca29a389c8-lua-line-extraction-70b7851f.md](tmp/stack_v2_comment_judge/reports/lua-line-a2ff8eca29a389c8-lua-line-extraction-70b7851f.md) | 2026-06-01T15:04:43+00:00 |
| mathematica | nested | failed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` | [mathematica-nested-3248c6016956a958-mathematica-nested-extraction-23f9eabc.md](tmp/stack_v2_comment_judge/reports/mathematica-nested-3248c6016956a958-mathematica-nested-extraction-23f9eabc.md) | 2026-06-01T15:06:58+00:00 |
| pascal | block | failed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` | [pascal-block-2f9135e5e95a6991-pascal-block-sanitation-9d073262.md](tmp/stack_v2_comment_judge/reports/pascal-block-2f9135e5e95a6991-pascal-block-sanitation-9d073262.md) | 2026-06-01T14:48:53+00:00 |
| pascal | line | failed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` | [pascal-line-dbf2d3aed438e1ac-pascal-line-sanitation-f657c720.md](tmp/stack_v2_comment_judge/reports/pascal-line-dbf2d3aed438e1ac-pascal-line-sanitation-f657c720.md) | 2026-06-01T14:45:51+00:00 |
| powershell | block | failed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` | [powershell-block-2473a890dff65a6e-powershell-block-sanitation-d164e6c9.md](tmp/stack_v2_comment_judge/reports/powershell-block-2473a890dff65a6e-powershell-block-sanitation-d164e6c9.md) | 2026-06-01T16:00:36+00:00 |
| prolog | line | failed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` | [prolog-line-e2f275d8bf1721c1-prolog-line-extraction-0fffc022.md](tmp/stack_v2_comment_judge/reports/prolog-line-e2f275d8bf1721c1-prolog-line-extraction-0fffc022.md) | 2026-06-01T15:16:19+00:00 |
| python | line | failed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` | [python-line-bb8043e742591e01-python-line-sanitation-3b584de2.md](tmp/stack_v2_comment_judge/reports/python-line-bb8043e742591e01-python-line-sanitation-3b584de2.md) | 2026-06-01T14:23:24+00:00 |
| raku | block | failed | 1 | manifest-generator | `84de62b2af13` | `a430f45c8797` | [manifest-raku-block-manifest_generation-33917390.md](tmp/stack_v2_comment_judge_less_known_500/reports/manifest-raku-block-manifest_generation-33917390.md) | 2026-05-26T09:52:49+00:00 |
| raku | block | failed | 1 | manifest-generator | `052d2e20a11e` | `3c1b3dc4e34b` | [manifest-raku-block-manifest_generation-33917390.md](tmp/stack_v2_comment_judge_raku_forth_fix/reports/manifest-raku-block-manifest_generation-33917390.md) | 2026-05-26T12:16:10+00:00 |
| raku | block | failed | 1 | manifest-generator | `1a3eca563cec` | `e7950d34cf30` | [manifest-raku-block-manifest_generation-33917390.md](tmp/stack_v2_comment_judge_raku_forth_fix/reports/manifest-raku-block-manifest_generation-33917390.md) | 2026-05-26T13:50:11+00:00 |
| raku | line | failed | 10 | gpt-5.4-mini | `052d2e20a11e` | `3c1b3dc4e34b` | [raku-line-55e9074c7c07ecbd-raku-line-extraction-f9ce1915.md](tmp/stack_v2_comment_judge_raku_forth_fix/reports/raku-line-55e9074c7c07ecbd-raku-line-extraction-f9ce1915.md) | 2026-05-26T12:17:06+00:00 |
| sql | line | failed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` | [sql-line-b589a5032878bc5b-sql-line-sanitation-11105a2b.md](tmp/stack_v2_comment_judge/reports/sql-line-b589a5032878bc5b-sql-line-sanitation-11105a2b.md) | 2026-06-01T15:22:05+00:00 |
| webassembly | line | failed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` | [webassembly-line-d9340259efa788c9-webassembly-line-judge_command-b77de502.md](tmp/stack_v2_comment_judge/reports/webassembly-line-d9340259efa788c9-webassembly-line-judge_command-b77de502.md) | 2026-06-01T15:27:31+00:00 |
| webassembly | nested | failed | 5 | ollama:gemma4:31b | `5110a544cdbd` | `ff933e980c01` | [webassembly-nested-358a86f42eab8f52-webassembly-nested-judge_command-7f306909.md](tmp/stack_v2_comment_judge/reports/webassembly-nested-358a86f42eab8f52-webassembly-nested-judge_command-7f306909.md) | 2026-06-01T15:30:32+00:00 |
