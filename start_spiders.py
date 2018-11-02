"""
@Author:lichunhui
@Time:   
@Description: 百度百科爬虫程序入口
"""
from scrapy import cmdline

# cmdline.execute("scrapy crawl baidu_spider".split())
# cmdline.execute("scrapy crawl baike_spider".split())
cmdline.execute("scrapy crawl wiki_zh_spider".split())
# cmdline.execute("scrapy crawl wiki_en_spider".split())
# cmdline.execute("scrapy crawlall".split())

