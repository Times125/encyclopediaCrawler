"""
@Author:lichunhui
@Time:   
@Description: 百度百科爬虫
"""
import re
from urllib.parse import unquote

from scrapy.spiders import Rule
from scrapy.selector import Selector
from baikeSpider.items import BaiduspiderItem
from scrapy.linkextractors import LinkExtractor
from .redis_spider import RedisCrawlSpider
from ..settings import BAIDU_ITEM_URLS
from ..cache.html_cache import CacheTool


class baiduSpider(RedisCrawlSpider):
    task_queue = BAIDU_ITEM_URLS
    base_url = "https://baike.baidu.com"
    name = 'baiduSpider'
    allowed_domains = ['baike.baidu.com']
    rules = (
        Rule(LinkExtractor(allow=('https://baike.baidu.com/item/')), callback='parse', follow=True),
    )
    custom_settings = {
        'FILES_STORE': 'E:\Repositories\\baiduSpider\BaiduCache',
        'ITEM_PIPELINES': {
            'baikeSpider.pipelines.BaiduspiderPipeline': 300,
            'baikeSpider.pipelines.BaiduSpiderRedisPipeline': 301,
            'baikeSpider.pipelines.WebCachePipeline': 302,
        },
    }

    def parse(self, response):
        items = BaiduspiderItem()
        selector = Selector(response)
        print(response.status, response)
        items['url'] = unquote(response.url)
        items['html'] = response.text
        title = selector.xpath("/html/head/title/text()").extract()
        if title:
            items['title'] = title[0].strip().encode('utf-8', errors='ignore').decode('utf-8')
        else:
            items['title'] = ''
        summary = selector.xpath("//div[@class=\"lemma-summary\"]").xpath("string(.)").extract()
        if summary:
            tmps = summary[0].encode('utf-8', errors='ignore').decode('utf-8')
            items['summary'] = re.sub('\r\n|\n|\r', ' ', tmps)
        else:
            items['summary'] = ''

        catalog = selector.xpath("//div[@class=\"lemmaWgt-lemmaCatalog\"]").xpath("string(.)").extract()
        if catalog:
            tmpc = catalog[0].encode('utf-8', errors='ignore').decode('utf-8')
            items['catalog'] = re.sub('\r\n|\n|\r', ' ', tmpc)
        else:
            items['catalog'] = ''

        # 进行迭代抓取的item链接
        urls = [unquote(item) for item in
                selector.xpath("//div[@class=\"para\"]//a[@target=\"_blank\"]/@href").extract()]
        items['keywords_url'] = list(set(filter(lambda x: 'item' in x, urls)))

        description = selector.xpath("//div[@class=\"content-wrapper\"]").xpath("string(.)").extract()
        if description:
            tmpd = description[0].encode('utf-8', errors='ignore').decode('utf-8')
            items['description'] = re.sub('\r\n|\n|\r', ' ', tmpd)
        else:
            items['description'] = ''

        # 匹配pic、js、css
        items['embed_image_url'] = CacheTool.parse_img(items['html'])
        items['js'] = CacheTool.parse_js(items['html'])
        items['css'] = CacheTool.parse_css(items['html'])

        album_pic_url = selector.xpath("//div[@class=\"album-list\"]//a[@class=\"more-link\"]/@href").extract()
        if album_pic_url:
            items['album_pic_url'] = self.base_url + unquote(album_pic_url[0])
        else:
            items['album_pic_url'] = ''

        update_time = selector.xpath("//span[@class = 'j-modified-time']").xpath("string(.)").extract()
        if update_time:
            tmpu = update_time[0].strip().encode('utf-8', errors='ignore').decode('utf-8')
            items['update_time'] = re.sub('\r\n|\n|\r', ' ', tmpu)
        else:
            items['update_time'] = ''

        reference_material = selector.xpath(
            "//dl[@class ='lemma-reference collapse nslog-area log-set-param']").xpath("string(.)").extract()
        if reference_material:
            tmpr = reference_material[0].encode('utf-8', errors='ignore').decode('utf-8')
            items['reference_material'] = re.sub('\r\n|\n|\r', ' ', tmpr)
        else:
            items['reference_material'] = ''

        item_tag = selector.xpath("//dd[@id = \"open-tag-item\"]").xpath("string(.)").extract()
        if item_tag:
            tmpi = item_tag[0].encode('utf-8', errors='ignore').decode('utf-8')
            items['item_tag'] = re.sub('\r\n|\n|\r', ' ', tmpi)
        else:
            items['item_tag'] = ''
        yield items
        # print(items['title'])
