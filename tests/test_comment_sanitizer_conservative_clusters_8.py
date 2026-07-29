"""Final-safe, SHA-pinned regressions for conservative comment cleaning."""

# ruff: noqa: E501

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

# These 78 cases were separately audited as having a deletion-only expected result.
# The conflicted RUNOFF 339998 case and DM e855 are deliberately not in this set.
CASE_PINS = {
    "basic-line-b6038018e4d44aae": (
        "2b5aaa0c1f63b54f3d29cef63ecaeb378b3b4118ea30152db4e4bb5ad938514b",
        "68583ce3920c61351ec6f643b48e21d601fe645f20a088caaf038b25457ad188",
    ),
    "chapel-nested-ac6b71a9b8d1899d": (
        "b5f5e2c79bc53c784df6b9ad507180e0a4d952e12f191edf4edc6165521f6d5e",
        "2c0d721c89790ac8e681fdf499606f9a49432a3fa31f4c10112b76d5c0eb6872",
    ),
    "coq-nested-bdb4d6c3e0e26dde": (
        "72963788445544bcb31d4c3703c08f8072157ee089f42caa458f53689b8b5783",
        "f6c6656238ff7fb0678854b4ff8dd31799b7f8b2428b18374025fcb68c39c19a",
    ),
    "cson-block-9f1e1ba2ad41e339": (
        "5ba30fddb6e0c117c28e3b846c7d92ef993cbc2c7a5e9fe1d94b62bb8810d253",
        "3a0feb072a37a826143ca5b19118c1cb6e73e2fe33569830d9e9abf50d0f3ed4",
    ),
    "csound_score-block-03423e278626d616": (
        "84ea62c4f505aa358a5f0d6e1ad95c84ffa8d5f22bf963fbe76079cc2500c814",
        "15b3323708012dd6e60a77e8672c2a95e23293edbb0eb3706042658af1dad096",
    ),
    "hoon-line-3efe19978cd95ad8": (
        "3ca7db2441d18edb217754615eb1d39fae692ba530cf088e0b5f780bc352e5c8",
        "8fca54ef8786a3ccfce3a9bf2b8136d810a6f9bb1f965b65ece0a48b0f8031b7",
    ),
    "jsx-block-52c3aed3ce348364": (
        "da78659b1a366eaae331c8dce24e03d4663100272e618569eeb7b5baa9911eda",
        "fda82ff02f4237cf2b30491de219ec3af7e3702a49f6a08ac5e0c0cc351dc9f4",
    ),
    "metal-block-80e5ff7359ed3dfc": (
        "bd8f0da040b7a09756b7df06ac567461a5601554e45490cdf1383e1ca476443a",
        "f9158e9e1e6517b5ba01e0f15fe74403d4fe82c92d4e35d99fb877ef8806e336",
    ),
    "monkey_c-block-19e822728e4ad251": (
        "9800567720a4c556779d919dcd62ef1de994f6adce1fa5ed571a25cf5bb2211c",
        "63778bce9a2243305952a1a8a4749bad1481d2b605cbfc23452859e31270b178",
    ),
    "moocode-block-10c021520bca655e": (
        "731bf742bee38772ea626552899339d2f5549246df0f2a517b7e032d79351962",
        "1ab245aebda631e97fe7f6245197454a0b1584bc67aa2693e5003a8cf728a519",
    ),
    "mupad-block-0d6002c3c3ff7e12": (
        "fc7d7e66660757ea246c2fcf6e835e7f75f82f080004f19816e74c0eb6300568",
        "721b68458f89a3f1fa707365e96636129a36351625977559d2034b6d5779540a",
    ),
    "pawn-block-e6956c51f991b22e": (
        "2667a14f5bb8da1615f2f7db96b5dd25b32889a23e9a28ce8f3e7bff9b843614",
        "c30cb1cd05a0892440dd720d380acbec14926cab5d8516f96331c09472c8a00e",
    ),
    "pike-block-14e4f8a2e539eec9": (
        "599b4f9ba7e364d4a61f472a431a097e789dfd484b7218738fa3aa46ba47d9a4",
        "83f3ceb239850cd59fad4f56e00deae86453bcc5b43b4ee8b7972b27ab9a5b64",
    ),
    "pike-block-186a538c8d37a564": (
        "599b4f9ba7e364d4a61f472a431a097e789dfd484b7218738fa3aa46ba47d9a4",
        "83f3ceb239850cd59fad4f56e00deae86453bcc5b43b4ee8b7972b27ab9a5b64",
    ),
    "pike-block-1d5b2e63380cea1d": (
        "599b4f9ba7e364d4a61f472a431a097e789dfd484b7218738fa3aa46ba47d9a4",
        "83f3ceb239850cd59fad4f56e00deae86453bcc5b43b4ee8b7972b27ab9a5b64",
    ),
    "pike-block-cebab9bbb33c685b": (
        "599b4f9ba7e364d4a61f472a431a097e789dfd484b7218738fa3aa46ba47d9a4",
        "83f3ceb239850cd59fad4f56e00deae86453bcc5b43b4ee8b7972b27ab9a5b64",
    ),
    "promela-block-0107db9716b95b6e": (
        "eb0f80009ca179fa8a0f8807caa55a721c7034f26b09b12140f73d05bbffce8b",
        "78fb50f5a148b100b2df0ba7747df80bb60ae9fff50a699c61cdbd0e14576e93",
    ),
    "q-line-c5fba6ebb317b121": (
        "0e4bd042d61f7bbb6a7d5f1b613bcd0f5191803f8ada7baac44e598c44727e16",
        "0ca4114bc6282ce6895c6128a135f847a58baba699cd9f2b2cea794cb8d2597d",
    ),
    "supercollider-nested-ad9446f40a31e7d9": (
        "36c6568bba7fcdf4b19b2c8c47f852c96e61a6ca2b87a1f9af8644fc06985e97",
        "37de89df9e39f33ec73b7bcee342eab56cb22869d20562fd7e4e147aad5a2ec7",
    ),
    "supercollider-nested-c792677afeb50802": (
        "cc01db2a8254a14c3e3cbe3ee806e1c38578da60c5424cb48e93188c5f8b9cb6",
        "73d91decbd8f5e841ed33b4a67a8eacd0719de837199798acbfb62de5251fa8e",
    ),
    "xml_property_list-block-47aeb800f1d95467": (
        "beb47aedee1717912c16ecf80a8ce3488d009a1431a105b6214e8e05b2677805",
        "c1b4d0a5222fca7833c47d18fbb48e16ae1ab09b6e714726476d09ee220d98dc",
    ),
    "xs-block-57c70df90223e3a1": (
        "8b4e867225b8da0c61fd1d6108bf37de11c25bad36618acac56aa8b9608f7ecf",
        "c669b357e39d3bea242c27097f2935284b8e1c7dc3159322ac7308fc9d8d03aa",
    ),
    "cobol-line-f55573105cb39c3f": (
        "c8961228ad8d10bb29bbe96a872c2767db122d6d660dcc99eddb68c981a63c88",
        "c5d88a047603c3dfdf5814276b3700989a90aaa8e8bd760dddf464a24652f597",
    ),
    "easybuild-line-8c9fae5c867bfec0": (
        "866d83c4fa889b45c4ea4e52c3db87223ea6007f54bdf559a9e0996e45337217",
        "b6b80828dc746e403065b6cc3093496483ad5625fdf8be49a9fe27a148d5fdf2",
    ),
    "elvish-line-d4950011ab6b81fe": (
        "d9c589487568e318585531f7c94685ac07914c69f445e2d4ed758a75e43dc469",
        "d944fcf530758031f731b45515298e4531dfac637a5922e0deb4433a909bf8d7",
    ),
    "mtml-block-14a6bab1df36fe7f": (
        "90598ad90183342ccce15fa84ea2e5fbb1bfe905d7b64567d66e94c79079991f",
        "d5707f5e696bd0d5de65638faa8d5f7fe79dc43fb2c75fcc6669c81baff2977d",
    ),
    "nanorc-line-d1556b57c7ff118d": (
        "e38ad414666f1d2fe7abebce872bb4ee3f53c18805e9459800b4329ac12a5d42",
        "8ecdb9d3715453e2b157e35a95bad1825112f7bac25602c6c1b4ece80ff79bf3",
    ),
    "parrot_internal_representation-line-d9245a7dc10c5709": (
        "bfc57e9f1f837a00216b66086ba5a376c98c04f206546806f712778ccf147fd3",
        "4ccaa2653fe14b3c99f4fa8d0ca0c8d1616b5a47d8cc82ba6179489c4ed38f62",
    ),
    "powershell-line-5dff6fa1541372f4": (
        "17c7ae935123171a2d44b614ba51044d8e67078ab605b72228b197da8e7df05b",
        "cc08973471730b8d7846b3ed87001c7bc8e2e37d62b7ee4ba6383f9f7117ff9d",
    ),
    "powershell-line-6c8cb2a8b60ce1a3": (
        "8935901d60be78c2a4a768267600aa69af383eb140168f1e63634445dcf1643d",
        "cf28a65e5120608db2297f1749cd60102d89ed4a02f2480fac59db4ad8f27eb1",
    ),
    "readline_config-line-e83c20cd64630034": (
        "b9a418108f637bf787eb2f5f86d464b1fa9c22a91650d539588415a7a459f2d3",
        "0bd50829ef680d46e6402ceb026d42c16cd5926eff00a9bccf7c850178f4897c",
    ),
    "rhtml-block-b9ef144f53447d44": (
        "29a7204236d6811450b2b7edc529f5ae01c16c8cc183ee085377ea1ab5d5f697",
        "19ac575975e1cbd887e859253b74e5d456c43de0644cca2e64c169e825309454",
    ),
    "routeros_script-line-b3a13578be0d5181": (
        "f1f9e58a6fd7dfc63d0d5cfe391de22550a9f98cadd23b48914a5d3a06331e85",
        "b0b4b1d98396ce6ec341faa75812211aacf41420d953b1c3b6a5e63f9010e158",
    ),
    "rpgle-line-e846c149d2d35fea": (
        "c16b31f47bbc7515578ff3e30f53af40811c4b62ec743658caefec9a93382ee3",
        "c786b41d012db3ad9c9ad2f9d80b7df1aa9f56c0e3bca52e12910111f259bb1b",
    ),
    "rpm_spec-line-edef6e8b9d0d60ec": (
        "1205b373c2386d46474ad2e5d12d2bc3541a0f99ddaf62ad29b35484dc5a9adb",
        "6da70544eb6f30831af961b74201b2d84d594ecebd2ca3626e853b0646ee45c0",
    ),
    "scss-line-867f8291c9d23948": (
        "460d22ba703098e881c6b865685cbdea0adc5ba657cbc85bfe6f7fafc2573620",
        "34499d7da80056de2821e9a906c73764d7a052c6f658e0a68e15a69a503c0269",
    ),
    "sieve-line-33777c4c998868fe": (
        "2ec81d07cca45228847de83a1cfe9f814b5fe67343247f0c5a47a97a6626747e",
        "4d8d0b1eba91ab20115d8f99af185936c0f7bb62b7a62db433c9028ddcd4633a",
    ),
    "slash-line-ff28ebed38b1c6f5": (
        "8167b998041b348b4de9cac76633dd68de0126ae75682afaa43c44739a163ebd",
        "3b4b8be518a6efa1b62d5328a960728fe2179b42e30be05daf523d7feb99e1e4",
    ),
    "smalltalk-line-2247eef810572f8f": (
        "a2f43ba15754869b88e1806ffe74bbf405f75e2cb49748da5685bc3f26591ef3",
        "604051b223a72f44fc21feed5191e535878e2ae3a6027ef563c041b5c97299e8",
    ),
    "sql-line-650f21879b8de3b8": (
        "210e18dfcfde97615dae82ccdcac05afc65a542581aa61ac36a2ee9ca76f830d",
        "4aabe42d31151ffcd4775a50f06f5692741c48d2d7b0325b86f3807f4474c92c",
    ),
    "stylus-line-eef3fbbfcfb4f349": (
        "82b10fe6bfec65f5b5ecb830c8369711557e6708c63767abb1d4eab96f4fad23",
        "28be339d3761bbcef7b677d556ba18e487a96b6872a767c469ab672a9a04f857",
    ),
    "tcl-line-32338121479b09e4": (
        "ca2e5220aff7af4a2565792e4e8f8fa05acffb960cbf39b3321a0efb06c4a499",
        "bc5c124a10d98c9744f6edac49a9da90b31636f8b2e242a08edf53d426b21355",
    ),
    "txl-line-1a16b199be4c8615": (
        "6474be3af95e35db22f2d008fada694baf5f051ad1578626f111e5cf074a1980",
        "27f19942b2fa511975d0b366ebe4afe0a9c376c999d3f356818281673a429b26",
    ),
    "vhdl-line-eded944db3842c29": (
        "1c2376a6e40633d2c16c3a2f7e28ba038ed1936b6bdb25e2420ddb81bc4afe64",
        "232b40cfa060258bf1abc51ebd7e00de6daeb5cf8a3dccb84238a300ca8704ed",
    ),
    "wavefront_object-line-83e7100288998680": (
        "bd53e39b7017ae871289b6421fa24b768a117ca3f3a1db975961f2288d34eeff",
        "89b1a9f2a91320e9db3132474d8833b9101c99c5c253d09d574e84d237b333e4",
    ),
    "wdl-line-f199d72e0d43a91d": (
        "b074d0579d983ec3a7a83c1a2240d910b426f6d1ea6a8beae3b77e59fb80225d",
        "51367deca1f95c768053e93723bdc9bca9ca12ac25dce7683df92072dc608379",
    ),
    "xbase-line-e97db82b4ca2d2a2": (
        "439be8b6a10bafc4cd323e293506691d2848f8d4775e043d53805ca851c9e108",
        "c6d6da5a2ccf84ea0a6d3d554c9bd91ad8b93e4d2b0f4d4217b1b3755fc94f89",
    ),
    "xml_property_list-block-28c17ebb8d66a99f": (
        "69b19b069270fa33304c59a716b2065037bb6c99de85ac28d31f5a8a4de0df68",
        "61348aeccb18b9f8c50fba1e1b0f465249a07971728526c54ddbbf32c0716c2a",
    ),
    "xtend-block-9d644462a6c03377": (
        "71bd0cae0b5a81ac44e5537ffeb93f6c571f6c377d6c38e6fcaab6f32b01d321",
        "d1edca3ff9573e6913209a25da8c22bddcb028711f1b8608e951194c07527ea7",
    ),
    "zimpl-line-299c8559db6d73bc": (
        "036d5bb5dc14b587c508c325812743c1f98af9ebc3be162cf0152a4064648dbb",
        "e0674c08405c851f851493d0fa81e8512dbdf9872e8ba920548c7edcf88e7803",
    ),
    "apex-block-10f87c23d2e61897": (
        "644babebeb2145d8d6844386f628a0761eccac7744bcbc6903c72cc56237aa56",
        "b7fb3b5b04a92612f76f8a811407f732246520adfa13dd50b726ecf9427f0956",
    ),
    "asn1-line-a12921c51cd41e04": (
        "63b0ffb3154031d7d946caac1a68a0c0ba8bc905490cde9400775985a161ceaa",
        "327a8c2318ee4bcd5865d05e670afe8077992f5f99161e306ae0861ef745b579",
    ),
    "asn_1-line-450a0c9c1c2664fd": (
        "26c28e94ff274654f2608f11009d35a16defce0435b54e0157f2e3041833f7a8",
        "6830788ac96ae8c4b17dcc14690250be9befb44db8fa38bdc3bb1ad92dd1b96d",
    ),
    "cobol-line-c5b42a0a980b4490": (
        "1a0ccde4ba947b31ab73d389e5a8058edaf5992011380a8d0b6034fb075d8285",
        "6a082ce6e5c66fd90706112e74081a795e31983925ffdc9f360966251113e2e2",
    ),
    "cuda-block-fea65387cbe82533": (
        "0ee16f2010c1f8d68fbfa8895c72a4f52bde41321e1897248d131dcb1e513a82",
        "bc93c8bd2f4e8f70b8300e56151d557484036b5db0f2d57734bddf36b0c62d8b",
    ),
    # Superseded by the authoritative repaired-run policy audit: the final
    # delimiter-only row is removed while its preceding blank line is retained.
    "cuda-line-9be1a4d25d76a815": (
        "22caff50931e203589724a066e1390de993b5061180fdee1fa7f4ef15b0ae08b",
        "d1b4dd38880377fa983c983cf40a598627d33e081998eeca22083e836eb81f7b",
    ),
    "dm-nested-e83321b0331aae0c": (
        "01f97207bb32706d340456d99c271f626bba13460ce81947a06a5c4304138e47",
        "9dcc524def66835ec36cb5302a42584cb718de3f988300dec34abbeb850a188f",
    ),
    "limbo-line-3e1cbd4afdb25b9b": (
        "0cb4573cec3258223018374df911ae0b4522e4dd8b16ac2fe94620ce177614fa",
        "8cff240eb6aefd92efbc955a14354d46597296ee7429abb2999a2e11cf24af41",
    ),
    # Superseded by the authoritative repaired-run policy audit: ``License``
    # is content inside the star frame, not part of the decorative edge.
    "makefile-line-04aa358fc4ea11c8": (
        "59cf3eaed91fdc6a2c885c7d1da622d2435c8d2f3d687a5563814909613ac0c9",
        "337ef31c2ef54b39626420e5fd36ad44cb7460c6cd7d187c27f08d260428929b",
    ),
    "metal-block-eba980b5d4b91997": (
        "97aeff97449326a19cd9fec0ba5a17e8a40783f02822becb759002ef115798bb",
        "c4056440c74f8a4d66a1ce222ad15f3aeee904a0cd70324cb070b775083e73b9",
    ),
    "motoko-nested-3c71454e62fcaa4e": (
        "5262ccf07d321c204976dd2f88b12ccee9bf05102f35aa3657261d3903316b1d",
        "e058c95ffb1ece6282d1df3ec25f9b9185abf94e12c62972671efec196d3fddf",
    ),
    "motoko-nested-e9a2bc0a96367f66": (
        "5262ccf07d321c204976dd2f88b12ccee9bf05102f35aa3657261d3903316b1d",
        "e058c95ffb1ece6282d1df3ec25f9b9185abf94e12c62972671efec196d3fddf",
    ),
    "mql5-line-5d961471001d4faa": (
        "2d529127897b0ee18c701132a51adef11d0122376f51c4c18c9a49bd1906526c",
        "ee8ec0a26e37862766ce70bc61b640fdf644ddf84dcf9cefd72f94e22c74a08e",
    ),
    "nextflow-block-008ca55e1da3e5d6": (
        "aa7e48a492be62dd476d2166283bae807fcd9f42b8d00660e1f61a60386242ab",
        "c9117f3de05a2bc5bcf4e09d2f6f3ed539fd3c7c8491949c828ed1ea675786ec",
    ),
    "nextflow-block-07311d11247641ec": (
        "efdda32d0ec67443f3be81591f1b28876cfa07e2e25bb15d78a1df1ee59d9c88",
        "e4de13d428812e4b5064458247e96ce1527591b0805a2a0ca0436b15aa474545",
    ),
    "opencl-block-3791a1dba23ca1f6": (
        "ca2dc2c6bdaaaa172a85d33cf76c5bb948dd1d5d493697ab469c9b1d5faa19cf",
        "28f5bba987db0b7ad7786a6e3411bcba7146fc82be087c868a8b3b8bfee2b7b1",
    ),
    "pep8-line-a87b47c8daeeb4ea": (
        "fc44626a53ecd65beda981451ad76635cc4b9bf01d3df548e7f3b0c437504341",
        "ca07c28b87d66bd90386befae7c50f3207caf68e366bcc921cfedd2522b3d56a",
    ),
    "routeros_script-line-407f9de0e9ccbb40": (
        "e60ba1e64ff962554f60f574574c1d6efddb8eeaa46dcea78ddfdd8bb1e7bdcd",
        "f3982d3229e4a89b0af74aaefb285fc34db87293d0a7498ea4d7e68d55b00f18",
    ),
    "verilog-line-c80f4d193a40534b": (
        "bd07065b1a51bd4b81f602d42351918b441970db6ca3ec3ac7496839368588a4",
        "1a11c94a0e471f60dabbf365196af66d3e2e3a8531de52cad1df513eec872517",
    ),
    "aidl-block-eaf73e966997d0f0": (
        "319213441f85d33adbecfcd62acfb7257f0026dc807f9e21be933daca755fe39",
        "301c06b732cb9f7fab5a0caf9c6276a5d446793d9564c3ae46a24615748346ec",
    ),
    "gn-line-c8ed500c7c0d6c16": (
        "263bfec766b654fb38d20b2d7cd67af6eb59093341b68de302d4d95e86040118",
        "23d1d69e08eea1ea8ae32118b1b8839fe3ed9a761f0e6663ddc1bba07a7f0429",
    ),
    "html_plus_php-line-d3d4538c06b70fa1": (
        "d984ecb58e334d6c51f3549b1a5c7b6e21b2f2929f0b5cef0e4aa5dc8553fcc5",
        "8c3f6f7dbf066ec6e7617dc947c75fddabf11df535fba6915cfbb3ec20c8d8d0",
    ),
    "logtalk-line-5bbae9d4dd0b637b": (
        "0d5bd1475fd61d1485ec53097363c9d28a31b194885fab31b2b9388dcf3bcdf0",
        "db5321461f14882824bbaf33666852e0c2e744932559690e020e0fcbb9b8db97",
    ),
    "logtalk-line-6775bd97bbb39ab0": (
        "82467e97e00fa78acb82768f5f2bafccda2f9d79b29f4e6156a847627a4b558c",
        "0b29b9c9d1c54214d7bcf018005e12c2306748cedd6b14693b48daffeab7e51d",
    ),
    "mql-line-995b093145ef5a66": (
        "ef9894341f734b5cdd872566b713eb1aefc0648650408d599b28cfb098e267c7",
        "500632169f1507edef1128e9d259e6ae1e4130ccf714652f0cf1b2d5ba7da50d",
    ),
    "mql4-line-a3e3115fc0af5cc2": (
        "ef9894341f734b5cdd872566b713eb1aefc0648650408d599b28cfb098e267c7",
        "500632169f1507edef1128e9d259e6ae1e4130ccf714652f0cf1b2d5ba7da50d",
    ),
    "proguard-line-dfadcb6dcef6af14": (
        "797fc08fdf7f20f57a80b1ce247118f421760b93c75c9e7f3a90bff42c07a113",
        "7bc079bd84eb9daaaf4c6e2209415e23bda601a1e98c0fa3c34da87155f06f29",
    ),
    "propeller_spin-block-852910b508fd06af": (
        "f7837a4290021b855f83ea0cf39dc095129321ddb19f0a20c39b007c0f973e1e",
        "706237d26c10655c6b96a6ea1741074de48f615736ae6a1d54b12eadc768ae63",
    ),
}

assert len(CASE_PINS) == 78
assert "dm-nested-e83321b0331aae0c" in CASE_PINS
assert "dm-nested-e855b5dad973eb48" not in CASE_PINS
assert "runoff-line-339998bf4316b7db" not in CASE_PINS


def _load_pinned_cases() -> dict[str, tuple[str, str, str]]:
    cases: dict[str, tuple[str, str, str]] = {}
    wanted = set(CASE_PINS)
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
    [
        (case_id, raw_sha256, expected_sha256)
        for case_id, (raw_sha256, expected_sha256) in CASE_PINS.items()
    ],
    ids=CASE_PINS,
)
def test_final_safe_real_world_regression_is_exact_and_deletion_only(
    case_id: str,
    raw_sha256: str,
    expected_sha256: str,
) -> None:
    language, raw_comment, expected = PINNED_CASES[case_id]
    assert hashlib.sha256(raw_comment.encode()).hexdigest() == raw_sha256
    assert hashlib.sha256(expected.encode()).hexdigest() == expected_sha256
    normalized_raw = raw_comment.replace("\r\n", "\n").replace("\r", "\n")
    assert _is_subsequence(expected, normalized_raw)

    actual = sanitize_comment(language, raw_comment)

    assert actual == expected
    assert _is_subsequence(actual, normalized_raw)


PRIOR_PASS_CONTROLS = (
    (
        "limbo-line-17c9b5107009c519",
        "limbo",
        "###################### Multipath Connection Information: ###############",
        "Multipath Connection Information:",
        "55291a5250821ce26133fd0eacc65d9e6faabef64cf69f7ed493cf9e415ecd30",
        "a6c6e8f319f16a7aaef6bdfef37d837cf92d172fb1e1795f5dde320c39dc7bf5",
    ),
    (
        "motoko-nested-3caf191235b4319f",
        "motoko",
        "/**\n"
        " * Module      : hex.mo\n"
        " * Description : Hexadecimal encoding and decoding routines.\n"
        " * Copyright   : 2019 Enzo Haussecker\n"
        " * License     : Apache 2.0\n"
        " * Maintainer  : Enzo Haussecker <enzo@dfinity.org>\n"
        " * Stability   : Experimental\n"
        " */",
        "Module      : hex.mo\n"
        "Description : Hexadecimal encoding and decoding routines.\n"
        "Copyright   : 2019 Enzo Haussecker\n"
        "License     : Apache 2.0\n"
        "Maintainer  : Enzo Haussecker <enzo@dfinity.org>\n"
        "Stability   : Experimental",
        "bea00f8c143b4841911563cda57b3e0cb7af28921dc4497c2bf0c24bfd32d405",
        "d18ffacd7ab16bf37378c604f39d7be466c2bddc5c5229285d06f4866190abd7",
    ),
    (
        "nextflow-block-bc6c462cd382ccca",
        "nextflow",
        "/*\n"
        " * -------------------------------------------------\n"
        " *  Nextflow config file\n"
        " * -------------------------------------------------\n"
        " */",
        "Nextflow config file",
        "eef8428f0e12b2572223a0d10887ee3b066884d6bc42c07d5fcb08035cef4ad8",
        "48e129817d0113236dc1972c389a4e61e15fd779ebba00692949b4c42f6d2c15",
    ),
    (
        "opencl-line-6fd02c46bad473f2",
        "opencl",
        "//===========================================================================\n"
        "// Copyright (c) 2017 The Khronos Group Inc.\n"
        "//\n"
        '// Licensed under the Apache License, Version 2.0 (the "License");\n'
        "// you may not use this file except in compliance with the License.\n"
        "// You may obtain a copy of the License at\n"
        "//\n"
        "//    http://www.apache.org/licenses/LICENSE-2.0\n"
        "//\n"
        "// Unless required by applicable law or agreed to in writing, software\n"
        '// distributed under the License is distributed on an "AS IS" BASIS,\n'
        "// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n"
        "// See the License for the specific language governing permissions and\n"
        "// limitations under the License.\n"
        "//===========================================================================",
        "Copyright (c) 2017 The Khronos Group Inc.\n"
        "\n"
        'Licensed under the Apache License, Version 2.0 (the "License");\n'
        "you may not use this file except in compliance with the License.\n"
        "You may obtain a copy of the License at\n"
        "\n"
        "   http://www.apache.org/licenses/LICENSE-2.0\n"
        "\n"
        "Unless required by applicable law or agreed to in writing, software\n"
        'distributed under the License is distributed on an "AS IS" BASIS,\n'
        "WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n"
        "See the License for the specific language governing permissions and\n"
        "limitations under the License.",
        "2eb54ef6c28864bbcbd5392b9872f39545f56920ad0f6cb6c2bc47afdd9a77b5",
        "069aef687a0584829f50fa4c3eaf3000234f544cb148f74ef88205b03714ea97",
    ),
)


@pytest.mark.parametrize(
    (
        "case_id",
        "language",
        "raw_comment",
        "expected",
        "raw_sha256",
        "expected_sha256",
    ),
    PRIOR_PASS_CONTROLS,
    ids=[row[0] for row in PRIOR_PASS_CONTROLS],
)
def test_prior_pass_controls_remain_exact(
    case_id: str,
    language: str,
    raw_comment: str,
    expected: str,
    raw_sha256: str,
    expected_sha256: str,
) -> None:
    assert case_id
    assert hashlib.sha256(raw_comment.encode()).hexdigest() == raw_sha256
    assert hashlib.sha256(expected.encode()).hexdigest() == expected_sha256
    actual = sanitize_comment(language, raw_comment)
    assert actual == expected
    assert _is_subsequence(actual, raw_comment)


PURE_RULER_CONTROLS = (
    (
        "sql-line-3961bceb6d1c7fad",
        "sql",
        "---------------------------------|--------|--------|--------|--------|--------|\r",
        "5c4c095e1f01fbce38c8ec27e9c7c6f59e42b9adeac763abe590661cbadefcc8",
    ),
    (
        "sql-line-5fbba174f11a9f1c",
        "sql",
        "--------|--------|--------|--------|---------------------|---------------------|\r",
        "f29f3d55446352001b9e3484744d3b44146bae488087f11bfe19b62855448b31",
    ),
    (
        "sql-line-95bc6c2777b6a204",
        "sql",
        "--------------------------------------------------------------------------------\r",
        "0905129ac9e7f0fb5ad7c04c518ddf3be5bf06ea6dbd0cccdc817b5a6eeb7550",
    ),
    (
        "sql-line-96b2adf9ac0f4d61",
        "sql",
        "-- --------------------------------------------------------------------------------\r",
        "6d65af942937436f521e9443f3c4b530ebe7275006a05536308cbfd92eccc4e2",
    ),
    (
        "sql-line-f4ba0f4dddb6b0ab",
        "sql",
        "--\r",
        "8e2a58dd919197d0bd51c24495e5af8e1f158e6b9b55744fa32e790c80658788",
    ),
    (
        "vhdl-line-18d3091023ec0308",
        "vhdl",
        "----------------------------------------------------------------------------------\r",
        "fa09531ad0bd50861817e181a23587bb3b83d1e8a5d0f304723b3f4f97d8a0c7",
    ),
    (
        "vhdl-line-5e1813ec9ca3c16d",
        "vhdl",
        "----------------------------------------------------------------------------------\r",
        "fa09531ad0bd50861817e181a23587bb3b83d1e8a5d0f304723b3f4f97d8a0c7",
    ),
)


@pytest.mark.parametrize(
    ("case_id", "language", "raw_comment", "raw_sha256"),
    PURE_RULER_CONTROLS,
    ids=[row[0] for row in PURE_RULER_CONTROLS],
)
def test_prior_pass_sql_and_vhdl_pure_rulers_stay_empty(
    case_id: str,
    language: str,
    raw_comment: str,
    raw_sha256: str,
) -> None:
    assert case_id
    assert hashlib.sha256(raw_comment.encode()).hexdigest() == raw_sha256
    assert sanitize_comment(language, raw_comment) == ""


def _token(generator: random.Random, length: int = 16) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(generator.choice(alphabet) for _ in range(length))


def test_hanging_indent_fuzz_preserves_payload_and_is_deletion_only() -> None:
    generator = random.Random(0xA11CE)
    for _ in range(48):
        heading = _token(generator)
        continuation = _token(generator)
        padding = " " * generator.randint(2, 10)
        raw_comment = f"/*  {heading}\n *{padding}{continuation}\n */"

        actual = sanitize_comment("chapel", raw_comment)

        assert actual != raw_comment
        assert actual.count(heading) == 1
        assert actual.count(continuation) == 1
        assert _is_subsequence(actual, raw_comment)


def test_fixed_card_fuzz_preserves_payload_and_is_deletion_only() -> None:
    generator = random.Random(0xCA4D5)
    for _ in range(32):
        content = _token(generator)
        width = len(content) + generator.randint(2, 12)
        horizontal = "-" * (width + 2)
        star_horizontal = "*" * (width + 4)
        padded = content.ljust(width)
        cards = (
            (
                "routeros_script",
                f"# +{horizontal}+\n# | {padded} |\n# +{horizontal}+",
            ),
            (
                "mql5",
                f"//+{horizontal}+\n//| {padded} |\n//+{horizontal}+",
            ),
            (
                "smalltalk",
                f'"{star_horizontal}"\n"* {padded} *"\n"{star_horizontal}"',
            ),
        )
        for language, raw_comment in cards:
            actual = sanitize_comment(language, raw_comment)
            assert actual != raw_comment
            assert actual.count(content) == 1
            assert _is_subsequence(actual, raw_comment)


def test_unframed_secondary_marker_fuzz_preserves_content_punctuation() -> None:
    generator = random.Random(0x5EC0D)
    for _ in range(48):
        heading = _token(generator)
        item = _token(generator)
        cell = _token(generator)
        warning = _token(generator)
        raw_comment = f"// ## {heading}\n// * {item}\n// | {cell} |\n// !! {warning}"
        expected = f"## {heading}\n* {item}\n| {cell} |\n!! {warning}"

        actual = sanitize_comment("c", raw_comment)

        assert actual == expected
        assert _is_subsequence(actual, raw_comment)


def test_proguard_triple_hash_does_not_enter_exact_double_hash_gate() -> None:
    raw_comment = "### keep both content hashes"
    expected = "## keep both content hashes"

    actual = sanitize_comment("proguard", raw_comment)

    assert actual == expected
    assert _is_subsequence(actual, raw_comment)


def test_propeller_spin_near_miss_preserves_deeper_indentation() -> None:
    raw_comment = "{{ Heading\r\n\r\n  body\r\n      deeper\r\n\r\n}}"
    expected = "Heading\n\n  body\n      deeper"

    actual = sanitize_comment("propeller_spin", raw_comment)

    assert actual == expected
    assert _is_subsequence(actual, raw_comment.replace("\r\n", "\n"))


@pytest.mark.parametrize("language", ["mql", "mql4", "mql5"])
def test_mql_card_keeps_nonempty_interior_pipe_content(language: str) -> None:
    raw_comment = "//+----------------+\n//| alpha | beta  |\n//+----------------+"
    expected = "alpha | beta"

    actual = sanitize_comment(language, raw_comment)

    assert actual == expected
    assert _is_subsequence(actual, raw_comment)


def test_unrelated_clean_ruler_content_is_unchanged() -> None:
    raw_comment = "alpha\n----- IMPORTANT -----\nomega"

    assert sanitize_comment("c", raw_comment) == raw_comment
