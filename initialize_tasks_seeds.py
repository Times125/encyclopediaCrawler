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

zh_seeds = ['猫', '薄一波', '路飞', '铁树', '梅花', '阿卡迪亚的牧人', '隆中对', '台球', '足球', '北京大学', '贝勒大学',
            '狗', '鸟', '中国', '美国', '日本', '唐朝', '宋朝', '南极', '北极', '太平洋', '泰山', '世界大战', '北京', '四川',
            '血液病', '癌症', '甲苯', '染色体', '大数定律', '计算机', '冰川', '第二次世界大战', '太岁', '腾讯', '黑洞', '台风',
            '地震', '雪崩', '泥石流']

wiki_en_seeds = ['Cat', 'Apple', 'Wiki', 'Culture', 'Art', 'Film', 'Portal:Contents']

for i in wiki_en_seeds:
    common_con.lpush(wiki_en_task_queue, 'https://en.wikipedia.org/wiki/{}'.format(i))

common_con.lpush(wiki_zh_task_queue, 'https://zh.wikipedia.org/wiki/{}'.format('Portal:首頁'))

for i in zh_seeds:
    common_con.lpush(baidu_task_queue, 'https://baike.baidu.com/item/{}'.format(i))
    common_con.lpush(baike_task_queue, 'http://www.baike.com/wiki/{}'.format(i))
    common_con.lpush(wiki_zh_task_queue, 'https://zh.wikipedia.org/wiki/{}'.format(i))

print('导入完成')
