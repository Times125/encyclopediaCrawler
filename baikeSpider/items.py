# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Field, Item


class BaiduspiderItem(Item):
    """ 百度百科 """
    title = Field()  # 此词条名称
    url = Field()  # 词条url
    summary = Field()  # 词条简介
    catalog = Field()  # 词条目录
    description = Field()  # 词条内容
    keywords = Field()  # 此词条内容所包含的其他词条
    keywords_url = Field()  # 此词条内容所包含的其他词条
    embed_image_url = Field()  # 词条插图图片地址 list
    album_pic_url = Field()  # 词条相册地址
    update_time = Field()  # 词条更新时间
    reference_material = Field()  # 参考资料
    item_tag = Field()  # 词条标签
    html = Field()  # 网页源码
    js = Field()  # 网页js
    css = Field()  # 网页css样式


class BaikespiderItem(Item):
    """ 互动百科 """
    title = Field()  # 此词条名称
    url = Field()  # 词条url
    summary = Field()  # 词条简介
    catalog = Field()  # 词条目录
    description = Field()  # 词条内容
    keywords = Field()  # 此词条内容所包含的其他词条
    keywords_url = Field()  # 此词条内容所包含的其他词条
    embed_image_url = Field()  # 词条插图图片地址 list
    album_pic_url = Field()  # 词条相册地址
    update_time = Field()  # 词条更新时间
    reference_material = Field()  # 参考资料
    item_tag = Field()  # 词条标签
