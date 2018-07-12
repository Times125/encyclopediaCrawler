#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:lichunhui
@Time:  2018/7/4 11:07
@Description: 页面离线缓存
"""
import re
import urllib3
import random
from ..settings import MY_USER_AGENT
from ..utils.log import logger


class FileException(Exception):
    """General media error exception"""


class CacheTool(object):
    """
    :param html: the response text
    :param path: the cache save path
    :param name: the lemma name
    """

    def __init__(self, html, path=None, name=None):
        self.html = html
        self.path = path
        self.name = name

    def parse_css(self):
        css_url = re.compile(r'href="(http[s]*.+?\.css)"')
        list_css = re.findall(css_url, self.html)
        list_css = list(set(list_css))
        return list_css

    def parse_img(self):
        img_url = re.compile(r'src="(http[s]*.+?\.[jpg]*[png]*[gif]*)"')
        list_img = re.findall(img_url, self.html)
        list_img = list(set(list_img))
        return list_img

    def parse_js(self):
        js_url = re.compile(r'src="(http[s]*.+?\.js)"')
        list_js = re.findall(js_url, self.html)
        list_js = list(set(list_js))
        return list_js

    @classmethod
    def get_response(cls, url, spider, title):
        try:
            userAgent = random.sample(MY_USER_AGENT, 1)[0]
            http = urllib3.PoolManager(timeout=5)
            response = http.request('GET', url, retries=3, headers={'User_Agent': userAgent})
            if response.status != 200:
                logger.warning(
                    'response status is not 200 when request [%s] from [%s]. spider : [%s]' % (url, title, spider.name))
                raise FileException
            if not response.data:
                logger.warning(
                    'response content is empty when request [%s] from [%s]. spider : [%s]' % (url, title, spider.name))
                raise FileException
            return response

        except Exception as e:
            logger.error(
                'response exception:[%s] when request [%s] from [%s]. spider : [%s]' % (e, url, title, spider.name))

    @classmethod
    def download_pic(cls):
        pass

    @classmethod
    def download_css(cls):
        pass

    @classmethod
    def download_js(cls):
        pass

    def reform_html(self):
        """ 更改原网页中得资源链接 """
        pass

    def write2file(self):
        pass
