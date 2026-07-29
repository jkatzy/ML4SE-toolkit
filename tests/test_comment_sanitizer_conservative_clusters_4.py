"""SHA-pinned regressions for strict deletion-only scaffold shapes."""

from __future__ import annotations

import hashlib
import json
import random
import string
from pathlib import Path

import pytest

from ml4setk import sanitize_comment

pytestmark = pytest.mark.unit

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "comment_cleaning_regressions"

CASE_PINS = (
    (
        "cweb-block-067dba871d887926",
        "63eb8082e07aac71c971378235814216fd7fbf3f0ee84c59e7bb3bfede959056",
        "92ab5b1fc09494df227be6f1f1275e47feca4412a729b393cd5154ed4666cfc0",
    ),
    (
        "cweb-block-3ef4dae78a08e9d3",
        "0a28233c990604c58af1eedf5e73b88af04a3d912fb18c1d984ff856c69b2357",
        "944b3d6dc4001a15e5716f9c9d6d26147d0fd1da6a536de38301e4dc48f1aa30",
    ),
    (
        "cweb-block-d7af8cdf3491a001",
        "314912bee920497cdca2caf47b7277a79aa271921ae1a2993b27d4e34ea3b03e",
        "c7f2aa93907805c8d406929e28fe7376255c90aab42e7ce48cf42c7a16fafe7a",
    ),
    (
        "ec-block-4d0fa18415731789",
        "d8a797fa2d1d84b9b73635739bf716615e920cddbd9233e1b52437e3e58627f2",
        "6252f8de087d9b778ca058b3341eb04795013c4d82d43a065e896f5893f16a48",
    ),
    (
        "ec-block-283b8d26c8d04782",
        "4e7f5983781d0197904ff831d1ce9c4f956b8f7796f09a2dfec6e6412e3a2466",
        "e6790aa1ea60cb3420887dff2e41726a77e673985a90bf73391434cd1daf2b8e",
    ),
    (
        "rpc-block-c4b0009e7b87c2ff",
        "4097d73031b96689a334add6dbd5c8b71d3315fe87f8c029c8259aa5447db50a",
        "414fe7c27a361c6fa9c6ad24bca358f502c99a0f1909445012f43c58ba6b9726",
    ),
    (
        "vala-block-b979046a3e35ef50",
        "a4ba362b54f207976c60eb6f97a670fe5c94edec5dd88f7b0bcf90d90c51bcfb",
        "2bac8d5bcfb7f8373f055f282732796ebb01c014debcd0cc671e09c8c4c41430",
    ),
    (
        "vala-block-b9d42f5c106243b2",
        "498df88569bcef36fad65e00c7877b3b506f1f5661a01a4d6ba6e168ce9bf89b",
        "9fbe95e7f0497e9e581f65142bd3e2fbbe46987839e4580ffa1a33a79fbde5cb",
    ),
    (
        "grammatical_framework-nested-c37be78beac3f2ba",
        "ce665510d1f179d38946e20ca1918e72476eeef29e9290b92dca2db1c04b3756",
        "dc5d032708b2df3d9bdecc981a79701c07c8081bab673d93923d6f77777f84b8",
    ),
    (
        "grammatical_framework-nested-d684be7bb9cdffe6",
        "6b3094c9e577ed18b98b06fd69c7adc997af67d2b59bba5d3877b46b7a9d8266",
        "cf4220f475d249871d27e4339386b199be2260b4884420df6d3d1f332346bdf3",
    ),
    (
        "actionscript-block-b345087c18e7b1c1",
        "1c6d437e227450692a33e8db4129172247e82bfdbdc460283021bdb418798e24",
        "f940673cd358de28fa826ed2e5495a6944868c8711403987eb52f3dfd83237ca",
    ),
    (
        "cadence-line-016084206ca4673c",
        "1ca73d41a371918fe2b494573bce51f31fdc31a9c258803148fcfb0f018e4922",
        "c81ac6922d976c3ed283b7386546658a916cf0f9c795b16ee4a3c5ba8c9a5c4b",
    ),
    (
        "cadence-line-71c33a7f87c558c1",
        "daa5e3b91208457408cbf6cbea304abb5b8a56c3f4987a335a3b943dd21f4b3a",
        "754e1b6132afd94b535f320c3f5c62b26520e1b24aec7d86b8b1962520afa56b",
    ),
    (
        "coldfusion-block-b837df22b2b7c18b",
        "779623f5d6335f482c4a9c7938b2ab4ffdfacd87fd2fd0ab9218c992ffdf32ac",
        "848cf93547d083f8a414572e70469b504d8acc5905bf4146d9ddcc06ec915b61",
    ),
    (
        "erlang-line-1263a3b449e63681",
        "908234524a57be58152b5627942070e28d25a8d60bb3770749e181bd6518658a",
        "fef1eb43ee0f52a098048103b7f1553b4a999b13d74873e7443b5320672053c4",
    ),
    (
        "erlang-line-59abd22d7e085736",
        "7719d7fffedbe4ad5a2763518e7adf6fa8c519b1c372916e104e825265b7bcac",
        "30c9cba0e423a878f5eadb2620dd03ccefdc78073c87458eb517e20b3b6c1feb",
    ),
    (
        "erlang-line-64574d055b3bba7d",
        "815d54741e42ff241c771574deab51791c350b8e547e0499b580a9db77f8023c",
        "a10e89501865e074570d4f305af355bbbd78bb354c449769165c186dc7b34339",
    ),
    (
        "module_management_system-line-193893f43a9fc88a",
        "37170c33e563cd898008bbc5e2f97332d163dcd6dc7c304b0f4d669d39504c1a",
        "560b4e4419164c4e5c824bacce869856a9729b2a71d2f42a39cbbd973edc8676",
    ),
    (
        "module_management_system-line-4cf10551d63035e4",
        "82c91d73734f76b6f2782c9ff0d512da559b218a263114bae757de132eaf9121",
        "6c705509f74ea2a232610297f241e19db04952b5576c0aaeb6f57d4a85fbd54c",
    ),
    (
        "module_management_system-line-5412b2b677c450d2",
        "37170c33e563cd898008bbc5e2f97332d163dcd6dc7c304b0f4d669d39504c1a",
        "560b4e4419164c4e5c824bacce869856a9729b2a71d2f42a39cbbd973edc8676",
    ),
    (
        "apacheconf-line-dde3894f1538f06b",
        "39e2d1a4948e2d1dd82cfeb053107b1c5717de661de32c5734c02d17d3fddfef",
        "817360b681f581f464347d310dc3f23339f55049739b34ae2f7a9be75094fe0e",
    ),
    (
        "alloy-line-7aabcf5c8920be22",
        "0a63bc0b16e0e72fe862e0da0b1901a942c89e17552fa65a60195acf9465e932",
        "d40f5b4b36d6a8c809d01bf18a88ba0aac728da951e5189da92308d33df6027e",
    ),
    (
        "cycript-block-22dfe91f94413dea",
        "694f9c1b10c07aa78b4223ad81556ee392d58a2e00269e9695ad7c2c0021ef8f",
        "0800f107f72440902abe6e3e15bcca2ec481152835da4f822a547789c21e6cfa",
    ),
    (
        "macaulay2-block-ae80841dc337b93a",
        "f2c4eb2c73a3e03193d7542a9b07d3294edcb62169541611c95dd2926a55efaa",
        "0892a10ece1f933ee98f5d554601b28f8437801d1aa1b77799e4035ddcb6950c",
    ),
    (
        "macaulay2-block-fc7042fe4a4c38ea",
        "f2c4eb2c73a3e03193d7542a9b07d3294edcb62169541611c95dd2926a55efaa",
        "0892a10ece1f933ee98f5d554601b28f8437801d1aa1b77799e4035ddcb6950c",
    ),
    (
        "html_plusdjango-block-cadca7f36eea2903",
        "11ed6b8ab565955418f7e0133fbc2121b759f600f2c2f8be93e18824d00edd88",
        "aaf53e35777cb901a7caed11f6849d4527309fa6078d06b86556d0c45ec8f4b9",
    ),
    (
        "jinja-block-d93c869ca1d93dbf",
        "11ed6b8ab565955418f7e0133fbc2121b759f600f2c2f8be93e18824d00edd88",
        "aaf53e35777cb901a7caed11f6849d4527309fa6078d06b86556d0c45ec8f4b9",
    ),
    (
        "papyrus-line-75012529dff04a34",
        "14edf02f12460124ed061cf87c6586d3a26a3be2faf9a3ec51535ef202c50dda",
        "de50242a6ddd20e5c705bbda9489adc7c164bac0b2f48781949d7a701adaa77f",
    ),
    (
        "papyrus-line-8f073a058453eae2",
        "71466dcc425f1c12737923a1ee656989c63c8f2126c967c45576080ba866bc84",
        "ae43692b2a310b8ed2443d2b7d2a3e4cf0b6d73115badd72831b3d22381f235f",
    ),
    (
        "pawn-block-ef9569fadf1d00dc",
        "35f3381287e8f224f575c81cf594d3680a15affd200406b5d95a2d2bc7c9dea4",
        "37419a1dc22bfda032025d737592085fde5c1b8d1cac716c31ed01fc837812c3",
    ),
    (
        "webassembly-nested-086f71e391944596",
        "30d76734f8d366a74eef8875249b105bad71b93e0945cc3e5dbd1f9e2638d819",
        "d6b773e5f260f1f073ddce907b9be7ff1b667a531c041b6a3445fa1586e7ce67",
    ),
    (
        "webassembly-nested-f7bf664946f34ad0",
        "613bdf032ad35e42c4839397d0690943073b666f92a3e08b7e2d8ec974698516",
        "9b23a8b9ddccd7c407378f9cf141d4645c96eee28cf2c0b000e415b7df204ebd",
    ),
    (
        "sqf-line-1b5e666572091a4d",
        "da66cdba2509f32610e80c36bead1600330e1d5615ebd7b92c50d6417907c67b",
        "65a37b2748696f4c0612421750614a91f3e08af4ea3d2c0ef281e8064ea7a589",
    ),
    (
        "asn1-line-f200d2573a500515",
        "6149c1bbbca0df5bfc05a65bc75583e2fb0a692ef35625426f768a822bdac3a2",
        "6875ba28a1f0aa002116aa51d2fc1e293b4cfad96d2fb9e55e8e6646efb716eb",
    ),
    (
        "asn_1-line-074b2553e4e0f57f",
        "6149c1bbbca0df5bfc05a65bc75583e2fb0a692ef35625426f768a822bdac3a2",
        "6875ba28a1f0aa002116aa51d2fc1e293b4cfad96d2fb9e55e8e6646efb716eb",
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
def test_strict_scaffold_real_world_regression(
    case_id: str,
    raw_sha256: str,
    expected_sha256: str,
) -> None:
    language, raw_comment, expected = PINNED_CASES[case_id]
    assert hashlib.sha256(raw_comment.encode()).hexdigest() == raw_sha256
    assert hashlib.sha256(expected.encode()).hexdigest() == expected_sha256

    actual = sanitize_comment(language, raw_comment)

    assert actual == expected
    normalized_raw = raw_comment.replace("\r\n", "\n").replace("\r", "\n")
    assert _is_subsequence(actual, normalized_raw)


def test_symmetric_scaffold_fuzz_is_deletion_only() -> None:
    generator = random.Random(0xC1A55E4)
    alphabet = string.ascii_letters + string.digits
    for _ in range(256):
        words = [
            "".join(generator.choice(alphabet) for _ in range(generator.randint(1, 12)))
            for _ in range(generator.randint(1, 5))
        ]
        content = " ".join(words)
        cases = (
            ("cweb", f"/*++ {content} --*/"),
            ("cycript", f"/*-------- {content} --------*/"),
            ("html_plusdjango", f"{{## {content} ##}}"),
            ("jinja", f"{{## {content} ##}}"),
            ("macaulay2", f"-*- {content} -*-"),
            ("sqf", f"// * {content} *"),
        )
        for language, raw_comment in cases:
            actual = sanitize_comment(language, raw_comment)
            assert actual == content
            assert _is_subsequence(actual, raw_comment)


def test_scaffold_shapes_remain_language_scoped() -> None:
    assert sanitize_comment("c", "/*++ content --*/") == "++ content --"
    assert sanitize_comment("c", "// * content *") == "* content *"
    assert sanitize_comment("handlebars", "{{! ## content ## }}") == "## content ##"
