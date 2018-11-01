#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:lichunhui
@Time:  2018/7/3 15:28
@Description: 
"""
from ..db import bloomfilter_con
from ..bloomfilter import hashfuncs

__all__ = ['BloomFilterRedis', ]


class BloomFilterRedis:
    default_key = 'bloomfilter'
    hash_list = ["rs_hash", "js_hash", "pjw_hash", "elf_hash",
                 "bkdr_hash", "sdbm_hash", "djb_hash", "dek_hash"]

    def __init__(self, block=2, key=None):
        """redis的一个string最大为512M,所以需要block进行扩容"""
        self.key = key if key else self.default_key
        self.blcok = block
        self.conn = bloomfilter_con

    @classmethod
    def random_generator(cls, hash_value):
        """
        将hash函数得出的函数值映射到[0, 2^32-1]区间内
        """
        return hash_value % (1 << 32)

    def is_exists(self, url):
        """
        检查是否是新的条目，是新条目则更新bitmap并返回False，是重复条目则返回True
        :param url: 需要进行去重验证的url
        :return: 验证结果
        """
        flag = True
        for hash_func_str in self.hash_list:
            hash_func = getattr(hashfuncs, hash_func_str)
            hash_value = hash_func(url)
            real_value = self.random_generator(hash_value)
            cur_block = str(real_value % self.blcok)
            key = ''.join((self.key, cur_block))
            if self.conn.getbit(key, real_value) == 0:
                self.conn.setbit(key, real_value, 1)
                flag = False
        return flag
