# _*_ coding:utf-8 _*_
from functools import wraps
from src.core.DT import DT
import logging as logger



def getImage(function):
    @wraps(function)
    def get_ErrImage(self, *args, **kwargs):
        self.dt = DT(self)
        try:
            result = function(self, *args, **kwargs)
        except Exception as e:
            self.dt.saveScreenshotPNG()
            logger.info(" %s 脚本运行失败" %(function.__name__))
            raise e
        else:
            logger.info(" %s 脚本运行正常" %(function.__name__))
    return get_ErrImage