#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:lichunhui
@Time:  2018/7/19 16:05
@Description: 利用谷歌翻译进行因为文本翻译
"""
import urllib.request
import urllib.parse
import execjs
import random
import json
import asyncio
from aiohttp import ClientSession
from baikeSpider.settings import MY_USER_AGENT


class Py4Js(object):
    """ 执行js脚本计算出tk值 """

    def __init__(self):
        self.ctx = execjs.compile(
            """
            function TL(a) {
            var k = "";
            var b = 406644;
            var b1 = 3293161072;
    
            var jd = ".";
            var $b = "+-a^+6";
            var Zb = "+-3^+b+-f";
    
            for (var e = [], f = 0, g = 0; g < a.length; g++) {
                var m = a.charCodeAt(g);
                128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023),
                e[f++] = m >> 18 | 240,
                e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224,
                e[f++] = m >> 6 & 63 | 128),
                e[f++] = m & 63 | 128)
            }
            a = b;
            for (f = 0; f < e.length; f++) a += e[f],
            a = RL(a, $b);
            a = RL(a, Zb);
            a ^= b1 || 0;
            0 > a && (a = (a & 2147483647) + 2147483648);
            a %= 1E6;
            return a.toString() + jd + (a ^ b)
        };
    
        function RL(a, b) {
            var t = "a";
            var Yb = "+";
            for (var c = 0; c < b.length - 2; c += 3) {
                var d = b.charAt(c + 2),
                d = d >= t ? d.charCodeAt(0) - 87 : Number(d),
                d = b.charAt(c + 1) == Yb ? a >>> d: a << d;
                a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d
            }
            return a
        }
        """)

    def getTk(self, text):
        return self.ctx.call("TL", text)


class GoogleTranslate(object):
    """ 调用谷歌翻译api """

    def __init__(self):
        self.js = Py4Js()

    async def open_url(self, url, header, sem):
        async with ClientSession() as session:
            async with sem:
                data = ''
                try:
                    async with session.post(url=url, headers=header) as response:
                        response = await response.read()
                        data = response.decode('utf8')
                except TimeoutError as e:
                    print(e)
                finally:
                    return data

    def translate(self, content):
        length = len(content)  # 传入内容长度
        sem = asyncio.Semaphore(50)
        loop = asyncio.get_event_loop()
        tasks = []
        n = length // 5000  # 分n次发送进行翻译
        remainder = length % 5000  # 剩余字节
        if remainder > 0:
            n += 1
        for i in range(1, n + 1):
            splitContent = content[5000 * (i - 1):5000 * i]
            # print("第%s次分割后的结果,此次长度为%s" % (i, len(splitContent)))
            tk = self.js.getTk(splitContent)
            splitContent = urllib.parse.quote(splitContent)
            headers = {'User-Agent': self.randomAgent()}
            url = "http://translate.google.cn/translate_a/single?client=t" \
                  "&sl=en&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca" \
                  "&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1" \
                  "&srcrom=0&ssel=0&tsel=0&kc=2&tk=%s&q=%s" % (tk, splitContent)
            tasks.append(asyncio.ensure_future(self.open_url(url, headers, sem)))
        res_list = loop.run_until_complete(asyncio.gather(*tasks))
        result = ""
        for res in res_list:
            result += self.parse_json(res)
        # print(result)
        return result

    @staticmethod
    def parse_json(data):
        result = ''
        if data:
            jsns = json.loads(data)[0]
            for lst in jsns:
                if not lst[0]:
                    continue
                result += lst[0]
        return result

    @staticmethod
    def randomAgent():
        agent_pools = MY_USER_AGENT
        return random.sample(agent_pools, 1)[0]


if __name__ == '__main__':
    import time
    gl = GoogleTranslate()
    c = '''
    President Donald Trump should work to form a "cyber NATO" in response to the Russian attack on the 2016 US elections and to prevent more cyber attacks, Rep. Joaquin Castro said Wednesday, even though NATO already cooperates on cybersecurity.
"He should be engaging with our allies to basically form a version of a cyber NATO, where with our allies, our close allies, we agree to essentially mutual defense in cyberspace and, if necessary, mutual cyber response," the Texas Democrat said in an interview with CNN's Wolf Blitzer on "The Situation Room."
According to a NATO fact sheet on cyber defense, NATO allies agreed to work together on cybersecurity in 2014."To keep pace with the rapidly changing threat landscape, NATO adopted an enhanced policy and action plan on cyber defence, endorsed by Allies at the Wales Summit in September 2014," the document reads. "The policy establishes that cyber defence is part of the Alliance's core task of collective defence, confirms that international law applies in cyberspace and intensifies NATO's cooperation with industry."
Castro also called for additional cybersecurity measures domestically.Trump should be "investing in greater election security and having the Congress work with state governments to pass laws to establish even a basic level of cybersecurity protection and election protection for our voting systems," he said. "Right now there isn't a single law -- and I can't find a state law -- that does that."
Castro also questioned Trump's commitment to protecting the US from attacks."Right now, quite honestly, it doesn't look like the President is fully committed to keeping the United States safe from Russian interference," he said.
    President Donald Trump should work to form a "cyber NATO" in response to the Russian attack on the 2016 US elections and to prevent more cyber attacks, Rep. Joaquin Castro said Wednesday, even though NATO already cooperates on cybersecurity.
"He should be engaging with our allies to basically form a version of a cyber NATO, where with our allies, our close allies, we agree to essentially mutual defense in cyberspace and, if necessary, mutual cyber response," the Texas Democrat said in an interview with CNN's Wolf Blitzer on "The Situation Room."
According to a NATO fact sheet on cyber defense, NATO allies agreed to work together on cybersecurity in 2014."To keep pace with the rapidly changing threat landscape, NATO adopted an enhanced policy and action plan on cyber defence, endorsed by Allies at the Wales Summit in September 2014," the document reads. "The policy establishes that cyber defence is part of the Alliance's core task of collective defence, confirms that international law applies in cyberspace and intensifies NATO's cooperation with industry."
Castro also called for additional cybersecurity measures domestically.Trump should be "investing in greater election security and having the Congress work with state governments to pass laws to establish even a basic level of cybersecurity protection and election protection for our voting systems," he said. "Right now there isn't a single law -- and I can't find a state law -- that does that."
Castro also questioned Trump's commitment to protecting the US from attacks."Right now, quite honestly, it doesn't look like the President is fully committed to keeping the United States safe from Russian interference," he said.
    President Donald Trump should work to form a "cyber NATO" in response to the Russian attack on the 2016 US elections and to prevent more cyber attacks, Rep. Joaquin Castro said Wednesday, even though NATO already cooperates on cybersecurity.
"He should be engaging with our allies to basically form a version of a cyber NATO, where with our allies, our close allies, we agree to essentially mutual defense in cyberspace and, if necessary, mutual cyber response," the Texas Democrat said in an interview with CNN's Wolf Blitzer on "The Situation Room."
According to a NATO fact sheet on cyber defense, NATO allies agreed to work together on cybersecurity in 2014."To keep pace with the rapidly changing threat landscape, NATO adopted an enhanced policy and action plan on cyber defence, endorsed by Allies at the Wales Summit in September 2014," the document reads. "The policy establishes that cyber defence is part of the Alliance's core task of collective defence, confirms that international law applies in cyberspace and intensifies NATO's cooperation with industry."
Castro also called for additional cybersecurity measures domestically.Trump should be "investing in greater election security and having the Congress work with state governments to pass laws to establish even a basic level of cybersecurity protection and election protection for our voting systems," he said. "Right now there isn't a single law -- and I can't find a state law -- that does that."
Castro also questioned Trump's commitment to protecting the US from attacks."Right now, quite honestly, it doesn't look like the President is fully committed to keeping the United States safe from Russian interference," he said.
    President Donald Trump should work to form a "cyber NATO" in response to the Russian attack on the 2016 US elections and to prevent more cyber attacks, Rep. Joaquin Castro said Wednesday, even though NATO already cooperates on cybersecurity.
"He should be engaging with our allies to basically form a version of a cyber NATO, where with our allies, our close allies, we agree to essentially mutual defense in cyberspace and, if necessary, mutual cyber response," the Texas Democrat said in an interview with CNN's Wolf Blitzer on "The Situation Room."
According to a NATO fact sheet on cyber defense, NATO allies agreed to work together on cybersecurity in 2014."To keep pace with the rapidly changing threat landscape, NATO adopted an enhanced policy and action plan on cyber defence, endorsed by Allies at the Wales Summit in September 2014," the document reads. "The policy establishes that cyber defence is part of the Alliance's core task of collective defence, confirms that international law applies in cyberspace and intensifies NATO's cooperation with industry."
Castro also called for additional cybersecurity measures domestically.Trump should be "investing in greater election security and having the Congress work with state governments to pass laws to establish even a basic level of cybersecurity protection and election protection for our voting systems," he said. "Right now there isn't a single law -- and I can't find a state law -- that does that."
Castro also questioned Trump's commitment to protecting the US from attacks."Right now, quite honestly, it doesn't look like the President is fully committed to keeping the United States safe from Russian interference," he said.&&
'''
    print(len(c))
    start = time.time()
    gl.translate(c)
    end = time.time()
    print("总共耗时%s秒" %(end - start))
    # for i in range(10):
    #     print(gl.randomAgent())
