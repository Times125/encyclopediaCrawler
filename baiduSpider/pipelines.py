# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql.cursors
from db.ItemData import ItemData
from db.dao import CommandOperate


class BaiduspiderPipeline(object):

    def process_item(self, item, spider):
        data = ItemData(title=item['title'], url=item['url'], summary=item['summary'],
                        catalog=item['catalog'],description=item['description'],
                        embed_image_url=item['embed_image_url'],album_pic_url=item['album_pic_url'],
                        reference_material=item['reference_material'],update_time=item['update_time'],
                        item_tag=['item_tag'])
        CommandOperate.add_one(data)
        """
        conn = pymysql.connect(host='127.0.0.1',
                               port=3306,
                               user='root',
                               password='',
                               db='test',
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)
        try:
            # print('pipelines==========>', item)
            with conn.cursor() as cursor:
                sql = "INSERT INTO baidu(name, url, summary, catalog, description, embed_image_url, album_pic_url, reference_material, update_time,item_tag) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (item['title'], item['url'], item['summary'], item['catalog'], item['description'],
                                     item['embed_image_url'], item['album_pic_url'], item['reference_material'],
                                     item['update_time'], item['item_tag']))
            conn.commit()
        except Exception as e:
            conn.rollback()  # 这里应该把插入失败后的item放到一个失败队列中，等以后再取出来重新爬数据
            print('exception:>', e)
        """
        return item
