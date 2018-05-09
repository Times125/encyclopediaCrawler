"""
@Author:lichunhui
@Time:   
@Description: 百度百科爬虫
"""
from scrapy.shell import inspect_response
from scrapy.spiders import Spider,CrawlSpider
from scrapy.selector import Selector

from baiduSpider.items import BaiduspiderItem


class baiduSpider(Spider):
    name = 'baiduSpider'
    allowed_domains = ['baike.baidu.com']
    start_urls = ['https://baike.baidu.com/item/英国跳猎犬']

    def parse(self, response):

        items = BaiduspiderItem()
        selector = Selector(response)
        items['name'] = selector.xpath("//dd[@class=\"lemmaWgt-lemmaTitle-title\"]/h1/text()[normalize-space()]").extract()[0]
        items['url'] = response.url
        items['keywords'] = set(selector.xpath(
            "//div[@class=\"main-content\"]//div[@class=\"para\"]//a[@target=\"_blank\"]/text()[normalize-space()]").extract())
        items['description'] = ''.join(
            selector.xpath(
                "//div[@class=\"main-content\"]//div[@class=\"para\"]//text()[normalize-space()]|//div[@class=\"main-content\"]//div[@label-module=\"para-title\"]//h2/text()[normalize-space()]").extract()).replace(
            "\n", "")
        items['embed_image_url'] = selector.xpath("//div[@class=\"para\"]//a[@class=\"image-link\"]//@data-src").extract()
        print(items['url'])
