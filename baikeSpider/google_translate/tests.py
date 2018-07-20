#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:lichunhui
@Time:  2018/7/19 20:32
@Description: 
"""
import asyncio
from aiohttp import ClientSession


async def test(url, header):
    async with ClientSession() as session:
        async with session.post(url=url, headers=header) as response:
            response = await response.read()
            print(response.decode('utf8'))


if __name__ == '__main__':
    url = "http://translate.google.cn/translate_a/single?client=t" \
          "&sl=en&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca" \
          "&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1" \
          "&srcrom=0&ssel=0&tsel=0&kc=2&tk=916060.754696&q=hello how are you"
    header = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0"}
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.ensure_future(test(url, header)))
