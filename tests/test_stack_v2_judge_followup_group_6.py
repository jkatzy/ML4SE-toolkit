import pytest

from ml4setk import CommentSanitizer, QueryMatch

pytestmark = pytest.mark.unit


def _sanitize(language: str, raw_comment: str) -> str:
    return CommentSanitizer(language).sanitize(QueryMatch("", "", raw_comment))


@pytest.mark.parametrize(
    ("language", "raw_comment", "expected_cleaned"),
    [
        pytest.param(
            "asymptote",
            "/*******************/\n/* DRAW DECORATION */\n/*******************/",
            "DRAW DECORATION",
            id="asymptote-block-76394f501d428bf8",
        ),
        pytest.param(
            "blade",
            "{{--            @if($message = Session::get('error'))--}}\n"
            '            {{--                <div class="alert alert-danger">--}}\n'
            "            {{--                    <p>{{ $message }}</p>--}}\n"
            "            {{--                </div>--}}\n"
            "            {{--            @endif--}}",
            "@if($message = Session::get('error'))\n"
            '    <div class="alert alert-danger">\n'
            "        <p>{{ $message }}</p>\n"
            "    </div>\n"
            "@endif",
            id="blade-block-572c96ed972bc96a",
        ),
        pytest.param(
            "blade",
            "{{--<div>--}}\n"
            '                        {{--<span class="captcha">'
            "{{ __('pages.session.create.form.label.captcha') }}*</span>--}}\n"
            '                        {{--<input id="captcha" '
            "class=\"form-control{{ $errors->has('captcha')?' error':'' }}\" "
            'name="captcha" value="" '
            "placeholder=\"{{ $errors->first('captcha') }}\" >--}}\n"
            '                        {{--<img class="thumbnail captcha" '
            "src=\"{{ captcha_src('flat') }}\" "
            "onclick=\"this.src='/captcha/flat?'+Math.random()\" "
            'title="点击图片重新获取验证码">--}}\n'
            "                    {{--</div>--}}",
            "<div>\n"
            '    <span class="captcha">'
            "{{ __('pages.session.create.form.label.captcha') }}*</span>\n"
            '    <input id="captcha" '
            "class=\"form-control{{ $errors->has('captcha')?' error':'' }}\" "
            'name="captcha" value="" '
            "placeholder=\"{{ $errors->first('captcha') }}\" >\n"
            '    <img class="thumbnail captcha" '
            "src=\"{{ captcha_src('flat') }}\" "
            "onclick=\"this.src='/captcha/flat?'+Math.random()\" "
            'title="点击图片重新获取验证码">\n'
            "</div>",
            id="blade-block-60a1cf3725568301",
        ),
        pytest.param(
            "css",
            "/* ===============================================\n"
            " *\n"
            " *\tRESTIR内追加CSS\n"
            " *\tHOMEのBLOG箇所　フォント\n"
            " *\n"
            " * ============================================== */",
            "RESTIR内追加CSS\nHOMEのBLOG箇所　フォント",
            id="css-block-3c3e8615bc9dbfc5",
        ),
        pytest.param(
            "gdb",
            "################################# config FCMD end "
            "####################################",
            "config FCMD end",
            id="gdb-line-529159e764c0ac71",
        ),
        pytest.param(
            "ini",
            r";C:\\Program Files (x86)\\glassfish-3.1.2.2\\glassfish\\domains\\"
            r"domain1]deployer:gfv3ee6wc:localhost:4848",
            r"C:\\Program Files (x86)\\glassfish-3.1.2.2\\glassfish\\domains\\"
            r"domain1]deployer:gfv3ee6wc:localhost:4848",
            id="ini-line-1591e90128da1c5e",
        ),
        pytest.param(
            "ini",
            "; 0 - no pre-training, 1 - phoneme loss, 2 - word loss + phoneme loss",
            "0 - no pre-training, 1 - phoneme loss, 2 - word loss + phoneme loss",
            id="ini-line-5ff6e55c2d55af24",
        ),
        pytest.param(
            "jinja",
            "########## Your custom locations & settings ##########",
            "Your custom locations & settings",
            id="jinja-line-45338e3d94a9d108",
        ),
        pytest.param(
            "jsonnet",
            "# Model details:\n"
            "# - NL2Code\n"
            "# - Pretrained, fixed word embeddings\n"
            "#   - glove-42B\n"
            "#   - min_freq 50\n"
            "# - Spiderv2 encoder\n"
            "#   - question_encoder ['emb', 'bilstm']\n"
            "#   - column_encoder ['emb', 'bilstm-summarize']\n"
            "#   - table_encoder ['emb', 'bilstm-summarize']\n"
            "#   - upd_steps 4\n"
            "# - Optimization\n"
            "#   - max_steps 40k\n"
            "#   - batch_size 10\n"
            "#   - Adam with lr 1e-3",
            "Model details:\n"
            "- NL2Code\n"
            "- Pretrained, fixed word embeddings\n"
            "  - glove-42B\n"
            "  - min_freq 50\n"
            "- Spiderv2 encoder\n"
            "  - question_encoder ['emb', 'bilstm']\n"
            "  - column_encoder ['emb', 'bilstm-summarize']\n"
            "  - table_encoder ['emb', 'bilstm-summarize']\n"
            "  - upd_steps 4\n"
            "- Optimization\n"
            "  - max_steps 40k\n"
            "  - batch_size 10\n"
            "  - Adam with lr 1e-3",
            id="jsonnet-block-50c14750c090051b",
        ),
        pytest.param(
            "pascal",
            "{******************************************************************************}\r\n"
            "{                                                                              }\r\n"
            "{       WiRL: RESTful Library for Delphi                                       }\r\n"
            "{                                                                              }\r\n"
            "{       Copyright (c) 2015-2019 WiRL Team                                      }\r\n"
            "{                                                                              }\r\n"
            "{       https://github.com/delphi-blocks/WiRL                                  }\r\n"
            "{                                                                              }\r\n"
            "{******************************************************************************}",
            "WiRL: RESTful Library for Delphi\n"
            "\n"
            "Copyright (c) 2015-2019 WiRL Team\n"
            "\n"
            "https://github.com/delphi-blocks/WiRL",
            id="pascal-nested-0cd626204bd97c38",
        ),
        pytest.param(
            "pascal",
            "{********************************************************************}\n"
            "{                                                                    }\n"
            "{       Developer Express Visual Component Library                   }\n"
            "{       ExpressDataController                                        }\n"
            "{                                                                    }\n"
            "{       Copyright (c) 1998-2011 Developer Express Inc.               }\n"
            "{       ALL RIGHTS RESERVED                                          }\n"
            "{                                                                    }\n"
            "{   The entire contents of this file is protected by U.S. and        }\n"
            "{   International Copyright Laws. Unauthorized reproduction,         }\n"
            "{   reverse-engineering, and distribution of all or any portion of   }\n"
            "{   the code contained in this file is strictly prohibited and may   }\n"
            "{   result in severe civil and criminal penalties and will be        }\n"
            "{   prosecuted to the maximum extent possible under the law.         }\n"
            "{                                                                    }\n"
            "{   RESTRICTIONS                                                     }\n"
            "{                                                                    }\n"
            "{   THIS SOURCE CODE AND ALL RESULTING INTERMEDIATE FILES            }\n"
            "{   (DCU, OBJ, DLL, ETC.) ARE CONFIDENTIAL AND PROPRIETARY TRADE     }\n"
            "{   SECRETS OF DEVELOPER EXPRESS INC. THE REGISTERED DEVELOPER IS    }\n"
            "{   LICENSED TO DISTRIBUTE THE EXPRESSDATACONTROLLER AND ALL         }\n"
            "{   ACCOMPANYING VCL CONTROLS AS PART OF AN EXECUTABLE PROGRAM ONLY. }\n"
            "{                                                                    }\n"
            "{   THE SOURCE CODE CONTAINED WITHIN THIS FILE AND ALL RELATED       }\n"
            "{   FILES OR ANY PORTION OF ITS CONTENTS SHALL AT NO TIME BE         }\n"
            "{   COPIED, TRANSFERRED, SOLD, DISTRIBUTED, OR OTHERWISE MADE        }\n"
            "{   AVAILABLE TO OTHER INDIVIDUALS WITHOUT EXPRESS WRITTEN CONSENT   }\n"
            "{   AND PERMISSION FROM DEVELOPER EXPRESS INC.                       }\n"
            "{                                                                    }\n"
            "{   CONSULT THE END USER LICENSE AGREEMENT FOR INFORMATION ON        }\n"
            "{   ADDITIONAL RESTRICTIONS.                                         }\n"
            "{                                                                    }\n"
            "{********************************************************************}",
            "    Developer Express Visual Component Library\n"
            "    ExpressDataController\n"
            "\n"
            "    Copyright (c) 1998-2011 Developer Express Inc.\n"
            "    ALL RIGHTS RESERVED\n"
            "\n"
            "The entire contents of this file is protected by U.S. and\n"
            "International Copyright Laws. Unauthorized reproduction,\n"
            "reverse-engineering, and distribution of all or any portion of\n"
            "the code contained in this file is strictly prohibited and may\n"
            "result in severe civil and criminal penalties and will be\n"
            "prosecuted to the maximum extent possible under the law.\n"
            "\n"
            "RESTRICTIONS\n"
            "\n"
            "THIS SOURCE CODE AND ALL RESULTING INTERMEDIATE FILES\n"
            "(DCU, OBJ, DLL, ETC.) ARE CONFIDENTIAL AND PROPRIETARY TRADE\n"
            "SECRETS OF DEVELOPER EXPRESS INC. THE REGISTERED DEVELOPER IS\n"
            "LICENSED TO DISTRIBUTE THE EXPRESSDATACONTROLLER AND ALL\n"
            "ACCOMPANYING VCL CONTROLS AS PART OF AN EXECUTABLE PROGRAM ONLY.\n"
            "\n"
            "THE SOURCE CODE CONTAINED WITHIN THIS FILE AND ALL RELATED\n"
            "FILES OR ANY PORTION OF ITS CONTENTS SHALL AT NO TIME BE\n"
            "COPIED, TRANSFERRED, SOLD, DISTRIBUTED, OR OTHERWISE MADE\n"
            "AVAILABLE TO OTHER INDIVIDUALS WITHOUT EXPRESS WRITTEN CONSENT\n"
            "AND PERMISSION FROM DEVELOPER EXPRESS INC.\n"
            "\n"
            "CONSULT THE END USER LICENSE AGREEMENT FOR INFORMATION ON\n"
            "ADDITIONAL RESTRICTIONS.",
            id="pascal-nested-785e41bb73b8c062",
        ),
        pytest.param(
            "pascal",
            "{******************************************************************************}\r\n"
            "{ Author      : Loda                                                           }\r\n"
            "{ Create Date : 20060728                                                       }\r\n"
            "{                                                                              }\r\n"
            "{ Description : varios class and utils for basic manipulations of              }\r\n"
            "{               XML file and nodes                                             }\r\n"
            "{                                                                              }\r\n"
            "{ Define Use  : [none]                                                         }\r\n"
            "{ Side Effect : call CoInitialize                                              }\r\n"
            "{                                                                              }\r\n"
            "{ see region Internal_Doc                                                      }\r\n"
            "{                                                                              }\r\n"
            "{******************************************************************************}",
            "Author      : Loda\n"
            "Create Date : 20060728\n"
            "\n"
            "Description : varios class and utils for basic manipulations of\n"
            "              XML file and nodes\n"
            "\n"
            "Define Use  : [none]\n"
            "Side Effect : call CoInitialize\n"
            "\n"
            "see region Internal_Doc",
            id="pascal-nested-ea91009a21b3ce2f",
        ),
        pytest.param(
            "smarty",
            '{*<div class="container">*}\n'
            '\t\t{*<div class="row pt-50">*}\n'
            '\t\t\t{*<div class="col-md-3">*}\n'
            '\t\t\t\t{*<img src="{$WEB_ROOT}/images/backup/backup.png"/>*}\n'
            "\t\t\t{*</div>*}\n"
            '\t\t\t{*<div class="col-md-9">*}\n'
            '\t\t\t\t{*<h2 class="pt-20"><span class="txt-green-1eba5c">'
            "EXA</span> BACKUP</h2>*}\n"
            '\t\t\t\t{*<p class="font-14 mb-20" '
            'style="line-height: 28px">*}\n'
            "\t\t\t\t\t{*Sao lưu và khôi phục dữ liệu kết hợp phòng chống "
            "Ransomware, Hybrid Cloud Backup-as-a-Service Solution công nghệ "
            "Acronis*}\n"
            "\t\t\t\t{*</p>*}\n"
            "\t\t\t{*</div>*}\n"
            "\t\t{*</div>*}\n"
            "\t{*</div>*}",
            '<div class="container">\n'
            '\t<div class="row pt-50">\n'
            '\t\t<div class="col-md-3">\n'
            '\t\t\t<img src="{$WEB_ROOT}/images/backup/backup.png"/>\n'
            "\t\t</div>\n"
            '\t\t<div class="col-md-9">\n'
            '\t\t\t<h2 class="pt-20"><span class="txt-green-1eba5c">'
            "EXA</span> BACKUP</h2>\n"
            '\t\t\t<p class="font-14 mb-20" style="line-height: 28px">\n'
            "\t\t\t\tSao lưu và khôi phục dữ liệu kết hợp phòng chống "
            "Ransomware, Hybrid Cloud Backup-as-a-Service Solution công nghệ "
            "Acronis\n"
            "\t\t\t</p>\n"
            "\t\t</div>\n"
            "\t</div>\n"
            "</div>",
            id="smarty-block-f8c3165e05fd3570",
        ),
    ],
)
def test_stack_v2_sanitation_removes_all_syntax_scaffolding(
    language: str, raw_comment: str, expected_cleaned: str
):
    assert _sanitize(language, raw_comment) == expected_cleaned
