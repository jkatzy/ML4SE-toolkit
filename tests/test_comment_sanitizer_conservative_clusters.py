"""Exact real-world regressions for conservative, language-scoped frame cleaning."""

# ruff: noqa: E501

from __future__ import annotations

import hashlib
import json

import pytest

from ml4setk import sanitize_comment

pytestmark = pytest.mark.unit

EXPECTED_CASE_IDS = frozenset(
    {
        "bluespec-block-406e85b8be149862",
        "bluespec-block-9fd3ac4903e8f2f9",
        "bluespec-block-b1f75f68f703356e",
        "bluespec-block-bae081cfe9ebc61b",
        "click-line-4c05aca9a22db07b",
        "click-line-51f748575cff8e2a",
        "clips-line-0e0549c53e2d4c7e",
        "clips-line-9e4b5786cd13a5ec",
        "clips-line-be48eef1d0d715d8",
        "clips-line-d7db48ece54b9300",
        "mercury-line-19b229c04183dfaa",
        "mercury-line-46a829fddea50406",
        "mercury-line-56b0ba15e0c506a3",
        "mercury-line-eb097df02c51903a",
        "scaml-line-35809bbddfb0e023",
        "scaml-line-98c97649b8c156bc",
        "scaml-line-9adbc61b881d6952",
        "scaml-line-ab455834d0dff9c9",
        "scaml-line-b599b8f7c5fdeb44",
        "scaml-line-c68e7052f03b9058",
        "uno-block-55260cd306b65d78",
        "uno-block-635e059067ee5d94",
        "uno-block-8c5c6bd319b6cf90",
        "uno-block-e70b0c1f7753614e",
        "uno-block-f23288d1521f9164",
    }
)

CASES = json.loads(
    r"""[
  {
    "case_id": "bluespec-block-406e85b8be149862",
    "expected_cleaned": "Copyright (c) 2013 Colin Rothwell\nAll rights reserved.\n\nThis software was developed by Colin Rothwell as part of his final year\nundergraduate project.\n\nRedistribution and use in source and binary forms, with or without\nmodification, are permitted provided that the following conditions\nare met:\n1. Redistributions of source code must retain the above copyright\n   notice, this list of conditions and the following disclaimer.\n2. Redistributions in binary form must reproduce the above copyright\n   notice, this list of conditions and the following disclaimer in the\n   documentation and/or other materials provided with the distribution.\n\nTHIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND\nANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE\nIMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE\nARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE\nFOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL\nDAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS\nOR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)\nHOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT\nLIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY\nOUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF\nSUCH DAMAGE.",
    "expected_sha256": "aba36bd16854bf18a1b7caeb176c559b8aa154aa52b504b78f63a326b0626377",
    "language": "bluespec",
    "raw_comment": "/*-\n * Copyright (c) 2013 Colin Rothwell\n * All rights reserved.\n *\n * This software was developed by Colin Rothwell as part of his final year\n * undergraduate project.\n * \n * Redistribution and use in source and binary forms, with or without\n * modification, are permitted provided that the following conditions\n * are met:\n * 1. Redistributions of source code must retain the above copyright\n *    notice, this list of conditions and the following disclaimer.\n * 2. Redistributions in binary form must reproduce the above copyright\n *    notice, this list of conditions and the following disclaimer in the\n *    documentation and/or other materials provided with the distribution.\n *\n * THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND\n * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE\n * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE\n * ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE\n * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL\n * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS\n * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)\n * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT\n * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY\n * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF\n * SUCH DAMAGE.\n */",
    "raw_sha256": "9932c75e8f91cdae80dd43bbf44b1f8edf2a40598624303f0f6f0d50a2fc7d54"
  },
  {
    "case_id": "bluespec-block-9fd3ac4903e8f2f9",
    "expected_cleaned": "Copyright (c) 2010 Greg Chadwick\nCopyright (c) 2012 Ben Thorner\nCopyright (c) 2013 Colin Rothwell\nCopyright (c) 2013 David T. Chisnall\nCopyright (c) 2013 Jonathan Woodruff\nCopyright (c) 2013 SRI International\nCopyright (c) 2013 Robert M. Norton\nCopyright (c) 2013 Robert N. M. Watson\nCopyright (c) 2013 Simon W. Moore\nCopyright (c) 2013 Alan A. Mujumdar\nCopyright (c) 2014 Colin Rothwell\nCopyright (c) 2014 Alexandre Joannou\nAll rights reserved.\n\nThis software was developed by SRI International and the University of\nCambridge Computer Laboratory under DARPA/AFRL contract FA8750-10-C-0237\n(\"CTSRD\"), as part of the DARPA CRASH research programme.\n\nThis software was developed by SRI International and the University of\nCambridge Computer Laboratory under DARPA/AFRL contract FA8750-11-C-0249\n(\"MRC2\"), as part of the DARPA MRC research programme.\n\n@BERI_LICENSE_HEADER_START@\n\nLicensed to BERI Open Systems C.I.C. (BERI) under one or more contributor\nlicense agreements.  See the NOTICE file distributed with this work for\nadditional information regarding copyright ownership.  BERI licenses this\nfile to you under the BERI Hardware-Software License, Version 1.0 (the\n\"License\"); you may not use this file except in compliance with the\nLicense.  You may obtain a copy of the License at:\n\n  http://www.beri-open-systems.org/legal/license-1-0.txt\n\nUnless required by applicable law or agreed to in writing, Work distributed\nunder the License is distributed on an \"AS IS\" BASIS, WITHOUT WARRANTIES OR\nCONDITIONS OF ANY KIND, either express or implied.  See the License for the\nspecific language governing permissions and limitations under the License.\n\n@BERI_LICENSE_HEADER_END@",
    "expected_sha256": "26ace6a0c813bd3b16ab3dbeba42400ef72d247abc8fe236732da178b9821a50",
    "language": "bluespec",
    "raw_comment": "/*-\n * Copyright (c) 2010 Greg Chadwick\n * Copyright (c) 2012 Ben Thorner\n * Copyright (c) 2013 Colin Rothwell\n * Copyright (c) 2013 David T. Chisnall\n * Copyright (c) 2013 Jonathan Woodruff\n * Copyright (c) 2013 SRI International\n * Copyright (c) 2013 Robert M. Norton\n * Copyright (c) 2013 Robert N. M. Watson\n * Copyright (c) 2013 Simon W. Moore\n * Copyright (c) 2013 Alan A. Mujumdar\n * Copyright (c) 2014 Colin Rothwell\n * Copyright (c) 2014 Alexandre Joannou\n * All rights reserved.\n *\n * This software was developed by SRI International and the University of\n * Cambridge Computer Laboratory under DARPA/AFRL contract FA8750-10-C-0237\n * (\"CTSRD\"), as part of the DARPA CRASH research programme.\n *\n * This software was developed by SRI International and the University of\n * Cambridge Computer Laboratory under DARPA/AFRL contract FA8750-11-C-0249\n * (\"MRC2\"), as part of the DARPA MRC research programme.\n *\n * @BERI_LICENSE_HEADER_START@\n *\n * Licensed to BERI Open Systems C.I.C. (BERI) under one or more contributor\n * license agreements.  See the NOTICE file distributed with this work for\n * additional information regarding copyright ownership.  BERI licenses this\n * file to you under the BERI Hardware-Software License, Version 1.0 (the\n * \"License\"); you may not use this file except in compliance with the\n * License.  You may obtain a copy of the License at:\n *\n *   http://www.beri-open-systems.org/legal/license-1-0.txt\n *\n * Unless required by applicable law or agreed to in writing, Work distributed\n * under the License is distributed on an \"AS IS\" BASIS, WITHOUT WARRANTIES OR\n * CONDITIONS OF ANY KIND, either express or implied.  See the License for the\n * specific language governing permissions and limitations under the License.\n *\n * @BERI_LICENSE_HEADER_END@\n */",
    "raw_sha256": "acadb87a4bc8974fcf410c53609164f427423bd041edaba663a475c7bd6effba"
  },
  {
    "case_id": "bluespec-block-b1f75f68f703356e",
    "expected_cleaned": "Copyright (c) 2018 Alexandre Joannou\nAll rights reserved.\n\nThis software was developed by SRI International and the University of\nCambridge Computer Laboratory (Department of Computer Science and\nTechnology) under DARPA contract HR0011-18-C-0016 (\"ECATS\"), as part of the\nDARPA SSITH research programme.\n\n@BERI_LICENSE_HEADER_START@\n\nLicensed to BERI Open Systems C.I.C. (BERI) under one or more contributor\nlicense agreements.  See the NOTICE file distributed with this work for\nadditional information regarding copyright ownership.  BERI licenses this\nfile to you under the BERI Hardware-Software License, Version 1.0 (the\n\"License\"); you may not use this file except in compliance with the\nLicense.  You may obtain a copy of the License at:\n\n  http://www.beri-open-systems.org/legal/license-1-0.txt\n\nUnless required by applicable law or agreed to in writing, Work distributed\nunder the License is distributed on an \"AS IS\" BASIS, WITHOUT WARRANTIES OR\nCONDITIONS OF ANY KIND, either express or implied.  See the License for the\nspecific language governing permissions and limitations under the License.\n\n@BERI_LICENSE_HEADER_END@",
    "expected_sha256": "d284eeec153c20daa9f780efbe91dd2be7eaad63524eaa0c4ef9b9710fa7f20b",
    "language": "bluespec",
    "raw_comment": "/*-\n * Copyright (c) 2018 Alexandre Joannou\n * All rights reserved.\n *\n * This software was developed by SRI International and the University of\n * Cambridge Computer Laboratory (Department of Computer Science and\n * Technology) under DARPA contract HR0011-18-C-0016 (\"ECATS\"), as part of the\n * DARPA SSITH research programme.\n *\n * @BERI_LICENSE_HEADER_START@\n *\n * Licensed to BERI Open Systems C.I.C. (BERI) under one or more contributor\n * license agreements.  See the NOTICE file distributed with this work for\n * additional information regarding copyright ownership.  BERI licenses this\n * file to you under the BERI Hardware-Software License, Version 1.0 (the\n * \"License\"); you may not use this file except in compliance with the\n * License.  You may obtain a copy of the License at:\n *\n *   http://www.beri-open-systems.org/legal/license-1-0.txt\n *\n * Unless required by applicable law or agreed to in writing, Work distributed\n * under the License is distributed on an \"AS IS\" BASIS, WITHOUT WARRANTIES OR\n * CONDITIONS OF ANY KIND, either express or implied.  See the License for the\n * specific language governing permissions and limitations under the License.\n *\n * @BERI_LICENSE_HEADER_END@\n */",
    "raw_sha256": "eb49ef00a0e5a747f6326455d661dc382235fb4bf38370f9428c3a5d5ddf6a7c"
  },
  {
    "case_id": "bluespec-block-bae081cfe9ebc61b",
    "expected_cleaned": "Copyright (c) 2013 Alex Horsman\nAll rights reserved.\n\nThis software was developed by SRI International and the University of\nCambridge Computer Laboratory under DARPA/AFRL contract FA8750-10-C-0237\n(\"CTSRD\"), as part of the DARPA CRASH research programme.\n\n@BERI_LICENSE_HEADER_START@\n\nLicensed to BERI Open Systems C.I.C. (BERI) under one or more contributor\nlicense agreements.  See the NOTICE file distributed with this work for\nadditional information regarding copyright ownership.  BERI licenses this\nfile to you under the BERI Hardware-Software License, Version 1.0 (the\n\"License\"); you may not use this file except in compliance with the\nLicense.  You may obtain a copy of the License at:\n\n  http://www.beri-open-systems.org/legal/license-1-0.txt\n\nUnless required by applicable law or agreed to in writing, Work distributed\nunder the License is distributed on an \"AS IS\" BASIS, WITHOUT WARRANTIES OR\nCONDITIONS OF ANY KIND, either express or implied.  See the License for the\nspecific language governing permissions and limitations under the License.\n\n@BERI_LICENSE_HEADER_END@",
    "expected_sha256": "00a7a398d9e7f4fcb970914edd801c9ce84fcdc0e7de81051f1f338c29789a9f",
    "language": "bluespec",
    "raw_comment": "/*-\n * Copyright (c) 2013 Alex Horsman\n * All rights reserved.\n *\n * This software was developed by SRI International and the University of\n * Cambridge Computer Laboratory under DARPA/AFRL contract FA8750-10-C-0237\n * (\"CTSRD\"), as part of the DARPA CRASH research programme.\n *\n * @BERI_LICENSE_HEADER_START@\n *\n * Licensed to BERI Open Systems C.I.C. (BERI) under one or more contributor\n * license agreements.  See the NOTICE file distributed with this work for\n * additional information regarding copyright ownership.  BERI licenses this\n * file to you under the BERI Hardware-Software License, Version 1.0 (the\n * \"License\"); you may not use this file except in compliance with the\n * License.  You may obtain a copy of the License at:\n *\n *   http://www.beri-open-systems.org/legal/license-1-0.txt\n *\n * Unless required by applicable law or agreed to in writing, Work distributed\n * under the License is distributed on an \"AS IS\" BASIS, WITHOUT WARRANTIES OR\n * CONDITIONS OF ANY KIND, either express or implied.  See the License for the\n * specific language governing permissions and limitations under the License.\n *\n * @BERI_LICENSE_HEADER_END@\n */",
    "raw_sha256": "04a42eedd88a7ef9c269354e9e5491fcc82f06b3026560f2b1f65fda45385231"
  },
  {
    "case_id": "click-line-4c05aca9a22db07b",
    "expected_cleaned": "DO NOT CHANGE THIS FILE: Any changes will be removed prior to the project defense.",
    "expected_sha256": "c5350d9da31c630e8d3bad0d6a07b7ad0cd9ebb088ca5bb56629fc9389407fc5",
    "language": "click",
    "raw_comment": "// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n// ! DO NOT CHANGE THIS FILE: Any changes will be removed prior to the project defense. !\n// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",
    "raw_sha256": "5761c05f86eb5d74657eedd8913bcc796ffe0452965f339bbc4742ae3107083c"
  },
  {
    "case_id": "click-line-51f748575cff8e2a",
    "expected_cleaned": "DO NOT CHANGE THIS FILE: Any changes will be removed prior to the project defense.",
    "expected_sha256": "c5350d9da31c630e8d3bad0d6a07b7ad0cd9ebb088ca5bb56629fc9389407fc5",
    "language": "click",
    "raw_comment": "// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n// ! DO NOT CHANGE THIS FILE: Any changes will be removed prior to the project defense. !\n// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",
    "raw_sha256": "5761c05f86eb5d74657eedd8913bcc796ffe0452965f339bbc4742ae3107083c"
  },
  {
    "case_id": "clips-line-0e0549c53e2d4c7e",
    "expected_cleaned": "Ejercicio 3 - Aparatado a",
    "expected_sha256": "5a41276184371c488be249a230bc3b966bc6875170d430f148660d3f2878fc6d",
    "language": "clips",
    "raw_comment": ";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;\n;;;;;;;;;;;;; Ejercicio 3 - Aparatado a ;;;;;;;;;;;;\n;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;",
    "raw_sha256": "c96b9e7dd1e357154e488340b212c346fd2cc45bd59b5897ed23ca6342e62319"
  },
  {
    "case_id": "clips-line-9e4b5786cd13a5ec",
    "expected_cleaned": "Definizione del modulo e dei template",
    "expected_sha256": "ca8a03597ebc53dd9c07450d8320ea230cf452228b877078004833e8ab14ed59",
    "language": "clips",
    "raw_comment": ";  ---------------------------------------------\n;  --- Definizione del modulo e dei template ---\n;  ---------------------------------------------",
    "raw_sha256": "97e0bc14784972647ca15ea497a6f9d38f1de36055a0df610a45b3cfedb23101"
  },
  {
    "case_id": "clips-line-be48eef1d0d715d8",
    "expected_cleaned": "objects_deftemplates definitions\nJ.Savage, UNAM\n1/5/20",
    "expected_sha256": "527ffbb8e3cba779d218b917426953185e8d0bccc0f7850d3f908229b5d06dcd",
    "language": "clips",
    "raw_comment": ";************************************************\r\n;*\t\t\t\t\t\t*\r\n;*\tobjects_deftemplates definitions\t*\r\n;*\t\t\t\t\t\t*\r\n;*\t\t\tJ.Savage, UNAM\t\t*\r\n;*\t\t\t1/5/20\t\t\t*\r\n;*\t\t\t\t\t\t*\r\n;************************************************",
    "raw_sha256": "d31fbfe7b2fb9e3eae880c54885a467d8ff0d58479cfc3d67f51ccff978d41d9"
  },
  {
    "case_id": "clips-line-d7db48ece54b9300",
    "expected_cleaned": "PARA EJECUTAR batch ((batch \"carga.clp\"))\nONTOLOGIA",
    "expected_sha256": "4c3a9ad727c8808327b6f0674dd85e698d4f99d865f7ee79cd4b089b9ffeb18b",
    "language": "clips",
    "raw_comment": ";;;PARA EJECUTAR batch ((batch \"carga.clp\"))\r\n;;;;;;;;;;;;;;;;;;;;;;;;; ONTOLOGIA ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;",
    "raw_sha256": "c7b938eca855e5a7d855e66bc5e7800afc6dad87262a6be4bf3ec451582bfa86"
  },
  {
    "case_id": "mercury-line-19b229c04183dfaa",
    "expected_cleaned": "Copyright (C) 2013-2014 Opturion Pty Ltd.\nCopyright (C) 2006-2009 NICTA.\n\nAuthor: Gregory J. Duck\n\nExtract lookups from ml_b_blocks.\n\nASSUMPTIONS:\n- 'loop' optimisation has not yet being performed.  Otherwise invalid\n  lookups may be generated.",
    "expected_sha256": "90491ee8be4eb0c1b2a95daf3921352de9e2b518fa7bc883ae6f9a0e5e0c9377",
    "language": "mercury",
    "raw_comment": "%---------------------------------------------------------------------------%\n% Copyright (C) 2013-2014 Opturion Pty Ltd.\n% Copyright (C) 2006-2009 NICTA.\n%---------------------------------------------------------------------------%\n%\n% Author: Gregory J. Duck\n%\n% Extract lookups from ml_b_blocks.\n%\n% ASSUMPTIONS: \n% - 'loop' optimisation has not yet being performed.  Otherwise invalid \n%   lookups may be generated.\n%\n%---------------------------------------------------------------------------%",
    "raw_sha256": "a38c323d7f2a05b520b61e535e333518633380a391aae47e348ae456c7ea1bf4"
  },
  {
    "case_id": "mercury-line-46a829fddea50406",
    "expected_cleaned": "vim: ft=mercury ts=4 sw=4 et wm=0 tw=0\nCopyright (C) 2016, Julien Fischer.\nSee the file COPYING for license details.\n\nAuthor: Julien Fischer <juliensf@gmail.com>\n\nThis module provides unsigned 8-bit integers.",
    "expected_sha256": "9bfc2939e20da61c7e319c1765e492a5aef5adbe11dfbb833ac935d8f7b82afd",
    "language": "mercury",
    "raw_comment": "%---------------------------------------------------------------------------%\n% vim: ft=mercury ts=4 sw=4 et wm=0 tw=0\n%---------------------------------------------------------------------------%\n% Copyright (C) 2016, Julien Fischer.\n% See the file COPYING for license details.\n%\n% Author: Julien Fischer <juliensf@gmail.com>\n%\n% This module provides unsigned 8-bit integers.\n%\n%---------------------------------------------------------------------------%",
    "raw_sha256": "81d584a3a05a2d73cd00be4984ea04d07b46e09822413c1bc15160ffe4dbd949"
  },
  {
    "case_id": "mercury-line-56b0ba15e0c506a3",
    "expected_cleaned": "vim: ft=mercury ts=4 sw=4 et\nCopyright (C) 2019, Julien Fischer.\nSee the file COPYING for license details.\n\nAuthor: Julien Fischer <juliensf@gmail.com>\n\nMercury wrapper for java.time.Month.",
    "expected_sha256": "816fcbefdb5db4f790c10a4a9e490c883fa179bd68a24c6339481d81403ea80e",
    "language": "mercury",
    "raw_comment": "%---------------------------------------------------------------------------%\n% vim: ft=mercury ts=4 sw=4 et\n%---------------------------------------------------------------------------%\n% Copyright (C) 2019, Julien Fischer.\n% See the file COPYING for license details.\n%\n% Author: Julien Fischer <juliensf@gmail.com>\n%\n% Mercury wrapper for java.time.Month.\n%\n%---------------------------------------------------------------------------%",
    "raw_sha256": "731d6cec550840568d1a0342c620e57d7faaa80c84dac1ff5bc8b2745618c60d"
  },
  {
    "case_id": "mercury-line-eb097df02c51903a",
    "expected_cleaned": "FILENAME : tapl.m\nAUTHOR   : Simon Nielsen Knights\nCOPYRIGHT: Copyright \u00a9 2019 Simon Nielsen Knights <tauoverpi@yandex.com>\nLICENSE  : MIT\nCREATED  : Fri Feb 15, 2019  03:45AM\nMODIFIED : Fri Feb 15, 2019  04:15AM\nTBD: write documentation",
    "expected_sha256": "5a3f6668783a214bb8fe89a75beaa1a33f13caa0f726f0f260d9c70ca94411b3",
    "language": "mercury",
    "raw_comment": "%----------------------------------------------------------------------------%\n% FILENAME : tapl.m\n% AUTHOR   : Simon Nielsen Knights\n% COPYRIGHT: Copyright \u00a9 2019 Simon Nielsen Knights <tauoverpi@yandex.com>\n% LICENSE  : MIT\n% CREATED  : Fri Feb 15, 2019  03:45AM\n% MODIFIED : Fri Feb 15, 2019  04:15AM\n%----------------------------------------------------------------------------%\n% TBD: write documentation\n%----------------------------------------------------------------------------%",
    "raw_sha256": "e53a5ad307eebfecb7125d670e4a25a50ec0910977c1ac5959b913a1ac20e39b"
  },
  {
    "case_id": "scaml-line-35809bbddfb0e023",
    "expected_cleaned": "[if lt IE 8]\n  %link{ \"href\" => \"/stylesheets/blueprint/ie.css\", :type => \"text/css\", :rel => \"stylesheet\", :media => \"screen, projection\" }",
    "expected_sha256": "834fa5b0c8258398c18a227dbe36141930d9184931b45e28e9da8a4db74b7ca2",
    "language": "scaml",
    "raw_comment": "    /[if lt IE 8]\n      %link{ \"href\" => \"/stylesheets/blueprint/ie.css\", :type => \"text/css\", :rel => \"stylesheet\", :media => \"screen, projection\" }",
    "raw_sha256": "74563527f4783ee7722c32f5952d010cdfa3aea1503000929825a105b2880757"
  },
  {
    "case_id": "scaml-line-98c97649b8c156bc",
    "expected_cleaned": "[if lt IF 9]\n %script{:src => \"http://html5shim.googlecode.com/svn/trunk/html5.js\"}",
    "expected_sha256": "b09d05a553f430cc57e4d152c4c3e53b9e6509bc9bb6656a36b2c7fdcd878281",
    "language": "scaml",
    "raw_comment": "  /[if lt IF 9]\n   %script{:src => \"http://html5shim.googlecode.com/svn/trunk/html5.js\"}",
    "raw_sha256": "3428cb4c536cf51c593fbe4a857114be232f953b45877709f926d45385d967c0"
  },
  {
    "case_id": "scaml-line-9adbc61b881d6952",
    "expected_cleaned": "[if lt IF 9]\n %script{:src => \"http://html5shim.googlecode.com/svn/trunk/html5.js\"}",
    "expected_sha256": "b09d05a553f430cc57e4d152c4c3e53b9e6509bc9bb6656a36b2c7fdcd878281",
    "language": "scaml",
    "raw_comment": "  /[if lt IF 9]\n   %script{:src => \"http://html5shim.googlecode.com/svn/trunk/html5.js\"}",
    "raw_sha256": "3428cb4c536cf51c593fbe4a857114be232f953b45877709f926d45385d967c0"
  },
  {
    "case_id": "scaml-line-ab455834d0dff9c9",
    "expected_cleaned": "[if lt IF 9]\n %script{:src => \"http://html5shim.googlecode.com/svn/trunk/html5.js\"}",
    "expected_sha256": "b09d05a553f430cc57e4d152c4c3e53b9e6509bc9bb6656a36b2c7fdcd878281",
    "language": "scaml",
    "raw_comment": "  /[if lt IF 9]\n   %script{:src => \"http://html5shim.googlecode.com/svn/trunk/html5.js\"}",
    "raw_sha256": "3428cb4c536cf51c593fbe4a857114be232f953b45877709f926d45385d967c0"
  },
  {
    "case_id": "scaml-line-b599b8f7c5fdeb44",
    "expected_cleaned": "[if lt IF 9]\n %script{:src => \"http://html5shim.googlecode.com/svn/trunk/html5.js\"}",
    "expected_sha256": "b09d05a553f430cc57e4d152c4c3e53b9e6509bc9bb6656a36b2c7fdcd878281",
    "language": "scaml",
    "raw_comment": "  /[if lt IF 9]\n   %script{:src => \"http://html5shim.googlecode.com/svn/trunk/html5.js\"}",
    "raw_sha256": "3428cb4c536cf51c593fbe4a857114be232f953b45877709f926d45385d967c0"
  },
  {
    "case_id": "scaml-line-c68e7052f03b9058",
    "expected_cleaned": "[if IE]\n  %meta(http-equiv=\"Pragma\" content=\"no-cache\")\n  %meta(http-equiv=\"Expires\" content=\"0\")",
    "expected_sha256": "4171a060f8db59669bee1e98b42b98244f4d5bd711d51d22b91786886f4cb2a2",
    "language": "scaml",
    "raw_comment": "  /[if IE]\n    %meta(http-equiv=\"Pragma\" content=\"no-cache\")\n    %meta(http-equiv=\"Expires\" content=\"0\")",
    "raw_sha256": "20e546b68ca64673fe8652435a947ebe9f611dab97c921468febcc07fc257395"
  },
  {
    "case_id": "uno-block-55260cd306b65d78",
    "expected_cleaned": "Draws a shadow behind an element.\n\n## Example\n\nThis example shows a rounded rectangle with a shadow that animates in size when pressed:\n\n\t<Rectangle Width=\"100\" Height=\"100\" Color=\"Red\" CornerRadius=\"5\">\n\t\t<Shadow ux:Name=\"RectangleShadow\" Size=\"10\" />\n\t\t<Clicked>\n\t\t\t<Change DurationBack=\"0.2\" RectangleShadow.Size=\"20\" />\n\t\t</Clicked>\n\t</Rectangle>",
    "expected_sha256": "aad8de3bddc95823933618368ef9be90299fbf736fdc4b683dc634fc33afd9bd",
    "language": "uno",
    "raw_comment": "/** Draws a shadow behind an element.\n\n\t\t## Example\n\n\t\tThis example shows a rounded rectangle with a shadow that animates in size when pressed:\n\n\t\t\t<Rectangle Width=\"100\" Height=\"100\" Color=\"Red\" CornerRadius=\"5\">\n\t\t\t\t<Shadow ux:Name=\"RectangleShadow\" Size=\"10\" />\n\t\t\t\t<Clicked>\n\t\t\t\t\t<Change DurationBack=\"0.2\" RectangleShadow.Size=\"20\" />\n\t\t\t\t</Clicked>\n\t\t\t</Rectangle>\n\n\t*/",
    "raw_sha256": "176652925238ea304cdcabf694e4ca5c09b4a6438a45029c9a49a546cd9f7a4e"
  },
  {
    "case_id": "uno-block-635e059067ee5d94",
    "expected_cleaned": "A list of named expressions that will be evaluated and injected as variables into the script.\n\nThis property allows injecting dependencies defined as UX expressions into the script using the `dep:` XML namespace.\n\nExample:\n```xml\n\t<JavaScript>\n\t\texports.foo = 123\n\t</JavaScript>\n\t<JavaScript dep:foo=\"{foo}\">\n\t\tfoo // this is now 123\n\t</JavaScript>\n```\nA script is not executed until all of its dependencies are available. If any of the dependencies change, the script is re-executed.\n\nThis has multiple use-cases:\n* Accessing data from data context `dep:foo=\"{foo}\"`\n* Accessing properties synchronously `dep:SomeProp=\"{Property SomeProp}\"`",
    "expected_sha256": "67ae0b4a3b77082ee1e1286d99e7432e0249512bcbb93748369dd1ec7c7a9f5d",
    "language": "uno",
    "raw_comment": "/** A list of named expressions that will be evaluated and injected as variables into the script.\n\n\t\t\tThis property allows injecting dependencies defined as UX expressions into the script using the `dep:` XML namespace.\n\n\t\t\tExample:\n\t\t\t```xml\n\t\t\t\t<JavaScript>\n\t\t\t\t\texports.foo = 123\n\t\t\t\t</JavaScript>\n\t\t\t\t<JavaScript dep:foo=\"{foo}\">\n\t\t\t\t\tfoo // this is now 123\n\t\t\t\t</JavaScript>\n\t\t\t```\n\t\t\tA script is not executed until all of its dependencies are available. If any of the dependencies change, the script is re-executed.\n\n\t\t\tThis has multiple use-cases:\n\t\t\t* Accessing data from data context `dep:foo=\"{foo}\"`\n\t\t\t* Accessing properties synchronously `dep:SomeProp=\"{Property SomeProp}\"`\n\t\t*/",
    "raw_sha256": "6143b98ddf20187db605d925a87c385021d498144bcc3dadcff30ee5b12295e6"
  },
  {
    "case_id": "uno-block-8c5c6bd319b6cf90",
    "expected_cleaned": "Launch the default email application with an optional template\n\nYou'll find this trigger action in the Fuse.Launcher package, which have to be referenced from your uno project.\nFor example:\n```json\n\t{\n\t\t\"Packages\": [\n\t\t\t\"Fuse\",\n\t\t\t\"FuseJS\",\n\t\t\t\"Fuse.Launcher\"\n\t\t]\n\t}\n```\n> Note it's expected that the 'To' parameter is set\n\n## Example\n```xml\n\t<StackPanel Margin=\"20\">\n\t\t<Button Margin=\"10\" Text=\"Send email\">\n\t\t\t<Clicked>\n\t\t\t\t<LaunchEmail To=\"email@example.com\" Subject=\"Test\" CarbonCopy=\"\" BlindCarbonCopy=\"\" Message=\"Hello world!\" />\n\t\t\t</Clicked>\n\t\t</Button>\n\t</StackPanel>\n```",
    "expected_sha256": "20c7f835ab0d11ac8016967f3dd454201cae8a812ebe3aa5d94c3ba7f4d600e6",
    "language": "uno",
    "raw_comment": "/** Launch the default email application with an optional template\n\n\t\tYou'll find this trigger action in the Fuse.Launcher package, which have to be referenced from your uno project.\n\t\tFor example:\n\t\t```json\n\t\t\t{\n\t\t\t\t\"Packages\": [\n\t\t\t\t\t\"Fuse\",\n\t\t\t\t\t\"FuseJS\",\n\t\t\t\t\t\"Fuse.Launcher\"\n\t\t\t\t]\n\t\t\t}\n\t\t```\n\t\t> Note it's expected that the 'To' parameter is set\n\n\t\t## Example\n\t\t```xml\n\t\t\t<StackPanel Margin=\"20\">\n\t\t\t\t<Button Margin=\"10\" Text=\"Send email\">\n\t\t\t\t\t<Clicked>\n\t\t\t\t\t\t<LaunchEmail To=\"email@example.com\" Subject=\"Test\" CarbonCopy=\"\" BlindCarbonCopy=\"\" Message=\"Hello world!\" />\n\t\t\t\t\t</Clicked>\n\t\t\t\t</Button>\n\t\t\t</StackPanel>\n\t\t```\n\t*/",
    "raw_sha256": "2646c26c175a852e6e86b9fee2cee8be4173550c3675f0f90524dfab25815e1c"
  },
  {
    "case_id": "uno-block-e70b0c1f7753614e",
    "expected_cleaned": "Returns the parameter of the given page (visual), parsed from a JSON string.\n\nUsage:\n\n\t<Text Value=\"parameter(this).title\" />\n\nThe parameter can be ommited",
    "expected_sha256": "acecf8782521870505924462286932deb41f2fbb2b2c28728aa6bb5a2f1d01d5",
    "language": "uno",
    "raw_comment": "/** Returns the parameter of the given page (visual), parsed from a JSON string.\n\n\t\tUsage:\n\n\t\t\t<Text Value=\"parameter(this).title\" />\n\n\t\tThe parameter can be ommited\n\t*/",
    "raw_sha256": "df5321ee74901169b559950476d37e13d165c3c81fd174c4af0983a4fb6bcb1a"
  },
  {
    "case_id": "uno-block-f23288d1521f9164",
    "expected_cleaned": "Provides an image fetched via HTTP which can be displayed by the @Image control.\n\n> *Note* @Image provides a shorthand for this, using its [Url](api:fuse/controls/image/url) property.\n\n## Example\n\n\t<Image>\n\t\t<HttpImageSource Url=\"https://upload.wikimedia.org/wikipedia/commons/0/06/Kitten_in_Rizal_Park%2C_Manila.jpg\" />\n\t</Image>",
    "expected_sha256": "829706c9016179f3d1b098536375e17f9d2347da0f15563ca4502efa64d9a5d4",
    "language": "uno",
    "raw_comment": "/** Provides an image fetched via HTTP which can be displayed by the @Image control.\n\t\n\t\t> *Note* @Image provides a shorthand for this, using its [Url](api:fuse/controls/image/url) property.\n\n\t\t## Example\n\n\t\t\t<Image>\n\t\t\t\t<HttpImageSource Url=\"https://upload.wikimedia.org/wikipedia/commons/0/06/Kitten_in_Rizal_Park%2C_Manila.jpg\" />\n\t\t\t</Image>\n\n\t*/",
    "raw_sha256": "8d75f51bbe80ffd5f755b915971dd00a1c4d5bb429088d4b2f2a2fb6eee65af1"
  }
]"""
)

assert len(CASES) == 25
assert {case["case_id"] for case in CASES} == EXPECTED_CASE_IDS


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["case_id"])
def test_conservative_real_world_failure_regressions(case):
    """Preserve the frozen input and exact deletion-only Sol proposal."""

    raw_comment = case["raw_comment"]
    expected_cleaned = case["expected_cleaned"]
    assert hashlib.sha256(raw_comment.encode("utf-8")).hexdigest() == case["raw_sha256"]
    assert hashlib.sha256(expected_cleaned.encode("utf-8")).hexdigest() == case["expected_sha256"]
    assert sanitize_comment(case["language"], raw_comment) == expected_cleaned
