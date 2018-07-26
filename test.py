#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:lichunhui
@Time:  2018/7/3 13:09
@Description: 
"""
import urllib
import urllib3
import random
import redis
import re
from baikeSpider.settings import MY_USER_AGENT
from baikeSpider.utils.utils import bytes2str
from baikeSpider.utils.utils import strips
from baikeSpider.db.basic import get_redis_conn
from baikeSpider.bloomfilter.filter import BloomFilterRedis
from baikeSpider.settings import FILTER_BLOCKS, BAIDU_BLOOM_KEY, BAIDU_HTML_CACHE, WEB_CACHE_DELAY, WEB_CACHE_FEED_SIZE
from baikeSpider.cache.html_cache import CacheTool
from baikeSpider.utils.log import *
import time
import asyncio
import aiofiles
from aiohttp import ClientSession
from WebDownloader.base import baseDownloader
from baikeSpider.cache.html_cache import CacheTool

async def download_js(url, sem):
    async with ClientSession() as session:
        async with sem:
            async with session.get(url) as response:
                res = await response.read()
                path = url.split('/')[-1]
                js_filename = '{}\\{}'.format("E:\Repositories\\baiduSpider\BaiduCache\js_resources", path)
                async with aiofiles.open(js_filename, 'w+', encoding='utf8') as writter:
                    await writter.write(bytes2str(res))
                return res


async def download_css(url, sem):
    async with ClientSession() as session:
        async with sem:
            async with session.get(url) as response:
                res = await response.read()
                # print(res)
                path = url.split('/')[-1]
                css_filename = '{}\\{}'.format("E:\Repositories\\baiduSpider\BaiduCache\css_resources", path)
                async with aiofiles.open(css_filename, 'w+', encoding='utf8') as writter:
                    await writter.write(bytes2str(res))
                return res


async def download_pic(url, sem, title):
    async with ClientSession() as session:
        async with sem:
            async with session.get(url) as response:
                res = await response.read()
                path = url.split('/')[-1]
                folder = strips(title)
                folder = '{}\\{}'.format("E:\Repositories\\baiduSpider\BaiduCache", folder)
                if not os.path.exists(folder):
                    os.makedirs(folder)
                pic_filename = '{}/{}'.format(folder, path)
                async with aiofiles.open(pic_filename, 'wb') as writter:
                    await writter.write(res)

                # with open(pic_filename, 'wb') as writter:
                #     writter.write(res)
                return res


# 获取redis连接
def get_redis_conn():
    host = '127.0.0.1'
    port = 6379
    pool = redis.ConnectionPool(host=host, port=port)
    handle = redis.StrictRedis(connection_pool=pool, charset='utf-8')
    return handle


def test_eval():
    handle = get_redis_conn()
    key = "resources:cache_task_queue"
    # with open("twitter.html", 'r+', encoding='utf8') as reader:
    #     html = reader.read()
    # value = dict(title='你好', htm=html, js=[1, 2], css=[3, 4], pic=[5, 6])
    # handle.lpush(key, value)
    res = handle.lpop(key)
    # print(type(res), "==>", res)
    tr_v = eval(res)
    return tr_v
    # print(type(tr_v), "===>", tr_v, bytes2str(tr_v['htm']))


def make_request_from_data(data):
    title = data['title']
    spiderName = data['from2']
    htm = data['htm']
    js = data['js']
    css = data['css']
    pic = data['pic']

    tasks = []

    loop = asyncio.get_event_loop()
    sem = asyncio.Semaphore(100)
    # for i in js:
    #     task = asyncio.ensure_future(download(i, sem))
    #     tasks.append(task)
    tasks = [asyncio.ensure_future(download_js(i, sem)) for i in js]
    js_res = loop.run_until_complete(asyncio.gather(*tasks))

    # for i in css:
    #     task = asyncio.ensure_future(download(i, sem))
    #     tasks.append(task)
    tasks = [asyncio.ensure_future(download_css(i, sem)) for i in css]
    css_res = loop.run_until_complete(asyncio.gather(*tasks))

    # for i in pic:
    #     task = asyncio.ensure_future(download(i, sem))
    #     tasks.append(task)
    tasks = [asyncio.ensure_future(download_pic(i, sem, title)) for i in pic]
    pic_res = loop.run_until_complete(asyncio.gather(*tasks))
    # loop.close()

    return js_res, css_res, pic_res


if __name__ == "__main__":

    # path = 'test.css'
    # css_filename = '{}/{}'.format("E:\Repositories\\baiduSpider\BaiduCache\css_resources", path)
    with open('twitter.html', 'r', encoding='utf8') as r:
        html = r.read()
    pic_url = re.compile(r'src="(//*.+?\.[jpg]*[png]*[gif]*)"')
    list_pic = re.findall(pic_url, html)
    list_pic = ['https:' + pic for pic in list(set(filter(lambda x: '/static/images/' not in x, list_pic)))]
    for i in list_pic:
        print(i)
    # redis_batch_size = WEB_CACHE_FEED_SIZE
    # task_queue = "resources:cache_task_queue"
    # fetch_one = get_redis_conn().lpop
    # while True:
    #     time.sleep(WEB_CACHE_DELAY)
    #     found = 0
    #     start_time = time.time()
    #     while found < redis_batch_size:
    #         data = fetch_one(task_queue)
    #
    #         if not data:
    #             # Queue empty.
    #             break
    #         data = eval(data)
    #         req1, req2, req3 = make_request_from_data(data)
    #         # if req1 and req2 and req3:
    #         #     # yield req
    #         found += 1
    #     end_time = time.time()
    #     print(end_time - start_time)
