# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Field, Item


class BaiduSpiderItem(Item):
    """ 百度百科 """
    title = Field()  # 此词条名称
    url = Field()  # 词条url
    summary = Field()  # 词条简介
    basic_info = Field()  # 词条基本信息
    catalog = Field()  # 词条目录
    description = Field()  # 词条内容
    keywords_url = Field()  # 此词条内容所包含的其他词条
    embed_image_url = Field()  # 词条插图图片地址 list
    album_pic_url = Field()  # 词条相册地址
    update_time = Field()  # 词条更新时间
    reference_material = Field()  # 参考资料
    item_tag = Field()  # 词条标签
    html = Field()  # 网页源码
    js = Field()  # 网页js
    css = Field()  # 网页css样式


class BaikeSpiderItem(Item):
    """ 互动百科 """
    title = Field()  # 此词条名称
    url = Field()  # 词条url
    summary = Field()  # 词条简介
    basic_info = Field()  # 词条基本信息
    catalog = Field()  # 词条目录
    description = Field()  # 词条内容
    keywords_url = Field()  # 此词条内容所包含的其他词条
    embed_image_url = Field()  # 词条插图图片地址 list
    album_pic_url = Field()  # 词条相册地址
    update_time = Field()  # 词条更新时间
    reference_material = Field()  # 参考资料
    item_tag = Field()  # 词条标签
    html = Field()  # 网页源码
    js = Field()  # 网页js
    css = Field()  # 网页css样式


class WikiZHSpiderItem(Item):
    """ 维基中文百科 """
    title = Field()  # 此词条名称
    url = Field()  # 词条url
    note = Field()  # 词条提示
    catalog = Field()  # 词条目录
    description = Field()  # 词条内容
    keywords_url = Field()  # 此词条内容所包含的其他词条
    embed_image_url = Field()  # 词条插图图片地址 list
    update_time = Field()  # 词条更新时间
    reference_material = Field()  # 参考资料
    item_tag = Field()  # 词条标签
    html = Field()  # 网页源码


class WikiENSpiderItem(Item):
    """ 维基英文百科 """
    title = Field()  # 此词条名称
    url = Field()  # 词条url
    note = Field()  # 词条提示
    catalog = Field()  # 词条目录
    description = Field()  # 词条内容
    keywords_url = Field()  # 此词条内容所包含的其他词条
    embed_image_url = Field()  # 词条插图图片地址 list
    update_time = Field()  # 词条更新时间
    reference_material = Field()  # 参考资料
    item_tag = Field()  # 词条标签
    html = Field()  # 网页源码
