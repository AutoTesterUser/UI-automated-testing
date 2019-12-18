
import pytest
import allure
import logging as logger
from src.core.action import Action ,ElementActions
from src.core.BaseTest import setUp
from src.utils.initCase import initCase

CaseData = initCase('Template.yml')
@allure.feature('Moudle')
class Test01():

    def setup_method(self):
        global driver , dt
        driver = setUp(self)
        dt = ElementActions(driver)
        dt.getWebPage()
    def teardown_method(self):
        dt.quit()
        logger.info("测试运行结束")


    @allure.story("S")
    @allure.severity('')
    def testCase(self):
        """
        admin
        """
        test_info = CaseData['test_info']
        test_case = test_info[0]['test_case']
        Action(dt,test_case)


