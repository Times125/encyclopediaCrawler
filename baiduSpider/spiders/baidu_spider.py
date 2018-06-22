"""
@Author:lichunhui
@Time:   
@Description: 百度百科爬虫
"""
import re
from urllib.parse import unquote
from filters.bloom_filter import BloomFilter
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from baiduSpider.items import BaiduspiderItem
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider


class baiduSpider(CrawlSpider):
    base_url = "https://baike.baidu.com"
    name = 'baiduSpider'
    allowed_domains = ['baike.baidu.com']
    start_urls = ['https://baike.baidu.com/item/英国跳猎犬']
    # redis_key = 'baiduSpider:start_urls'
    rules = (
        Rule(LinkExtractor(allow=('https://baike.baidu.com/item/')), callback='parse', follow=True),
    )
    """
    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(baiduSpider, self).__init__(*args, **kwargs)
    """

    def parse(self, response):
        items = BaiduspiderItem()
        selector = Selector(response)
        items['url'] = unquote(response.url)

        title = selector.xpath("/html/head/title/text()").extract()
        if len(title) != 0:
            items['title'] = title[0].strip().encode('utf-8', errors='ignore').decode('utf-8')
        else:
            items['title'] = 'none'
        summary = selector.xpath("//div[@class=\"lemma-summary\"]").xpath("string(.)").extract()
        if len(summary) != 0:
            tmps = summary[0].encode('utf-8', errors='ignore').decode('utf-8')
            items['summary'] = re.sub('\r\n|\n|\r', ' ', tmps)
        else:
            items['summary'] = 'none'

        catalog = selector.xpath("//div[@class=\"lemmaWgt-lemmaCatalog\"]").xpath("string(.)").extract()
        if len(catalog) != 0:
            tmpc = catalog[0].encode('utf-8', errors='ignore').decode('utf-8')
            items['catalog'] = re.sub('\r\n|\n|\r', ' ', tmpc)
        else:
            items['catalog'] = 'none'

        # 进行迭代抓取的item链接
        urls = [unquote(item) for item in
                selector.xpath("//div[@class=\"para\"]//a[@target=\"_blank\"]/@href").extract()]
        items['keywords_url'] = list(set(filter(lambda x: 'item' in x, urls)))

        description = selector.xpath("//div[@class=\"content-wrapper\"]").xpath("string(.)").extract()
        if len(description) != 0:
            tmpd = description[0].encode('utf-8', errors='ignore').decode('utf-8')
            items['description'] = re.sub('\r\n|\n|\r', ' ', tmpd)
        else:
            items['description'] = 'none'

        embed_image_url = selector.xpath("//div[@class=\"para\"]//a[@class=\"image-link\"]//@data-src").extract()
        if len(embed_image_url) != 0:
            items['embed_image_url'] = ','.join(embed_image_url)
        else:
            items['embed_image_url'] = 'none'

        album_pic_url = selector.xpath("//div[@class=\"album-list\"]//a[@class=\"more-link\"]/@href").extract()
        if len(album_pic_url) != 0:
            items['album_pic_url'] = self.base_url + unquote(album_pic_url[0])
        else:
            items['album_pic_url'] = 'none'

        update_time = selector.xpath("//span[@class = 'j-modified-time']").xpath("string(.)").extract()
        if len(update_time) != 0:
            tmpu = update_time[0].strip().encode('utf-8', errors='ignore').decode('utf-8')
            items['update_time'] = re.sub('\r\n|\n|\r', ' ', tmpu)
        else:
            items['update_time'] = 'none'

        reference_material = selector.xpath(
            "//dl[@class ='lemma-reference collapse nslog-area log-set-param']").xpath("string(.)").extract()
        if len(reference_material) != 0:
            tmpr = reference_material[0].encode('utf-8', errors='ignore').decode('utf-8')
            items['reference_material'] = re.sub('\r\n|\n|\r', ' ', tmpr)
        else:
            items['reference_material'] = 'none'

        item_tag = selector.xpath("//dd[@id = \"open-tag-item\"]").xpath("string(.)").extract()
        if len(item_tag) != 0:
            tmpi = item_tag[0].encode('utf-8', errors='ignore').decode('utf-8')
            items['item_tag'] = re.sub('\r\n|\n|\r', ' ', tmpi)
        else:
            items['item_tag'] = 'none'
        # 布隆过滤器过滤已经下载的词条
        # urls = [u for u in items['keywords_url'] if BloomFilter().is_contain(u) is False]
        old_urls = items['keywords_url']
        print(old_urls)
        yield items
        for i in old_urls:
            new_url = self.base_url + i
            yield Request(new_url, callback=self.parse)
