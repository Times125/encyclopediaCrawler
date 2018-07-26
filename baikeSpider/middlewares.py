# -*- coding: utf-8 -*-

import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
from .settings import PROXY_IP, PROXY_PORT

from .db.basic import get_redis_conn


class MyUserAgentMiddleware(UserAgentMiddleware):
    '''
    设置User-Agent
    '''

    def __init__(self, user_agent):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user_agent=crawler.settings.get('MY_USER_AGENT')
        )

    def process_request(self, request, spider):
        agent = random.sample(self.user_agent, 1)[0]
        # print('===>', agent)
        request.headers['User-Agent'] = agent


class MyRetryMiddleware(RetryMiddleware):
    """ 重试失败则将url放到失败任务队列 """
    handle = get_redis_conn()

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            key = "{}:{}".format('task_failed_queue', spider.name)
            value = request.url
            self.handle.lpush(key, value)
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and not request.meta.get('dont_retry', False):
            key = "{}:{}".format('task_failed_queue', spider.name)
            value = request.url
            self.handle.lpush(key, value)
            return self._retry(request, exception, spider)


# 代理
class MyProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        # 设置代理的主机和端口号
        request.meta['proxy'] = "http://{}:{}".format(PROXY_IP, PROXY_PORT)
        # # 设置代理的认证用户名和密码
        # proxy_user_pass = ""
        # encoded_user_pass = base64.encodebytes(proxy_user_pass)
        #
        # # 设置代理
        # request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
