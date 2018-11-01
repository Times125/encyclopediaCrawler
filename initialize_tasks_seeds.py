#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:lichunhui
@Time:  2018/7/3 13:09
@Description: 
"""
from baikeSpider.config import (baidu_task_queue, baike_task_queue,
                                wiki_zh_task_queue, wiki_en_task_queue)
from baikeSpider.db import common_con

common_con.lpush(baidu_task_queue, 'https://baike.baidu.com/item/树脂')
common_con.lpush(baike_task_queue, 'http://www.baike.com/wiki/猫')
common_con.lpush(wiki_en_task_queue, 'https://en.wikipedia.org/wiki/Wiki')
common_con.lpush(wiki_zh_task_queue, 'https://zh.wikipedia.org/wiki/第二次世界大战')
print('导入完成')
