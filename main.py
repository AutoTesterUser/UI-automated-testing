# _*_ coding:utf-8 _*_
import logging
import os,time
import pytest
import subprocess
from src.utils.logger import LogConfig

EVN = 'xxx'
PATH = os.path.split(os.path.realpath(__file__))[0]

def invoke(md):
    output, errors = subprocess.Popen(md, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    o = output.decode("utf-8")
    return o


def run_test():
    """
    --workers=1 : 1进程
    --tests-per-worker=2 : 2个线程
    allure generate est-output -o allure-report
    :return:
    """
    currentPath = os.path.dirname(os.path.abspath(__file__))
    date = time.strftime("%Y-%m-%d", time.localtime())
    report_path = os.path.join(currentPath ,'test-output',date)
    # test_folder = os.path.join(currentPath , 'src/testcase/')
    if EVN == 'Debug':
        args = ['-s', '-q', 'src/testcase/test_001.py','--alluredir=%s' % (report_path)]
    else:
        args = [ '-vsq','--alluredir=%s' %(report_path)]
    pytest.main(args)
    cmd = 'allure generate --clean %s -o %s' % ('test-output/%s'%(date),'allure-report')
    #cmd = 'allure server %s'%('test-output/%s'%(date))
    invoke(cmd)

if __name__ == "__main__":
    LogConfig(PATH)
    run_test()
