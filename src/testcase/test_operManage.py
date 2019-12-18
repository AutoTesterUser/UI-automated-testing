
import pytest
import allure
import logging as logger
from src.core.action import Action ,ElementActions
from src.core.BaseTest import setUp
from src.utils.initCase import initCase

CaseData = initCase('operManage.yml')
@allure.feature('操作员管理')
class Test01():

    def setup_method(self):
        global driver , dt
        driver = setUp(self)
        dt = ElementActions(driver)
        dt.getWebPage()
    def teardown_method(self):
        dt.quit()
        logger.info("测试运行结束")


    @allure.story("添加操作员-添加成功")
    @allure.severity('')
    def testCase_01(self):
        """
        添加操作员-添加成功
        """
        test_info = CaseData['test_info']
        test_case = test_info[0]['test_case']
        Action(dt,test_case)


