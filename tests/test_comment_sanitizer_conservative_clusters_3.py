"""SHA-pinned regressions for conservative nested and fixed-frame cleaning."""

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
        "ant_build_system-block-0d2d0796f080e172",
        "4323d20c6846f40dd8489f76e25713857edfe582d6a6e2f257281a997974ad02",
        "8641b3bc42acf603a0a97437bfe7e1d629696057abd0f5620c3fd9cfffe7ed97",
    ),
    (
        "ant_build_system-block-a18573e6f1dcd59a",
        "38e63dd6ddab32b310864f37b09113b3e790851a98be1ff3ee01febba21a157a",
        "31bd7ccaa6dfa50ca6924cfe1f17726899311c735e75ed1038567b7d243a099d",
    ),
    (
        "ant_build_system-block-a4061d3caf4c1257",
        "225dab3422720c1375623bd7a29ab96b775212eacc22a8f2479102bdb53b3d92",
        "e371ca9f658a3e5c104bc8ffdf0e2b8ca2f3d3180dfe35bf11682dcb234571eb",
    ),
    (
        "asn1-line-4371f62af8b45bf4",
        "7eadca6a65e454a1632675e6f3eb30d7a8ba49b6cfd81365d118b6a59b550ab4",
        "fd87f318d8b907cec952f99ad969f73c9f7219b7fb479a3f1e2e2597fd02a145",
    ),
    (
        "asn_1-line-23914fbdd8924b44",
        "7eadca6a65e454a1632675e6f3eb30d7a8ba49b6cfd81365d118b6a59b550ab4",
        "fd87f318d8b907cec952f99ad969f73c9f7219b7fb479a3f1e2e2597fd02a145",
    ),
    (
        "batchfile-line-f488b29503fb7d33",
        "99c250b73e3d9c00a8d5f3de605e348d5e4b10fbde80a201d5391eff9afdbc41",
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    ),
    (
        "c-block-96b308dcb2b2b658",
        "f6834a4cc599a133a45842844f47bfbfca4792bee81b208462a4ce824f8bd2ad",
        "887ea8c4ea8bf73ac542b780940bd47984abba1cda35c1fe24f2dd37dc52f870",
    ),
    (
        "c-block-96b308dcb2b2b658--requested-c-sharp-2d899f6fc9",
        "f6834a4cc599a133a45842844f47bfbfca4792bee81b208462a4ce824f8bd2ad",
        "887ea8c4ea8bf73ac542b780940bd47984abba1cda35c1fe24f2dd37dc52f870",
    ),
    (
        "c-block-96b308dcb2b2b658--requested-csharp-7fc218f23b",
        "f6834a4cc599a133a45842844f47bfbfca4792bee81b208462a4ce824f8bd2ad",
        "887ea8c4ea8bf73ac542b780940bd47984abba1cda35c1fe24f2dd37dc52f870",
    ),
    (
        "cap_cds-line-7f590f8266d9a995",
        "150b510922924ffbdb4a474d02045d40b42c0b3014b39b007de9e488ff226932",
        "bebf033999b52f27cc72fbd4491116d74f995db940bf8873deac4cb496231a85",
    ),
    (
        "common_lisp-line-197f61d54a7f842a",
        "125dd33495fe714f66d4d5e807f3ee89c9a8be37a099f3c3f0e026d08170508a",
        "a4780a3cc71b1d182c02b2bf5b04937335bd083060a634f004148ab105942219",
    ),
    (
        "css-block-4ffe4db311a0abe4",
        "981919218a69e64e2e2abb3f22fe48d78700e1737240e452ee8e63b3608dd05f",
        "b6a1bde98dad87ad3f55719698964131485540463dbcb01e7ddc5d6d6da71118",
    ),
    (
        "forth-line-c51e8c12329b12aa",
        "4d1d4e1061b04a5a96a7cd39cc54c42f3fea35fc03e438629efe20524dba5954",
        "74c9e3c1e1f10f2a7847ee1f72f4dc37740cdbce496162014a1f3bee4213d894",
    ),
    (
        "gams-line-36ad2b22e166143c",
        "9671cacb900faa91ca12a1aa9c2aff4e84583f58c79035dce5e97885fb0670b1",
        "4cfdfb43021126ba852d472ab8809c8c49e12ddbceb5e77849f7f9e32c26fa03",
    ),
    (
        "java_properties-line-99110cc7317eb2ac",
        "0ced727ef002146a45d4f3eeda6ca740a07f7ae75e6d4401209071cc2c4ef33f",
        "d70ceccc5b89fcc5ddf0dad7181481d29b2eb6ff0047be14cd3eef6e0b6b67b9",
    ),
    (
        "java_properties-line-e1f61e1717e92eae",
        "0ced727ef002146a45d4f3eeda6ca740a07f7ae75e6d4401209071cc2c4ef33f",
        "d70ceccc5b89fcc5ddf0dad7181481d29b2eb6ff0047be14cd3eef6e0b6b67b9",
    ),
    (
        "lark-line-f90ee87fd27198a4",
        "892d30f92cfbb1ca5ae8b146493e12efd0964d235e94d64e4a8717e26acdc79e",
        "ac9b402c683531de2413612ffa73a817f926df2773342de83a1106c47aee9c21",
    ),
    (
        "linker_script-block-22c593ca06029400",
        "088fe3d493567cd8ac0b5f694ac574b22299e553ad366ff436438abc2303dd8b",
        "ad694711ea39c68724a753fc46bc468a2b81a17bd2acf9931e69432cd257273d",
    ),
    (
        "lisp-line-2d19a37e083bc57b",
        "125dd33495fe714f66d4d5e807f3ee89c9a8be37a099f3c3f0e026d08170508a",
        "a4780a3cc71b1d182c02b2bf5b04937335bd083060a634f004148ab105942219",
    ),
    (
        "mcfunction-line-b25679636af10d25",
        "8fe0ec49c8766cf77589866401d3e0e763488cb826cf01fe49303aafe39f14ab",
        "dbcef528ac42a5faf93f30b7e04871be6cc28509dd2ffbfa08fd92c077d0d51e",
    ),
    (
        "nanorc-line-8810a2f833844a07",
        "a0d2d87ce2f3f40e9995a2a122fea44d23a2aab1e50106c69ed5ab1ab6b9eaf0",
        "f01e7c05beae8a1304092064d3fb6ab8edf3467ef27239333ba6a5da933bc092",
    ),
    (
        "ncl-line-b1896ff5b2411d2e",
        "ed7037ac7c5de4bbbee089d7ed8923bf18e3066e27753fb58f5978d96f19f1d4",
        "0131114274926b0ead7457ea540b0a4fba1bda147c011aa98103751238ff2724",
    ),
    (
        "nwscript-line-137e13688e36c3ec",
        "66cb3e9cecfba06aa0e2e5813c17cc18ddca9bec454b15e69424ff1f862c1bbd",
        "d9ddf955d94680af65df1ffd336b7bb866bf863a2632ad5f18fe4cb5e2b4ba88",
    ),
    (
        "nwscript-line-bbe93e29ea2d1d13",
        "e2dcca025b70bd25c101a24af87bb88ffe2b8dadd921857e15619ad833259677",
        "c708e878e214ea7688cbf0b27c9148e645d0af983743b91371950d89eb0cb3e0",
    ),
    (
        "nwscript-line-d44574f619a17e3b",
        "0e941527bdf6670e996ec3aa21e1ed0238751c96d21841a3bee9e6986e0fe81d",
        "0c12055a9f4595abb4fe5c8e1465e00394fbe0c6858d3a65f081af1ac62281a1",
    ),
    (
        "php-block-2d3fc839befc3725",
        "cdc61718d78ba4bbf84517f260af4d911000c1497ede200bc6dd57705cf73b98",
        "07d6cea34a85273ec1e31e5c25ae4c63a8ad5ad8efc611121f7948e23e9110e4",
    ),
    (
        "php-block-8b8d30aff4b195ef",
        "2a688c4d9fd9cf97743390d62efb0f6765315a8997b22cfa72fea942b5ac0fdb",
        "40cf527ba37d2d996f54b416823bac218496aee3651d03b220be54aa5559f8cd",
    ),
    (
        "rpc-block-640ae21dff22e6f1",
        "2a47c8a04e9a1967ed2df874d240b54100d5a1eb0af0f279cdd2616bfcd799f0",
        "280f8628a4fe49015965cfa6a82d69ac5245e3513780287baf07ef80e8661f2d",
    ),
    (
        "smarty-block-dfae83687e6b1bd7",
        "7256e7caf9d7566ed33571559499957ac8d004eb9dbf8afeef731481223be584",
        "02c176681d3b95cfd1ed6f380189feff8939307629c40b56b858ef339281e2a3",
    ),
    (
        "sqf-block-ac1b7b6e34050384",
        "8e91f167f280dedc296fdabec8f442300bd611690713207eb2c125ce44402107",
        "71883c064101352b0648ef91a99d838360eed7f04f0af022dfee370b34aaa5dd",
    ),
    (
        "tcsh-line-677347cab7c537aa",
        "c56c7cca4d2ed68e432733bcc50899410cb6cd5afcc05805e51c1e671a699b2b",
        "3928be1f3d969cdd11f1a0ec78c0dbb38e377eb20b563c36165503d670e65a4b",
    ),
    (
        "visual_basic-line-2e93337631719015",
        "ac9bfe4af6e471146aa91865586d767958615fbaf7337f4afbe662a1bdac8891",
        "2b6ae65a4e3c7bb08b839c57e2da6b09e9638928a8b82950a711bf715ec7974a",
    ),
    (
        "visual_basic-line-57789caa34832e63",
        "ac9bfe4af6e471146aa91865586d767958615fbaf7337f4afbe662a1bdac8891",
        "2b6ae65a4e3c7bb08b839c57e2da6b09e9638928a8b82950a711bf715ec7974a",
    ),
    (
        "visual_basic_net-line-0af40e0a6f69bdb4",
        "ac9bfe4af6e471146aa91865586d767958615fbaf7337f4afbe662a1bdac8891",
        "2b6ae65a4e3c7bb08b839c57e2da6b09e9638928a8b82950a711bf715ec7974a",
    ),
    (
        "visual_basic_net-line-54043eb692eb46ed",
        "ac9bfe4af6e471146aa91865586d767958615fbaf7337f4afbe662a1bdac8891",
        "2b6ae65a4e3c7bb08b839c57e2da6b09e9638928a8b82950a711bf715ec7974a",
    ),
    (
        "xbase-block-7964df0d282453ca",
        "a6d0ea1b16e7f62e5327b26f1402ac20e8c6fa5fe4c4bfeda5b11644c2ada38c",
        "48aad3a2bdf46df24eed1280efa1a21e7a84716a06f209c3081b3096e3f1b1ff",
    ),
    (
        "zephir-block-13889fb49222678a",
        "294947241651aacf93152411bb799ffa2dc4890199a1f70b8e30fbce1ea0bef3",
        "1a6162e3074d804f296cb2f3c569ae6bc74043f62e37b14054cb5bf2b7be966c",
    ),
    (
        "zephir-block-27f774454313588a",
        "155e0003d2623fdc3569a52ce6b9f11dbedd969aa535fae9ce631ecfeb643212",
        "fcfe32fc35fad9b1c35f2939f6df63391e6c1c1eccede8b17d9b14229d2b2894",
    ),
    (
        "zephir-block-47afd5ea76622313",
        "155e0003d2623fdc3569a52ce6b9f11dbedd969aa535fae9ce631ecfeb643212",
        "fcfe32fc35fad9b1c35f2939f6df63391e6c1c1eccede8b17d9b14229d2b2894",
    ),
    (
        "zephir-block-bd1086c41f127369",
        "e8faeeb91cf0bcc1c718eee1c1df900e7331c051c68d9bf14fd00368ee56a132",
        "ebb0c5b700e3c51d34eb0507fec532bae77d3d0309463baebc6416f9c8d9310f",
    ),
)


def _load_pinned_cases() -> dict[str, tuple[str, str, str]]:
    cases: dict[str, tuple[str, str, str]] = {}
    wanted = {case_id for case_id, _, _ in CASE_PINS}
    for path in FIXTURE_DIR.glob("*.json"):
        payload = json.loads(path.read_text(encoding="utf-8"))
        for section in ("sanitizer_cases", "oracle_exception_cases"):
            for row in payload.get(section, []):
                case_id = row["case_id"]
                if case_id not in wanted:
                    continue
                expected = row.get("expected_cleaned")
                if expected is None:
                    expected = row["oracle_exception"]["proposal"]["expected_cleaned"]
                cases[case_id] = (row["language"], row["raw_comment"], expected)
    assert cases.keys() == wanted
    return cases


PINNED_CASES = _load_pinned_cases()


@pytest.mark.parametrize(
    ("case_id", "raw_sha256", "expected_sha256"),
    CASE_PINS,
    ids=[case_id for case_id, _, _ in CASE_PINS],
)
def test_conservative_real_world_frame_regression(
    case_id: str,
    raw_sha256: str,
    expected_sha256: str,
) -> None:
    language, raw_comment, expected = PINNED_CASES[case_id]
    assert hashlib.sha256(raw_comment.encode()).hexdigest() == raw_sha256
    assert hashlib.sha256(expected.encode()).hexdigest() == expected_sha256
    assert sanitize_comment(language, raw_comment) == expected


def test_secondary_gutter_without_frame_evidence_is_preserved() -> None:
    raw_comment = "** alpha\n** beta\n** gamma"
    assert sanitize_comment("gams", raw_comment) == "* alpha\n* beta\n* gamma"


def test_secondary_gutter_preserves_markdown_and_unframed_shebang() -> None:
    markdown = "/*\n * # Heading\n * * item one\n * * item two\n */"
    assert sanitize_comment("css", markdown) == "# Heading\n* item one\n* item two"

    shebang = "#! /bin/csh -f\n#! Name: demo\n#! Purpose: test"
    assert sanitize_comment("tcsh", shebang) == "! /bin/csh -f\n! Name: demo\n! Purpose: test"


def test_unframed_secondary_gutter_fuzz_preserves_content() -> None:
    generator = random.Random(0xC0FFEE)
    alphabet = string.ascii_letters + string.digits
    for _ in range(128):
        words = [
            "".join(generator.choice(alphabet) for _ in range(generator.randint(1, 24)))
            for _ in range(generator.randint(3, 12))
        ]
        raw_comment = "\n".join(f"** {word}" for word in words)
        assert sanitize_comment("gams", raw_comment) == "\n".join(f"* {word}" for word in words)
