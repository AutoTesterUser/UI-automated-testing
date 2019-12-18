import os
from faker import Faker ,Factory
import logging as logger
"""
address 地址
person 人物类：性别、姓名等
barcode 条码类
color 颜色类
company 公司类：公司名、公司email、公司名前缀等
credit_card 银行卡类：卡号、有效期、类型等
currency 货币
date_time 时间日期类：日期、年、月等
file 文件类：文件名、文件类型、文件扩展名等
internet 互联网类
job 工作
lorem 乱数假文
misc 杂项类
phone_number 手机号码类：手机号、运营商号段
python python数据
profile 人物描述信息：姓名、性别、地址、公司等
ssn 社会安全码(身份证号码)
user_agent 用户代理
"""

class Mock:

    mc = Factory.create()
    def get_name(self):
        """
        随机姓名
        :return:
        """
        return self.mc.name()
    def get_username(self):
        """
        随机用户名
        :return:
        """
        return self.mc.user_name()
    def get_phone(self):
        """
        随机手机号
        :return:
        """
        return self.mc.phone_number()
    def get_bankCar(self):
        """
        随机银行卡
        :return:
        """
        return self.mc.credit_card_number()
    def get_barcode(self):
        """
        获取随机条码码
        :return:
        """
        return self.mc.user_name()
    def get_email(self):
        """
        获取随机邮箱号
        :return:
        """
        return self.mc.free_email()

    def get_password(self):
        """
        获取随机密码
        :return:
        """
        return self.mc.password()

    def methods(self):
        return (list(filter(lambda m: not m.startswith("__") and not m.endswith("__") and callable(getattr(self, m)),dir(self))))

def mk_dir(path):
    path = path.strip()
    path = path.rstrip("\\")
    path = path.rstrip("/")
    is_exists = os.path.exists(path)
    if not is_exists:
        try:
            os.makedirs(path)
        except Exception as e:
            logger.info("logs目录创建失败：%s" % e)
    else:
        logger.debug("logs目录已存在：%s" % str(path))
        pass

