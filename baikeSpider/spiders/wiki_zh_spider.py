#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:lichunhui
@Time:  2018/7/26 9:38
@Description: 
"""
import re
from itertools import chain
from urllib.parse import unquote

from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import Rule

from baikeSpider.cache.html_cache import CacheTool
from baikeSpider.items import WikiZHSpiderItem
from .redis_spider import RedisCrawlSpider
from ..config import wiki_zh_task_queue, wiki_zh_spider_name


class WikeZHSpider(RedisCrawlSpider):
    task_queue = wiki_zh_task_queue
    base_url = "https://zh.wikipedia.org"
    name = wiki_zh_spider_name
    allowed_domains = ['zh.wikipedia.org']
    rules = (
        Rule(LinkExtractor(allow=('https://zh.wikipedia.org/wiki/',)), callback='parse', follow=True),
    )
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddleware.useragent.UserAgentMiddleware': None,
            'baikeSpider.middlewares.MyUserAgentMiddleware': 400,
            'baikeSpider.middlewares.MyRetryMiddleware': 501,
            'baikeSpider.middlewares.MyProxyMiddleware': 100,
            'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
        }
    }

    def parse(self, response):
        items = WikiZHSpiderItem()
        selector = Selector(response)
        items['url'] = unquote(response.url)
        items['html'] = response.text
        title = selector.xpath("/html/head/title/text()").extract()
        if title:
            items['title'] = title[0].strip().encode('utf-8', errors='ignore').decode('utf-8')
        else:
            items['title'] = ''

        note = selector.xpath("//div[@class=\"hatnote\"]").xpath("string(.)").extract()
        if note:
            tmps = note[0].encode('utf-8', errors='ignore').decode('utf-8')
            items['note'] = re.sub('(\r\n){2,}|\n{2,}|\r{2,}', '\n', tmps)
        else:
            items['note'] = ''

        catalog = selector.xpath("//div[@class=\"toc\"]").xpath("string(.)").extract()
        if catalog:
            tmpc = catalog[0].encode('utf-8', errors='ignore').decode('utf-8')
            items['catalog'] = re.sub('(\r\n){2,}|\n{2,}|\r{2,}', '\n', tmpc)
        else:
            items['catalog'] = ''

        # 进行迭代抓取的item链接
        sub_urls = [unquote(item) for item in selector.xpath("//a[@title]/@href").extract()]
        items['keywords_url'] = list(set(filter(lambda x: 'wiki' in x and 'http' not in x, sub_urls)))

        description = selector.xpath("//div[@class=\"mw-parser-output\"]//p").xpath("string(.)").extract()
        if description:
            tmpds = [d.encode('utf-8', errors='ignore').decode('utf-8') for d in description]
            tmpd = ''.join(tmpds)
            items['description'] = re.sub('(\r\n){2,}|\n{2,}|\r{2,}', '\n', tmpd)
        else:
            items['description'] = ''

        # 匹配pic
        items['embed_image_url'] = CacheTool.parse_wiki_pic(items['html'])

        # //*[@id="footer-info-lastmod"]
        update_time = selector.xpath("//*[@id=\"footer-info-lastmod\"]").xpath("string(.)").extract()
        if update_time:
            tmpu = update_time[0].strip().encode('utf-8', errors='ignore').decode('utf-8')
            items['update_time'] = re.sub('(\r\n){2,}|\n{2,}|\r{2,}', '\n', tmpu)
        else:
            items['update_time'] = ''

        rm_1 = selector.xpath(
            "//div[@class =\"refbegin columns references-column-count references-column-count-3\"]").xpath(
            "string(.)").extract()
        rm_2 = selector.xpath(
            "//div[@class =\"refbegin columns references-column-count references-column-count-2\"]").xpath(
            "string(.)").extract()
        rm_3 = selector.xpath(
            "//div[@class =\"reflist columns references-column-count references-column-count-2\"]").xpath(
            "string(.)").extract()
        rm_4 = selector.xpath("//ol[@class =\"references\"]").xpath("string(.)").extract()
        reference_material = list(chain(rm_1, rm_2, rm_3, rm_4))
        if reference_material:
            tmpr = [rm.encode('utf-8', errors='ignore').decode('utf-8') for rm in reference_material]
            tmpr = ' '.join(tmpr)
            items['reference_material'] = re.sub('(\r\n){2,}|\n{2,}|\r{2,}', '\n', tmpr)
        else:
            items['reference_material'] = ''

        item_tag = selector.xpath("//div[@id = \"mw-normal-catlinks\"]/ul").xpath("string(.)").extract()
        if item_tag:
            tmpi = item_tag[0].encode('utf-8', errors='ignore').decode('utf-8')
            items['item_tag'] = re.sub('(\r\n){2,}|\n{2,}|\r{2,}', '\n', tmpi)
        else:
            items['item_tag'] = ''
        print(items['url'], items['keywords_url'])
        yield items
