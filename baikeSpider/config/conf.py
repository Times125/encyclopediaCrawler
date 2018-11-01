"""
@Author:lichunhui
@Time:   
@Description: 爬虫配置文件，与scrapy 配置文件settings区分开来，对爬虫的一些个性化设置在此文件中，scrapy设置在settings文件中；
"""

# mysql database settings
db_host = '127.0.0.1'
db_port = 3306
db_user = 'root'
db_pwd = ''
db_name = 'test'
db_charset = 'utf8mb4'
db_type = 'mysql'

# redis settings
redis_host = '127.0.0.1'
redis_port = 6379
redis_pwd = ''

# common redis db for scheduler and other modules.
common_db = 1

# bloom filter settings
bloomfilter_db = 1

# 日志缓存目录
log_dir = "logs_dir"
log_name = "baike.log"

# 爬虫要抓取的任务队列
baidu_task_queue = 'task_queue.baidu_spider'
baike_task_queue = 'task_queue.baike_spider'
wiki_zh_task_queue = 'task_queue.wiki_zh_spider'
wiki_en_task_queue = 'task_queue.wiki_en_spider'

# 爬虫名字
baidu_spider_name = "baidu_spider"
baike_spider_name = "baike_spider"
wiki_zh_spider_name = "wiki_zh_spider"
wiki_en_spider_name = "wiki_en_spider"

# 爬虫已爬词条布隆过滤器
baidu_bloom_key = 'bloomfilter.baidu_spider'
baike_bloom_key = 'bloomfilter.baike_spider'
wiki_zh_bloom_key = 'bloomfilter.wiki_zh_spider'
wiki_en_bloom_key = 'bloomfilter.wiki_en_spider'

# 布隆过滤器block数量
filter_blocks = 2
