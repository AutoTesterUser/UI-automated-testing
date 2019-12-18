pytest_web
====================

初始环境搭建
> 运行环境要求python3.6.0以上。

> 浏览器及浏览器对应版本的driver安装。

> Allure运行环境安装。

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
