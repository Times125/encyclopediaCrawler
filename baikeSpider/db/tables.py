#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/10/31 21:01
@Description: 
"""
from sqlalchemy import Table, Column, INTEGER, String, Text
from .basic import metadata

baidu = Table('baidu', metadata,
              Column('id', INTEGER, primary_key=True, autoincrement=True),
              Column('name', String(128)),
              Column('url', String(512)),
              Column('summary', String(1024)),
              Column('basic_info', String(1024)),
              Column('catalog', String(1024)),
              Column('description', Text),
              Column('embed_image_url', String(1024)),
              Column('album_pic_url', String(1024)),
              Column('reference_material', String(2048)),
              Column('update_time', String(128)),
              Column('item_tag', String(512)),
              Column('fetch_time', String(128)),
              )

baike = Table('baike', metadata,
              Column('id', INTEGER, primary_key=True, autoincrement=True),
              Column('name', String(128)),
              Column('url', String(512)),
              Column('summary', String(1024)),
              Column('basic_info', String(1024)),
              Column('catalog', String(1024)),
              Column('description', Text),
              Column('embed_image_url', String(1024)),
              Column('album_pic_url', String(1024)),
              Column('reference_material', String(2048)),
              Column('update_time', String(128)),
              Column('item_tag', String(512)),
              Column('fetch_time', String(128)),
              )

wiki_zh = Table('wiki_zh', metadata,
                Column('id', INTEGER, primary_key=True, autoincrement=True),
                Column('name', String(128)),
                Column('url', String(512)),
                Column('note', String(1024)),
                Column('catalog', String(1024)),
                Column('description', Text),
                Column('embed_image_url', String(1024)),
                Column('reference_material', String(2048)),
                Column('update_time', String(128)),
                Column('item_tag', String(512)),
                Column('fetch_time', String(128)),
                )

wiki_en = Table('wiki_en', metadata,
                Column('id', INTEGER, primary_key=True, autoincrement=True),
                Column('name', String(128)),
                Column('url', String(512)),
                Column('note', String(1024)),
                Column('catalog', String(1024)),
                Column('description', Text),
                Column('embed_image_url', String(1024)),
                Column('reference_material', String(2048)),
                Column('update_time', String(128)),
                Column('item_tag', String(512)),
                Column('fetch_time', String(128)),
                )
