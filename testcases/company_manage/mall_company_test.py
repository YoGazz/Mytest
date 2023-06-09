# NOTE: Generated By HttpRunner v4.3.0
# FROM: testcases/company_manage/mall_company.yml
from httprunner import HttpRunner, Config, Step, RunRequest
from httprunner import RunTestCase

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from testcases.login.login_test import TestCaseLogin as Login


class TestCaseMallCompany(HttpRunner):

    config = (
        Config("字典项")
        .variables(**{"code": "D0067"})
        .base_url("${ENV(java_base_url)}")
        .verify(False)
    )

    teststeps = [
        Step(RunTestCase("用户登录").call(Login).export(*["access_token"])),
        Step(
            RunRequest("获取公司类型")
            .get("/pbc-system/sysDictInfo/findByCode")
            .with_params(**{"code": "$code"})
            .with_headers(**{"Authorization": "Bearer $access_token"})
            .extract()
            .with_jmespath("body.msg[0].itemValue", "default_company_type")
            .with_jmespath("body.msg[1].itemValue", "main_company_type")
            .with_jmespath("body.msg[1].itemValue", "sub_company_type")
            .with_jmespath("body.msg[1].itemValue", "branch_company_type")
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.success", True)
        ),
        Step(
            RunRequest("获取集团列表")
            .get("/pbc-system/sysGroupCompanyInfo/getGroupCompanyList")
            .with_headers(**{"Authorization": "Bearer $access_token"})
            .extract()
            .with_jmespath("body.msg[0].id", "group_company_id")
            .with_jmespath("body.msg[0].name", "group_name")
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.success", True)
        ),
    ]


if __name__ == "__main__":
    TestCaseMallCompany().test_start()
