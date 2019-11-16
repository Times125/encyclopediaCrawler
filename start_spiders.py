"""
@Author:lichunhui
@Time:   
@Description: 百度百科爬虫程序入口
"""
from scrapy import cmdline

#  开始执行百度爬虫
cmdline.execute("scrapy crawl baidu".split())
# cmdline.execute("scrapy crawl zh.wiki".split())
# cmdline.execute("scrapy crawl en.wiki".split())
