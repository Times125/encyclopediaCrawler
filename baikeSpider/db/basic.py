"""
@Author:lichunhui
@Time:   
@Description: 
"""
import redis
from sqlalchemy import create_engine, MetaData
from ..config.conf import get_mysql_args, get_redis_args
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pymysql.err import OperationalError
from ..utils.log import logger


# 获取redis连接
def get_redis_conn():
    redis_args = get_redis_args()
    host = redis_args['host']
    port = redis_args['port']
    pool = redis.ConnectionPool(host=host, port=port)
    handle = redis.StrictRedis(connection_pool=pool, charset='utf-8')
    return handle


# 获取mysql引擎
def get_engine():
    try:
        args = get_mysql_args()
        """数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名"""
        connect_str = "{}+pymysql://{}:{}@{}:{}/{}?charset={}".format(args['db_type'], args['user'], args['password'],
                                                                      args['host'], args['port'], args['database'],
                                                                      args['charset'])
        print(connect_str)
        egine = create_engine(connect_str, encoding="utf-8", pool_size=10, echo=False)
        return egine
    except OperationalError as e:
        logger.error(e)
        print(e)


engine = get_engine()
Session = sessionmaker(bind=engine)
Base = declarative_base()
db_session = Session()

__all__ = ['engine', 'Base', 'db_session']
