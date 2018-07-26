#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:lichunhui
@Time:  2018/7/3 15:04
@Description: 互动百科爬虫
"""
import re
from urllib.parse import unquote

from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import Rule

from baikeSpider.cache.html_cache import CacheTool
from baikeSpider.items import BaikeSpiderItem
from .redis_spider import RedisCrawlSpider
from ..settings import BAIKE_ITEM_URLS, BAIKE_SPIDER_NAME


class BaikeSpider(RedisCrawlSpider):
    task_queue = BAIKE_ITEM_URLS
    base_url = "https://www.baike.com"
    name = BAIKE_SPIDER_NAME
    allowed_domains = ['www.baike.com']
    rules = (
        Rule(LinkExtractor(allow=('https://www.baike.com/wiki/',)), callback='parse', follow=True),
    )

    def parse(self, response):
        items = BaikeSpiderItem()
        selector = Selector(response)
        items['url'] = unquote(response.url)
        items['html'] = response.text

        title = selector.xpath("/html/head/title/text()").extract()
        if title:
            items['title'] = title[0].strip().encode('utf-8', errors='ignore').decode('utf-8')
        else:
            items['title'] = ''
        summary = selector.xpath("//div[@class=\"summary\"]//p").xpath("string(.)").extract()
        if summary:
            tmps = summary[0].encode('utf-8', errors='ignore').decode('utf-8')
            items['summary'] = re.sub('(\r\n){2,}|\n{2,}|\r{2,}', '\n', tmps)
        else:
            items['summary'] = ''

        basic_info = selector.xpath("//div[@class=\"module zoom\"]").xpath("string(.)").extract()
        if basic_info:
            tmpb = basic_info[0].encode('utf-8', errors='ignore').decode('utf-8')
            items['basic_info'] = re.sub('(\r\n){2,}|\n{2,}|\r{2,}', '\n', tmpb)
        else:
            items['basic_info'] = ''

        catalog = selector.xpath("//fieldset[@id=\"catalog\"]").xpath("string(.)").extract()
        if catalog:
            tmpc = catalog[0].encode('utf-8', errors='ignore').decode('utf-8')
            items['catalog'] = re.sub('(\r\n){2,}|\n{2,}|\r{2,}', '\n', tmpc)
        else:
            items['catalog'] = ''

        # 进行迭代抓取的item链接
        sub_urls = [unquote(item) for item in selector.xpath("//a[@target=\"_blank\"]/@href").extract()]
        items['keywords_url'] = list(set(filter(lambda x: 'wiki' in x, sub_urls)))

        description = selector.xpath("//div[@id=\"content\"]").xpath("string(.)").extract()
        if description:
            tmpd = description[0].encode('utf-8', errors='ignore').decode('utf-8')
            items['description'] = re.sub('(\r\n){2,}|\n{2,}|\r{2,}', '\n', tmpd)
        else:
            items['description'] = ''

        # 匹配pic、js、css
        items['embed_image_url'] = CacheTool.parse_img(items['html'])
        items['js'] = CacheTool.parse_js(items['html'])
        items['css'] = CacheTool.parse_css(items['html'])

        # // *[ @ id = "moreGrayc"]
        album_pic_url = selector.xpath("//*[@id=\"moreGrayc\"]//a[@id=\"moreId\"]/@href").extract()
        if album_pic_url:
            items['album_pic_url'] = unquote(album_pic_url[0])
        else:
            items['album_pic_url'] = ''

        update_time = selector.xpath("//div[@class = 'rightdiv cooperation cooperation_t']/ol/li[3]").xpath(
            "string(.)").extract()
        if update_time:
            tmpu = update_time[0].strip().encode('utf-8', errors='ignore').decode('utf-8')
            items['update_time'] = re.sub('(\r\n){2,}|\n{2,}|\r{2,}', '\n', tmpu)
        else:
            items['update_time'] = ''

        reference_material = selector.xpath("//dl[@class ='reference bor-no']").xpath("string(.)").extract()
        if reference_material:
            tmpr = reference_material[0].encode('utf-8', errors='ignore').decode('utf-8')
            items['reference_material'] = re.sub('(\r\n){2,}|\n{2,}|\r{2,}', '\n', tmpr)
        else:
            items['reference_material'] = ''

        item_tag = selector.xpath("//dd[@id = \"h27\"]").xpath("string(.)").extract()
        if item_tag:
            tmpi = item_tag[0].encode('utf-8', errors='ignore').decode('utf-8')
            items['item_tag'] = re.sub('(\r\n){2,}|\n{2,}|\r{2,}', '\n', tmpi)
        else:
            items['item_tag'] = ''
        yield items
