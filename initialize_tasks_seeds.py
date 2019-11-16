#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:lichunhui
@Time:  2018/7/3 13:09
@Description: 
"""
from encyclopediaCrawler.config import spider_args
from encyclopediaCrawler.db import get_redis_conn

common_con = get_redis_conn()

with open('seeds_for_zh.txt', 'r+', encoding='utf8') as r:
    zh_seeds = r.readlines()

wiki_en_seeds = ['Cat', 'Apple', 'Wiki', 'Culture', 'Art', 'Film', 'Portal:Contents']

for i in wiki_en_seeds:
    common_con.lpush(spider_args['wiki_en_task_queue'], 'https://en.wikipedia.org/wiki/{}'.format(i))

for seed in zh_seeds:
    common_con.lpush(spider_args['baidu_task_queue'], 'https://baike.baidu.com/item/{}'.format(seed.strip('\n')))
    common_con.lpush(spider_args['wiki_zh_task_queue'], 'https://zh.wikipedia.org/wiki/{}'.format(seed.strip('\n')))
print('导入完成')
