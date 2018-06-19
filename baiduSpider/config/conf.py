"""
@Author:lichunhui
@Time:   
@Description: config file in project
"""
from scrapy.utils.project import get_project_settings


# mysql config
def get_mysql_args():
    mysql_args = dict()
    mysql_args['db_type'] = get_project_settings().get('DB_TYPE')
    mysql_args['host'] = get_project_settings().get('MYSQL_HOST')
    mysql_args['port'] = get_project_settings().get('MYSQL_PORT')
    mysql_args['user'] = get_project_settings().get('MYSQL_USER')
    mysql_args['password'] = get_project_settings().get('MYSQL_PWD')
    mysql_args['database'] = get_project_settings().get('MYSQL_DB')
    mysql_args['charset'] = get_project_settings().get('MYSQL_CHARSET')
    return mysql_args


# redis config
def get_redis_args():
    redis_args = dict()
    redis_args['host'] = get_project_settings().get('REDIS_HOST')
    redis_args['port'] = get_project_settings().get('REDIS_PORT')
    return redis_args


# bloom filter config
def get_bloom_args():
    bloom_args = dict()
    bloom_args['hash_list'] = get_project_settings().get('BLOOM_HASH_LIST')
    bloom_args['key'] = get_project_settings().get('BLOOM_REDIS_KEY')
    return bloom_args
