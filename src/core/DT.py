import time

import allure
import pytest
import pymysql
import os, sys,shutil
from selenium.common.exceptions import NoSuchWindowException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from configparser import ConfigParser
import logging as logger

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
Pic_Base_Dir=os.path.join(BASE_DIR , 'Screenshot')
currentPath = os.path.dirname(os.path.abspath(__file__))
root_path1 = os.path.abspath(os.path.join(currentPath, "../.."))
config_data = os.path.join(root_path1, 'config.properties')
conf = ConfigParser()
conf.read(config_data)

def Action(cls,data):
    """
    Case Action
    :param data:
    :return:
    """
    # pool = ['method','name','by','element','assertText']
    for operate in data:
        if 'element' in operate:
            #params = cls.__getattribute__(operate['method']).__code__.co_varnames
            if operate['method'] == 'inputText' or operate['method'] == 'assertDtEquals':
                try:
                    cls.__getattribute__(operate['method'])(operate['by'], operate['element'],operate['text'])
                except TypeError as e:
                    logger.info('%s' % (e))
            else:
                try:
                    cls.__getattribute__(operate['method'])(operate['by'], operate['element'])
                except TypeError as e:
                    logger.info('%s' % (e))
        else:
            try:
                cls.__getattribute__(operate['method'])()
            except TypeError as e:
                logger.info('%s' % (e))

class DT(object):

    waitTime = int(conf.get("SectionA", "wTime"))
    def __init__(self,driver):
        self.driver= driver

    def quit(self):
        self.driver.quit()

    def getWebPage(self):
        self.driver.get(conf.get("Url","url"))

    def findWebView(self,webview):
        driver = self.driver
        if not webview is None:
            return driver.find_element_by_xpath(webview)
        return None

    def find_element(self, *loc):
        return self.driver.find_element(*loc)

    def find_elements(self, *loc):
        return self.driver.find_elements(*loc)

    def inputText(self, way,value,text):
        # return self.findView(way, value).send_keys(text)
        try:
            self.findView(way,value).clear()
            self.findView(way, value).send_keys(text)
            logger.info("通过" + way + "方式定位到元素：" + value + "输入值：" + text)
        except TimeoutException as timee:
            logger.info("通过" + way + "方式定位元素：" + value + "超时")
            raise timee
        except Exception as e:
            logger.info("未通过" + way + "方式定位到元素：" + value + "输入值：" + text)
            raise e

    def inputByAutoIT(self, way,value,exepath):
        try:
            self.click(way,value)
            os.system(exepath)
            logger.info("执行上传文件通过")
        except Exception as e:
            logger.info("执行上传文件失败")
            raise e


    def click(self, way,value):
        # return self.findView(way,value).click()
        try:
            self.findView(way, value).click()
            logger.info("通过" + way + "方式定位到元素：" + value + "点击")
        except TimeoutException as timee:
            logger.info("通过" + way + "方式定位元素：" + value + "超时")
            raise timee
        except Exception as e:
            logger.info("未通过" + way + "方式定位到元素：" + value + "点击")
            raise e


    def get_title(self):
        return self.driver.title

    def set_cookies(self):
        kwargs = dict(
            name=conf.get('Cookie','name')
            ,value=conf.get('Cookie','value')
        )
        self.driver.add_cookie(kwargs)
        self.getWebPage()
    #移除某个属性值
    def removeAttribute(self,way,value,attribute):
        js = 'document.getElementById("%s").removeAttribute("%s");'%(value,attribute)  # 移除属性
        self.driver.execute_script(js)

    #fixme 需要左滑动和右滑动的js代码
    def swipe(self,way=0,value=0,direction="UP"):
        '''web页面滑动，
           :Args: UP:滑动到最底部
           :Args DOWN:滑动到最上部
        '''
        driver = self.driver
        try:
            if(direction is "UP"):
                js="window.scrollTo(0,document.body.scrollHeight)"
                driver.execute_script(js)
            elif(direction is "DOWN"):
                js = "window.scrollTo(0,0)"
                driver.execute_script(js)
            elif (direction is "ELE"):
                target = self.findView(way,value)
                driver.execute_script("arguments[0].scrollIntoView();", target)
        except Exception as e:
            raise e

    #获取text0520
    def get_attribute_text(self,way,value):
        return self.findView(way,value).text

    #获取tag_name0520
    def get_attribute_tag_name(self,way,value):
        return self.findView(way,value).tag_name

    #获取某个属性值0520
    def get_attribute(self,way,value,attribute):
        return self.findView(way,value).get_attribute(attribute)

    def saveScreenshotPNG(self,path=Pic_Base_Dir):
        # 去除首位空格
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")
        #日期
        riqi= time.strftime("%Y-%m-%d", time.localtime())
        pic_dir_path = os.path.join(path, riqi)
        isExists = os.path.exists(pic_dir_path)
        if not isExists:
            os.makedirs(pic_dir_path)
        else:
            pass

        date = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
        filepath=os.path.join(pic_dir_path,date+".png")
        # screen =self.driver.save_screenshot(pic_dir_path+"/"+date+".png")
        self.driver.get_screenshot_as_file(filepath)
        with allure.step('screenshots'):
            allure.attach.file(filepath, attachment_type=allure.attachment_type.PNG)
        return filepath

    def clickWithscreenshot(self,way,value):
        '''
          点击带截图
        '''
        self.click(way,value)
        self.saveScreenshotPNG()

    def findView(self,way,value):
        driver = self.driver
        if(way == "ID"):
            return WebDriverWait(self.driver, self.waitTime).until(lambda driver: driver.find_element(by=By.ID, value=value))
        elif(way == "NAME"):
            return WebDriverWait(self.driver, self.waitTime).until(lambda driver: driver.find_element(by=By.NAME, value=value))
        elif (way ==  "CLASS_NAME"):
            value1 = value.split(":")
            viewList = WebDriverWait(self.driver, self.waitTime).until(lambda driver: driver.find_elements(by=By.CLASS_NAME, value=value1[0]))
            return viewList[value1[1]]
        elif (way == "XPATH"):
            return WebDriverWait(self.driver, self.waitTime).until(lambda driver: driver.find_element(by=By.XPATH, value=value))
        elif (way == "CSS_SELECTOR"):
            return WebDriverWait(self.driver, self.waitTime).until(lambda driver: driver.find_element(by=By.CSS_SELECTOR, value=value))
        elif (way == "PARTIAL_LINK_TEXT"):
            return WebDriverWait(self.driver, self.waitTime).until(lambda driver: driver.find_element(by=By.PARTIAL_LINK_TEXT, value=value))
        elif (way == "TAG_NAME"):
            return WebDriverWait(self.driver, self.waitTime).until(lambda driver: driver.find_element(by=By.TAG_NAME, value=value))
        elif (way == "LINK_TEXT"):
            return WebDriverWait(self.driver, self.waitTime).until(lambda driver: driver.find_element(by=By.LINK_TEXT, value=value))
        else:
            logger.info("无效的定位方式")
            return False

    def getValue(self,way,value):
        return self.findView(way,value).text

    def assertDtEquals(self,way,value,expect):
        '''
          断言实际值等于期望值
        '''

        try:
            actual = self.findView(way, value).text
            assert (actual == expect)
        except TimeoutException as timee:
            logger.info("断言相等失败，通过" + way + "方式定位元素：" + value + "超时")
            raise timee
        except Exception as e:
            logger.info("断言相等失败，实际值：" + actual + "；" + "期望值：" + expect)
            raise e


    def assertDtEqualsDB(self,way,value,sql):
        '''
          断言实际值等于期望值
        '''
        # actual = self.findView(way,value).text
        # expect = self.mysql_search(sql)
        try:
            actual = self.findView(way, value).text
            expect = self.mysql_search(sql)
            assert (actual == expect)
        except TimeoutException as timee:
            logger.info("断言相等失败，通过" + way + "方式定位元素：" + value + "超时")
            raise timee
        except Exception as e:
            logger.info("断言相等失败，实际值：" + actual + "；" + "期望值：" + expect)
            raise e

    def assertDtContainDB(self,way,value,sql):
        '''
          断言实际值包含期望值
        '''
        # actual = self.findView(way,value).text
        # expect = self.mysql_search(sql)

        try:
            actual = self.findView(way, value).text
            expect = self.mysql_search(sql)
            assert expect in actual
        except TimeoutException as timee:
            logger.info("断言包含失败，通过" + way + "方式定位元素：" + value + "超时")
            raise timee
        except Exception as e:
            logger.info("断言包含失败，实际值：" + actual + "；" + "期望值：" + expect)
            raise e

    def assertDtNotEqualsDB(self,way,value,sql):
        '''
          断言实际值不等于期望值
        '''
        # actual = self.findView(way,value).text
        # expect = self.mysql_search(sql)

        try:
            actual = self.findView(way, value).text
            expect = self.mysql_search(sql)
            assert (actual != expect)
        except TimeoutException as timee:
            logger.info("断言不相等失败，通过" + way + "方式定位元素：" + value + "超时")
            raise timee
        except Exception as e:
            logger.info("断言不相等失败，实际值：" + actual + "；" + "期望值：" + expect)
            raise e


    def assertDtNotEquals(self,way,value,expect):
        '''
          断言实际值不等于期望值
        '''
        # actual=self.findView(way,value).text
        try:
            actual = self.findView(way, value).text
            assert (actual != expect)
        except TimeoutException as timee:
            logger.info("断言不相等失败，通过" + way + "方式定位元素：" + value + "超时")
            raise timee
        except Exception as e:
            logger.info("断言不相等失败，实际值：" + actual + "；" + "期望值：" + expect)
            raise e


    def assertDtContain(self,way,value,expect):
        '''
          断言期期望值含有实际值
        '''
        # actual = self.findView(way, value).text
        try:
            actual = self.findView(way, value).text
            assert expect in actual
        except TimeoutException as timee:
            logger.info("断言包含失败，通过" + way + "方式定位元素：" + value + "超时")
            raise timee
        except Exception as e:
            logger.info("断言包含失败，实际值：" + actual + "；" + "期望值：" + expect)

            raise e

    def assertIsSelected(self,way,value):
        '''
          断言期某个值是否被选中0520
        '''
        try:
            assert self.findView(way,value).is_selected()
            logger.info("通过" + way + "方式定位的元素：" + value + "被选中")
        except TimeoutException as timee:
            logger.info("断言被选中失败，通过" + way + "方式定位元素：" + value + "超时")
            raise timee
        except Exception as e:
            logger.info("断言被选中失败，通过" + way + "方式定位的元素：" + value + "未被选中")
            raise e


    def assertIsNotSelected(self,way,value):
        '''
          断言期某个值是否被选中0520
        '''
        try:
            assert self.findView(way,value).is_selected() == False
            logger.info("通过" + way + "方式定位的元素：" + value + "未被选中")
        except TimeoutException as timee:
            logger.info("断言未被选中失败，通过" + way + "方式定位元素：" + value + "超时")
            raise timee
        except Exception as e:
            logger.info("断言未被选中失败，通过" + way + "方式定位的元素：" + value + "被选中")
            raise e


    def assertIsDisplayed(self,way,value):
        '''
          断言期某个值是否显示0520
        '''
        try:
            assert self.findView(way,value).is_displayed()
            logger.info("通过" + way + "方式定位的元素：" + value + "已显示")
        except TimeoutException as timee:
            logger.info("断言显示失败，通过" + way + "方式定位元素：" + value + "超时")
            raise timee
        except Exception as e:
            logger.info("断言显示失败，通过" + way + "方式定位的元素：" + value + "未显示")
            raise e


    def assertIsNotDisplayed(self,way,value):
        '''
          断言期某个值是否显示0520
        '''
        try:
            assert self.isElementExist(way,value) == False
            logger.info("通过" + way + "方式定位的元素：" + value + "未显示")
        except TimeoutException as timee:
            logger.info("断言不显示失败，通过" + way + "方式定位元素：" + value + "超时")
            raise timee
        except Exception as e:
            logger.info("断言不显示失败，通过" + way + "方式定位的元素：" + value + "已显示")

            raise e
    
    def isElementExist(self,way,value):
        '''
          判断元素是否存在
        '''
        try:
            self.findView(way,value)
            return True
        except Exception as e:
            return False

    def assertIsEnabled(self,way,value):
        '''
          断言期某个值是否可编辑0520
        '''
        try:
            assert self.findView(way,value).is_enabled()
            logger.info("通过" + way + "方式定位的元素：" + value + "可编辑")
        except TimeoutException as timee:
            logger.info("断言可编辑失败，通过" + way + "方式定位元素：" + value + "超时")
            raise timee
        except Exception as e:
            logger.info("断言可编辑失败，通过" + way + "方式定位的元素：" + value + "不可编辑")
            raise e


    def assertIsNotEnabled(self,way,value):
        '''
          断言期某个值是否可编辑0520
        '''
        try:
            assert self.findView(way,value).is_enabled() == False
            logger.info("通过" + way + "方式定位的元素：" + value + "不可编辑")
        except TimeoutException as timee:
            logger.info("断言不可编辑失败，通过" + way + "方式定位元素：" + value + "超时")
            raise timee
        except Exception as e:
            logger.info("断言不可编辑失败，通过" + way + "方式定位的元素：" + value + "可编辑")
            raise e


    def assertAttribute(self,way,value,attribute,expect):
        '''
          断言属性值与期望值相同
        '''
        # actual = self.get_attribute(way,value,attribute)
        try:
            actual = self.get_attribute(way, value, attribute)
            assert (expect == actual)
        except TimeoutException as timee:
            logger.info("断言属性值失败，通过" + way + "方式定位元素：" + value + "超时")
            raise timee
        except Exception as e:
            logger.info("断言属性值失败，实际值：" + actual + "；" + "期望值：" + expect)
            raise e


    def assertAlertMessage(self,expect):
        '''
          断言alert的text值与期望值相同
        '''
        t = self.driver.switch_to.alert
        actual = t.text
        t.accept
        try:
            assert (expect == actual)
        except Exception as e:
            logger.info("实际值：" + actual + "；" + "期望值：" + expect)
            raise e


    def dbClick(self,way,value):
        '''寻找元素进行双击
           :Args: way:string
           :Args value:string
        '''

        driver = self.driver
        web_element = self.findView(way,value)
        ActionChains(driver).double_click(web_element).perform()

    def longPress(self,way,value):
        '''寻找元素保持点击
                   :Args: way:string
                   :Args value:string
                '''
        web_element = self.findView(way, value)
        ActionChains(self.driver).click_and_hold(web_element).perform()

    #fixme 需要左滑动和右滑动的js代码
    def swipe(self,direction="UP"):
        '''web页面滑动，
           :Args: UP:滑动到最底部
           :Args DOWN:滑动到最上部
        '''
        driver = self.driver
        try:
            if(direction is "UP"):
                js="window.scrollTo(0,document.body.scrollHeight)"
                driver.execute_script(js)
            elif(direction is "DOWN"):
                js = "window.scrollTo(0,0)"
                driver.execute_script(js)
            else:
                logger.info("无效的方向")
        except Exception as e:
            logger.info("滑动失败")
            raise e

    def swipeToElement(self,way=0,value=0,direction="ELE"):
        '''web页面滑动，
           :Args: UP:滑动到最底部
           :Args DOWN:滑动到最上部
        '''
        driver = self.driver
        try:
            if (direction is "ELE"):
                target = self.findView(way,value)
                driver.execute_script("arguments[0].scrollIntoView();", target)
            else:
                logger.info("无效的方向")
        except Exception as e:
            logger.info("滑动失败")
            raise e

    def drag_and_drop(self,way,value,way1,value1):
        '''寻找元素进行拖拽
                   :Args: way:string
                   :Args value:string
                '''
        web_element_source = self.findView(way, value) #源元素
        web_element_target = self.findView(way1, value1) #目标元素
        ActionChains(self.driver).drag_and_drop(web_element_source,web_element_target).perform()

    def sleep(self,second):
        time.sleep(second)

    # fixme 切换回主窗口时需要增加一个方法
    def frame(self,name):
        #driver定位至frame/iframe
        driver = self.driver
        driver.switch_to.frame(name)
        # driver.switch_to.default_content()   切换回主窗口

    def frameByElement(self,way,value):
        driver = self.driver
        frame = self.findView(way,value)
        driver.switch_to.frame(frame)
        # driver.switch_to.default_content()   切换回主窗口

    def switch2Window(self,i):
        #切换到特定窗口句柄0520
        handles = self.driver.window_handles
        self.driver.switch_to_window(handles[i])

    def window(self,*windowTitle):
        # driver当前页面的所有句柄，默认切换到最后一个
        handles = self.driver.window_handles
        if windowTitle != ():
            for s in handles:
                self.driver.switch_to_window(s)
                if self.driver.title == windowTitle[0]:
                    print("Switch to window: " + windowTitle[0] + " successfully!")
                    break
                else:
                    continue
            else:
                print("Window: " + windowTitle[0] + " not found!")
        else:
            self.driver.switch_to_window(handles[-1])
            print("1111")

    # 通过Title来切换窗口
    def switchToWindowByTitle(self,windowTitle):
        currentHandle = self.driver.current_window_handle
        handles = self.driver.window_handles
        for s in handles:
            if s == currentHandle:
                continue
            else:
                self.driver.switch_to_window(s)
                if self.driver.title == windowTitle:
                    print("Switch to window: "+ windowTitle + " successfully!")
                    break
                else:
                    continue
        else:
            print("Window: " +windowTitle + " not found!")

    def close(self):
        # driver关闭当前页面
        self.driver.close()

    #右击
    def clickRight(self,way,value):
        web_element = self.findView(way, value)
        ActionChains(self.driver).context_click(web_element).perform()

    #鼠标悬停0520
    def mouseOver(self,way,value):
        web_element = self.findView(way, value)
        ActionChains(self.driver).move_to_element(web_element).perform()

    def frame2Default(self):
        self.driver.switch_to.default_content()

    def carriageReturn(self):
        ActionChains(self.driver).sendKeys(Keys.ENTER).perform()

    #执行键盘操作0520
    def executeKeyBoard(self,*args):
        ActionChains(self.driver).sendKeys(*args).perform()

    #执行js0520
    def executeJs(self,js,*target):
        self.driver.execute_script(js,*target)

    #复选框单选0520
    def selectOneCheckBox(self,way,value):
        self.findView(way,value).click()

    # 复选框全选0520
    def selectAllCheckBox(self, *locator):
        checkboxs = WebDriverWait(self.driver,10).until(lambda x:x.find_elements(*locator))
        for i in checkboxs:
            i.click()

    def switch2Alert(self):
        '''
          切换进alert，accpet
        '''
        t = self.driver.switch_to.alert
        t.accept()

    def switch2AlertAndGetText(self):
        '''
          切换进alert，accept，并返回text
        '''
        t = self.driver.switch_to.alert
        text = t.text
        t.accept()
        return text

    def switch2AlertSendkeys(self,text):
        '''
          切换进alert，accept，并返回text
        '''
        t = self.driver.switch_to.alert
        t.send_keys(text)
        t.accept()

    def selectSelectByIndex(self,way,vlaue,index):
        '''
          按下标选择下拉选项
        '''
        el = self.findView(way,vlaue)
        Select(el).select_by_index(index)

    def selectSelectByValue(self,way,vlaue,text):
        '''
          按value值选择下拉选项
        '''
        el = self.findView(way,vlaue)
        Select(el).select_by_value(text)

    def selectSelectByVisibleText(self,way,vlaue,visibletext):
        '''
          按可见文本选择下拉选项
        '''
        el = self.findView(way,vlaue)
        Select(el).select_by_visible_text(visibletext)
		
    def assertIsTitle(self, _text):
        try:
            ele = WebDriverWait(self.driver, 10).until(EC.title_is(_text))
            assert ele
        except Exception as e:
            raise e

    def assertIsTitleContains(self, _text):
        try:
            ele = WebDriverWait(self.driver, 10).until(EC.title_contains(_text))
            assert ele
        except Exception as e:
            raise e

    def assertIsAlertPresent(self):
        '''判断是否有alert'''
        try:
            ele = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            assert ele
        except Exception as e:
            raise e

    def connectDb(self):
        '''连接数据库'''
        try:
            #连接数据库
            self.conn = pymysql.connect(host=conf.get('SectionDb','host'),
                                        user=conf.get('SectionDb','username'),
                                        password=conf.get('SectionDb','password'),
                                        db=conf.get('SectionDb','database'),
                                        port=int(conf.get('SectionDb','port')),
                                        charset='utf8',
                                        cursorclass=pymysql.cursors.DictCursor)
            # 通过cursor创建游标
            self.cur = self.conn.cursor()
        except Exception as e:
            logger.error("连接数据库错误")
            raise e

    def mysql_search(self,sql):
        '''查询数据'''
        try:
            self.connectDb()
            self.cur.execute(sql)
            result = self.cur.fetchone()  # 查询数据库单条数据
            if(len(result)>=1):
                res = str(list(result.values())[0])
            else:
                logger.error("未查询到数据")
            # res = re.match('','')
            # result = cursor.fetchall() #查询数据库多条数据
            # 提交sql
            self.conn.commit()
            self.conn.close()
            return res
        except Exception as e:
            self.conn.close()
            logger.error("查询错误")
            raise e









