#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:lichunhui
@Time:  2018/7/3 15:04
@Description: 互动百科爬虫
"""
import re
from urllib.parse import unquote

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import Rule

from baikeSpider.items import BaikespiderItem
from .redis_spider import RedisCrawlSpider
from ..settings import BAIKE_ITEM_URLS


class baikeSpider(RedisCrawlSpider):
    task_queue = BAIKE_ITEM_URLS
    base_url = "https://www.baike.com"
    name = 'baikeSpider'
    allowed_domains = ['www.baike.com']
    rules = (
        Rule(LinkExtractor(allow=('https://www.baike.com/wiki/')), callback='parse', follow=True),
    )
    custom_settings = {
        'ITEM_PIPELINES': {
            'baikeSpider.pipelines.BaikespiderPipeline': 300,
            'baikeSpider.pipelines.BaikeSpiderRedisPipeline': 301,
        },
    }

    # 重写解析
    def parse(self, response):
        items = BaikespiderItem()
        selector = Selector(response)
        items['url'] = unquote(response.url)

        title = selector.xpath("/html/head/title/text()").extract()
        if len(title) != 0:
            items['title'] = title[0].strip().encode('utf-8', errors='ignore').decode('utf-8')
        else:
            items['title'] = 'none'
        summary = selector.xpath("//div[@class=\"lemma-summary\"]").xpath("string(.)").extract()
        if len(summary) != 0:
            tmps = summary[0].encode('utf-8', errors='ignore').decode('utf-8')
            items['summary'] = re.sub('\r\n|\n|\r', ' ', tmps)
        else:
            items['summary'] = 'none'

        catalog = selector.xpath("//div[@class=\"lemmaWgt-lemmaCatalog\"]").xpath("string(.)").extract()
        if len(catalog) != 0:
            tmpc = catalog[0].encode('utf-8', errors='ignore').decode('utf-8')
            items['catalog'] = re.sub('\r\n|\n|\r', ' ', tmpc)
        else:
            items['catalog'] = 'none'

        # 进行迭代抓取的item链接
        urls = [unquote(item) for item in
                selector.xpath("//div[@class=\"para\"]//a[@target=\"_blank\"]/@href").extract()]
        items['keywords_url'] = list(set(filter(lambda x: 'item' in x, urls)))

        description = selector.xpath("//div[@class=\"content-wrapper\"]").xpath("string(.)").extract()
        if len(description) != 0:
            tmpd = description[0].encode('utf-8', errors='ignore').decode('utf-8')
            items['description'] = re.sub('\r\n|\n|\r', ' ', tmpd)
        else:
            items['description'] = 'none'

        embed_image_url = selector.xpath("//div[@class=\"para\"]//a[@class=\"image-link\"]//@data-src").extract()
        if len(embed_image_url) != 0:
            items['embed_image_url'] = ','.join(embed_image_url)
        else:
            items['embed_image_url'] = 'none'

        album_pic_url = selector.xpath("//div[@class=\"album-list\"]//a[@class=\"more-link\"]/@href").extract()
        if len(album_pic_url) != 0:
            items['album_pic_url'] = self.base_url + unquote(album_pic_url[0])
        else:
            items['album_pic_url'] = 'none'

        update_time = selector.xpath("//span[@class = 'j-modified-time']").xpath("string(.)").extract()
        if len(update_time) != 0:
            tmpu = update_time[0].strip().encode('utf-8', errors='ignore').decode('utf-8')
            items['update_time'] = re.sub('\r\n|\n|\r', ' ', tmpu)
        else:
            items['update_time'] = 'none'

        reference_material = selector.xpath(
            "//dl[@class ='lemma-reference collapse nslog-area log-set-param']").xpath("string(.)").extract()
        if len(reference_material) != 0:
            tmpr = reference_material[0].encode('utf-8', errors='ignore').decode('utf-8')
            items['reference_material'] = re.sub('\r\n|\n|\r', ' ', tmpr)
        else:
            items['reference_material'] = 'none'

        item_tag = selector.xpath("//dd[@id = \"open-tag-item\"]").xpath("string(.)").extract()
        if len(item_tag) != 0:
            tmpi = item_tag[0].encode('utf-8', errors='ignore').decode('utf-8')
            items['item_tag'] = re.sub('\r\n|\n|\r', ' ', tmpi)
        else:
            items['item_tag'] = 'none'
        yield items
