#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/8/28 19:52
@Description: 
"""
import os
import logging
from logging import config as log_conf
from ..config import logger_args

__all__ = ["db_logger", "download_logger", "parse_logger", "other_logger"]


abs_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), logger_args['log_dir'])
if not os.path.exists(abs_path):
    os.mkdir(abs_path)
log_path = os.path.join(abs_path, logger_args['log_name'])
# print(abs_path)
log_config = {
    'version': 1.0,
    'formatters': {
        'detail': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'simple': {
            'format': '%(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'detail'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 10,
            'filename': log_path,
            'level': 'INFO',
            'formatter': 'detail',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        'download_logger': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
        'parser_logger': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'other_logger': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'db_logger': {
            'handlers': ['file'],
            'level': 'INFO',
        }
    }
}

log_conf.dictConfig(log_config)

db_logger = logging.getLogger("db_logger")
parse_logger = logging.getLogger("parser_logger")
download_logger = logging.getLogger("download_logger")
other_logger = logging.getLogger("other_logger")
