# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime

from .db import (BaiduItemData, BaikeItemData, WikiZHItemData,
                 WikiENItemData, CommandOperate, common_con)
from .logger import db_logger
from .bloomfilter.filter import BloomFilterRedis
from .config import (filter_blocks, baidu_bloom_key, baike_bloom_key,
                     baidu_task_queue, baike_task_queue,
                     baidu_spider_name, baike_spider_name,
                     wiki_zh_bloom_key, wiki_en_bloom_key, wiki_zh_spider_name,
                     wiki_en_spider_name, wiki_zh_task_queue, wiki_en_task_queue)

try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO


class SpiderPipeline(object):
    """ 百度、互动百科 """

    def process_item(self, item, spider):

        fetch_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if spider.name == baidu_spider_name:
            try:
                data = BaiduItemData()
                data.name = item['title']
                data.url = item['url']
                data.summary = item['summary']
                data.basic_info = item['basic_info']
                data.catalog = item['catalog']
                data.description = item['description']
                data.embed_image_url = ','.join(item['embed_image_url'])
                data.album_pic_url = item['album_pic_url']
                data.reference_material = item['reference_material']
                data.update_time = item['update_time']
                data.item_tag = item['item_tag']
                data.fetch_time = fetch_time
                CommandOperate.add_one(data)
            except Exception as e:
                db_logger.error(e)
        elif spider.name == baike_spider_name:
            try:
                # print('爬虫名字是：', spider.name)
                data = BaikeItemData()
                data.name = item['title']
                data.url = item['url']
                data.summary = item['summary']
                data.basic_info = item['basic_info']
                data.catalog = item['catalog']
                data.description = item['description']
                data.embed_image_url = ','.join(item['embed_image_url'])
                data.album_pic_url = item['album_pic_url']
                data.reference_material = item['reference_material']
                data.update_time = item['update_time']
                data.item_tag = item['item_tag']
                data.fetch_time = fetch_time
                CommandOperate.add_one(data)
                # print('向数据库提交数据===>', item['title'])
            except Exception as e:
                db_logger.error(e)
                # print('在提交的时候发生异常')
        elif spider.name == wiki_zh_spider_name:
            try:
                data = WikiZHItemData()
                data.name = item['title']
                data.url = item['url']
                data.note = item['note']
                data.catalog = item['catalog']
                data.description = item['description']
                data.embed_image_url = ','.join(item['embed_image_url'])
                data.reference_material = item['reference_material']
                data.update_time = item['update_time']
                data.item_tag = item['item_tag']
                data.fetch_time = fetch_time
                CommandOperate.add_one(data)
            except Exception as e:
                db_logger.error(e)
        elif spider.name == wiki_en_spider_name:
            try:
                # data = WikiENItemData(name=item['title'], url=item['url'], note=item['note'],
                #                       catalog=item['catalog'], description=item['description'],
                #                       embed_image_url=','.join(item['embed_image_url']),
                #                       reference_material=item['reference_material'], update_time=item['update_time'],
                #                       item_tag=item['item_tag'])
                data = WikiENItemData()
                data.name = item['title']
                data.url = item['url']
                data.note = item['note']
                data.catalog = item['catalog']
                data.description = item['description']
                data.embed_image_url = ','.join(item['embed_image_url'])
                data.reference_material = item['reference_material']
                data.update_time = item['update_time']
                data.item_tag = item['item_tag']
                data.fetch_time = fetch_time
                CommandOperate.add_one(data)
            except Exception as e:
                db_logger.error(e)
        return item


# request queue
class SpiderRedisPipeline(object):
    """ use bloomfilter to filter the request which had been sent """
    # 百度百科
    base_url = "https://baike.baidu.com"
    bf = BloomFilterRedis(block=filter_blocks, key=baidu_bloom_key)
    # 互动百科
    bf2 = BloomFilterRedis(block=filter_blocks, key=baike_bloom_key)
    # 维基中文百科
    base_url_ZH = "https://zh.wikipedia.org"
    bf3 = BloomFilterRedis(block=filter_blocks, key=wiki_zh_bloom_key)

    # 维基英文百科
    base_url_EN = "https://en.wikipedia.org"
    bf4 = BloomFilterRedis(block=filter_blocks, key=wiki_en_bloom_key)

    def process_item(self, item, spider):
        if not item['keywords_url']:
            return item
        if spider.name == baidu_spider_name:
            for url in item['keywords_url']:
                if self.bf.is_exists(url):
                    continue
                else:
                    new_url = self.base_url + url
                    common_con.lpush(baidu_task_queue, new_url)
        elif spider.name == baike_spider_name:
            # print('这一批任务长度为{}'.format(len(item['keywords_url'])))
            for url in item['keywords_url']:
                if self.bf2.is_exists(url):
                    # print('要爬取的url重复了')
                    continue
                else:
                    new_url = url
                    common_con.lpush(baike_task_queue, new_url)
                    # print('将新的url==》{}放入任务队列'.format(new_url))
        elif spider.name == wiki_zh_spider_name:
            for url in item['keywords_url']:
                if self.bf3.is_exists(url):
                    continue
                else:
                    new_url = self.base_url_ZH + url
                    common_con.lpush(wiki_zh_task_queue, new_url)
        elif spider.name == wiki_en_spider_name:
            for url in item['keywords_url']:
                if self.bf4.is_exists(url):
                    continue
                else:
                    new_url = self.base_url_EN + url
                    common_con.lpush(wiki_en_task_queue, new_url)
        return item


# resources queue
# 新的解决方法：将每个词条的资源连接push到一个专门的下载队列中，然后单独使用下载器来下载任务，低耦合
class WebCachePipeline(object):
    """ push the resource urls into task queue """

    def process_item(self, item, spider):
        bloomKey = "{}.{}".format("bloomfilter", "CacheCSSandJSFilter")
        js_urls = []
        css_urls = []
        bf = BloomFilterRedis(block=2, key=bloomKey)
        # WIKI网站没有可以下载的js和css
        if spider.name in (baike_spider_name, baidu_spider_name):
            for url in item['js']:
                # if '<' in url: # 这里不知道为什么会传过来的item数据会变化
                #     continue
                if bf.is_exists(url):
                    continue
                else:
                    print("js为", url)
                    js_urls.append(url)
            for url in item['css']:
                # if '<' in url:
                #     continue
                if bf.is_exists(url):
                    continue
                else:
                    css_urls.append(url)

        key = "{}.{}".format("resources", "cache_task_queue")
        value = dict(title=item['title'], from2=spider.name, htm=item['html'], js=js_urls, css=css_urls,
                     pic=item['embed_image_url'])
        common_con.lpush(key, value)
        return item
