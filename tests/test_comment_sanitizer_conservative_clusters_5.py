"""SHA-pinned regressions for secondary gutters, dividers, and fixed frames."""

from __future__ import annotations

import hashlib
import json
import random
import string
from pathlib import Path

import pytest

from ml4setk import (
    CommentSanitizer,
    QueryMatch,
    sanitize_comment,
    sanitize_comment_text,
)

pytestmark = pytest.mark.unit

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "comment_cleaning_regressions"

CASE_PINS = (
    (
        "freemarker-block-79a158c40ab99823",
        "363d2828ac6be49edaeb4cc04fcc6a668fdb2caf9f5b4d5072e54b2adbf44633",
        "d1599cfbe297df49ad9b99c7087d89f98e3381c0357eff9e66905e5f0133b391",
    ),
    (
        "freemarker-block-cbd449c5353adab4",
        "e855800ae7037a97359ac9fe6a5f7d4db214e5fbd027aa314e2a8cca5bd3b946",
        "2cfa3b39468a7bf2f92d2ef17008ea339d0ba00094c100b8ab85ce5a6818739b",
    ),
    (
        "imagej_macro-block-24ab709c93555406",
        "b05ae7e2683893d9cf375007f03416d7ea7fd54a7d5f21b3ea1ed7a5a702201d",
        "e59adea17e5b49403760d8e4fae94644ae36e70dafe6a9e0c834a1896f302ea6",
    ),
    (
        "imagej_macro-block-5f517cfad88d0fc3",
        "aa23605baac67742f39e1b8f449bfb50ef2eb1386656363da3ea7483a77b00de",
        "71178e9b7299b963d2be015b11a090647172c151e00db4138707e9515f51dd4c",
    ),
    (
        "imagej_macro-block-ee3796a316eb1106",
        "d2cf2580fbd4dc6b2e1f0a0386baeb7a9015aef5ffd57b79ec3ebde63123588e",
        "03e9b9f8c663f6f92da1654ea8764a0ef6fedff3024913a05c6c97c94e646617",
    ),
    (
        "peg_js-block-55ea607f30fa2a5f",
        "55770de0fea2ab29cbbca0ff030446008633eaef06854b616ed62e6d80d549cc",
        "1bee1c5d2373688d35c65db0cb819d4db540e331a10952c18fc1f83b2a65711a",
    ),
    (
        "pegjs-block-167424450d9cb5c8",
        "55770de0fea2ab29cbbca0ff030446008633eaef06854b616ed62e6d80d549cc",
        "1bee1c5d2373688d35c65db0cb819d4db540e331a10952c18fc1f83b2a65711a",
    ),
    (
        "promela-block-65d207d401ceb302",
        "f8d02f26cd70404a10b24d6c7e2be0bb7ddc18bd1827f86bddc207234f23ef19",
        "0a8c30c4dc64a9fabbdeeba6bfe84cd5b4779a615a9f7f2f6ef1b02508ef24ae",
    ),
    (
        "pascal-nested-6b06909ebd4e6c2e",
        "805eeb523a9205d6de201eb0257d42eeaf67c71e42132843d26e877ac3fe0de9",
        "d4d9d071192905f39bb5bf496828cde3aec1db82092903d07db28c86529490a1",
    ),
    (
        "pawn-block-bfbc771eba3b1250",
        "2b84ed7c30ddcc0ad3213dadd3ef867a7ed924090979b5b6ff11e63ad44c5418",
        "f0a3efc59a91bcc6bd3b47e563c61b07c88340f1d6a2118a9d9c27315fbdd1fa",
    ),
    (
        "rpgle-block-d643f341e4648f03",
        "d57283fd67bf6f8d5db3811ef6e7db54a04b8a33d25d90ea050d52ede056c341",
        "ff1d82c29cd88cae60b52b5a34eff3dd3ce30cf762baae89f0b16a0cdc6d2e6b",
    ),
    (
        "sql-line-23c886e7f7bbd538",
        "308d2af5245e3aa42f6aa22bb5aab9420ee0aee6e01a6d04d1a24e3e6352042e",
        "f0c8ba1700c54783ccc911b74b3d79353f9246081e4a68672c211379b574d29f",
    ),
    (
        "groovy_server_pages-line-6fd4d43f3bd7f2b5",
        "2cf167ede2fa114c6dca9f0502a695a9267ed6aab73d3d57bd91374a9eb7f4ba",
        "ab4249b2006fa83f695cebd904f579675b2445aa4e4eafd0936c88cede159951",
    ),
    (
        "maven_pom-block-95b7ad316ace9b3f",
        "b96e833dd3fe87d9c28e14cd4ad81a1ce53043ad3e96a9176473c26b51c7a893",
        "309cc5a4e0302475af7c1677454616fc97d58c6aea806e36daab4a09b9d12dba",
    ),
    (
        "eclipse-line-3308fa4d78886612",
        "34f857b0a5e1319a764c37b50a8ff05b074548a21443174c279eb5da60a43753",
        "31e68ad70847866be4cf746081e7450f800f2248b3f1ef60069c48cc59b36bb2",
    ),
    (
        "eclipse-line-68f734cf9618561f",
        "65674a8b2e3b239265eb5ac187f7aba2fca62b173fc0cde32adfd7edff3cb239",
        "5dd3889c8e7bfbf3e4811dd83c0ac268eb54c122a8b2783163ab7d55cb48bc04",
    ),
    (
        "openedge_abl-block-4deb998123bda64b",
        "2a3546eaf07df4b4f0fbf59dac32073204f5bfe132c0b0e414a648878f24969d",
        "82a16ca4686166505227ed62e1b9b8235339c56483517a284de6610b92a3936a",
    ),
    (
        "openedge_abl-block-89c1c11a2a5e1999",
        "7b6d64b6d50b65a27ae53d5a9447b15e935bcdb81cc2a1ef6f497e3af81cd6c2",
        "5516a670328cc819c038425995821620ef7579b146167b2c6615c2240930884d",
    ),
    (
        "openedge_abl-block-a5fb879a3f425888",
        "088e601ee832b0d8d4e669c28259bcf29d1c275a2fe5f0ac553e9a6b2ae92554",
        "9abf5e2f8c420c1314f9f3ab60418916931be52d778fe00cf6c556d525e4d9a1",
    ),
    (
        "desktop-line-25331719e87b3d8f",
        "7d831c3f872d51dc3353f2182f071724a07d5ab97a66a5a4fbec68811e16ae0b",
        "71c23e285fa1a39b7fb6d8bd91eca1c08d1a8b96ae24f91e1ff9fd79a7331737",
    ),
    (
        "4d-block-7544d30c65a5d09f",
        "c2695e4cd1ed32853058bb15e4fd6ae5ba0de2429872991dd4fbfb4e3b200e41",
        "4bf5fc21c832f154b9894cccdade5fb20a31db2b391e719bb92a4f2b225fcc95",
    ),
    (
        "cython-line-d60b8dc8b6578128",
        "194573991e3928120fb7ec4589c34c33d9c7e0892777718a518db39427309537",
        "9425e7776ebe09f077ccf6239c9e436a518a7ed2ac62aa2a821359d31202b126",
    ),
    (
        "fortran-line-29801ed07a9252e3",
        "d443076e4d8763519fa8f3003f38dec4b17b98cfa6d6376510b9ac86a2271d6f",
        "c37681a4d636da2b2723d9669f1920cc5602132d40e60fa533c203046e47ad56",
    ),
    (
        "fortran-line-69f26a5c9fe81469",
        "3f3fe0cbc03f7352b29021c101998ccd74e9fac62702d714bfdb0b31dcf87cbe",
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    ),
    (
        "fortran_free_form-line-a5192d5264812b06",
        "3c342882d4530c7d6803dc76b3b6ac41c9f6805f9b050abed3fbfad0b61d06fa",
        "c2925ecf6bb368b7153a368e5c510776164b51e3332bee22014ae5019f6d033a",
    ),
    (
        "git_config-line-23dd164425e671b0",
        "ceccad08de7c4d1ed53d89e6317f52707aeb507612b53d583cea12359c54d95c",
        "e4f4a3bd5a1932e4690cebcf06d493c66a285a9ee50a81133b3e13123e80278b",
    ),
    (
        "hyphy-line-40e8408dfda034e4",
        "c46f4dd4b7c43faf48c8ef018cd53a0fff69b376d6332462222472c57ee58a4b",
        "3d844d249c6c3a1e0a952aadb391a8c7ccc9b4458c33e15b413506b291ed212b",
    ),
    (
        "jade-line-83b0ed9c11e49863",
        "56f2a8082243a8fcf9010600feffd370f5439a57ecc9390ede4851564c5851f6",
        "9694e255bac970537d16de8600b3a5d4926d10493437babed6ee67897f1586cb",
    ),
    (
        "pug-line-25639bbdefeab821",
        "56f2a8082243a8fcf9010600feffd370f5439a57ecc9390ede4851564c5851f6",
        "9694e255bac970537d16de8600b3a5d4926d10493437babed6ee67897f1586cb",
    ),
    (
        "kakounescript-line-33af2864eaf79230",
        "943ca4c0eaaefa92002522d6f2c6016919f6af6f97437adaac86ed2e97ee2931",
        "3461549b04adeb45d8344a265b6d5da11e6b56e1f6a7673782b7c1d6e2eccfbf",
    ),
    (
        "m4-line-8079900631003d7a",
        "2af4d42cdd80f3214a648e8e555ee9d496433682c1d6f99d93e78fe2a0fadc27",
        "5cfa4d6cb756a81cc6a4e4c2466278555bb577a186aab8b267e52fa404ae9dfb",
    ),
    (
        "mirah-line-a0ed606a78bedb3e",
        "3abb7291585e2548ac64e3a9ddc479e99d1780a964fa73e73de48cb4aa98cf21",
        "945ae040001414267e50cf230f52625529645f40a1ff00fbf53402801e1a5a20",
    ),
    (
        "objective_j-line-7eab20dbbd74516c",
        "39f386db75a517ebd13a97616a69e3ab3dc3d6e37b0ff109d896c32dfc31e465",
        "92367df7339ed7d8c8d05c6e80e84eb7035388307de2c517ab586152d228f717",
    ),
    (
        "plsql-line-000c92df37f3c6b5",
        "f38ef8ed88f014825403f2d547026f8858303971f9bb591a3f7e4fdb586a9d47",
        "b0bc5ef78684b637aa796ceadf866f8e0170c9559d19a5bd233ac1aa87a29788",
    ),
    (
        "saltstack-line-59429e7ff4aaec55",
        "7bab007bdde72abb447c3ea450f791b3223ea533d7abd952df6d91582fc17009",
        "f9760869a2348dbf39eb520feb83a920ff9148bd6c0ed8c87272174971b10a63",
    ),
    (
        "saltstack-line-cfee08bb610d5cde",
        "a2bafd3694d73712aaba6ffc13ee246edd3fc65e936d2303334a4847bd03c0ae",
        "415764e95ee84b8fadefbb3aef290a9fe43cda8fbca22e67b5408b8ca769a9b1",
    ),
    (
        "shellcheck_config-line-0c93794e0ae8754e",
        "a00d0d36b151e5ca72f5d8bf5089ec7d6f0a28cbaa553ad84674a532357be1d6",
        "787f1bd0dbd468e6b00919ee292349ff0ed7e89574cec8a594d9502580c6a46c",
    ),
    (
        "shellcheck_config-line-9b6df47c8e1d61cb",
        "83ac96ec57c3f4038711b93cc47b951eb54738d3c30b1f2cc9019b396097b6e9",
        "4497a4c4e5c0c2e5529de86ca2cde3c5af6bfd94a803cde5ad53032c62b61861",
    ),
    (
        "systemverilog-block-fd066aeeeedd1749",
        "3b282a7d68827a21b222de0e59bc742c4f3ef0027c5c960dd05e08fb136a659b",
        "dfc15fc84c887499b3e288e81ec380f73b3e99727019a4c3b3d89bef85b928ae",
    ),
    (
        "zig-line-4265843ec59f8aab",
        "1d1dcc1eb514883c740e839a4b5cfba2710083885256c42898fde8f772354663",
        "a726007978a555b5513915067248af9e3c23dc287d012d6334bc4c45ef74a7f8",
    ),
    (
        "bibtex-line-9daacfa445396e26",
        "cb486a3f23fb060fe9521a891c6eda7c0c983407b9b5ea0701ff874573a94711",
        "935dae11676760daa7ebe6acff087c6112f91168ebff8f84d77384bd3770705b",
    ),
    (
        "blitzbasic-line-26365f83e97f0f75",
        "6ce6823a1e8ff1f63c7b6364fa82b142fa5abc80f3a2623723a13926e9434239",
        "df8e55b3a8f5160baea89c916115bcbda7e0bc74f9cdba3bdb1d03f6a168f547",
    ),
    (
        "blitzbasic-line-dbe6540d3504846f",
        "ff41e129e9799e111e2f6725b11c5f9aa55138e12cb949049209c5a363a100c2",
        "8b9cfe7df6578eadad56157a07b345a92f2e562f2d3862226d2bd50f90eded15",
    ),
    (
        "clips-line-6fec32ec737aff0e",
        "a181bc25256ee3e0b811364b70b9439382b022d03a69966cfcc3b27952fc53ec",
        "3cf6652031511913b08394dfdfb663cfaa07314eb892d239b97047e5a6143a39",
    ),
    (
        "clojure-line-94892495ebb462a7",
        "6d466ee34da02c9232384a97b1be68d774bfa8def82240567cd09d5e6c2a7f33",
        "d692029a2faecff4dac54760dcc6f04cca52225564ee36ef9baec3b5501df630",
    ),
    (
        "cmake-line-db5fca5df6556847",
        "e121b6547889104da48b7a6a9ac87425e1b723cb94b49fc9e82a9df2728e5172",
        "d0b1a869600d21076a3fa8b5f52546e55920588ce73dfb7e56ca9dc08bdcaf3e",
    ),
    (
        "denizenscript-line-e1bb6e717bb23cd8",
        "90d4a8382a429566e4872f79522c8458469a2f238d2ba18aeca269c8b69aa62a",
        "f4bf3f3609a599b4d930cdd8f5d319683539f92a22d28a4e7c25d050bb4e8608",
    ),
    (
        "ebnf-nested-5f6c70a467c12bcf",
        "7c6bc2f4aa45f8a415427f5a2658a476aa893b3299cc013a47ed421607005cc8",
        "fdd7a8965aaf6959e9f89732eba70972eed64ec1cf8e3fcbb777188d03eaeadc",
    ),
    (
        "ninja-line-414607a27fcc0cd6",
        "dd98af2c83156c74d75049e513760a87a51376d3086a7e3934d77a5cf1fcac92",
        "d17aae0655e55effe01f64bb9579c9e83df707ca63a647ee4c370808e9323afc",
    ),
    (
        "nsis-block-a04100c6a26e33e8",
        "a98915eb2a3cf649d31eacc2a32b383b586e096da3002c41f1ccfc650330e6ef",
        "dfdbb446897be1ad22904e57ea11c72bc5bb9123af6533a919530f2e94257ef4",
    ),
)


def _load_pinned_cases() -> dict[str, tuple[str, str, str]]:
    cases: dict[str, tuple[str, str, str]] = {}
    wanted = {case_id for case_id, _, _ in CASE_PINS}
    for path in FIXTURE_DIR.glob("*.json"):
        payload = json.loads(path.read_text(encoding="utf-8"))
        for row in payload.get("sanitizer_cases", []):
            if row["case_id"] in wanted:
                cases[row["case_id"]] = (
                    row["language"],
                    row["raw_comment"],
                    row["expected_cleaned"],
                )
    assert cases.keys() == wanted
    return cases


PINNED_CASES = _load_pinned_cases()


def _is_subsequence(candidate: str, source: str) -> bool:
    offset = 0
    for character in candidate:
        offset = source.find(character, offset)
        if offset < 0:
            return False
        offset += 1
    return True


@pytest.mark.parametrize(
    ("case_id", "raw_sha256", "expected_sha256"),
    CASE_PINS,
    ids=[case_id for case_id, _, _ in CASE_PINS],
)
def test_validated_scaffold_regression(
    case_id: str,
    raw_sha256: str,
    expected_sha256: str,
) -> None:
    language, raw_comment, expected = PINNED_CASES[case_id]
    assert hashlib.sha256(raw_comment.encode()).hexdigest() == raw_sha256
    assert hashlib.sha256(expected.encode()).hexdigest() == expected_sha256

    raw_match = QueryMatch("", "", raw_comment)
    sanitizer = CommentSanitizer(language)
    actual = sanitizer.sanitize(raw_comment)

    assert actual == expected
    assert sanitizer.sanitize(raw_match) == expected
    assert sanitize_comment(language, raw_comment) == expected
    assert sanitize_comment_text(language, raw_match) == expected
    normalized_raw = raw_comment.replace("\r\n", "\n").replace("\r", "\n")
    assert _is_subsequence(actual, normalized_raw)
    assert "".join(filter(str.isalnum, actual)) == "".join(filter(str.isalnum, normalized_raw))


def test_scaffold_shapes_are_language_and_completeness_scoped() -> None:
    assert sanitize_comment("c", "### content ###") == "### content ###"
    assert sanitize_comment("clips", "; ; content") == "; content"
    assert sanitize_comment("desktop", "### first ###\n### second ###") == "## first\n## second"
    assert sanitize_comment("cmake", "#-- OPTIONS --#") == "-- OPTIONS --#"
    assert sanitize_comment("ebnf", "(*\n! -------\n! content\n*)") == ("! -------\n! content")


def test_validated_scaffold_fuzz_is_deletion_only() -> None:
    generator = random.Random(0x5CAFF01D)
    alphabet = string.ascii_letters + string.digits
    for _ in range(128):
        words = [
            "".join(generator.choice(alphabet) for _ in range(generator.randint(1, 12)))
            for _ in range(3)
        ]
        expected = "\n".join(words)
        cases = (
            ("desktop", "\n".join(f"### {word} ###" for word in words)),
            ("clips", "\n".join(f"; ; {word}" for word in words)),
            ("imagej_macro", f"/* {words[0]}\n * {words[1]}\n{words[2]}\n*/"),
            ("nsis", "#********#\n" + "\n".join(f"#******** {word} ********#" for word in words)),
        )
        for language, raw_comment in cases:
            actual = sanitize_comment(language, raw_comment)
            assert actual == expected
            assert _is_subsequence(actual, raw_comment)
            assert "".join(filter(str.isalnum, actual)) == "".join(filter(str.isalnum, raw_comment))
