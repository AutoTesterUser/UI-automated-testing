

import allure
import time
import os.path
import logging as logger
from src.utils.common import Mock
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import * #导入所有的异常类
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from src.utils.config import conf_manage
from src.utils.common import mk_dir
conf = conf_manage()
baseDir = os.path.abspath(os.path.dirname(__file__)).split('src')[0]
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
                if operate['text'] not in Mock().methods():
                    with allure.step("%s"%(operate['name'])):
                        allure.attach(operate['text'])
                        cls.__getattribute__(operate['method'])((operate['by'], operate['element']),operate['text'])
                else:
                    with allure.step("%s" % (operate['name'])):
                        allure.attach(cls.__getattribute__( operate['text'])())
                        cls.__getattribute__(operate['method'])((operate['by'], operate['element']),cls.__getattribute__(operate['text'])())
            else:
                try:
                    with allure.step("%s"%(operate['name'])):
                        cls.__getattribute__(operate['method'])((operate['by'], operate['element']))
                except TypeError as e:
                    logger.info('%s' % (e))
        else:
            try:
                with allure.step("%s" % (operate['name'])):
                    cls.__getattribute__(operate['method'])()
            except TypeError as e:
                logger.info('%s' % (e))

class ElementActions(Mock):
    waitTime = int(conf.time_manage("${wTime}$"))
    def __init__(self,driver):
        """
        :param driver:打开浏览器驱动
        """
        self.driver = driver

    def get_page_title(self):
        logger.info("当前页面的title为: %s" % self.driver.title)
        return self.driver.title


    def find_element(self, *loc):
        try:
            # 元素可见时，返回查找到的元素；以下入参为元组的元素，需要加*
            WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element(*loc).is_displayed())
            return self.driver.find_element(*loc)
        except NoSuchElementException:
            logger.warning('找不到定位元素: %s' % loc[1])
            raise
        except TimeoutException:
            logger.warning('查找元素超时: %s' % loc[1])
            raise
    def set_cookies(self):
        kwargs = dict(
            name=conf.cookie_manage('${name}$')
            ,value=conf.cookie_manage('${value}$')
        )
        self.driver.add_cookie(kwargs)
        self.getWebPage()

    def findView(self,*loc):
        way, value = loc[0],loc[1]
        wayList = ["ID","NAME","CLASS_NAME","XPATH","CSS_SELECTOR","PARTIAL_LINK_TEXT","TAG_NAME","LINK_TEXT"]
        driver = self.driver
        if loc[0] in wayList:
            return WebDriverWait(self.driver, self.waitTime).until(
                lambda driver: driver.find_element(by=loc[0].lower(), value=value))
        else:
            logger.info("未找到此定位方法")
            return False

    def getWebPage(self):
        self.driver.get(conf.host_manage('${host}$'))


    def get_screent_img(self,dir=baseDir):
        '''将页面截图下来'''
        riqi = time.strftime("%Y-%m-%d", time.localtime())
        now = time.strftime("%Y-%m-%d_%H_%M_%S")
        file_path = os.path.join(dir,'src','Screenshot',riqi)
        mk_dir(file_path)
        pic_file_path = os.path.join(file_path,now+'.png')
        try:
            self.driver.get_screenshot_as_file(pic_file_path)
            logger.info("页面已截图，截图的路径在项目: /Screenshots路径下")
            with allure.step('Screenshots'):
                allure.attach.file(pic_file_path, attachment_type=allure.attachment_type.PNG)
            return pic_file_path
        except NameError as ne:
            logger.error("失败截图 %s" % ne)
            self.get_screent_img()

    def inputText(self, loc, text):
        logger.info('清空文本框内容: %s...' % loc[1])
        self.findView(*loc).clear()
        time.sleep(1)
        logger.info('输入内容方式 by %s: %s...' % (loc[0], loc[1]))
        logger.info('输入内容: %s' % text)
            #self.log.myloggger('Input: %s' % text, flag=0)
        try:
            self.findView(*loc).send_keys(text)
        except Exception as e:
            logger.error("输入内容失败 %s" % e)
            self.get_screent_img()

    def click(self, loc):
        logger.info('点击元素 by %s: %s...' % (loc[0], loc[1]))
        try:
            self.findView(*loc).click()
            time.sleep(1)
        except AttributeError as e:
            logger.error("无法点击元素: %s" % e)
            raise

    def clear(self,loc):
        '''输入文本框清空操作'''
        element = self.findView(*loc)
        try:
            element.clear()
            logger.info('清空文本框内容')
        except NameError as ne:
            logger.error("清空文本框内容失败: %s" % ne)
            self.get_screent_img()

    def move_to_element(self, loc):
        '''
        鼠标悬停操作
        Usage:
        element = ("id","xxx")
        drivers.move_to_element(element)
        '''
        element = self.findView(*loc)
        ActionChains(self.driver).move_to_element(element).perform()

    def back(self):
        """
        浏览器返回窗口
        """
        self.driver.back()
        logger.info('返回上一个页面')

    def forward(self):
        """
        浏览器前进下一个窗口
        """
        self.driver.forward()
        logger.info('前进到下一个页面')

    def wait(self,seconds):
        self.driver.implicitly_wait(seconds)
        logger.info("等待 %d 秒" % seconds)

    def close(self):
        """
        关闭浏览器
        """
        try:
            self.driver.close()
            logger.info('关闭浏览器窗口')
        except NameError as ne:
            logger.error("关闭浏览器窗口失败 %s" % ne)

    def quit(self):
        """
        退出浏览器
        """
        self.driver.quit()

    def get_title(self):
        '''获取title'''
        return self.driver.title

    def get_text(self, loc):
        '''获取文本'''
        element = self.findView(*loc)
        return element.text

    def get_attribute(self, loc, name):
        '''获取属性'''
        element = self.findView(*loc)
        return element.get_attribute(name)

    def js_execute(self, js):
        '''执行js'''
        return self.driver.execute_script(js)

    def js_focus_element(self, loc):
        '''聚焦元素'''
        target = self.findView(*loc)
        self.driver.execute_script("arguments[0].scrollIntoView();", target)

    def js_scroll_top(self):
        '''滚动到顶部'''
        js = "window.scrollTo(0,0)"
        self.driver.execute_script(js)

    def js_scroll_end(self):
        '''滚动到底部'''
        js = "window.scrollTo(0,document.body.scrollHeight)"
        self.driver.execute_script(js)

    def select_by_index(self, loc, index):
        '''通过索引,index是索引第几个，从0开始'''
        element = self.findView(*loc)
        Select(element).select_by_index(index)

    def select_by_value(self, loc, value):
        '''通过value属性'''
        element = self.findView(*loc)
        Select(element).select_by_value(value)

    def select_by_text(self, loc, text):
        '''通过文本值定位'''
        element = self.findView(*loc)
        Select(element).select_by_value(text)

    def is_text_in_element(self,loc,text,timeout=10):
        """判断文本在元素里，没定位到元素返回False，定位到元素返回判断结果布尔值"""
        try:
            result = WebDriverWait(self.driver,timeout,1).until(EC.text_to_be_present_in_element(loc,text))
        except TimeoutException:
            print("元素没有定位到:"+str(loc))
            return False
        else:
            return result

    def is_text_in_value(self,loc,value,timeout = 10):
        '''
        判断元素的value值，没定位到元素返回false,定位到返回判断结果布尔值
        result = drivers.text_in_element(element, text)
        '''
        try:
            result = WebDriverWait(self.driver, timeout, 1).until(
                EC.text_to_be_present_in_element_value(loc, value))
        except TimeoutException:
            print("元素没定位到：" + str(loc))
            return False
        else:
            return result
    def assertDtEquals(self,loc,value):
        '''
        断言实际值等于期望值
        '''

        try:
            actual = self.findView(*loc).text
            assert (actual == value)
        except TimeoutException as timee:
            logger.info("断言相等失败，通过" + loc[0] + "方式定位元素：" + loc[1] + "超时")
            raise timee
        except Exception as e:
            logger.info("断言相等失败，实际值：" + actual + "；" + "期望值：" + value)
            raise e

    def is_title(self, title, timeout=10):
        '''判断title完全等于'''
        result = WebDriverWait(self.driver, timeout, 1).until(EC.title_is(title))
        return result

    def is_title_contains(self, title, timeout=10):
        '''判断title包含'''
        result = WebDriverWait(self.driver, timeout, 1).until(EC.title_contains(title))
        return result

    def is_selected(self, loc, timeout=10):
        '''判断元素被选中，返回布尔值,'''
        result = WebDriverWait(self.driver, timeout, 1).until(EC.element_located_to_be_selected(loc))
        return result

    def is_selected_be(self, loc, selected=True, timeout=10):
        '''判断元素的状态，selected是期望的参数true/False
        返回布尔值'''
        result = WebDriverWait(self.driver, timeout, 1).until(EC.element_located_selection_state_to_be(loc, selected))
        return result

    def is_alert_present(self, timeout=10):
        '''判断页面是否有alert，
        有返回alert(注意这里是返回alert,不是True)
        没有返回False'''
        result = WebDriverWait(self.driver, timeout, 1).until(EC.alert_is_present())
        return result

    def is_visibility(self, loc, timeout=10):
        '''元素可见返回本身，不可见返回Fasle'''
        result = WebDriverWait(self.driver, timeout, 1).until(EC.visibility_of_element_located(loc))
        return result

    def is_invisibility(self, loc, timeout=10):
        '''元素可见返回本身，不可见返回True，没找到元素也返回True'''
        result = WebDriverWait(self.driver, timeout, 1).until(EC.invisibility_of_element_located(loc))
        return result

    def is_clickable(self, loc, timeout=10):
        '''元素可以点击is_enabled返回本身，不可点击返回Fasle'''
        result = WebDriverWait(self.driver, timeout, 1).until(EC.element_to_be_clickable(loc))
        return result

    def is_located(self, loc, timeout=10):
        '''判断元素有没被定位到（并不意味着可见），定位到返回element,没定位到返回False'''
        result = WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_element_located(loc))
        return result

    def click_alert(self):
        '''操作点击弹窗'''
        alert = self.driver.switch_to.alert
        time.sleep(1)
        alert.accept()


if __name__ == '__main__':
    print(baseDir)