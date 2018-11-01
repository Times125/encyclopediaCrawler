#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:lichunhui
@Time:  2018/7/12 10:13
@Description: 
"""
import os
import time
import asyncio

import aiofiles
from aiohttp import ClientSession
from baikeSpider.settings import (WEB_CACHE_DELAY, WEB_CACHE_FEED_SIZE, BAIDU_HTML_CACHE, BAIKE_HTML_CACHE, )
from baikeSpider.config import (baidu_spider_name, baike_spider_name, wiki_zh_spider_name,
                                wiki_en_spider_name)
from baikeSpider.db import common_con
from baikeSpider.utils.utils import bytes2str, strips


class baseDownloader(object):
    """
    下载资源

    """

    def __init__(self):
        pass

    def run(self):
        redis_batch_size = WEB_CACHE_FEED_SIZE
        task_queue = "resources:cache_task_queue"
        fetch_one = common_con.lpop
        while True:
            time.sleep(WEB_CACHE_DELAY)
            found = 0
            while found < redis_batch_size:
                data = fetch_one(task_queue)
                if not data:
                    # Queue empty.
                    break
                data = eval(data)
                req1, req2, req3 = self.make_request_from_data(data)
                # if req1 and req2 and req3:
                #     # yield req
                found += 1

    def make_request_from_data(self, data):
        title = data['title']
        spiderName = data['from2']
        htm = data['htm']
        js = data['js']
        css = data['css']
        pic = data['pic']

        loop = asyncio.get_event_loop()
        sem = asyncio.Semaphore(100)

        tasks = [asyncio.ensure_future(self.download_js(i, spiderName, sem)) for i in js]
        js_res = loop.run_until_complete(asyncio.gather(*tasks))

        tasks = [asyncio.ensure_future(self.download_css(i, spiderName, sem)) for i in css]
        css_res = loop.run_until_complete(asyncio.gather(*tasks))

        tasks = [asyncio.ensure_future(self.download_pic(i, spiderName, sem, title)) for i in pic]
        pic_res = loop.run_until_complete(asyncio.gather(*tasks))

        return js_res, css_res, pic_res

    # TODO: 文件存储方法改为写入KAFKA
    @classmethod
    async def download_js(cls, url, spiderName, sem):
        async with ClientSession() as session:
            async with sem:
                res = ""
                try:
                    async with session.get(url) as response:
                        res = await response.read()
                        path = url.split('/')[-1]
                        js_filename = None
                        if spiderName == "baiduSpider":
                            folder = os.path.join(BAIDU_HTML_CACHE, 'js_resources')
                            cls.file_exists(folder)
                            js_filename = os.path.join(folder, path)
                        elif spiderName == "baikeSpider":
                            folder = os.path.join(BAIKE_HTML_CACHE, 'js_resources')
                            cls.file_exists(folder)
                            js_filename = os.path.join(folder, path)
                        async with aiofiles.open(js_filename, 'w+', encoding='utf8') as writter:
                            await writter.write(bytes2str(res))
                except Exception or TimeoutError as e:
                    print(e)
                finally:
                    return res

    # TODO: 文件存储方法改为写入KAFKA
    @classmethod
    async def download_css(cls, url, spiderName, sem):
        async with ClientSession() as session:
            async with sem:
                res = ""
                try:
                    async with session.get(url) as response:
                        res = await response.read()
                        # print(res)
                        css_filename = None
                        path = url.split('/')[-1]

                        if spiderName == "baiduSpider":
                            folder = os.path.join(BAIDU_HTML_CACHE, 'css_resources')
                            cls.file_exists(folder)
                            css_filename = os.path.join(folder, path)
                        elif spiderName == "baikeSpider":
                            folder = os.path.join(BAIKE_HTML_CACHE, 'css_resources')
                            cls.file_exists(folder)
                            css_filename = os.path.join(folder, path)

                        async with aiofiles.open(css_filename, 'w+', encoding='utf8') as writter:
                            await writter.write(bytes2str(res))
                except Exception or TimeoutError as e:
                    print(e)
                finally:
                    return res

    # TODO: 文件存储方法改为写入KAFKA
    @classmethod
    async def download_pic(cls, url, spiderName, sem, title):
        async with ClientSession() as session:
            async with sem:
                res = ""
                try:
                    async with session.get(url) as response:
                        res = await response.read()
                        path = url.split('/')[-1]
                        folder = strips(title)
                        pic_filename = None
                        if spiderName == "baiduSpider":
                            folder = os.path.join(BAIDU_HTML_CACHE, folder)
                            cls.file_exists(folder)
                            pic_filename = os.path.join(folder, path)
                        elif spiderName == "baikeSpider":
                            folder = os.path.join(BAIKE_HTML_CACHE, folder)
                            cls.file_exists(folder)
                            pic_filename = os.path.join(folder, path)
                        async with aiofiles.open(pic_filename, 'wb') as writter:
                            await writter.write(res)
                except Exception or TimeoutError as e:
                    print(e)
                finally:
                    return res

    @classmethod
    def file_exists(cls, folder):
        if not os.path.exists(folder):
            os.makedirs(folder)
