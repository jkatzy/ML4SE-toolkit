"""Focused regressions for deletion-only layout restoration."""

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
        "apacheconf-line-02ce3bab76d24c9c",
        "1ece369dc49fed74efda4a98ff43ababe81645eeec3fa288da2668c3f595881d",
        "c5ce1517c8457d29cec5d22be9b9ff2e896b42a8c327fab0c6e7737eded29ffa",
    ),
    (
        "blade-block-f908789547d4004d",
        "abfd75827970a2815f6aa53ca4961f638943502fbfeda40a1120eb43ec566d82",
        "95163f94d007f3a128c17216159b91cb5ab562724c62508ae5d9d38ffd7a34d8",
    ),
    (
        "chapel-nested-a6aba54e88ce6a2f",
        "9fa44d2b492ce1cc1e55137c0d0b0f49587fa47468878e5bffc9b63e8914d517",
        "785d6092e052c33385c96dbd56c1e659284fcafeef3ba8595919056c443b1d03",
    ),
    (
        "chapel-nested-e8fab64bd1815882",
        "268754f808ae4a018b216dc6235ba31388224634b1d0b579bed9e9eac032fdfd",
        "c79bf548fa5b6899dd79643512f6f6b47d27ff5da0e72ea7970d0f6675dd9a0e",
    ),
    (
        "dm-nested-37560f6933005679",
        "0b593fb8790ca53e5af9847a4d863f47f043f683f04d45f60e94743764349571",
        "4cfa73bc3fc5c582d76611a57d9fc5d8b96badee44ea6888c750eb944634e79d",
    ),
    (
        "dm-nested-e855b5dad973eb48",
        "3952e006916c2deeeb2c02968b9cec606f762ca9b99079d91568b6221b2f245c",
        "d611c2445b3263836b7a9bf5fb054117b56d9b444daf06a410bf71952cbc9ea6",
    ),
    (
        "euphoria-block-956270d48a959efc",
        "bef0970c493f909e4a14a3de117fd1ffd628439462ef31af00a5a7fdf5fff116",
        "dea327af5f693c415d781435b1cb73dbe4ebaaa0c5075d8632542dc526d946d8",
    ),
    (
        "f-line-753bf86641597258",
        "2bec1603cbfa5d167ff00fba7141902b4575cbc376adafcfa6f6e901e0a6da87",
        "c16f2aa135e3aa9a4a37eaae10b611fe6d05c9ceedbf7931797070fe83a65844",
    ),
    (
        "faust-block-078fdd1e9531a36b",
        "bf246bda35c247059e2996601831f5112780ce21a1254725485c8f821d67b29b",
        "b3bff7ddfa7773404591c51266c56fe4047717b085f456e5a01f7909ed944b37",
    ),
    (
        "faust-block-2fcdd32f33f9174c",
        "a488e18c6b9c7aca63fe747695816a7efa28356ad952f83f0b62e84f6cba53d3",
        "7ae8aebdbff8f786547a9c9decf8215bf005d83c8a4e6a403258f2d51c91b7bf",
    ),
    (
        "fortran_free_form-line-96be0e592e723099",
        "4aa1df5e0d1e843a873613041f0f4fc65ffbafe4665522a32b1c5e743d188945",
        "81a6568694e8ebb79f7a2d77abf1da21b4be4ca65a068477e0bb7d056640e404",
    ),
    (
        "fortran_free_form-line-9b428351db7400ff",
        "1f7ab4fc69aa6703ffbacb7939fab22f6f064ad59d4a26b6051cd9107ef7620a",
        "6ce81a28d0f217a42c0147cb5f3fa6f655a1c119266a7e91aa95a649e71467df",
    ),
    (
        "haml-line-b973f4f459cbe7e6",
        "a8979e87a6e13543bb99e3acbf4dd25dafab92bc42ccbe26da421ed4ae522578",
        "1803f41d423f218c6af92b2e2325b405aa3617fa512915213403de434e02534d",
    ),
    (
        "hy-line-f8032347ff3508bf",
        "552bea1b3953262c61f21a16cb07761354d0f7a569ea8833536d33073003737d",
        "fb9c391c0bcac8d4eec211ae99bfd477b2dc635ec399e14af0ace62ffeb5c8e8",
    ),
    (
        "jade-line-d117d9cd047f8347",
        "b7ce8fb297dff519ec8f15611bc7dd7c8c3c335b642a28d1fec3f98582c92ce8",
        "31809cf6057641d8d89a2318a8c1b366b5bd2370e3642185bfce12746e16803e",
    ),
    (
        "javascript-block-b4c60bb156f3b96b",
        "d55e349485be4162ce3a076b8dc01c82c9ff0b95ff2a1f2f5048e38ced905a27",
        "6ce8b4caa1fdf2efb04141e423d47b2d73462bb3ed9ff9fc03675899bd838367",
    ),
    (
        "jsx-block-cc5ccdd7665b9862",
        "d55e349485be4162ce3a076b8dc01c82c9ff0b95ff2a1f2f5048e38ced905a27",
        "64250518a344b212bf12d86824456a475a3059be5a8c0ca481f2c37bf7dfb4b1",
    ),
    (
        "liquid-block-13f35c9fbf185412",
        "1a2072a5bf8800f7646692583512580eda37a4e08b33f2b7c81a8f4346cf00bd",
        "6716c9dbbf33a7609cc84b05215f39c245b4f9d966a9f12843c3c67495d4bb8d",
    ),
    (
        "muse-directive-8a21125acb7ed97d",
        "d996531d659a88b56227e0dd9579005f8a14bf0232ae6e0f918cb9370e54af33",
        "8a65d17ec09ed4b1705fc6f844a59f6b5d8949a4013277deaefd36173aaa4e1d",
    ),
    (
        "nix-line-fcca42b104e91afa",
        "82f124f4436d320a1b73bb09a9ec73869fb3b6cca8e5a7fb193fed1ab35514c4",
        "52e4854a510570519562596f9937c8b027668bd1e2558d181dd3fa4624026a2b",
    ),
    (
        "prolog-block-cdb7b9e0ea6a9a96",
        "33422b4fb918089214643d4bc4b6c6fe5e71f7c6a9901b754dc2042e294713f6",
        "ec0325747129264936efb86867595a83d3100bac3d58e450ab0897b2a7efcfd4",
    ),
    (
        "robots_txt-line-f58c36c905889fb8",
        "eeab4de55b5d0a406f89b9b2f2a7a0c5ab8f5bb096b4d39807378f8437487bbc",
        "68715ef523c044f7b3c65a6032ee9efbc14b55d1ddbce5cff1fdd8c28317089e",
    ),
    (
        "rpc-block-9595657e40bcf45a",
        "eb5c50ff53993e9718b1073f58258dd1ad65f6833eb58df8b5b555b48ad09b6b",
        "9031202bff217642227f3def299acf693efc1caf541cad7802405bb42fd2bc72",
    ),
    (
        "shellcheck_config-line-fb4dabfc11af7963",
        "510ed414d31857a0e38fee69e480f449d084e661c304f824477606f9f1df65a9",
        "114344acb7b52123669054a55348ee03ba77e1cd7308a1443721e41b1ce9dc9b",
    ),
    (
        "unrealscript-block-679459953550b80a",
        "9389e6e8b3410375402b82e4a27989b9a8fc92452b33684fe10e3af07b2a6d06",
        "c71b9edf33880c7476dbc41cf418f209922c3f40c85f0201a689d17a048ed810",
    ),
    (
        "xml-block-751bdcb073fda965",
        "cdb8439b043eb0d3c4837081996007a48aa985a33b96245cf5879f790c8d6269",
        "a61a7deceefd1ded90f9261ddfc65d40ea6f53e8775844eb1f63a27ca062a9a6",
    ),
)


def _load_pinned_cases() -> dict[str, tuple[str, str, str]]:
    cases: dict[str, tuple[str, str, str]] = {}
    wanted = {case_id for case_id, _, _ in CASE_PINS}
    for path in FIXTURE_DIR.glob("*.json"):
        payload = json.loads(path.read_text(encoding="utf-8"))
        for row in payload.get("sanitizer_cases", []):
            case_id = row["case_id"]
            if case_id in wanted:
                cases[case_id] = (
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
def test_strict_restoration_matches_all_public_sanitizer_apis(
    case_id: str,
    raw_sha256: str,
    expected_sha256: str,
) -> None:
    language, raw_comment, expected = PINNED_CASES[case_id]
    assert hashlib.sha256(raw_comment.encode()).hexdigest() == raw_sha256
    assert hashlib.sha256(expected.encode()).hexdigest() == expected_sha256

    raw_match = QueryMatch("", "", raw_comment)
    sanitizer = CommentSanitizer(language)
    actuals = (
        sanitizer.sanitize(raw_comment),
        sanitizer.sanitize(raw_match),
        sanitize_comment(language, raw_comment),
        sanitize_comment_text(language, raw_match),
    )

    assert actuals == (expected,) * len(actuals)
    assert _is_subsequence(expected, raw_comment.replace("\r\n", "\n").replace("\r", "\n"))


def test_aliases_with_distinct_reviewed_layout_do_not_enter_exact_language_branches() -> None:
    _, fsharp_raw, _ = PINNED_CASES["f-line-753bf86641597258"]
    alias_expected = (
        "let rec createState (h : H) : S =\n"
        "   match h with\n"
        "       | Div a -> SDiv (a |> AList.toList |> List.map createState)\n"
        "       | T s -> ST s"
    )
    assert sanitize_comment("f_sharp", fsharp_raw) == alias_expected
    assert sanitize_comment("fsharp", fsharp_raw) == alias_expected

    _, jade_raw, _ = PINNED_CASES["jade-line-d117d9cd047f8347"]
    assert sanitize_comment("pug", jade_raw) == (
        ".item.item-icon-left.item-icon-right.bg-white("
        'ui-sref="scan({user: $root.project.model.user, '
        "project: $root.project.model.project, origin: 'setting'})\")\n"
        'img.item-icon-height-width.icon(src="./img/svg/account-add.svg")\n'
        "span.font-14.white 新增设备\n"
        'img.icon.right.img-item(src="./img/svg/arrow-right.svg")'
    )


def test_policy_sensitive_nearby_scaffolds_keep_their_existing_semantics() -> None:
    assert (
        sanitize_comment(
            "faust",
            "/* =============== DESCRIPTION ================= :\n\n- Pentatonic flute\n\n*/",
        )
        == "DESCRIPTION :\n\n- Pentatonic flute"
    )
    assert sanitize_comment("unrealscript", "//================") == ""
    assert sanitize_comment("robots_txt", "#__") == "__"
    assert sanitize_comment("xml", "<!-- Summary\n * details\n * more\n -->") == (
        "Summary\ndetails\nmore"
    )
    assert sanitize_comment("chapel", "/* Title\n * prose\n */") == "Title\nprose"
    assert sanitize_comment("haml", "  / note\n    continued") == "note\ncontinued"
    assert sanitize_comment("jade", "  //- note\n    continued") == "note\ncontinued"


@pytest.mark.parametrize("language", ["chapel", "dm"])
def test_tabbed_star_gutter_restoration_fuzz_is_exact_and_deletion_only(
    language: str,
) -> None:
    generator = random.Random(0x57A2)
    alphabet = string.ascii_letters + string.digits
    for _ in range(256):
        gutter_indent = " " * generator.randint(1, 4)
        padding = " " * generator.randint(1, 3)
        tab_width = generator.randint(1, 4)
        tab_prefix = "\t" * tab_width
        title = "".join(generator.choice(alphabet) for _ in range(12))
        first_item = "".join(generator.choice(alphabet) for _ in range(12))
        second_item = "".join(generator.choice(alphabet) for _ in range(12))
        first_tab_padding = padding if generator.choice((False, True)) else ""
        second_tab_padding = padding if generator.choice((False, True)) else ""
        raw_comment = (
            f"/*{padding}{title}\n"
            f"{gutter_indent}*{padding}Contains:\n"
            f"{gutter_indent}*{first_tab_padding}{tab_prefix}{first_item}\n"
            f"{gutter_indent}*{second_tab_padding}{tab_prefix}{second_item}\n"
            f"{gutter_indent}*/"
        )
        expected = f"{title}\nContains:\n{tab_prefix}{first_item}\n{tab_prefix}{second_item}"

        actual = sanitize_comment(language, raw_comment)

        assert actual == expected
        assert _is_subsequence(actual, raw_comment)
