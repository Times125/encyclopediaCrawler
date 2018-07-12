#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:lichunhui
@Time:  2018/7/3 13:09
@Description: 
"""
import urllib
import urllib3
import random
from baikeSpider.settings import MY_USER_AGENT
from baikeSpider.utils.utils import bytes2str
from baikeSpider.utils.utils import strips
from baikeSpider.db.basic import get_redis_conn
from baikeSpider.bloomfilter.filter import BloomFilterRedis
from baikeSpider.settings import FILTER_BLOCKS, BAIDU_BLOOM_KEY
from baikeSpider.cache.html_cache import CacheTool
from baikeSpider.utils.log import *


class A(object):
    def a(self, m):
        self.b()
        print('a', m, type(self))


class B(object):
    def b(self):
        print('b', type(self))


class C(A, B):
    def __init__(self):
        obj = super(C, self)
        obj.a(3)


def download():
    a = "https://bkssl.bdimg.com/static/wiki-lemma/pkg/wiki-lemma_ade1573.js"
    urllib.request.urlretrieve(a, "test.js")


import redis
import re

# 获取redis连接
def get_redis_conn():
    host = '127.0.0.1'
    port = 6379
    pool = redis.ConnectionPool(host=host, port=port)
    handle = redis.StrictRedis(connection_pool=pool, charset='utf-8')
    return handle


if __name__ == "__main__":
    handle = get_redis_conn()
    key = 'redis:test'
    with open("twitter.html", 'r+', encoding='utf8') as reader:
        html = reader.read()
    value = dict(title='你好', htm=html, js=[1, 2], css=[3, 4], pic=[5, 6])
    handle.lpush(key, value)
    res = handle.lpop(key)
    print(type(res), "==>", res)
    tr_v = eval(res)
    print(type(tr_v), "===>", tr_v, bytes2str(tr_v['htm']))
