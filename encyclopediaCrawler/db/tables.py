#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/10/31 21:01
@Description: 
"""
from sqlalchemy import (
    Column, Table, ForeignKey
)
from sqlalchemy.dialects.mysql import (
    VARCHAR, DATETIME, SMALLINT,
    TEXT, INTEGER, ENUM
)
from .basic import metadata

encyclopedia = Table('encyclopedia_data', metadata,
                     Column('id', INTEGER, primary_key=True, autoincrement=True, nullable=False),
                     Column('name', VARCHAR(128)),  # 百科词条名称
                     Column('name_en', VARCHAR(128)),  # 百科英文名称
                     Column('name_other', VARCHAR(512)),  # 百科其他语言名称
                     Column('source_site', ENUM('百度百科', '互动百科', '维基百科')),  # 百科来源：百度百科？互动百科？维基百科？
                     Column('summary', TEXT),  # 词条简介
                     Column('edit_number', INTEGER),  # 词条被编辑次数
                     Column('update_time', DATETIME),  # 词条最近一次被更新时间
                     Column('fetch_time', DATETIME),  # 词条抓取时间
                     Column('item_tag', VARCHAR(1024)),  # 词条所属分类
                     Column('original_url', VARCHAR(512), nullable=False),  # 词条原始url
                     Column('thumbnail_url', VARCHAR(1024)),  # 词条缩率图图片url
                     Column('album_url', VARCHAR(1024)),  # 词条图册url
                     )

# 百科扩展,主要存储正文内容
encyclopedia_expand = Table('encyclopedia_data_expand', metadata,
                            Column('id', INTEGER, primary_key=True, autoincrement=True),
                            Column('pid', INTEGER, ForeignKey("encyclopedia_data.id"), nullable=False),  # 词条id
                            Column('basic_info_name', VARCHAR(128)),  # 词条基本属性名称
                            Column('basic_info_value', VARCHAR(512)),  # 词条基本属性内容
                            Column('text_title', VARCHAR(128)),  # 正文部分二级子标题
                            Column('text_content', TEXT),  # 正文部分二级子标题下的内容
                            Column('text_image', TEXT),  # 正文部分二级子标题下的所有图片链接
                            Column('serial_number', SMALLINT, ),  # 百科词条序号
                            )