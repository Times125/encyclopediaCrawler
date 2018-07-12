#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:lichunhui
@Time:  2018/7/3 11:20
@Description: 
"""
import re


def bytes2str(data, encoding='utf8'):
    """
    return a str if a bytes objects is given.
    :param data: byte
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
