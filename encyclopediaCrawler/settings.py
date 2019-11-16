# -*- coding: utf-8 -*-
# Scrapy settings for encyclopediaCrawler project

# scrapy basic settings
BOT_NAME = 'encyclopediaCrawler'
SPIDER_MODULES = ['encyclopediaCrawler.spiders']
NEWSPIDER_MODULE = 'encyclopediaCrawler.spiders'

# downloader settings
ROBOTSTXT_OBEY = False
COOKIES_ENABLED = False
RETRY_ENABLED = True
DOWNLOAD_TIMEOUT = 30
FEED_EXPORT_ENCODING = 'utf-8'  # 中文转码
LOG_LEVEL = 'INFO'
RETRY_TIMES = 0
RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 408]

DEPTH_PRIORITY = 1

CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS = 8
DOWNLOAD_DELAY = 10

DOWNLOADER_MIDDLEWARES = {
    'encyclopediaCrawler.middlewares.MyUserAgentMiddleware': 400,
    # 'encyclopediaCrawler.middlewares.MyRetryMiddleware': 501
}

ITEM_PIPELINES = {
    'encyclopediaCrawler.pipelines.SpiderPipeline': 300,
    'encyclopediaCrawler.pipelines.SpiderRedisPipeline': 301,
}
