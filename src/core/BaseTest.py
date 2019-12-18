import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging as logger

def setUp(self):
    sysstr = platform.system()
    if (sysstr == "Windows"):
        print("Windows 系统")
        self.driver = webdriver.Chrome(r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
    elif (sysstr == "Linux"):
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')  # 无头参数
        options.add_argument('--disable-gpu')
        # options.add_argument('--headless')
        # options.add_argument('--no-sandbox')  # options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(executable_path="/home/shdy/drivers/bin/chromedriver", options=options)
        self.driver.maximize_window()
        logger.info("测试开始: 打开Chrome浏览器")
        self.driver.implicitly_wait(30)
        logger.info("设置隐士等待时间30秒")
    elif (sysstr == "Darwin"):
        logger.info("当前系统: macos")
        self.driver = webdriver.Chrome('/Users/wanghaitao/PycharmProjects/uiautotesting/driver/chromedriver')
        self.driver.maximize_window()
        logger.info("测试开始: 打开Chrome浏览器")
        self.driver.implicitly_wait(30)
        logger.info("设置隐士等待时间30秒")
    else:
        logger.error("不支持当前系统～")
    return self.driver
