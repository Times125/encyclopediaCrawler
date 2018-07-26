# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
from .db.model import BaiduItemData, BaikeItemData, WikiZHItemData, WikiENItemData
from .db.dao import CommandOperate
from .db.basic import get_redis_conn
from .utils.log import logger
from .bloomfilter.filter import BloomFilterRedis
from .settings import (FILTER_BLOCKS, BAIDU_BLOOM_KEY, BAIKE_BLOOM_KEY, BAIDU_ITEM_URLS, BAIKE_ITEM_URLS,
                       BAIDU_SPIDER_NAME, BAIKE_SPIDER_NAME, WIKI_ZH_BLOOM_KEY, WIKI_EN_BLOOM_KEY, WIKI_ZH_SPIDER_NAME,
                       WIKI_EN_SPIDER_NAME, WIKI_ZH_ITEM_URLS, WIKI_EN_ITEM_URLS)

try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

handle = get_redis_conn()


class SpiderPipeline(object):
    """ 百度、互动百科 """

    def process_item(self, item, spider):
        if spider.name == BAIDU_SPIDER_NAME:
            try:
                data = BaiduItemData(name=item['title'], url=item['url'], summary=item['summary'],
                                     basic_info=item['basic_info'],
                                     catalog=item['catalog'], description=item['description'],
                                     embed_image_url=','.join(item['embed_image_url']),
                                     album_pic_url=item['album_pic_url'],
                                     reference_material=item['reference_material'], update_time=item['update_time'],
                                     item_tag=item['item_tag'])
                CommandOperate.add_one(data)

            except Exception as e:
                logger.error(e)
        elif spider.name == BAIKE_SPIDER_NAME:
            try:
                data = BaikeItemData(name=item['title'], url=item['url'], summary=item['summary'],
                                     basic_info=item['basic_info'],
                                     catalog=item['catalog'], description=item['description'],
                                     embed_image_url=','.join(item['embed_image_url']),
                                     album_pic_url=item['album_pic_url'],
                                     reference_material=item['reference_material'], update_time=item['update_time'],
                                     item_tag=item['item_tag'])
                CommandOperate.add_one(data)
            except Exception as e:
                logger.error(e)
        elif spider.name == WIKI_ZH_SPIDER_NAME:
            try:
                data = WikiZHItemData(name=item['title'], url=item['url'], note=item['note'],
                                      catalog=item['catalog'], description=item['description'],
                                      embed_image_url=','.join(item['embed_image_url']),
                                      reference_material=item['reference_material'], update_time=item['update_time'],
                                      item_tag=item['item_tag'])
                CommandOperate.add_one(data)
            except Exception as e:
                logger.error(e)
        elif spider.name == WIKI_EN_SPIDER_NAME:
            try:
                data = WikiENItemData(name=item['title'], url=item['url'], note=item['note'],
                                      catalog=item['catalog'], description=item['description'],
                                      embed_image_url=','.join(item['embed_image_url']),
                                      reference_material=item['reference_material'], update_time=item['update_time'],
                                      item_tag=item['item_tag'])
                CommandOperate.add_one(data)
            except Exception as e:
                logger.error(e)
        return item


# request queue
class SpiderRedisPipeline(object):
    """ use bloomfilter to filter the request which had been sent """
    # 百度百科
    base_url = "https://baike.baidu.com"
    bf = BloomFilterRedis(block=FILTER_BLOCKS, key=BAIDU_BLOOM_KEY)
    # 互动百科
    bf2 = BloomFilterRedis(block=FILTER_BLOCKS, key=BAIKE_BLOOM_KEY)
    # 维基中文百科
    base_url_ZH = "https://zh.wikipedia.org"
    bf3 = BloomFilterRedis(block=FILTER_BLOCKS, key=WIKI_ZH_BLOOM_KEY)

    # 维基英文百科
    base_url_EN = "https://en.wikipedia.org"
    bf4 = BloomFilterRedis(block=FILTER_BLOCKS, key=WIKI_EN_BLOOM_KEY)

    def process_item(self, item, spider):
        if not item['keywords_url']:
            return item
        if spider.name == BAIDU_SPIDER_NAME:
            for url in item['keywords_url']:
                if self.bf.is_exists(url):
                    continue
                else:
                    new_url = self.base_url + url
                    handle.lpush(BAIDU_ITEM_URLS, new_url)
        elif spider.name == BAIKE_SPIDER_NAME:
            for url in item['keywords_url']:
                if self.bf2.is_exists(url):
                    continue
                else:
                    new_url = url
                    handle.lpush(BAIKE_ITEM_URLS, new_url)
        elif spider.name == WIKI_ZH_SPIDER_NAME:
            for url in item['keywords_url']:
                if self.bf3.is_exists(url):
                    continue
                else:
                    new_url = self.base_url_ZH + url
                    handle.lpush(WIKI_ZH_ITEM_URLS, new_url)
        elif spider.name == WIKI_EN_SPIDER_NAME:
            for url in item['keywords_url']:
                if self.bf4.is_exists(url):
                    continue
                else:
                    new_url = self.base_url_EN + url
                    handle.lpush(WIKI_EN_ITEM_URLS, new_url)
        return item


# resources queue
# 新的解决方法：将每个词条的资源连接push到一个专门的下载队列中，然后单独使用下载器来下载任务，低耦合
class WebCachePipeline(object):
    """ push the resource urls into task queue """

    def process_item(self, item, spider):
        bloomKey = "{}:{}".format("bloomfilter", "CacheCSSandJSFilter")
        js_urls = []
        css_urls = []
        bf = BloomFilterRedis(block=1, key=bloomKey)
        # WIKI网站没有可以下载的js和css
        if spider.name in (BAIKE_SPIDER_NAME, BAIDU_SPIDER_NAME):
            for url in item['js']:
                if bf.is_exists(url):
                    continue
                else:
                    js_urls.append(url)

            for url in item['css']:
                if bf.is_exists(url):
                    continue
                else:
                    css_urls.append(url)

        key = "{}:{}".format("resources", "cache_task_queue")
        value = dict(title=item['title'], from2=spider.name, htm=item['html'], js=js_urls, css=css_urls,
                     pic=item['embed_image_url'])
        handle.lpush(key, value)
        print('from:', spider.name)
        return item
