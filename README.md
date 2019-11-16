# baiduSpider
[![](https://img.shields.io/badge/python-3-brightgreen.svg)](https://www.python.org/downloads/)
[![](https://img.shields.io/badge/scrapy-1.5-blue.svg)](https://scrapy.org/)
## 百科类网站爬虫

### 特性
- 百科类网站全站词条抓取，包括百度百科、互动百科、wiki中英文站点；
- 支持断点续爬；
- 支持缓存百科词条页面；
- 可分布式部署；
- 经过单机测试，在i5-7400 内存8G 20M网络带宽下，百度百科词条一天可以抓取大概30w条(默认系统配置下)；互动百科测试结果
类似，wiki网站抓取数据量较少，受到配置的代理延迟影响较大；

### 如何使用
- 安装依赖 `pip install -r requirement.txt`
- 初始数据库 `python initialize_db.py`
- 初始化爬虫种子  `python initialize_tasks_seeds.py`
- 开始运行爬虫 `python start_spiders.py`


### 常见问题
- 理论上来说，只要你给的种子够全面，你就可以尽可能的抓取到更多的词条信息；我是通过每个类别都去找一些关键词来做
的种子，尽可能的把所有分类都涵盖完全；
- 抓取维基百科需要FQ，并且维基百科的存在反爬虫机制，建议使用代理IP池，并且调低爬虫爬取频率。


### 一些闲话
- 大家要是感兴趣，请动动你们勤劳的小手儿给我点个💗💗吧！非常感谢~
- 欢迎大家讨论并给作者提出一些宝贵的改进建议；


