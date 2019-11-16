#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:lichunhui
@Time:  2018/7/26 9:38
@Description: 
"""
import re
import calendar
import random
from datetime import datetime
from collections import OrderedDict
from urllib.parse import unquote
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from encyclopediaCrawler.items import EncyclopediaItem
from .redis_spider import RedisCrawlSpider
from ..config import spider_args


class WikiZHSpider(RedisCrawlSpider):
    proxy_mode = 1  # use proxy
    task_queue = spider_args['wiki_en_task_queue']
    base_url = "https://en.wikipedia.org"
    name = spider_args['wiki_en_spider_name']
    allowed_domains = ['en.wikipedia.org']
    rules = (
        Rule(LinkExtractor(allow=('https://en.wikipedia.org/wiki/',)), callback='parse', follow=True),
    )
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'encyclopediaCrawler.middlewares.MyRetryMiddleware': 501,
            'encyclopediaCrawler.middlewares.MyProxyMiddleware': 110,
        }
    }

    def parse(self, response):
        basic_info_dict = OrderedDict()  # 词条属性值
        content_h2_dict = OrderedDict()  # 词条内容值
        img_dict = OrderedDict()  # 表示子标题中出现的图片url
        items = EncyclopediaItem()
        soup = BeautifulSoup(response.text, "html.parser")
        items['original_url'] = unquote(response.url)

        # 多义词, 消歧义
        items['polysemous'] = False
        # 词条名称
        name = soup.find('h1', attrs={'id': 'firstHeading'}).get_text()
        items['name'] = name if name else None
        # wiki解释
        summary = ''
        for children in soup.find('div', attrs={'class': 'mw-parser-output'}).children:
            if '</p>' in str(children):
                try:
                    summary += '<p>' + re.sub('\r|\n', '', children.get_text()) + '</p>'
                except Exception:
                    pass
            elif '</h2>' in str(children):
                break
        items['summary'] = summary
        # 词条来源
        items['source_site'] = '维基百科'
        # 词条编辑次数
        items['edit_number'] = 1
        # 词条最近更新时间
        latest = soup.find('li', attrs={'id': 'footer-info-lastmod'})
        latest = latest.get_text() if latest else ''
        month = 1
        for i in range(12):
            if calendar.month_name[i + 1] in latest:
                month = list(calendar.month_name).index('December')
        ftb = lambda x, y: '-'.join([x[1], str(y), x[0]]) + ' ' + ':'.join(x[2:])
        items['update_time'] = ftb(re.compile(r'([\d]+)').findall(latest), month) if latest else None
        # 词条抓取时间
        items['fetch_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 词条的分类标签（路径）
        item_tag_lis = soup.find('div', attrs={'id': 'mw-normal-catlinks'}).findAll('li')
        item_tag_str = ''
        for li in item_tag_lis:
            if li:
                item_tag_str += re.sub('\r|\n', '', li.get_text()) + '，'
        items['item_tag'] = item_tag_str[:512]
        # 词条缩率图链接
        items['thumbnail_url'] = None
        # 获得下一步需要采集的关键词
        kw_urls = list()
        for kws in soup.findAll('p'):
            try:
                kw = kws.find('a').get('href')
                if kw:
                    kw_urls.append(unquote(kw))
            except Exception:
                continue
        items['keywords_url'] = list(set(filter(lambda x: 'wiki' in x and 'http' not in x, kw_urls)))
        # 词条的简要简介
        items['name_en'] = None
        items['name_other'] = None

        tf = lambda x, y: x if x else y
        table = tf(soup.find('table', attrs={'class': 'infobox geography vcard'}),
                   soup.find('table', attrs={'class': 'infobox vcard'}))
        if table:
            table = table.findAll('tr')
            for tr in table:
                if 'colspan' in str(tr):
                    other_name = tr.find('span', attrs={'class': 'fn org country-name'})
                    if other_name:
                        items['name_other'] = other_name.get_text()
                        # print(items['name_other'])
                else:
                    attr = tr.find('th', attrs={'scope': 'row'})
                    if attr:
                        td_row = tr.find('td')
                        attr_text = re.sub('\\?|•', '', attr.get_text())
                        dict_key = ''.join(attr_text.split())
                        dict_value = ''.join(td_row.get_text().split())
                        basic_info_dict[dict_key] = dict_value

        # 简要信息
        items['basic_info'] = basic_info_dict
        items['album_url'] = None
        # 解析正文中的子标题和对应的正文以及包含的图片
        flag = False  # 标志着已经找到第一个开始的子标题
        sub_title = '正文'
        for children in soup.find('div', attrs={'class': 'mw-parser-output'}).children:
            if 'h2' in str(children.name):
                sub_title = children.find('span', attrs={'class': 'mw-headline'}).get_text()  # 子标题名称
                content_h2_dict[sub_title] = ''
                img_dict[sub_title] = list()
                flag = True
                continue
            elif 'h3' in str(children.name):
                # 3级标题名称
                content_h2_dict[sub_title] += '<h3>' + children.get_text() + '</h3>'
            elif 'p' in str(children.name) and flag is True:
                content_h2_dict[sub_title] += '<p>' + re.sub('\r|\n', '', children.get_text()) + '</p>'
            elif 'ul' in str(children.name) and flag is True:
                content_h2_dict[sub_title] += '<p>' + re.sub('\r|\n', '', children.get_text()) + '</p>'
            elif 'references' in str(children):
                lis = soup.find('ol', attrs={'class': 'references'}).find_all('li')
                refer = ''
                for index, li in enumerate(lis):
                    refer += '<li>' + re.sub('\r|\n', '', li.get_text()) + '</li>'
                content_h2_dict[sub_title] += '<ul>' + refer + '</ul>'
            elif 'thumbinner' in str(children) and flag is True:
                try:
                    img_url = children.find('img').get('src')
                    if img_url:
                        img_dict[sub_title].append('http:' + img_url)
                except Exception:
                    pass
            elif 'reflist' in str(children) and flag is True:
                # 参考资料
                reference_material = children.find('ol', attrs={'class': 'references'})
                if reference_material:
                    for li in reference_material.findAll('li'):
                        if li:
                            cont_value = li.get_text()
                            if cont_value:
                                content_h2_dict[sub_title] += '<p>' + re.sub('\r|\n', '', cont_value) + '</p>'
        # 正文内容
        items['text_content'] = content_h2_dict
        # 正文中包含的图片
        items['text_image'] = img_dict
        # 词条抓取时间
        items['fetch_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        yield items  # 深拷贝的目的是默认浅拷贝item会在后面的pipelines传递过程中会出现错误，比如串数据了
