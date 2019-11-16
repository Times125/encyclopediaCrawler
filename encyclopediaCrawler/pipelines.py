# -*- coding: utf-8 -*-

from scrapy.exceptions import DropItem
from twisted.internet.threads import deferToThread

from .db import (
    CommandOperate, EncyclopediaItemDataExpand,
    EncyclopediaItemData, get_redis_conn
)

from .config import spider_args
from .bloomfilter import BloomFilterRedis

# spider.name 到 spider.task.queue的映射
maps = {
    spider_args['baidu_spider_name']: spider_args['baidu_task_queue'],
    spider_args['baike_spider_name']: spider_args['baike_task_queue'],
    spider_args['wiki_zh_spider_name']: spider_args['wiki_zh_task_queue'],
    spider_args['wiki_en_spider_name']: spider_args['wiki_en_task_queue'],
}


class BasePipeline(object):
    redis_conn = get_redis_conn()
    bf = BloomFilterRedis(block=spider_args['filter_blocks'],
                          key=spider_args['bloom_key'],
                          redis_conn=redis_conn)
    redis_handler = redis_conn.sadd if spider_args['use_set'] else redis_conn.rpush

    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):
        raise NotImplementedError


# 300
class SpiderPipeline(BasePipeline):

    # TODO 数据导入到数据库
    def _process_item(self, item, spider):
        if not item['polysemous']:  # 如果是多义词，则舍弃
            deferToThread(self._insert_basic_info, item)
        return item

    @classmethod
    def _insert_basic_info(cls, item):
        data = EncyclopediaItemData()
        data.name = item['name']
        data.name_en = item['name_en']
        data.name_other = item['name_other']
        data.original_url = item['original_url']
        data.summary = item['summary']
        data.source_site = item['source_site']
        data.edit_number = item['edit_number']
        data.fetch_time = item['fetch_time']
        data.update_time = item['update_time']
        data.item_tag = item['item_tag']
        data.thumbnail_url = item['thumbnail_url']
        data.album_url = item['album_url']
        CommandOperate.add_one(data)  # 提交词条的基本信息数据
        record = CommandOperate.query(data.name, data.fetch_time)  # 然后查询此条记录的id
        cls._insert_text(item, record)

    @classmethod
    def _insert_text(cls, item, record):
        # 获得插入的数据的ID
        basic_info, text_content, text_image = item['basic_info'], item['text_content'], item['text_image']
        serial_number = 0
        expand_list = list()
        for key, value in basic_info.items():
            # print('basic_info', key, ' : ', value)
            data_exp = EncyclopediaItemDataExpand()
            data_exp.pid = record.id
            data_exp.basic_info_name = key
            data_exp.basic_info_value = value
            data_exp.serial_number = serial_number
            serial_number += 1
            expand_list.append(data_exp)
        for key, value in text_content.items():
            # print('text_content', key, ' : ', value)
            data_exp = EncyclopediaItemDataExpand()
            data_exp.pid = record.id
            data_exp.text_title = key
            data_exp.text_content = value
            data_exp.text_image = ','.join(text_image[key]) if text_image[key] else None
            data_exp.serial_number = serial_number
            serial_number += 1
            expand_list.append(data_exp)
        CommandOperate.add_batches(expand_list)


# 301
class SpiderRedisPipeline(BasePipeline):
    """ use bloomfilter to filter the request which had been sent """

    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):

        if not item['keywords_url']:
            return item
        if not hasattr(spider, 'base_url') or not spider.base_url:
            raise DropItem(
                "Not detecting attr 'base_url', you must indicate attr 'base_url' in your spider object.")
        for url in item['keywords_url']:
            new_url = spider.base_url + url
            if self.bf.is_exists(new_url) or '/w/api.php' in url or '/w/index.php' in url:
                continue
            else:
                self.redis_handler(maps[spider.name], new_url)
        return item
