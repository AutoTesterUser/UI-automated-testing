Dragontesting pytest_web
====================

初始环境搭建
> 运行环境要求python3.6.0以上。

> 浏览器及浏览器对应版本的driver安装。

> Allure运行环境安装。

###Ps:环境搭建可参考以下地址:[Web 自动化测试执行指南](http://help.dragontesting.cn/yihao/1.0/doc/%E9%BE%99%E6%B5%8B1%E5%8F%B7%E8%BF%90%E8%A1%8C%E6%B5%8B%E8%AF%95%E6%8C%87%E5%8D%97-Selenium.pdf)

## 目前使用python+pytest+selenium作为基础，二次封装常用API，简化代码，采用allure产生报告。


## 使用相关
在龙测自动化平台上完成自动化案例的编写后，在测试代码处点击下载测试项目，在平台上维护的流程信息与手机配置信息均可自动生成在项目工程中，环境配置正确无误的情况下可选用一键执行文件，即可开始自动化测试之旅。
一键执行文件使用说明：window系统下，在项目的根目录下，双击run.bat文件即可完成一键启动。linux/MAC系统下，命令行进入项目的根目录下，使用sh run.sh 触发一键启动。ps:若项目类型为Android和ios，运行一键启动前需要先连接手机及appium。
###python一键执行文件使用相关
目前一键执行文件只使用于python变量。即在命令行下输入python 可进入python3的运行器。若本地环境同时安装python2和python3,环境变量使用python2和3区分，可修改一键执行文件中的python为python3.

## 目录结构

初始的目录结构如下：

~~~
pytest_web
├─test-output                   APP运行结果的报告存放目录
|─config.properties             配置文件：涉及手机信息及待测软件信息
├─main.py                       python待执行脚本管理统一入口
│-run.bat                       windows环境下一键执行文件
│-run.sh                        linux/mac 环境下一键执行文件
├─src                           框架系统目录
│  ├─main                       空目录
│  └─test                       框架类库目录
│     └─java                    框架类库目录
│       ├─core
│       │   ├─BaseTest.py       基础测试类
│       │   └─DT.py             常用API文件
│       ├─fields                元素管理文件夹
│       │   └─Elements          项目元素管理问题
│       └─testcase              脚本文件
│     
├─README.md                     README 文件
~~~

 

## 其他说明
交流QQ群号：230125864

## 版权信息
苏州龙测智能科技有限公司