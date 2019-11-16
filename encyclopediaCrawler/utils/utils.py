#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:lichunhui
@Time:  2018/7/3 11:20
@Description: 
"""
import threading
import sys
import random
import re
import hashlib
import time
from functools import (partial, wraps)
from ..logger import download_logger

first_num = random.randint(55, 69)
third_num = random.randint(0, 3500)
fourth_num = random.randint(0, 140)


class FakeChromeUA:
    os_type = [
        '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
        '(Macintosh; Intel Mac OS X 10_13_6)'
    ]

    chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

    @classmethod
    def get_ua(cls):
        return ' '.join(['Mozilla/5.0', random.choice(cls.os_type), 'AppleWebKit/537.36',
                         '(KHTML, like Gecko)', cls.chrome_version, 'Safari/537.36'])


def bytes2str(data, encoding='utf8'):
    """
    return a str if a bytes objects is given.
    """
    if isinstance(data, bytes):
        return data.decode(encoding)
    return data


def strips(path):
    """
    :param path: 需要清洗的文件夹名字
    :return: 清洗掉Windows系统非法文件夹名字的字符串
    """
    path = re.sub(r'[?\\*|"<>:/]', '', str(path))
    path = path.replace(' ', '-')
    return path


def md5(data):
    """
    return md5 value
    :param data:
    :return:
    """
    if not isinstance(data, str):
        data = str(data)
    hl = hashlib.md5()
    hl.update(data.encode('utf-8'))
    return hl.hexdigest()
