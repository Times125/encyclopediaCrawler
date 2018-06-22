"""
@Author:lichunhui
@Time:   
@Description: 
"""
from sqlalchemy import create_engine, MetaData
from baiduSpider.config.conf import get_mysql_args
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


def get_engine():
    args = get_mysql_args()
    """数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名"""
    connect_str = "{}+pymysql://{}:{}@{}:{}/{}?charset={}".format(args['db_type'], args['user'],
                                                                  args['password'], args['host'],
                                                                  args['port'], args['database'],
                                                                  args['charset'])
    print(connect_str)
    egine = create_engine(connect_str, encoding="utf-8", pool_size=10, echo=True)
    return egine


engine = get_engine()
Session = sessionmaker(bind=engine)
Base = declarative_base()
db_session = Session()

__all__ = ['engine', 'Base', 'db_session']
