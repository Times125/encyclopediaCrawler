# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
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
            key = "{}:{}".format(spider.name, 'task_failed_queue')
            value = request.url
            self.handle.lpush(key, value)
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and not request.meta.get('dont_retry', False):
            key = "{}:{}".format(spider.name, 'task_failed_queue')
            value = request.url
            self.handle.lpush(key, value)
            return self._retry(request, exception, spider)
