#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:lichunhui
@Time:  2018/7/9 14:23
@Description: 
"""
import logging
import os
from ..settings import LOG_PATH

# 自定义日志级别
level_none = logging.NOTSET
level_debug = logging.DEBUG
level_info = logging.INFO
level_warn = logging.WARN
level_error = logging.ERROR
level_critical = logging.CRITICAL


class CustomLogger(object):
    def __init__(self, s_name_log, s_path_log=LOG_PATH, i_level_log=logging.DEBUG):
        # 自定义一个名为s_name_log的logger
        self.customLogger = logging.getLogger(s_name_log)

        # 实例化一个format,定义了log的格式
        fmt = logging.Formatter('%(asctime)s %(levelname)s %(message)s', '%Y-%m-%d %H:%M:%S')
        # 实例化一个filehander，log可以将message写入文件中
        fh = logging.FileHandler(os.path.join(s_path_log, s_name_log))
        # 实例化一个streamhandler，log可以将message输出到控制台中
        sh = logging.StreamHandler()
        # 实例化一个filter，对logger的name进行过滤，如果s_name_log=='JeremyLogging'，输出；反之，过滤掉
        # 这个filter可以配置到handler中，也可以直接配置到logger中
        # ft = logging.Filter('JeremyLogging')

        fh.setFormatter(fmt)
        fh.setLevel(i_level_log)
        # fh.addFilter(ft)
        sh.setFormatter(fmt)
        sh.setLevel(i_level_log)
        # sh.addFilter(ft)

        self.customLogger.addHandler(fh)
        self.customLogger.addHandler(sh)
        # self.customLogger.addFilter(ft)

    def debug(self, s_message_log):
        self.customLogger.debug(s_message_log)

    def info(self, s_message_log):
        self.customLogger.info(s_message_log)

    def warning(self, s_message_log):
        self.customLogger.warning(s_message_log)

    def error(self, s_message_log):
        self.customLogger.error(s_message_log)

    def critical(self, s_message_log):
        self.customLogger.critical(s_message_log)


logger = CustomLogger('log.log', i_level_log=level_info)
