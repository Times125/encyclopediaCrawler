"""
@Author:lichunhui
@Time:   
@Description: 百度百科爬虫
"""
import re
from bs4 import BeautifulSoup
from urllib.parse import unquote
from datetime import datetime
from scrapy.spiders import Rule
from collections import OrderedDict
from scrapy.linkextractors import LinkExtractor
from .redis_spider import RedisCrawlSpider
from ..config import spider_args
from ..items import EncyclopediaItem


class BaiduSpider(RedisCrawlSpider):
    proxy_mode = 0  # not use proxy
    task_queue = spider_args['baidu_task_queue']
    base_url = "https://baike.baidu.com"
    name = spider_args['baidu_spider_name']
    allowed_domains = ['baike.baidu.com']
    rules = (
        Rule(LinkExtractor(allow=('https://baike.baidu.com/item/',)), callback='parse', follow=True),
    )

    def parse(self, response):
        basic_info_dict = OrderedDict()  # 词条基本信息值
        content_h2_dict = OrderedDict()  # 词条正文内容值
        img_dict = OrderedDict()  # 表示子标题中出现的图片url
        items = EncyclopediaItem()  # 基础信息

        soup = BeautifulSoup(response.text, "html.parser")
        # 词条是否为多义词
        items['polysemous'] = '/view/10812277.htm' in response.text
        # 词条url
        items['original_url'] = unquote(response.url)
        # 词条名称
        name = soup.title.get_text()
        items['name'] = name.split('_百度百科')[0] if name else None
        # name = soup.find('dd', attrs={'class': 'lemmaWgt-lemmaTitle-title'}).find('h1')
        # items['name'] = name.get_text() if name else None
        # 百科解释
        summary = soup.find('div', attrs={'class': 'lemma-summary'})
        items['summary'] = re.sub(r'\r|\n', '', summary.get_text()) if summary else None
        # 词条来源
        items['source_site'] = '百度百科'
        # 词条被编辑次数
        desc_text = soup.find('dl', attrs={'class': 'side-box lemma-statistics'})
        edit_number = re.compile(r'编辑次数：([\d]+)次').findall(desc_text.get_text())[0] if desc_text else None
        items['edit_number'] = int(edit_number) if edit_number else 1
        # 词条最近更新时间
        latest = soup.find('span', attrs={'class': 'j-modified-time'})
        items['update_time'] = latest.get_text().replace('（', '').replace('）', '') if latest else None
        # 词条抓取时间
        items['fetch_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 词条的分类标签（路径）
        item_tag = soup.find('dd', attrs={'id': 'open-tag-item'})
        items['item_tag'] = re.sub(r'\r|\n|\s', '', item_tag.get_text()) if item_tag else None
        # 词条缩率图链接
        thumbnail_url = soup.find('div', attrs={'class': 'summary-pic'})
        items['thumbnail_url'] = thumbnail_url.find('img').get('src') if thumbnail_url else None
        # 获得下一步需要采集的关键词
        kw_urls = list()
        for tag_obj in soup.findAll('div', attrs={'class': 'para'}):
            try:
                kw_urls.append(unquote(tag_obj.find('a', attrs={'target': '_blank'}).get('href')))
            except (AttributeError, TypeError):
                pass
        items['keywords_url'] = list(set(filter(lambda x: 'item' in x, kw_urls)))
        # 词条的简要简介
        items['name_en'] = None
        items['name_other'] = None
        basic_info_item_name = soup.findAll('dt', attrs={'class': 'basicInfo-item name'})
        basic_info_item_value = soup.findAll('dd', attrs={'class': 'basicInfo-item value'})
        for basic_info in zip(basic_info_item_name, basic_info_item_value):
            dict_key = ''.join(basic_info[0].get_text(strip=True).split())
            dict_value = basic_info[1].get_text(strip=True).strip()
            if '英文名称' == dict_key:
                items['name_en'] = dict_value
            elif dict_key in ['外文名', '外文名称']:
                items['name_other'] = dict_value
            else:
                basic_info_dict[dict_key] = dict_value

        #找到第一个class为para-title且class为level-2的div标签
        sibling = soup.find('div', attrs={'class': lambda x: x and 'para-title' in x and 'level-2' in x})

        #如果没有二级标题，那么就是正文
        if not sibling:
            h2_title = '正文'
            content_h2_dict[h2_title] = ''
            img_dict[h2_title] = list()
            for para in soup.find_all('div', attrs={'class': 'para'}):
                content_h2_dict[h2_title] += '<p>' + re.sub(r'\r|\n', '', para.get_text()) + '</p>'
                try:
                    img_url = para.find('img').get('data-src')
                    if img_url:
                        img_dict[h2_title].append(img_url)
                except AttributeError:
                    pass

        #如果有二级标题，分别获取每个二级标题下的内容
        else:
            while sibling is not None:
                if 'para-title level-2' in str(sibling):
                    h2_title = sibling.find('h2', attrs={'class': 'title-text'}).get_text('$$').split('$$')[-1]  # h2标题
                    content_h2_dict[h2_title] = ''
                    img_dict[h2_title] = list()
                # elif 'para' in str(sibling):
                elif 'para-title level-3' in str(sibling):
                    # 3级标题名称
                    content_h2_dict[h2_title] += '<h3>' + sibling.find('h3').get_text('$$').split('$$')[-1] + '</h3>'
                elif 'class=\"para' in str(sibling):
                    # 对应的正文内容
                    content_h2_dict[h2_title] += '<p>' + re.sub(r'\r|\n', '', sibling.get_text()).strip() + '</p>'
                    try:
                        img_url = sibling.find('img').get('data-src')
                        if img_url:
                            img_dict[h2_title].append(img_url)
                    except AttributeError:
                        pass
                try:
                    sibling = next(sibling.next_siblings)
                except StopIteration:
                    sibling = None
                    
        # 参考资料
        try:
            reference_key = soup.find('dt', attrs={'class': 'reference-title'}).get_text()
            reference_value = ''
            reference_urls = []
            lis = soup.find('ul', attrs={'class': 'reference-list'}).find_all('li')
            for index, li in enumerate(lis):
                reference_value += '<p>'.format(index) + re.sub(r'\r|\n', '', li.get_text()) + '</p>'
                url = li.find('a', attrs={'rel': 'nofollow'})
                if url:
                    reference_urls.append(self.base_url + url.get('href'))
            content_h2_dict[reference_key] = reference_value if reference_value else None
            img_dict[reference_key] = reference_urls
        except (AttributeError, TypeError):
            pass
        # 词条图册链接
        album_url = soup.find('div', attrs={'class': 'album-list'})
        if album_url:
            album_url = album_url.find('a', attrs={'class': 'more-link'}).get('href')
        items['album_url'] = self.base_url + album_url if album_url else None
        # 简要信息
        items['basic_info'] = basic_info_dict
        # 正文内容
        items['text_content'] = content_h2_dict
        # 正文中包含的图片
        items['text_image'] = img_dict
        # print(items['name'], items['polysemous'])
        yield items  # 深拷贝的目的是默认浅拷贝item会在后面的pipelines传递过程中会出现错误，比如串数据了
