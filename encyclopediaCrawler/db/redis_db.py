#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/9/10 6:21
@Description: 
"""
import redis
from ..config import redis_args

__all__ = ['get_redis_conn']


def get_redis_conn():
    # 获取redis连接
    _redis_args = {
        'host': redis_args['redis_host'],
        'port': redis_args['redis_port'],
        'password': redis_args['redis_pwd'],
    }
    return redis.StrictRedis(**_redis_args, db=redis_args['db'])
