# -*- coding: utf-8 -*-

import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
from .config import spider_args
from .db import get_redis_conn
from .utils import FakeChromeUA


class MyUserAgentMiddleware(UserAgentMiddleware):
    """
    设置User-Agent
    """

    def process_request(self, request, spider):
        request.headers['User-Agent'] = FakeChromeUA.get_ua()


class MyRetryMiddleware(RetryMiddleware):
    """ 重试失败则将url放到失败任务队列 """
    redis_conn = get_redis_conn()
    redis_handler = redis_conn.sadd if spider_args['use_set'] else redis_conn.lpush

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            key = "{}:{}".format('encyclopedia:failed:queue', spider.name)
            value = request.url
            self.redis_handler(key, value)
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and not request.meta.get('dont_retry', False):
            key = "{}:{}".format('encyclopedia:failed:queue', spider.name)
            value = request.url
            self.redis_handler(key, value)
            return self._retry(request, exception, spider)


# 代理
class MyProxyMiddleware(object):
    def process_request(self, request, spider):
        if not hasattr(spider, 'proxy_mode') or not spider.proxy_mode:
            return
        if spider.proxy_mode == 0:
            pass
        if spider.proxy_mode == 1:
            # 设置代理的主机和端口号
            request.meta['proxy'] = random.choice(spider_args['http_proxies'])
