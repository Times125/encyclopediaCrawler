#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:lichunhui
@Time:  2018/6/15 12:02
@Description: 布隆过滤器
"""
import redis
from filters import GeneralHashFunctions
from baiduSpider.config.conf import get_bloom_args, get_redis_args


class BloomFilter:

    def __init__(self):
        bloom_args = get_bloom_args()
        redis_args = get_redis_args()
        self.host = redis_args['host']
        self.port = redis_args['port']
        self.hash_list = bloom_args['hash_list']
        self.key = bloom_args['key']
        self.pool = redis.ConnectionPool(host=self.host, port=self.port)
        self.handle = redis.StrictRedis(connection_pool=self.pool, charset='utf-8')

    def is_contain(self, item):
        flag = True
        for hs in self.hash_list:
            hash_func = getattr(GeneralHashFunctions, hs)  # 获取hash 函数
            h_value = hash_func(item)
            r_value = h_value % (1 << 32)  # 将hash值映射为32位长
            # print(hash_func,r_value)
            # 当发现0时，item 记录之中，返回false
            if self.handle.getbit(self.key, r_value) == 0:
                self.handle.setbit(self.key, r_value, 1)
                flag = False
        return flag


if __name__ == '__main__':
    pass
    # bf = BloomFilter()
    # f = bf.is_contain('英国跳猎犬')
    # tmps = ['英-国跳猎犬', '美-国跳猎犬','中-国跳猎犬']
    # urls = [u for u in tmps if BloomFilter().is_contain(u) is False]
    # print(urls)
    #
    # for i in []:
    #     print(i)
