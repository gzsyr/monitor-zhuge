import os
import time

import pytest

WORKSPACE_DIR = os.path.abspath(os.getcwd())

if __name__ == '__main__':
    print("run __main__ ")

    allure_result_path = WORKSPACE_DIR + "\\allureResult\\result-" + time.strftime('%Y-%m-%d')
    pytest.main(["-v",
                 "-s",
                 # "-rs",
                 # "--show-capture=all",
                 "--html=pytestReport.html",  # html的报告
                 # "--co",  # 仅收集用例
                 "--alluredir", allure_result_path,  # 使用allure报告
                 "./tt.py::test_",
                 ])

    a_report_path = WORKSPACE_DIR + '\\allureReport\\report-'+time.strftime('%Y-%m-%d')  # allure 报告路径

    command_allure_generate = f"allure generate --clean {allure_result_path} -o {a_report_path}"
    os.system(command_allure_generate)  # 生成测试报告

    # command_allure_open = f'allure open {a_report_path}'
    # os.system(command_allure_open)  # 打开测试报告