# -*- coding: utf-8 -*-

import os
import re
import logging as logger
from configparser import ConfigParser

confPath = os.path.abspath(os.path.dirname(__file__)).split('src')[0]

class Config:

    def __init__(self):
        """
        初始化
        """
        self.config = ConfigParser()
        self.conf_path = os.path.join(confPath, 'config.ini')
        if not os.path.exists(self.conf_path):
            raise FileNotFoundError("请确保配置文件存在！")

    def set_conf(self, title, value, text):
        """
        配置文件修改
        :param title:
        :param value:
        :param text:
        :return:
        """
        self.config.set(title, value, text)
        with open(self.conf_path, "w+") as f:
            return self.config.write(f)

    def add_conf(self, title):
        """
        配置文件添加
        :param title:
        :return:
        """
        self.config.add_section(title)
        with open(self.conf_path, "w+") as f:
            return self.config.write(f)

    def read_host(self):
        """
        读取配置文件中host相关信息
        :return:
        """
        self.config.read(self.conf_path, encoding='utf-8')
        host = self.config['host']
        return host

    def read_cookie(self):
        """
        读取配置文件中的cookie相关信息
        :return:
        """
        self.config.read(self.conf_path,encoding='utf-8')
        cookie = self.config['cookies']
        return cookie

    def read_email(self):
        """
        读取配置文件中email相关信息
        :return:
        """
        self.config.read(self.conf_path, encoding='utf-8')
        email = self.config['mail']
        return email

    def read_mysql(self):
        """
        读取配置文件中mysql相关信息
        :return:
        """
        self.config.read(self.conf_path, encoding='utf-8')
        mysql = self.config['mysql']
        return mysql

    def read_time(self):
        """
        读取配置文件中time相关信息
        :return:
        """
        self.config.read(self.conf_path, encoding='utf-8')
        wTime = self.config['time']
        return wTime

class conf_manage:

    def host_manage(self,hos):
        """
        host关联配置
        :param hos:
        :return:
        """
        try:
            relevance_list = re.findall("\${(.*?)}\$", hos)
            for n in relevance_list:
                pattern = re.compile('\${' + n + '}\$')
                host_cf = Config()
                host_relevance = host_cf.read_host()
                hos = re.sub(pattern, host_relevance[n], hos, count=1)
        except TypeError:
            pass
        return hos

    def mail_manage(self,ml):
        """
        email关联配置
        :param ml:
        :return:
        """
        try:
            relevance_list = re.findall("\${(.*?)}\$", ml)
            for n in relevance_list:
                pattern = re.compile('\${' + n + '}\$')
                email_cf = Config()
                email_relevance = email_cf.read_email()
                ml = re.sub(pattern, email_relevance[n], ml, count=1)
        except TypeError:
            pass
        return ml

    def cookie_manage(self,ck):
        """
        cookie关联配置
        :param cookie:
        :return:
        """
        try:
            relevance_list = re.findall("\${(.*?)}\$", ck)
            for n in relevance_list:
                pattern = re.compile('\${' + n + '}\$')
                ck_cf = Config()
                ck_relevance = ck_cf.read_cookie()
                ck = re.sub(pattern, ck_relevance[n], ck, count=1)
        except TypeError:
            pass
        return ck

    def mysql_manage(self, my):
        """
        mysql关联配置
        :param my:
        :return:
        """
        try:
            relevance_list = re.findall("\${(.*?)}\$",my)
            for n in relevance_list:
                pattern = re.compile('\${' + n + '}\$')
                my_cf = Config()
                my_relevance = my_cf.read_cookie()
                my = re.sub(pattern, my_relevance[n], my, count=1)
        except TypeError:
            pass
        return my

    def time_manage(self, tm):
        """
        time关联配置
        :param tm:
        :return:
        """
        try:
            relevance_list = re.findall("\${(.*?)}\$", tm)
            for n in relevance_list:
                pattern = re.compile('\${' + n + '}\$')
                tm_cf = Config()
                tm_relevance = tm_cf.read_time()
                tm = re.sub(pattern, tm_relevance[n], tm, count=1)
        except TypeError:
            pass
        return tm
if __name__ == '__main__':
    cf = conf_manage()
    print(cf.time_manage("${wTime}$"))