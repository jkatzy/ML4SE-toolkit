"""SHA-pinned real-world regressions for narrowly supported cleaner frames."""

# ruff: noqa: E501

from __future__ import annotations

import hashlib
import json
import random
import re

import pytest

from ml4setk import sanitize_comment

pytestmark = pytest.mark.unit

EXPECTED_CASE_IDS = frozenset(
    {
        "clean-nested-15586329cfbde571",
        "clean-nested-988f22861a2d06f9",
        "clean-nested-f50c942bd0b45132",
        "clean-nested-ff67f73b6eb3aebb",
        "cobol-line-9552e5d8f13890de",
        "cobol-line-9b0f246af81200f2",
        "cobol-line-b4f556bf9e9ea63d",
        "cobol-line-d2b6c383c7984a0b",
        "cobol-line-e0d3bf8ac4b232e2",
        "denizenscript-line-27c06dd2c1857ccd",
        "denizenscript-line-7c3583cbf39f3fac",
        "denizenscript-line-88d4bdd6a7752a2d",
        "denizenscript-line-9990a4ad0dee6975",
        "faust-block-278ee8d0b62fe768",
        "faust-block-d704a5c5c728a6bc",
        "faust-block-e17f8520726cd5b7",
        "faust-block-eafab09aa121607e",
        "faust-line-f459430c7870de5b",
        "gap-line-58a727678f658832",
        "gap-line-8a4b0550d104b342",
        "gap-line-9761e5bcc90caa30",
        "genero-line-104e774995e1ecc5",
        "genero-line-b75081a55b79022e",
        "genero-line-d9436cb8c45dd87a",
        "monkey-block-12808ff9605b7af6",
        "monkey-block-ed720fb7946ad0e9",
        "monkey-line-57881f48896cb800",
        "powerbuilder-line-0a5443c26f6d5ca4",
        "powerbuilder-line-4472e6cc98861812",
        "powerbuilder-line-682a801ecb551822",
        "win32_message_file-directive-788589bffafad54c",
        "win32_message_file-directive-79289e6926df4ccd",
        "win32_message_file-directive-7a8dffcc46b17cc8",
    }
)

CASES = json.loads(
    r"""
[
  {
    "case_id": "clean-nested-15586329cfbde571",
    "expected_cleaned": "A node selector represents the union of the results of one or more label queries over a\nset of nodes; that is, it represents the OR of the selectors represented by the node selector\nterms.",
    "expected_sha256": "792d5be7708af925937bbb18dd8a57bcb46174f09d623a6cbafa4cf741f348c5",
    "language": "clean",
    "oracle_input_sha256": "3ac5e3a2c86249092166532ee32da3c3b4cc1075bfd22a774333758060050a48",
    "raw_comment": "/**A node selector represents the union of the results of one or more label queries over a\n set of nodes; that is, it represents the OR of the selectors represented by the node selector\n terms.*/",
    "raw_sha256": "2f733db539d55124c07cfffdf375f0154d81342b6d1b704d0237c7b8d2d95735"
  },
  {
    "case_id": "clean-nested-988f22861a2d06f9",
    "expected_cleaned": "StatusCause provides more information about an api.Status failure, including cases when\nmultiple errors are encountered.",
    "expected_sha256": "cdcfb7548b42c9c036e33b74be9f94bb48e4e97e71ade22b3c3787b51e90eb31",
    "language": "clean",
    "oracle_input_sha256": "3982b9287edd6c9fb0ea833be9be37c1456ce090e3c82ed6372ad810405f6b6a",
    "raw_comment": "/**StatusCause provides more information about an api.Status failure, including cases when\n multiple errors are encountered.*/",
    "raw_sha256": "654ad4a288827e826195b24dffd205b6b7ca5f8d35a876fb0ffa020ffc493c06"
  },
  {
    "case_id": "clean-nested-f50c942bd0b45132",
    "expected_cleaned": "TokenReview attempts to authenticate a token to a known user. Note: TokenReview requests\nmay be cached by the webhook token authenticator plugin in the kube-apiserver.",
    "expected_sha256": "4c83d253361df9d91c1242510590632499efac96cdc139fa38ddc2ad13dc93f3",
    "language": "clean",
    "oracle_input_sha256": "85efde6cbee41561be7f9d909f5d5ee1eb1ce468d7a45be0593c0f0f976081ad",
    "raw_comment": "/**TokenReview attempts to authenticate a token to a known user. Note: TokenReview requests\n may be cached by the webhook token authenticator plugin in the kube-apiserver.*/",
    "raw_sha256": "94395d203160a416e22430c9803d28b668bac1b47b9d90bd2b3b9b341b9fc444"
  },
  {
    "case_id": "clean-nested-ff67f73b6eb3aebb",
    "expected_cleaned": "This NetworkPolicyIngressRule matches traffic if and only if the traffic matches both ports\nAND from.",
    "expected_sha256": "f0daee0a09570a587db5fda9f3299e55c06b9275941b76de081865c6d5de994c",
    "language": "clean",
    "oracle_input_sha256": "bc7e0c2ad24328f240bc3da872c778d8ca4591c286028200b7569405539d8f27",
    "raw_comment": "/**This NetworkPolicyIngressRule matches traffic if and only if the traffic matches both ports\n AND from.*/",
    "raw_sha256": "658ed05534f4b4e08a8272b676277173f631e6f54cab89e81519ac136abeecb6"
  },
  {
    "case_id": "cobol-line-9552e5d8f13890de",
    "expected_cleaned": "",
    "expected_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "language": "cobol",
    "oracle_input_sha256": "72196f14dd6d829fb2505b537b14b7ebee09bf0222930f851d429d9989332cc6",
    "raw_comment": "000010**************************************\r",
    "raw_sha256": "0bb13a089cceb12d8d8cc3d9ed710846f14617e152bc88eade8ed039ed16fcde"
  },
  {
    "case_id": "cobol-line-9b0f246af81200f2",
    "expected_cleaned": "",
    "expected_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "language": "cobol",
    "oracle_input_sha256": "231e20a538b5544d9015ec56b08424a8ec45fb95bc75748f27d6c728a97aa687",
    "raw_comment": "000010************************************************",
    "raw_sha256": "7c3e1ee6ac371650f532321ce7777fc6967691bdd18cfe630daf42406dab9e62"
  },
  {
    "case_id": "cobol-line-b4f556bf9e9ea63d",
    "expected_cleaned": "",
    "expected_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "language": "cobol",
    "oracle_input_sha256": "4aff7ef1b383e818a7012c0841f2e1f7ed1bcc10bdfba0af2f4f6edc3b4985b2",
    "raw_comment": "000600******************************************************************",
    "raw_sha256": "c564dd5cd519a37198fd2a59b4c736dfe0cea2096f275d9f8c138ef5ce70f958"
  },
  {
    "case_id": "cobol-line-d2b6c383c7984a0b",
    "expected_cleaned": "",
    "expected_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "language": "cobol",
    "oracle_input_sha256": "c124f570608949653f80b551a523c04b22d0e54b1fc98001b6c35acb20022a21",
    "raw_comment": "000010************************************************",
    "raw_sha256": "7c3e1ee6ac371650f532321ce7777fc6967691bdd18cfe630daf42406dab9e62"
  },
  {
    "case_id": "cobol-line-e0d3bf8ac4b232e2",
    "expected_cleaned": "",
    "expected_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "language": "cobol",
    "oracle_input_sha256": "af63caed25260a9c5fbf00c4cbecd9810b8fc45f35699ed5889168af2dab73f5",
    "raw_comment": "000010************************************************",
    "raw_sha256": "7c3e1ee6ac371650f532321ce7777fc6967691bdd18cfe630daf42406dab9e62"
  },
  {
    "case_id": "denizenscript-line-27c06dd2c1857ccd",
    "expected_cleaned": "@file\n\nCopyright (c) 2018, Intel Corporation. All rights reserved.<BR>\nSPDX-License-Identifier: BSD-2-Clause-Patent",
    "expected_sha256": "730ab19a4d2f6a68b053a3cca6154dfb2a84f6e6d6ca5668eedecc3f801ed143",
    "language": "denizenscript",
    "oracle_input_sha256": "32379d140fdfc9fdd654b5b46f06c12914a918ce5c7e25f0320cb145750fc672",
    "raw_comment": "## @file\n#\n#  Copyright (c) 2018, Intel Corporation. All rights reserved.<BR>\n#  SPDX-License-Identifier: BSD-2-Clause-Patent\n#\n##",
    "raw_sha256": "ab7bdb1a96f7c3ed4c06d0dba71d787ccd89e744dfa395d84c49826c4d5f4050"
  },
  {
    "case_id": "denizenscript-line-7c3583cbf39f3fac",
    "expected_cleaned": "ItemClear Command\n\nA drop-in command script to clear out dropped items around you.\n\n@author mcmonkey\n@date 2022-09-19\n@denizen-build REL-1777\n@script-version 1.0\n\nItemClear is a simple command to clear out dropped items near you. This is a very common staff utility.\nThis also stores a temporary copy of items deleted, so if you accidentally delete something important you can get it back.\nTemporary copies last 30 minutes before expiration, and can be accessed via clickable output from the command.\nThere is a maximum limit of 540 stacks (10 invs) saved at a time (with a 108 stack (2 invs) leeway range).\nThese times and limits can be configured via the config below this header.\n\nInstallation:\nJust put the script in your scripts folder and reload.\n\nUsage:\n/itemclear (range)\nRange defaults to 100 if unspecified.\n\nFor example: /itemclear\nOr: /itemclear 50\n\nPermission: dscript.itemclear",
    "expected_sha256": "1723913071d3c1fa6d6ae15b8cc04125e6d41e15b20e15ebfc3394c65291682f",
    "language": "denizenscript",
    "oracle_input_sha256": "65dfa395efecc0279b17832799c002bd5acb5ee8cb34c74400ff1d865f9c0be7",
    "raw_comment": "# +------------------\n# |\n# | ItemClear Command\n# |\n# | A drop-in command script to clear out dropped items around you.\n# |\n# +------------------\n#\n# @author mcmonkey\n# @date 2022-09-19\n# @denizen-build REL-1777\n# @script-version 1.0\n#\n# ItemClear is a simple command to clear out dropped items near you. This is a very common staff utility.\n# This also stores a temporary copy of items deleted, so if you accidentally delete something important you can get it back.\n# Temporary copies last 30 minutes before expiration, and can be accessed via clickable output from the command.\n# There is a maximum limit of 540 stacks (10 invs) saved at a time (with a 108 stack (2 invs) leeway range).\n# These times and limits can be configured via the config below this header.\n#\n# Installation:\n# Just put the script in your scripts folder and reload.\n#\n# Usage:\n# /itemclear (range)\n# Range defaults to 100 if unspecified.\n#\n# For example: /itemclear\n# Or: /itemclear 50\n#\n# Permission: dscript.itemclear\n#\n# ---------------------------- END HEADER ----------------------------",
    "raw_sha256": "e264e59e5c23bf41e9123dc13bc7f4db032e22683790a945471833f000816cce"
  },
  {
    "case_id": "denizenscript-line-88d4bdd6a7752a2d",
    "expected_cleaned": "This file contains 'Framework Code' and is licensed as such\nunder the terms of your license agreement with Intel or your\nvendor.  This file may not be modified, except as allowed by\nadditional terms of your license agreement.\n\n@file\nBpCommonPkg Package\n\nThis package provides common modules on Bailey Park.\nCopyright (c) 2012 - 2019, Intel Corporation. All rights reserved.<BR>\n\n   This software and associated documentation (if any) is furnished\n   under a license and may only be used or copied in accordance\n   with the terms of the license. Except as permitted by such\n   license, no part of this software or documentation may be\n   reproduced, stored in a retrieval system, or transmitted in any\n   form or by any means without the express written consent of\n   Intel Corporation.",
    "expected_sha256": "a2da9e08f3b498b0f514e09e2d0b97916379f8fcabc6e4c249622c7768ce645a",
    "language": "denizenscript",
    "oracle_input_sha256": "7a8ec5bc3b9e86152fcff7801a0e0acf3691f51d2fa9edcb2cb00153488f5849",
    "raw_comment": "#\n# This file contains 'Framework Code' and is licensed as such\n# under the terms of your license agreement with Intel or your\n# vendor.  This file may not be modified, except as allowed by\n# additional terms of your license agreement.\n#\n## @file\n# BpCommonPkg Package\n#\n# This package provides common modules on Bailey Park.\n# Copyright (c) 2012 - 2019, Intel Corporation. All rights reserved.<BR>\n#\n#    This software and associated documentation (if any) is furnished\n#    under a license and may only be used or copied in accordance\n#    with the terms of the license. Except as permitted by such\n#    license, no part of this software or documentation may be\n#    reproduced, stored in a retrieval system, or transmitted in any\n#    form or by any means without the express written consent of\n#    Intel Corporation.\n#\n##",
    "raw_sha256": "b865be8f83af0861d52b03c4ccc6b6a23811da237eacdab2eec2a9b0ea6a2d56"
  },
  {
    "case_id": "denizenscript-line-9990a4ad0dee6975",
    "expected_cleaned": "@file\n Platform description.\n\nCopyright (c) 2017 - 2018 Intel Corporation. All rights reserved.<BR>\n\nThis program and the accompanying materials are licensed and made available under\nthe terms and conditions of the BSD License which accompanies this distribution.\nThe full text of the license may be found at\nhttp://opensource.org/licenses/bsd-license.php\n\nTHE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN \"AS IS\" BASIS,\nWITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.",
    "expected_sha256": "15048e42483f735f59d5d2e20caeed5d0f9df3bbf7b4df9be565296efefabbb6",
    "language": "denizenscript",
    "oracle_input_sha256": "b73ee9334e76b9622140204e61855fb58d1570dc0ccaf2d12d9e3b46e3e9317d",
    "raw_comment": "## @file\n#  Platform description.\n#\n# Copyright (c) 2017 - 2018 Intel Corporation. All rights reserved.<BR>\n#\n# This program and the accompanying materials are licensed and made available under\n# the terms and conditions of the BSD License which accompanies this distribution.\n# The full text of the license may be found at\n# http://opensource.org/licenses/bsd-license.php\n#\n# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN \"AS IS\" BASIS,\n# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.\n#\n##",
    "raw_sha256": "f8a2316ca0063a009d83ee3b19123a154d0217493008ec1aac26154d95f52398"
  },
  {
    "case_id": "faust-block-278ee8d0b62fe768",
    "expected_cleaned": "AdminLTE v2.3.8\nAuthor: Almsaeed Studio\nWebsite: Almsaeed Studio <http://almsaeedstudio.com>\nLicense: Open source - MIT\n        Please visit http://opensource.org/licenses/MIT for more information",
    "expected_sha256": "54baf22e8f63c7aba71fa67b0b04188f61a792700ffb183dfb992040eadb6078",
    "language": "faust",
    "oracle_input_sha256": "796185360ea3483ed582c6449412b980032c7b0d0d6ed9499bdea11672ddab95",
    "raw_comment": "/*!\n *   AdminLTE v2.3.8\n *   Author: Almsaeed Studio\n *\t Website: Almsaeed Studio <http://almsaeedstudio.com>\n *   License: Open source - MIT\n *           Please visit http://opensource.org/licenses/MIT for more information\n!*/",
    "raw_sha256": "16eeae8a19f7642fd23be38c46ae0d93e1d7f489a92bb5437f7aead4d1c7cc55"
  },
  {
    "case_id": "faust-block-d704a5c5c728a6bc",
    "expected_cleaned": "DESCRITPION\n\nA simple bowed string model\n    - inputs: bow position (move it slowly to yield self-sustained oscillations!).\n    - outputs: two listening points on the string.\n    - controls: bow pressure and string stiffness.",
    "expected_sha256": "4d42a1251321e2495f5bf5bdd48c8b23ed743a99fde62633484038f526bc7a7e",
    "language": "faust",
    "oracle_input_sha256": "dc6693c0f1ed18793faac8f5f0aa783c1cb447b0ab6386c09c43deba4e629869",
    "raw_comment": "/* ========= DESCRITPION =============\n\nA simple bowed string model\n    - inputs: bow position (move it slowly to yield self-sustained oscillations!).\n    - outputs: two listening points on the string.\n    - controls: bow pressure and string stiffness.\n*/",
    "raw_sha256": "5491aeb93ffc0fe6691bd92457e9d84662f8e53b02ff1519059cd7ac552da4ed"
  },
  {
    "case_id": "faust-block-e17f8520726cd5b7",
    "expected_cleaned": "Modulo VCO\n\nEntradas:\n\t\n\t1) x_vco_in_frec1: frecuencia (para modular)\n\t2) x_vco_in_frec2: frecuencia (para modular)\n\t3) x_vco_in_pw: ancho de pulso (para modular)\n\t\nControles:\n\t\n\t1) x_vco_att_freq0: atenuador de la modulacion\n\t2) x_vco_att_freq1: atenuador de la modulacion\n\t3) x_vco_att_pw: atenuador de la modulacion pw\n\t4) x_vco_shape: forma de onda\n\t5) x_vco_freq: frecuencia\n\t6) x_vco_offset: desvío de frecuencia\n\t7) x_vco_pw: ancho de pulso\n\t8) x_vco_on-off ¿funciona como en Pd?\n\t\nSalidas:\n\n\t1) audio: en la API debe ser algo como 'x_vco_out'",
    "expected_sha256": "bb863407a63280231453dd6550f20cb85474161db9f8126a328d8971ad45c062",
    "language": "faust",
    "oracle_input_sha256": "df25dfeba61463302bfcff9da881aeb979c6acdcec10e748a1ad0e07687fa148",
    "raw_comment": "/*\t############\n\t Modulo VCO\n\t############\n\t\n\tEntradas:\n\t\t\n\t\t1) x_vco_in_frec1: frecuencia (para modular)\n\t\t2) x_vco_in_frec2: frecuencia (para modular)\n\t\t3) x_vco_in_pw: ancho de pulso (para modular)\n\t\t\n\tControles:\n\t\t\n\t\t1) x_vco_att_freq0: atenuador de la modulacion\n\t\t2) x_vco_att_freq1: atenuador de la modulacion\n\t\t3) x_vco_att_pw: atenuador de la modulacion pw\n\t\t4) x_vco_shape: forma de onda\n\t\t5) x_vco_freq: frecuencia\n\t\t6) x_vco_offset: desvío de frecuencia\n\t\t7) x_vco_pw: ancho de pulso\n\t\t8) x_vco_on-off ¿funciona como en Pd?\n\t\t\n\tSalidas:\n\t\n\t\t1) audio: en la API debe ser algo como 'x_vco_out'\n\n*/",
    "raw_sha256": "b27644965e7c2f07878ac4984f640d7cfa8591b3f08fa0494f6f71e08557bf2f"
  },
  {
    "case_id": "faust-block-eafab09aa121607e",
    "expected_cleaned": "DESCRIPTION :\n\n- Pentatonic flute\n- Rocking = playing all notes from low to high frequencies\n- Left = Silence/Slow rhythm\n- Right = Fast rhythm\n- Head = Reverberation\n- Front = long notes\n- Back = short notes",
    "expected_sha256": "f619c994fe380a9895f513dd68318fe194dcbd874812c6ae676a31e75a3d4a7b",
    "language": "faust",
    "oracle_input_sha256": "074cdcdaa71cc0aaa8e10fb3261c522266caa71f3622f1f70e0a610432fadf04",
    "raw_comment": "/* =============== DESCRIPTION ================= :\n\n- Pentatonic flute\n- Rocking = playing all notes from low to high frequencies\n- Left = Silence/Slow rhythm\n- Right = Fast rhythm\n- Head = Reverberation\n- Front = long notes\n- Back = short notes\n\n*/",
    "raw_sha256": "552cfb38848eb2bf854ecabcdcf73ed146c6b2e976381e37ff53b4295e1f3b97"
  },
  {
    "case_id": "faust-line-f459430c7870de5b",
    "expected_cleaned": "`diodeLadder`\n4th order virtual analog diode ladder filter. In addition to the individual\nstates used within each independent 1st-order filter, there are also additional\nfeedback paths found in the block diagram. These feedback paths are labeled\nas connecting states. Rather than separately storing these connecting states\nin the Faust implementation, they are simply implicitly calculated by\ntracing back to the other states (s1,s2,s3,s4) each recursive step.\n\nThis filter was implemented in Faust by Eric Tarr during the\n[2019 Embedded DSP With Faust Workshop](https://ccrma.stanford.edu/workshops/faust-embedded-19/).\n\nModified by Christopher Arndt to change the cutoff frequency param\nto be given in Hertz instead of normalized 0.0 - 1.0.\n\n#### References\n\n* <https://www.willpirkle.com/virtual-analog-diode-ladder-filter/>\n* <http://www.willpirkle.com/Downloads/AN-6DiodeLadderFilter.pdf>\n\n#### Usage\n\n```\n_ : diodeLadder(normFreq,Q) : _\n```\n\nWhere:\n\n* `freq`: cutoff frequency (20-20000 Hz)\n* `Q`: filter Q (0.707 - 25.0)",
    "expected_sha256": "d0e74402128907c32cbee99a7ab9237119b4785ec0e74e84c995c3a8da781557",
    "language": "faust",
    "oracle_input_sha256": "fd50b10e92ac3fe1e64b1829d78d2f949828e06a31a1eea35c9af8a5ccf45b95",
    "raw_comment": "//------------------`diodeLadder`-----------------\n// 4th order virtual analog diode ladder filter. In addition to the individual\n// states used within each independent 1st-order filter, there are also additional\n// feedback paths found in the block diagram. These feedback paths are labeled\n// as connecting states. Rather than separately storing these connecting states\n// in the Faust implementation, they are simply implicitly calculated by\n// tracing back to the other states (s1,s2,s3,s4) each recursive step.\n//\n// This filter was implemented in Faust by Eric Tarr during the\n// [2019 Embedded DSP With Faust Workshop](https://ccrma.stanford.edu/workshops/faust-embedded-19/).\n//\n// Modified by Christopher Arndt to change the cutoff frequency param\n// to be given in Hertz instead of normalized 0.0 - 1.0.\n//\n// #### References\n//\n// * <https://www.willpirkle.com/virtual-analog-diode-ladder-filter/>\n// * <http://www.willpirkle.com/Downloads/AN-6DiodeLadderFilter.pdf>\n//\n// #### Usage\n//\n// ```\n// _ : diodeLadder(normFreq,Q) : _\n// ```\n//\n// Where:\n//\n// * `freq`: cutoff frequency (20-20000 Hz)\n// * `Q`: filter Q (0.707 - 25.0)\n//---------------------------------------------------------------------",
    "raw_sha256": "cf5b76bb9210ee15445a406656a25079ded33d394ac9618a5a86b038585759ac"
  },
  {
    "case_id": "gap-line-58a727678f658832",
    "expected_cleaned": "F CompatibilityLevelOfMultiplicitySequences(M)\nThe input is a list of two multiplicity sequences.\nThe output is the maximum level where the tree\ncan ramify. It can be infinite if both sequences are\nequal.\nImplementation done with G. Zito",
    "expected_sha256": "8a6cccda4664b834428965b9b440e5e31586471636740f7325d62e86e2c174e6",
    "language": "gap",
    "oracle_input_sha256": "1c55d605490068bfc65c0efe5c98175d00df82c24a539691f13e71e97d4f0680",
    "raw_comment": "#################################################\n##\n#F CompatibilityLevelOfMultiplicitySequences(M)\n## The input is a list of two multiplicity sequences.\n## The output is the maximum level where the tree\n## can ramify. It can be infinite if both sequences are\n## equal.\n## Implementation done with G. Zito\n#################################################",
    "raw_sha256": "10404306c51a22fb50590ce8614ec07e360cec9b7196db97b1ea7963756b3778"
  },
  {
    "case_id": "gap-line-8a4b0550d104b342",
    "expected_cleaned": "W  grppclat.gd                GAP library                   Alexander Hulpke\n\n\nY  Copyright (C)  1997\nY  (C) 1998 School Math and Comp. Sci., University of St Andrews, Scotland\nY  Copyright (C) 2002 The GAP Group\n\nThis  file contains declarations for the subgroup lattice functions for\npc groups.",
    "expected_sha256": "dec54a713db64056d34ea4409311c5bd6953c478ad669f4c223ad459a7062c4a",
    "language": "gap",
    "oracle_input_sha256": "61d30f11387d546b49e5d2bba57ce415d818222bd075416961c42b26e1a75998",
    "raw_comment": "#############################################################################\n##\n#W  grppclat.gd                GAP library                   Alexander Hulpke\n##\n##\n#Y  Copyright (C)  1997  \n#Y  (C) 1998 School Math and Comp. Sci., University of St Andrews, Scotland\n#Y  Copyright (C) 2002 The GAP Group\n##\n##  This  file contains declarations for the subgroup lattice functions for\n##  pc groups.\n##",
    "raw_sha256": "d2301d49f3d92a31cacc70ac22f55e8b3ddaa0de52f6ef02e9a810282c1812b3"
  },
  {
    "case_id": "gap-line-9761e5bcc90caa30",
    "expected_cleaned": "W  global.gi                   GAP library                      Steve Linton\n\n\nY  Copyright (C)  1996,  Lehrstuhl D für Mathematik,  RWTH Aachen,  Germany\nY  (C) 1998 School Math and Comp. Sci., University of St Andrews, Scotland\nY  Copyright (C) 2002 The GAP Group\n\n\nThis file contains the second stage of the \"public\" interface to\nthe global variable namespace, allowing globals to be accessed and\nset by name.\n\nThis is defined in two stages. global.g defines \"capitalized\" versions\nof the functions which do not use Info or other niceties and are not\nset up with InstallGlobalFunction. This can thus be read early, and\nthe functions it defines can be used to define functions used to read\nmore of the library.\n\nThis file and global.gd   install the really \"public\"\nfunctions and can be read later (once Info, DeclareGlobalFunction,\netc are there)\n\nAll of these functions give a warning at level 2 if the global\nvariable name contains characters not recognised as part of\nidentifiers by the GAP parser\n\nFunctions that read data give Info messages at level 3 for InfoGlobal\nFunctions that change data give Info messages at level 2 for InfoGlobal",
    "expected_sha256": "156a343b64fe9b0ba8dca0e1216c07a9138eadbe2fcdfcfdfbb505aec944a54d",
    "language": "gap",
    "oracle_input_sha256": "0082ac631dcce188e298aa1a5076ce8e03b51a4fd80170e99d5633e028092d18",
    "raw_comment": "#############################################################################\n##\n#W  global.gi                   GAP library                      Steve Linton\n##\n##\n#Y  Copyright (C)  1996,  Lehrstuhl D für Mathematik,  RWTH Aachen,  Germany\n#Y  (C) 1998 School Math and Comp. Sci., University of St Andrews, Scotland\n#Y  Copyright (C) 2002 The GAP Group\n##\n##\n##  This file contains the second stage of the \"public\" interface to\n##  the global variable namespace, allowing globals to be accessed and\n##  set by name.\n##\n##  This is defined in two stages. global.g defines \"capitalized\" versions\n##  of the functions which do not use Info or other niceties and are not\n##  set up with InstallGlobalFunction. This can thus be read early, and\n##  the functions it defines can be used to define functions used to read\n##  more of the library.\n##\n##  This file and global.gd   install the really \"public\"\n##  functions and can be read later (once Info, DeclareGlobalFunction,\n##  etc are there)\n##\n##  All of these functions give a warning at level 2 if the global\n##  variable name contains characters not recognised as part of\n##  identifiers by the GAP parser\n##\n##  Functions that read data give Info messages at level 3 for InfoGlobal\n##  Functions that change data give Info messages at level 2 for InfoGlobal\n##",
    "raw_sha256": "b881cf0aac17416b8fb72e810a93fa7bea70418904adf6bc1b6ce67867164cff"
  },
  {
    "case_id": "genero-line-104e774995e1ecc5",
    "expected_cleaned": "Aubit SQL Access Program ASQL\nCopyright (c) 2003-5 Aubit Computing Ltd\nProduction of this software was sponsored by\n                Cassens Transport Company\nThis program is free software; you can redistribute it and/or modify\nit under the terms of one of the following licenses:\n\n A) the GNU General Public License as published by the Free Software\n    Foundation; either version 2 of the License, or (at your option)\n    any later version.\n\n B) the Aubit License as published by the Aubit Development Team and\n    included in the distribution in the file: LICENSE\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of both licenses referred to here.\nIf you did not, or have any questions about Aubit licensing, please\ncontact afalout@ihug.co.nz",
    "expected_sha256": "a6aa9264f996129b688ec2258c9e38ba9cc2e46ce3634dd275c52d03a5e4c4c7",
    "language": "genero",
    "oracle_input_sha256": "6b6d1eeba1788774ce9518323e2741a665ce79367b818c8b7912fd95a6b91374",
    "raw_comment": "# +----------------------------------------------------------------------+\n# | Aubit SQL Access Program ASQL                                        |\n# +----------------------------------------------------------------------+\n# | Copyright (c) 2003-5 Aubit Computing Ltd                             |\n# +----------------------------------------------------------------------+\n# | Production of this software was sponsored by                         |\n# |                 Cassens Transport Company                            |\n# +----------------------------------------------------------------------+\n# | This program is free software; you can redistribute it and/or modify |\n# | it under the terms of one of the following licenses:                 |\n# |                                                                      |\n# |  A) the GNU General Public License as published by the Free Software |\n# |     Foundation; either version 2 of the License, or (at your option) |\n# |     any later version.                                               |\n# |                                                                      |\n# |  B) the Aubit License as published by the Aubit Development Team and |\n# |     included in the distribution in the file: LICENSE                |\n# |                                                                      |\n# | This program is distributed in the hope that it will be useful,      |\n# | but WITHOUT ANY WARRANTY; without even the implied warranty of       |\n# | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        |\n# | GNU General Public License for more details.                         |\n# |                                                                      |\n# | You should have received a copy of both licenses referred to here.   |\n# | If you did not, or have any questions about Aubit licensing, please  |\n# | contact afalout@ihug.co.nz                                           |\n# +----------------------------------------------------------------------+",
    "raw_sha256": "42968276a7bb71087908685b68aa80c695d6da7adcbde7e9dd06b409c560e676"
  },
  {
    "case_id": "genero-line-b75081a55b79022e",
    "expected_cleaned": "Prog. Version..: '5.25.02-11.03.23(00010)'\n\nPattern name...: cemt100.4gl\nDescriptions...: 重要设备维保记录作业\nDate & Author..: 18/07/27 By lixwz",
    "expected_sha256": "f030585693718d0d89a2fdec572f2525cccc854a9b4c0f0e5e820d6b8a75022b",
    "language": "genero",
    "oracle_input_sha256": "8e8ae41dead088a3811389c244dc2ac6688e8b76303cb0176c004eaa1f132786",
    "raw_comment": "# Prog. Version..: '5.25.02-11.03.23(00010)'     #\n#\n# Pattern name...: cemt100.4gl\n# Descriptions...: 重要设备维保记录作业\n# Date & Author..: 18/07/27 By lixwz",
    "raw_sha256": "cce75a356d1dcbb71a9c86d0768d95c71b4b7651f124eea96b12b643db0cd422"
  },
  {
    "case_id": "genero-line-d9436cb8c45dd87a",
    "expected_cleaned": "Prog. Version..: '5.25.02-11.03.23(00000)'\n\nPattern name...: axmt620.4gl\nDescriptions...: 出貨單維護作業\nDate & Author..: 95/01/05 By Roger\nModify.........: No.FUN-4A0081 05/08/09 By saki 指定單據編號、執行功能\nModify.........: No.TQC-640011 06/03/01 By echo 將單號cahr(10)放大至char(16)\nModify.........: No.FUN-680137 06/09/04 By flowld 欄位型態定義,改為LIKE\nModify.........: No.FUN-6A0094 06/10/25 By yjkhero l_time轉g_time\nModify.........: No.FUN-710016 07/01/19 By kim GP3.6 行業別架構\nModify.........: No.FUN-730018 07/03/28 By kim 行業別架構\nModify.........: No.FUN-7C0017 08/02/20 By bnlent axmt620.4gl-> axmt620.src.4gl\nModify.........: No.FUN-840012 08/10/08 By kim mBarcode 功能修改\nModify.........: No.FUN-960007 09/06/03 By chenmoyan global檔內沒有定義rowid變量\nModify.........: No.FUN-980030 09/08/31 By Hiko 加上GP5.2的相關設定\nModify.........: No.TQC-A10080 10/01/10 By destiny 取货机构调整为noentry\nModify.........: No:CHI-A40068 10/05/26 By Summer 變更\"串查button真正對應的程式\nModify.........: No.FUN-A60035 10/07/09 By hongmei 行业别架构",
    "expected_sha256": "cfb172df48a0d29c0660dc7bdf4b8acbf3ab09b2fdf205304eff3be9e0c6c626",
    "language": "genero",
    "oracle_input_sha256": "9562d861a1c2af6cfb4235ad982f1264c864fcd145e718ce08e31fb20c77e7f7",
    "raw_comment": "# Prog. Version..: '5.25.02-11.03.23(00000)'     #\n#\n# Pattern name...: axmt620.4gl\n# Descriptions...: 出貨單維護作業\n# Date & Author..: 95/01/05 By Roger\n# Modify.........: No.FUN-4A0081 05/08/09 By saki 指定單據編號、執行功能\n# Modify.........: No.TQC-640011 06/03/01 By echo 將單號cahr(10)放大至char(16)\n# Modify.........: No.FUN-680137 06/09/04 By flowld 欄位型態定義,改為LIKE\n# Modify.........: No.FUN-6A0094 06/10/25 By yjkhero l_time轉g_time\n# Modify.........: No.FUN-710016 07/01/19 By kim GP3.6 行業別架構\n# Modify.........: No.FUN-730018 07/03/28 By kim 行業別架構\n# Modify.........: No.FUN-7C0017 08/02/20 By bnlent axmt620.4gl-> axmt620.src.4gl \n# Modify.........: No.FUN-840012 08/10/08 By kim mBarcode 功能修改\n# Modify.........: No.FUN-960007 09/06/03 By chenmoyan global檔內沒有定義rowid變量\n# Modify.........: No.FUN-980030 09/08/31 By Hiko 加上GP5.2的相關設定\n# Modify.........: No.TQC-A10080 10/01/10 By destiny 取货机构调整为noentry\n# Modify.........: No:CHI-A40068 10/05/26 By Summer 變更\"串查button真正對應的程式\n# Modify.........: No.FUN-A60035 10/07/09 By hongmei 行业别架构",
    "raw_sha256": "7fd2110798b58fad55c6514150fcf55f22551e24b7d75a8740aac6362d12dd9a"
  },
  {
    "case_id": "monkey-block-12808ff9605b7af6",
    "expected_cleaned": "monkeydoc True if no more data can be read from the stream.\n\nYou can still write to a filestream even if `Eof` is true - disk space permitting!",
    "expected_sha256": "dfcaefc53d402f4ca7df190901cb6bb6d7c6384581e3517ebb7ec794aba3a3f8",
    "language": "monkey",
    "oracle_input_sha256": "36e3b813d5d8a2d769d736fcf3addcc2410469ce1b661e1fd7f7e5034f060c85",
    "raw_comment": "\t#rem monkeydoc True if no more data can be read from the stream.\n\t\n\tYou can still write to a filestream even if `Eof` is true - disk space permitting!\n\t\n\t#end",
    "raw_sha256": "1a365128310d48085eb75a5a1c6424f3dbee0835015d5e92ae150e1c726db8b5"
  },
  {
    "case_id": "monkey-block-ed720fb7946ad0e9",
    "expected_cleaned": "'\t\tIf atype.elemType.IsGeneric Throw New SemantEx( \"Array element type '\"+atype.elemType.Name+\"' is generic\" )\n\nLocal sizes:Value[],inits:Value[]\nIf Self.inits\n\n\t'TODO...\n\tIf atype.rank<>1 Throw New SemantEx( \"Array must be 1 dimensional\" )\n\n\tinits=SemantArgs( Self.inits,scope )\n\tinits=UpCast( inits,atype.elemType )\nElse\n\tsizes=SemantArgs( Self.sizes,scope )\n\tsizes=UpCast( sizes,Type.IntType )\nEndif\n\nReturn New NewArrayValue( atype,sizes,inits )",
    "expected_sha256": "c1b203717c399ad07c226e549d2258e8ab65e151c57d7b4be413a727d25ea1e1",
    "language": "monkey",
    "oracle_input_sha256": "867b6e7382adc29b5a08bdb63ce8d3bb47de7c2965c78aeffbdb4b7d236ec1d8",
    "raw_comment": "\t\t#rem\n'\t\tIf atype.elemType.IsGeneric Throw New SemantEx( \"Array element type '\"+atype.elemType.Name+\"' is generic\" )\n\t\t\n\t\tLocal sizes:Value[],inits:Value[]\n\t\tIf Self.inits\n\t\t\n\t\t\t'TODO...\n\t\t\tIf atype.rank<>1 Throw New SemantEx( \"Array must be 1 dimensional\" )\n\t\t\t\n\t\t\tinits=SemantArgs( Self.inits,scope )\n\t\t\tinits=UpCast( inits,atype.elemType )\n\t\tElse\n\t\t\tsizes=SemantArgs( Self.sizes,scope )\n\t\t\tsizes=UpCast( sizes,Type.IntType )\n\t\tEndif\n\t\t\n\t\tReturn New NewArrayValue( atype,sizes,inits )\n\t\t#end",
    "raw_sha256": "d7c06c468b2cfd4291e2a02424c3350fe6f32cad725260769f34c6ea89ed6543"
  },
  {
    "case_id": "monkey-line-57881f48896cb800",
    "expected_cleaned": "== COMMERCIAL BREAK START ==\n============================\n\nTired of setting things up? Monkey-Wizard to the rescue!\n--> https://github.com/michaelcontento/monkey-wizard\n\nAnd the whole thing should be easy as:\n--> wizard IosAppodeal ../myproject/myproject.build/ios\n\n============================\n==  COMMERCIAL BREAK END  ==",
    "expected_sha256": "db4ffa27bcf62e9537703d5c9ada5c3a354626b88d49027451722f5e6214bfed",
    "language": "monkey",
    "oracle_input_sha256": "95ad6b66e3eca73141afa7735c4bc99af0a46f2181918d7b53e57fa0cbea5edd",
    "raw_comment": "' ============================\n' == COMMERCIAL BREAK START ==\n' ============================\n'\n' Tired of setting things up? Monkey-Wizard to the rescue!\n' --> https://github.com/michaelcontento/monkey-wizard\n'\n' And the whole thing should be easy as:\n' --> wizard IosAppodeal ../myproject/myproject.build/ios\n'\n' ============================\n' ==  COMMERCIAL BREAK END  ==\n' ============================",
    "raw_sha256": "44eb2cbd9a52bd439e8f2042e51323210758d8828f93e424177238071983c23c"
  },
  {
    "case_id": "powerbuilder-line-0a5443c26f6d5ca4",
    "expected_cleaned": "Declare: Instance Variables()\nDescription:\nArguments: (none)\nReturns: (none)\nAuthor: \tlaihaichun\t\tDate: 2003/12/31\nModify History:\nCopyRight 2003----???? Appeon Inc.",
    "expected_sha256": "43442bf994333a73d301d7166bd060a0c12cfa41844129cf3325ee160c16d629",
    "language": "powerbuilder",
    "oracle_input_sha256": "3ffed5e73960a55d42722b234cf650db772aa52685aa77e9dc914743bda25b44",
    "raw_comment": "//====================================================================\n// Declare: Instance Variables()\n//--------------------------------------------------------------------\n// Description: \n//--------------------------------------------------------------------\n// Arguments: (none)\n//--------------------------------------------------------------------\n// Returns: (none)\n//--------------------------------------------------------------------\n// Author: \tlaihaichun\t\tDate: 2003/12/31\n//--------------------------------------------------------------------\n// Modify History: \n//\t\n//--------------------------------------------------------------------\n// CopyRight 2003----???? Appeon Inc.\n//====================================================================",
    "raw_sha256": "514830f49b67dc1cf217d1c6dcd04b276b41eaf7e5e633c94445b294f3bf8b31"
  },
  {
    "case_id": "powerbuilder-line-4472e6cc98861812",
    "expected_cleaned": "Declare: Instance Variables()\nDescription:\nArguments: (none)\nReturns: (none)\nAuthor: \tlaihaichun\t\tDate: 2003/12/31\nModify History:\nCopyRight 2003----???? Appeon Inc.",
    "expected_sha256": "43442bf994333a73d301d7166bd060a0c12cfa41844129cf3325ee160c16d629",
    "language": "powerbuilder",
    "oracle_input_sha256": "76f15a048b14e659c5e68a65e112447ffe50e0db886a2a108ecdb8ffe8040777",
    "raw_comment": "//====================================================================\n// Declare: Instance Variables()\n//--------------------------------------------------------------------\n// Description: \n//--------------------------------------------------------------------\n// Arguments: (none)\n//--------------------------------------------------------------------\n// Returns: (none)\n//--------------------------------------------------------------------\n// Author: \tlaihaichun\t\tDate: 2003/12/31\n//--------------------------------------------------------------------\n// Modify History: \n//\t\n//--------------------------------------------------------------------\n// CopyRight 2003----???? Appeon Inc.\n//====================================================================",
    "raw_sha256": "514830f49b67dc1cf217d1c6dcd04b276b41eaf7e5e633c94445b294f3bf8b31"
  },
  {
    "case_id": "powerbuilder-line-682a801ecb551822",
    "expected_cleaned": "Function: u_js_zd_cmbzgylxzd::uf_del()\nDescription:\nArguments:(None)\nReturns:  integer\nAuthor:\tyukk\t\tDate: 2017.xx.xx\nModify History:",
    "expected_sha256": "99203c94ea09c0d3514976a40cb089ff6ec677109165a40f91d855e3c5374847",
    "language": "powerbuilder",
    "oracle_input_sha256": "6d42461c7cef832744fac20eff545f10aef27e65880246951ce5bc0b7f96ab4f",
    "raw_comment": "//==============================================================================\n// Function: u_js_zd_cmbzgylxzd::uf_del()\n//------------------------------------------------------------------------------\n// Description: \n//------------------------------------------------------------------------------\n// Arguments:(None)\n//------------------------------------------------------------------------------\n// Returns:  integer\n//------------------------------------------------------------------------------\n// Author:\tyukk\t\tDate: 2017.xx.xx\n//------------------------------------------------------------------------------\n// Modify History: \n//\t\n//==============================================================================",
    "raw_sha256": "7c730593a65e0938136a4042660aab0a5dbbf44610f738d0c8cc41ef0453a32d"
  },
  {
    "case_id": "win32_message_file-directive-788589bffafad54c",
    "expected_cleaned": "Copyright (c) Microsoft Corporation 1998\nAll rights reserved\n\n\nDefinitions for file deployment events.\n\n\n#ifndef _FDEVENTS_\n#define _FDEVENTS_",
    "expected_sha256": "6afafcdc220fb435453cbb49e7f5433565a74f396f88b82698cda8e3bd971668",
    "language": "win32_message_file",
    "oracle_input_sha256": "470513cc9f93aa6c69436a962b6f2739f087ed157af01edcb04f0eb94278fada",
    "raw_comment": ";/*++\r\n;\r\n; Copyright (c) Microsoft Corporation 1998\r\n; All rights reserved\r\n;\r\n;\r\n; Definitions for file deployment events.\r\n;\r\n;--*/\r\n;\r\n;#ifndef _FDEVENTS_\r\n;#define _FDEVENTS_\r\n;",
    "raw_sha256": "00147da469f2584934df7c0913d8512ab2c7bc0077c6eb5c6f440507586adeb9"
  },
  {
    "case_id": "win32_message_file-directive-79289e6926df4ccd",
    "expected_cleaned": "BUILD Version: 0001    // Increment this if a change has global effects\n\nCopyright (c) 1994-7  Microsoft Corporation\n\nModule Name:\n\n   cpuhold.h\n\nAbstract:\n\n   Definitions for RCmdSrv messages.\n\nAuthor:\n\n   Sean Selitrennikoff (v-seans) Feb-10-1999\n\nRevision History:\n\nNotes:\n\n   This file is generated by the MC tool from the rcmdsrv.mc file.\n\n   Inserts are defined as:\n   %1 = USERNAME\n   %2 = USERDOMAIN\n   %3 = MACHINENAME\n   %4 = SUBERROR\n\n\n#ifndef _CPUHOLDMESSAGE_\n#define _CPUHOLDMESSAGE_",
    "expected_sha256": "c4500a2c401640ae7c747310a9c4a166b30ceda2d16a3a78cd5e9581839dbd02",
    "language": "win32_message_file",
    "oracle_input_sha256": "d235e8a1c12c254ae9daea09d945fdf3959279615cc6e4cd40e8b0c13bba4a03",
    "raw_comment": ";/*++ BUILD Version: 0001    // Increment this if a change has global effects\n;\n;Copyright (c) 1994-7  Microsoft Corporation\n;\n;Module Name:\n;\n;    cpuhold.h\n;\n;Abstract:\n;\n;    Definitions for RCmdSrv messages.\n;\n;Author:\n;\n;    Sean Selitrennikoff (v-seans) Feb-10-1999\n;\n;Revision History:\n;\n;Notes:\n;\n;    This file is generated by the MC tool from the rcmdsrv.mc file.\n;\n;    Inserts are defined as:\n;    %1 = USERNAME\n;    %2 = USERDOMAIN\n;    %3 = MACHINENAME\n;    %4 = SUBERROR\n;\n;--*/\n;\n;#ifndef _CPUHOLDMESSAGE_\n;#define _CPUHOLDMESSAGE_\n;",
    "raw_sha256": "69635d50a7d6b2f84b1846f28ffdc6234dbbb0b04bb4a85db7d90f24b4649ff4"
  },
  {
    "case_id": "win32_message_file-directive-7a8dffcc46b17cc8",
    "expected_cleaned": "Copyright (c) 1994 Microsoft Corporation\n\nModule Name:\n\n   RnrMsg.h\n\nAbstract:\n\n   This file is generated by the MC tool from the RNRMSG.MC message\n   file.\n\nAuthor:\n\n   Charles K. Moore (keithmo)   24-July-1994\n\nRevision History:\n\n\n#ifndef _RNRMSG_H_\n#define _RNRMSG_H_",
    "expected_sha256": "1e6bc95d9cca2d806a478a1e6701288d9c985e6560ee65f608be331a49e609f1",
    "language": "win32_message_file",
    "oracle_input_sha256": "e8cb99649089cae620aa841aa3507c7a012d447c7c5d42285be826ff71827f74",
    "raw_comment": ";/*++\r\n;\r\n;Copyright (c) 1994 Microsoft Corporation\r\n;\r\n;Module Name:\r\n;\r\n;    RnrMsg.h\r\n;\r\n;Abstract:\r\n;\r\n;    This file is generated by the MC tool from the RNRMSG.MC message\r\n;    file.\r\n;\r\n;Author:\r\n;\r\n;    Charles K. Moore (keithmo)   24-July-1994\r\n;\r\n;Revision History:\r\n;\r\n;--*/\r\n;\r\n;#ifndef _RNRMSG_H_\r\n;#define _RNRMSG_H_\r\n;",
    "raw_sha256": "151e96069e02a4f43ece0f29f3d8e1fd69143bf04e7b12a89467b5229c4887fb"
  }
]"""
)

assert len(CASES) == 33
assert {case["case_id"] for case in CASES} == EXPECTED_CASE_IDS


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["case_id"])
def test_conservative_cluster_real_world_regressions(case):
    """Keep each frozen failure and provisional deletion-only oracle exact."""

    raw_comment = case["raw_comment"]
    expected = case["expected_cleaned"]
    assert hashlib.sha256(raw_comment.encode()).hexdigest() == case["raw_sha256"]
    assert hashlib.sha256(expected.encode()).hexdigest() == case["expected_sha256"]
    assert re.fullmatch(r"[0-9a-f]{64}", case["oracle_input_sha256"])
    assert sanitize_comment(case["language"], raw_comment) == expected


def test_conservative_cluster_targeted_frame_fuzz():
    """Exercise structural variants without inventing content deletion rules."""

    rng = random.Random(0xC0FFEE)
    for _ in range(250):
        token = "".join(rng.choice("abcdef0123456789") for _ in range(16))
        stars = "*" * rng.randint(8, 96)
        sequence = "".join(rng.choice("0123456789") for _ in range(6))
        assert sanitize_comment("cobol", sequence + stars) == ""

        clean_raw = f"/**{token} first\n {token} second\n {token} third*/"
        assert sanitize_comment("clean", clean_raw) == (
            f"{token} first\n{token} second\n{token} third"
        )

        faust_raw = (
            f"//----------{token}----------\n"
            f"// #### {token}\n"
            f"// Markdown {token} == #\n"
            "//------------------------"
        )
        assert sanitize_comment("faust", faust_raw) == (
            f"{token}\n#### {token}\nMarkdown {token} == #"
        )

        gap_raw = (
            f"################################\n##\n#W  {token}\n##  prose {token}\n#Y  {token}\n##"
        )
        assert sanitize_comment("gap", gap_raw) == (f"W  {token}\nprose {token}\nY  {token}")

        denizen_raw = f"## @file\n#\n#  {token}\n#  SPDX-{token}\n##"
        assert sanitize_comment("denizenscript", denizen_raw) == (f"@file\n\n{token}\nSPDX-{token}")

        genero_raw = f"# Prog: {token}     #\n#\n# Description: {token}"
        assert sanitize_comment("genero", genero_raw) == (f"Prog: {token}\n\nDescription: {token}")

        win32_raw = f";/*++\n;\n; {token}\n;\n;--*/\n;\n;#ifndef {token}\n;#define {token}\n;"
        assert sanitize_comment("win32_message_file", win32_raw) == (
            f"{token}\n\n\n#ifndef {token}\n#define {token}"
        )


def test_conservative_cluster_targeted_complete_template_fuzz():
    """Keep inner punctuation while removing only complete outer templates."""

    rng = random.Random(0x5CAFF01D)
    for _ in range(250):
        token = "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(12))
        monkey_raw = (
            "' ============================\n"
            f"' == {token} START ==\n"
            "' ============================\n"
            f"' Markdown # {token} = value\n"
            "' ============================\n"
            f"' == {token} END ==\n"
            "' ============================"
        )
        assert sanitize_comment("monkey", monkey_raw) == (
            f"== {token} START ==\n"
            "============================\n"
            f"Markdown # {token} = value\n"
            "============================\n"
            f"== {token} END =="
        )

        powerbuilder_raw = (
            "//================================\n"
            f"// Function: {token}()\n"
            "//--------------------------------\n"
            f"// Description: {token} # ==\n"
            "//--------------------------------\n"
            f"// Returns: {token}\n"
            "//================================"
        )
        assert sanitize_comment("powerbuilder", powerbuilder_raw) == (
            f"Function: {token}()\nDescription: {token} # ==\nReturns: {token}"
        )
