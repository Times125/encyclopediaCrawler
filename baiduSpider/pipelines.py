# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql.cursors
import redis

class BaiduspiderPipeline(object):
    def process_item(self, item, spider):
        # conn = pymysql.connect(host='localhost',
        #                        port=3306,
        #                        user='user',
        #                        password='psw',
        #                        db='db',
        #                        charset='utf8mb4',
        #                        cursorclass=pymysql.cursors.DictCursor)
        # try:
        #     with conn.cursor() as cursor:
        #         sql = """INSERT INTO baidubaike (name, url, summary, catalog, description,
        #                   keywords, embed_image_url, album_pic_url, update_time,reference_material, item_tag)
        #                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        #         cursor.execute(sql, (
        #             item['name'], item['url'], item['summary'], item['catalog'], item['description'], item['keywords'],
        #             item['embed_image_url'], item['album_pic_url'], item['update_time'], item['reference_material'],
        #             item['item_tag']))
        #     conn.commit()
        # except Exception as e:
        #     conn.rollback()  # 这里应该把插入失败后的item放到一个失败队列中，等以后再取出来重新爬数据
        return item
