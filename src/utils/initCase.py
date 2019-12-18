#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import yaml
import logging as logger

filePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def initCase(fileName):
    """
    初始化测试用例数据
    :param fileName:t
    :return:
    """
    try:
        with open(os.path.join(filePath,'field',fileName),'r+',encoding='utf8') as fb:
            case_list = yaml.load(fb.read(),Loader=yaml.FullLoader)
            return case_list
    except FileNotFoundError:
        logger.info('%s 文件不存在'%(os.path.join(filePath,'field',fileName)))

if __name__ == '__main__':
    print(initCase('roleManage.yml'))