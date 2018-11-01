#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:lichunhui
@Time:  2018/7/25 22:15
@Description: 启动所有爬虫
"""
from scrapy.commands import ScrapyCommand

__all__ = ['Command']


class Command(ScrapyCommand):
    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Runs all of the spiders'

    def run(self, args, opts):
        spider_list = self.crawler_process.spiders.list()
        for name in spider_list:
            self.crawler_process.crawl(name, **opts.__dict__)
        self.crawler_process.start()
