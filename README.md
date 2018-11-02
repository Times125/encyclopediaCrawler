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
类似，wiki网站抓取数据量较少，收到配置的代理延迟影响较大；

### 如何使用
- 安装依赖 `pip install -r requirement.txt`
- 初始数据库 `python initialize_db.py`
- 初始化爬虫种子  `python initialize_tasks_seeds.py`
- 开始运行爬虫 `python start_spiders.py`


### 常见问题
- 暂无

### 一些闲话
- 大家要是感兴趣，请动动你们勤劳的小手儿给我点个💗💗吧！非常感谢~
- 欢迎大家讨论并给作者提出一些宝贵的改进建议；
- 苦逼学生党，被无情压榨廉价劳动力，只有在基♂hub上找点快乐了；

