"""
@Author:lichunhui
@Time:   
@Description: 爬虫配置文件，与scrapy 配置文件settings区分开来，对爬虫的一些个性化设置在此文件中，scrapy设置在settings文件中；
"""
import os
import yaml

__all__ = ['db_args', 'redis_args', 'logger_args', 'spider_args']

yaml_path = os.path.join(os.path.dirname(__file__), 'common_config.yaml')

with open(yaml_path, encoding='utf-8') as f:
    yaml_cont = f.read()

cf = yaml.load(yaml_cont, Loader=yaml.SafeLoader)

db_args = cf.get('mysql')
redis_args = cf.get('redis')
logger_args = cf.get('logger')
spider_args = cf.get('spider')
