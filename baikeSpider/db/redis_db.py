#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/9/10 6:21
@Description: 
"""
import redis
from ..config import (redis_host, redis_port,
                      redis_pwd, common_db, bloomfilter_db)

__all__ = ['common_con', 'bloomfilter_con']

# 获取redis连接
_redis_args = {
    'host': redis_host,
    'port': redis_port,
    'password': redis_pwd
}

common_con = redis.StrictRedis(**_redis_args, db=common_db)
bloomfilter_con = redis.StrictRedis(**_redis_args, db=bloomfilter_db)
