"""
@Author:lichunhui
@Time:   
@Description: 百度百科爬虫
"""
from scrapy.shell import inspect_response
from scrapy.spiders import Spider, CrawlSpider
from scrapy.selector import Selector

from baiduSpider.items import BaiduspiderItem


class baiduSpider(Spider):
    base_url = "https://baike.baidu.com"
    name = 'baiduSpider'
    allowed_domains = ['baike.baidu.com']
    start_urls = ['https://baike.baidu.com/item/英国跳猎犬']

    def parse(self, response):
        items = BaiduspiderItem()
        selector = Selector(response)
        items['name'] = selector.xpath("//dd[@class=\"lemmaWgt-lemmaTitle-title\"]/h1/text()").extract()[0].encode('utf-8')
        items['url'] = response.url.encode('utf-8')
        items['summary'] = selector.select("//div[@class=\"lemma-summary\"]").xpath("string(.)").extract()[0]
        items['catalog'] = selector.select("//div[@class=\"lemmaWgt-lemmaCatalog\"]").xpath("string(.)").extract()[0]
        items['keywords'] = set(selector.xpath("//div[@class=\"para\"]//a[@target=\"_blank\"]/text()[normalize-space()]").extract())
        items['description'] = selector.select("//div[@class=\"content-wrapper\"]").xpath("string(.)").extract()[0].encode('utf-8')
        items['embed_image_url'] = selector.xpath("//div[@class=\"para\"]//a[@class=\"image-link\"]//@data-src").extract()
        items['album_pic_url'] = self.base_url + selector.xpath("//div[@class=\"album-list\"]//a[@class=\"more-link\"]/@href").extract()[0]
        items['update_time'] = selector.select("//span[@class = 'j-modified-time']").xpath("string(.)").extract()[0].encode('utf-8')
        items['reference_material'] = selector.select("//dl[@class ='lemma-reference collapse nslog-area log-set-param']").xpath("string(.)").extract()[0].encode('utf-8')
        items['item_tag'] = selector.select("//dd[@id = \"open-tag-item\"]").xpath("string(.)").extract()[0]
        print(items['item_tag'])
