
import pytest
import allure
import logging as logger
from src.core.action import Action ,ElementActions
from src.core.BaseTest import setUp
from src.utils.initCase import initCase

CaseData = initCase('roleManage.yml')
@allure.feature('角色管理')
class Test01():

    def setup_method(self):
        global driver , dt
        driver = setUp(self)
        dt = ElementActions(driver)
        dt.getWebPage()
    def teardown_method(self):
        dt.quit()
        logger.info("测试运行结束")


    @allure.story("添加角色-添加成功")
    @allure.severity('')
    def testCase_01(self):
        """
        添加角色-添加成功
        """
        test_info = CaseData['test_info']
        test_case = test_info[0]['test_case']
        Action(dt,test_case)


    @allure.story("添加角色-角色已存在")
    @allure.severity('')
    def testCase_02(self):
        """
        添加角色-角色已存在
        """
        test_info = CaseData['test_info']
        test_case = test_info[1]['test_case']
        Action(dt,test_case)


    @allure.story("查询角色")
    @allure.severity('')
    def testCase_03(self):
        """
        查询角色
        """
        test_info = CaseData['test_info']
        test_case = test_info[2]['test_case']
        Action(dt,test_case)


    @allure.story("修改角色权限")
    @allure.severity('')
    def testCase_04(self):
        """
        修改角色权限
        """
        test_info = CaseData['test_info']
        test_case = test_info[3]['test_case']
        Action(dt,test_case)


