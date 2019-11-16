#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/11/12 13:41
@Description: 
"""
import sys
import warnings
from .basic import (create_db, metadata)
from ..logger import db_logger

sys.path.append('..')
sys.path.append('.')

__all__ = ['create_all', ]


def create_all():
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore')  # 忽略警告输出
        try:
            create_db()
            metadata.create_all()
            db_logger.info("execute tasks:create_db(),metadata.create_all() success!")
        except Exception as e:
            print(e)
            db_logger.error("exception '{}' happened when create db".format(e))
