# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Field, Item


class BaiduspiderItem(Item):
    name = Field()  # 此词条名称
    keywords = Field()  # 此词条内容所包含的其他词条
    description = Field()  # 词条内容
    url = Field()  # 词条url
    embed_image_url = Field()  # 词条插图图片地址
    album_pic_url = Field()  # 词条相册地址
