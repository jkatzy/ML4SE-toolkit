"""SHA-pinned regressions for validated padding and legacy comment cards."""

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
        "angelscript-block-e0bad7380b2da8f3",
        "c8400d1fef563be0882d85c3ede02067abbbd8ffb184685e75fabf68a122db5b",
        "cfde41cc2112e3eeb22570d838f1d43bb2b25e63dadeaaef36deed9e34bd2f87",
    ),
    (
        "angelscript-block-f1fb14e14383f575",
        "91de7f0c9dacd6c80c57334a0f5c1c2bf4e06563f8e4c151f1bc8868741cad15",
        "f6d32895ece351d3ed44cf3af717841e31c51369d06799292d7a9c273d0f5c7c",
    ),
    (
        "apex-block-0290403b172877d3",
        "ecc324f4316b035388416804eeb93a589d3f201e3b896ae0ae8b1f61cbed48bb",
        "a9649b6b0d80113988b20616b124a36fef052295bb3ed2d46663f5f0d3c539b6",
    ),
    (
        "apex-block-77694893e81c28be",
        "c89ee85db7fded6be4ddfe116e6d89f9d4df73d01e62e8d7d06e1f46b02e7bb5",
        "f35d8111faef030cce14e1f4c3665892cca96e59eb1f236e2f43157bbaf86c76",
    ),
    (
        "applescript-line-d1ceac3f90aa3268",
        "65022f9310707c747dfdf346112d03ee73c1aa3faafc26b2ca01f13e36a5e52a",
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    ),
    (
        "applescript-nested-ad1ab7d564cb4f7b",
        "5c130b12ee71048f99462fcbe9159dfbf0d2fb45f83a266e207728457fb6a27c",
        "4423b67e9ea2eae42b5f6d8a14a403ddbef02ac8a91c17966da71f839f9f0a08",
    ),
    (
        "batchfile-line-fe400ca3d7d5a1bc",
        "53e4f9fcc60705f44d3e232e6a7203c4b150ed8c6eda2d50c06c71fe4bda355e",
        "b68f119aa6a20751830790ec8b59977cfd9cce2b78a591a406c6fb2e787d093b",
    ),
    (
        "c-block-4ea119dd25f82771",
        "e698275ed2a833b3e920a7c071fe0f2c2bb66dce2a9a7b87509dfc798ef4c22b",
        "adb08b9696ea9a8bcfb4eb770b4beaa9d8906409d1ab224aec0077839d2a9861",
    ),
    (
        "c-block-12f97704927376b4",
        "45e24a697d4afddcb95a3c00fba0feed35f6d16b27ec383b34d0f6b3a9d883f2",
        "aa059393cfe0c78ccdb9ec7994acc89d5a4cc4bb19a6209095bd3833fb26d488",
    ),
    (
        "c-block-12f97704927376b4--requested-c-sharp-2d899f6fc9",
        "45e24a697d4afddcb95a3c00fba0feed35f6d16b27ec383b34d0f6b3a9d883f2",
        "aa059393cfe0c78ccdb9ec7994acc89d5a4cc4bb19a6209095bd3833fb26d488",
    ),
    (
        "coldfusion-block-10cddcb25a644854",
        "daf4a44e3015ad21aae62e3f4a1ecdbba4bad2f15b1765cec77aebd0f7764989",
        "f60478feb63c13bd8526a038a3d881af3f1839d683384c9593ee3c21ce83f3fe",
    ),
    (
        "c-block-12f97704927376b4--requested-csharp-7fc218f23b",
        "45e24a697d4afddcb95a3c00fba0feed35f6d16b27ec383b34d0f6b3a9d883f2",
        "aa059393cfe0c78ccdb9ec7994acc89d5a4cc4bb19a6209095bd3833fb26d488",
    ),
    (
        "csound_score-line-debe309ad0a40f75",
        "dc20914907bd5fc0cc98548667fea43fd0fbcccbb446fdc749031f8eb1b7a153",
        "bc1de356a7deb9f215314409fda705ad99e43763b1a8455f178bf9daa7bc4bbc",
    ),
    (
        "debian_package_control_file-line-bf9789aca450c699",
        "2bd713b81aa6fee6f54827f3dce9e1ba45958580287bee3eb03a14afd5b16c9a",
        "b2c1a7b3ce928a44408cec93fa329689a6165e33459f2f76fdcdfd5cc7fc6ed4",
    ),
    (
        "dircolors-line-1727b3fd275068e2",
        "d961f3695c3c49506c8238f5b6b944526cd3fc6a48218d53fee7db613973ddbb",
        "ddce7ead4bd68833a0bbb5568d8b30d78ca9e01f7227624028b439013565ecd0",
    ),
    (
        "dylan-line-31513e8271d34445",
        "054439a3d94206fbed6aa7c1dc356b24030d1019c1873d3583baa6e3458593ac",
        "6ff43e0489a9584e8e742885a36b9ebc65b0a5f332f1d4a1296a7690845e6f78",
    ),
    (
        "fancy-line-69754c2f18ddf3a5",
        "f2f3cc4e854874688f3385cf48f8ed6519639ec55b468d432ac87ea0c8be8359",
        "565db88b6e9f636ece08f1987c23b17cb7872726d92d8a413903c34bac58258b",
    ),
    (
        "gettext_catalog-line-60c2ed46b244fa0e",
        "9731f4caeb6070b6005113c4c1e4243242efd4ac9e104710a78e348e08c9113b",
        "f9139d195d7fb12481dfb8110a42574d76cea4ec2cf38be867cb5cf9f305bf90",
    ),
    (
        "golo-line-6fe5135adb248173",
        "2cc57aad03502c2607a082495e43994a78a3f427f08d617bfe07aa92dfdfd576",
        "3f0c09db42da75359505cdadfd79a05636aa2e9ee09cffefe62e51c9fbd3f3dd",
    ),
    (
        "hocon-line-8a28114a6baa74d1",
        "3a0db7ad94141394fb99aa9cd050e4d3cd62d915276cc89c309e6430b1d7f42d",
        "b4e90075e370ff6379663e998bdd1cf81457601f940797de11a6bc42902cf8e7",
    ),
    (
        "hoon-line-0d7bc921429bf8f8",
        "be111bf6b63b1975ce303a2fd6eff6bf990a081a74e15b2f6d56f02d24263093",
        "b6034bb5bc98674c642d017cb58e4f45a034985970fe9d5db0c6a4cfd6f5426d",
    ),
    (
        "html_plus_ecr-block-cb7f349e53af432e",
        "7bff2981b4718a35aa20cfce16a7b8ee103fe7e477fcc95a2651faba9926365c",
        "54032daa7b736d4bd94e38e876e6b6a812e5fc4b3179acd8ffa28d339c4cef2e",
    ),
    (
        "less-block-8f6dd87a04f118a9",
        "cb6695a9771b82d626bd848cd0b37c65f8051e329133e0c237dc58457c133ea2",
        "f3168554aae6d02f4de0af6d731ecbe8e7079eb0713237712c783cfffb9fdd0d",
    ),
    (
        "lex-block-c0886d71aed3ce9c",
        "20035e119ccbe86ca5e3d566f38da7d382b67a4f3dd6d6726cace1990c7e1eb4",
        "3e28a0bddad53b071292f3d1e1ba6d5902a6302a8e01f7565e949bc896b2230c",
    ),
    (
        "literate_coffeescript-block-1b3d89eb4edf4a39",
        "6fc0b567c4f42c58f8485155c88192cbb8c64d0ad2343bff48137c88cb6aadec",
        "3f3a11412049ec12709aa025c2132c849791eccf733768cf225ae5ad2e3be244",
    ),
    (
        "lolcode-line-43d9c0fe6e991c6d",
        "d97979fad866710623dfb4fd13d43dbbb059eca4202b83c5dbd1a52cda9db043",
        "a4d886d567f30b0846a5724abd32a90cf0884e10f229d1d2f2e5eb36e42d3183",
    ),
    (
        "lookml-line-77ebd525168f8025",
        "2f358bd058063aa5b13ef434680654676ec07add6928e57ec396fc7e5d7c243a",
        "e362cf0b80f68902fcd0687ea20a08208bca1ca2ada9b06c52e501b0d387ea01",
    ),
    (
        "lsl-line-e43e2798044d6100",
        "40fc4ede6fa716d3a18904c2e96a93c9d9c5c7759b5575ac349fd3f5f518bc70",
        "203787ed42ef830da7de791d92461e89f9095a225291dacf7940b0fa38f02ea6",
    ),
    (
        "matlab-line-224ed460eaecc4aa",
        "d6dbd5a846c2e4f3f9613ebf6d695d2019e8388beb9bd060194a9622ea7b2224",
        "ec3d578db264bcdb8f821782e84875256b587c9fc00c6d6edfdc6ad94014c222",
    ),
    (
        "monkey_c-block-5c868cf166ffac37",
        "44b6e3916d89bbf88c4f82cc0ec6e9d344b5516c3c1cc78f6564513cb2b2d343",
        "3a9c5db0beddbdec1c53ad64018ac6e0f57dbce105a530ca95e8007e95656367",
    ),
    (
        "muse-directive-4ec24396dc382bcf",
        "985302610acae05f911e08391cd348f5305caaa2d1373239f89dc326de2f89be",
        "74cb7f4e774348013a0e916447e9248faaa4390c122ee197811619bc2a122f2d",
    ),
    (
        "muse-directive-639cf3dea69c5991",
        "e0fd1a3dbd0251aba191de11b81e2c31c8580898cc1c036ff2e016c5895b453c",
        "58e1891ae70ce3414835767c1bbbc558b99736f31d2d55c5c3527f9d66b9d9d5",
    ),
    (
        "nasl-line-9cad4451e7bba322",
        "5bbc7756e024f0231065f95c896b86c54bb8671055e91a063dba53537b9336e0",
        "92ed4712488a85a21cc238ddbd430f0eb9f3295746f3a83554ed04b0781eb7f9",
    ),
    (
        "nasl-line-f60db92a6511e712",
        "9ceb9521c2e7e6ed10e2da239b2df7662d4456c2d4b7270b6f2c8525040f4961",
        "3b23db7c03a2d660ded7e3ad8e8fe199cf39e6264cb5736b08944eed89b235a3",
    ),
    (
        "nginx-line-a2bbe013a6995e37",
        "e71004c3dda0392c92a522e02e5e0e27113e753f7347c04685ce2bc3524a3a01",
        "1cf2a3faf54a536f054e7e32dd05c0769a38e73d302b6e2e2e66c52f59955ca9",
    ),
    (
        "nwscript-block-d6fc12138fd1e1ea",
        "3388b32f7c1d9bcb73e7a3b546c734127628f0719781e42db611a8f462bef3cc",
        "a06c99c0d0a086877dba71b4a4f1ea20e359065eed30b61fdecded4bb1ccc0b4",
    ),
    (
        "objective_c-block-ddd75d6545f28007",
        "a1398672138454034920fd0abc6b6d7cc698490c7d45cb0fba8088a384d99ea3",
        "20ce677768aab228e5c398590a920a9623efef611f429480b74c78c14eed1fb8",
    ),
    (
        "objective_c-line-e9fd2a9d9d8f00ea",
        "f5c39873148ce91b5217eceb5190d4489752c6946298cfccb96104eb9e2d1501",
        "1c9bebdfa6541039b2cf40637cbf229af02ad7c45884df11b9cfc3daee991fc3",
    ),
    (
        "objective_j-block-1759b24afc43171d",
        "8530452bf5f20ffa0d3e9b012123fbfe3109d586a1859eb6336826127462a95a",
        "805a48ecfa3b6748219746a8c6f741c7de4501d0a99fa32684cf752c4eb07ae9",
    ),
    (
        "openscad-block-b95f89ee57ce5ad6",
        "a41076b9ce7d3226efbb798cd3568753797eff0bda346769d5d500c126e606f8",
        "79afdb466d54916e7555a28b978b8a61ffbe07e02202cc998a32d64a8bc0fff9",
    ),
    (
        "pascal-block-5a7c03a4fcef552d",
        "450d82c0b2a4a7c514f4d98f7832ba787a8801cb5fe69edc317d3c4da153f121",
        "9b242a87934c7dd179cbe82704c0c31ef86bce8597adb04e9cd2943e10274b5f",
    ),
    (
        "pawn-line-b66a5469f24d67a9",
        "8c85ef8dd6977d2f62ef6b190efa0a1b89e81f15f3dc0c05b0efe4958db1cf2f",
        "9a0ae466994548ca376191f60cd40f4bb16a27351cd3ac0e0bde769c6f78312e",
    ),
    (
        "rescript-line-d29a447f266bcbef",
        "047b815f40f78b42aaaf30a2b295f72a5214eac202e73f54371d4f6d7da0511e",
        "fcaca15e8237f14d1b22bcdb6ce0c14a1fba247490cd27c08c1d9d900a9dead7",
    ),
    (
        "slice-block-82590a916c960a17",
        "77821be84f7bead4f70c532221b2f07848624dc15dcc9dc4bb3c1bea4b84f3dc",
        "e061f40e999235196d6340b76c1342ed3e8520b0d7632d16c1fa0e2f15534e4e",
    ),
    (
        "slice-block-fb24bcd65d80cb56",
        "5780132fc90f8f5a27c23b958f5903dffa783f1fac99d723967a08f3b5cc5389",
        "47051e946fa93a469c7c5a41353add84e74e72767a843d9dd54b25a86884796f",
    ),
    (
        "stylus-line-2f4b756bcfe24b28",
        "adc6ccb6cfcd0f64f49c8df7b795c450f858ba8a58eca684a3cb9848c853ab0b",
        "3edb67ad71b43c66afdb71d965c4f4b292eb884c5a363ef8746fce751be96727",
    ),
    (
        "unrealscript-block-74b4b76030a396b6",
        "b87100bada58958b10b9b37e88846812f24c4796325967c3896303eb1aec8e30",
        "bd60c6247eedf44fb4bd991624d1c25a019bd67d5f72f3ae76504d662849657a",
    ),
    (
        "zenscript-block-1a0b7384358c891f",
        "4f8ec9c614485f4b169b3448c6a107e8e42b81b57202a5c97944798bd91cd5d5",
        "408eb7d5ae32b976222c0756e85bcef31c9e017f608ade8642e0ac2c7e42373f",
    ),
    (
        "zenscript-block-829a390f5bc9cb46",
        "d4944e908b1bde871a2a4a976d6f81ef46dec64df2c834af019dad3e72161c1a",
        "a1f38e3792e550a1331f026ac45465087104c34bccd9e143364558f960cfbb13",
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


def _content_alphanumerics(language: str, raw_comment: str) -> str:
    if language == "batchfile":
        raw_comment = "\n".join(
            line.split(maxsplit=1)[1] if len(line.split(maxsplit=1)) == 2 else ""
            for line in raw_comment.split("\n")
        )
    elif language == "lolcode":
        raw_comment = "\n".join(
            line[3:].lstrip(" \t") if line.startswith("BTW") else line
            for line in raw_comment.split("\n")
        )
    return "".join(filter(str.isalnum, raw_comment))


@pytest.mark.parametrize(
    ("case_id", "raw_sha256", "expected_sha256"),
    CASE_PINS,
    ids=[case_id for case_id, _, _ in CASE_PINS],
)
def test_validated_padding_and_legacy_frame_regression(
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
    assert "".join(filter(str.isalnum, actual)) == _content_alphanumerics(
        language,
        normalized_raw,
    )


def test_oracle_conflicts_remain_deterministic_and_non_destructive() -> None:
    scaml = (
        '  /[if lt IF 9]\n   %script{:src => "http://html5shim.googlecode.com/svn/trunk/html5.js"}'
    )
    assert sanitize_comment("scaml", scaml) == (
        '[if lt IF 9]\n %script{:src => "http://html5shim.googlecode.com/svn/trunk/html5.js"}'
    )
    assert sanitize_comment("runoff", ".!++") == "++"


def test_validated_shapes_are_language_and_completeness_scoped() -> None:
    assert sanitize_comment("c", "#\N{NO-BREAK SPACE}title\n# body") == (
        "#\N{NO-BREAK SPACE}title\n# body"
    )
    assert sanitize_comment("gettext_catalog", "#: /single/path") == ": /single/path"
    assert sanitize_comment("hocon", "### title ###\n#setting = true") == (
        "## title ###\nsetting = true"
    )
    assert sanitize_comment("lookml", "#### heading ####") == "### heading"
    assert sanitize_comment("muse", "; *literal") == "*literal"
    assert sanitize_comment("rescript", "////*******literal") == "/*******literal"
    assert sanitize_comment("openscad", "/*** literal ***/") == "literal"


def test_incomplete_frames_do_not_activate_strict_unwrappers() -> None:
    assert sanitize_comment("less", "/* ======== *\\\n * title *") != "title"
    assert sanitize_comment("lex", "/*\n+--------+\n| title |\n*/") != "title"
    assert sanitize_comment("nwscript", "/*::////////////////////\n//:: title\n*/") != "title"
    assert (
        sanitize_comment(
            "applescript",
            "(*\n++++++++++++++++++++\n+++ title ++++\ncontent\n*)",
        )
        != "title"
    )


def test_validated_padding_and_frame_fuzz_is_deletion_only() -> None:
    generator = random.Random(0xC1A57E7)
    alphabet = string.ascii_letters + string.digits
    for _ in range(128):
        first = "".join(generator.choice(alphabet) for _ in range(generator.randint(1, 12)))
        second = "".join(generator.choice(alphabet) for _ in range(generator.randint(1, 12)))
        cases = (
            ("c#", f"/********* {first}\n {second} *********/", f"{first}\n{second}"),
            (
                "gettext_catalog",
                f"#: /{first}\n#: /{second}",
                f"/{first}\n/{second}",
            ),
            (
                "lookml",
                f"#### {first} ####\n### {second} #####",
                f"{first}\n{second}",
            ),
            ("rescript", f"////********{first}", first),
            (
                "less",
                f"/* ============ *\\\n * {first} *\n\\* ============ */",
                first,
            ),
        )
        for language, raw_comment, expected in cases:
            actual = sanitize_comment(language, raw_comment)
            assert actual == expected
            assert _is_subsequence(actual, raw_comment)
            assert "".join(filter(str.isalnum, actual)) == "".join(filter(str.isalnum, raw_comment))
