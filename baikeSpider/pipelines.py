# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
from .db.model import BaiduItemData, BaikeItemData
from .db.dao import CommandOperate
from .db.basic import get_redis_conn
from .settings import BAIDU_ITEM_URLS, BAIKE_ITEM_URLS, BAIDU_HTML_CACHE
from .bloomfilter.filter import BloomFilterRedis
from .settings import FILTER_BLOCKS, BAIDU_BLOOM_KEY, BAIKE_BLOOM_KEY
from .utils.log import logger

try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO


class BaiduspiderPipeline(object):
    """ 百度百科 """

    def process_item(self, item, spider):
        try:
            data = BaiduItemData(name=item['title'], url=item['url'], summary=item['summary'],
                                 catalog=item['catalog'], description=item['description'],
                                 embed_image_url=','.join(item['embed_image_url']), album_pic_url=item['album_pic_url'],
                                 reference_material=item['reference_material'], update_time=item['update_time'],
                                 item_tag=item['item_tag'])
            CommandOperate.add_one(data)
            return item
        except Exception as e:
            logger.error(e)


# request queue
class BaiduSpiderRedisPipeline(object):
    """use bloomfilter to filter the request which had been sent"""
    handle = get_redis_conn()
    base_url = "https://baike.baidu.com"
    bf = BloomFilterRedis(block=FILTER_BLOCKS, key=BAIDU_BLOOM_KEY)

    def process_item(self, item, spider):
        if not item['keywords_url']:
            return item
        for url in item['keywords_url']:
            if self.bf.is_exists(url):
                continue
            else:
                new_url = self.base_url + url
                self.handle.lpush(BAIDU_ITEM_URLS, new_url)
        return item


# resources queue
# 新的解决方法：将每个词条的资源连接push到一个专门的下载队列中，然后单独使用下载器来下载任务，松耦合
class BaiduSpiderCachePipeline(object):
    """ push the resource urls into task queue """
    handle = get_redis_conn()

    def process_item(self, item, spider):
        bloomKey = "{}:{}".format(spider.name, "CacheCSSandJSFilter")
        js_urls = []
        css_urls = []
        bf = BloomFilterRedis(block=1, key=bloomKey)
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
        key = "{}:{}".format(spider.name, "cache_task_queue")
        value = dict(title=item['title'], from2=spider.name, htm=item['html'], js=js_urls, css=css_urls,
                     pic=item['embed_image_url'])
        self.handle.lpush(key, value)
        return item
        """
        if not os.path.exists('{}\css_resources'.format(BAIDU_HTML_CACHE)):
            os.makedirs('{}\css_resources'.format(BAIDU_HTML_CACHE))
        if not os.path.exists('{}\js_resources'.format(BAIDU_HTML_CACHE)):
            os.makedirs('{}\js_resources'.format(BAIDU_HTML_CACHE))
        for url in js_urls:
            if bf.is_exists(url):
                continue
            path = url.split('/')[-1]
            js_filename = '{}\js_resources\{}'.format(BAIDU_HTML_CACHE, path)
            print(js_filename)
            response = self.get_response(url, spider, item['title'])
            with open(js_filename, 'w+', encoding='utf8') as w:
                w.write(bytes2str(response.data))
        for url in css_urls:

            if bf.is_exists(url):
                continue
            path = url.split('/')[-1]
            print(url)
            css_filename = '{}\css_resources\{}'.format(BAIDU_HTML_CACHE, path)
            response = self.get_response(url, spider, item['title'])
            with open(css_filename, 'w+', encoding='utf8') as w:
                w.write(bytes2str(response.data))
        """


class BaikespiderPipeline(object):
    """" 互动百科 """

    def process_item(self, item, spider):
        data = BaikeItemData(name=item['title'], url=item['url'], summary=item['summary'],
                             catalog=item['catalog'], description=item['description'],
                             embed_image_url=item['embed_image_url'], album_pic_url=item['album_pic_url'],
                             reference_material=item['reference_material'], update_time=item['update_time'],
                             item_tag=item['item_tag'])
        CommandOperate.add_one(data)
        return item


class BaikeSpiderRedisPipeline(object):
    """use bloomfilter to filter the request which had been sent"""
    handle = get_redis_conn()
    base_url = "https://www.baike.com"
    bf = BloomFilterRedis(block=FILTER_BLOCKS, key=BAIKE_BLOOM_KEY)

    def process_item(self, item, spider):
        for url in item['keywords_url']:
            if self.bf.is_exists(url):
                continue
            else:
                new_url = self.base_url + url
                self.handle.lpush(BAIKE_ITEM_URLS, new_url)
        return item
