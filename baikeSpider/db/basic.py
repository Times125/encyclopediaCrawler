"""
@Author:lichunhui
@Time:   
@Description: 
"""
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import (sessionmaker, scoped_session)
from sqlalchemy.ext.declarative import declarative_base
from pymysql.err import OperationalError
from contextlib import contextmanager
from ..logger import db_logger
from ..config import (db_host, db_port, db_name,
                      db_pwd, db_user,
                      db_type, db_charset)

__all__ = ['metadata', 'Base', 'get_db_session', 'create_db']


# 获取mysql引擎
def get_engine():
    try:

        """数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名"""
        connect_str = "{}+pymysql://{}:{}@{}:{}/{}?charset={}".format(db_type, db_user, db_pwd,
                                                                      db_host, db_port, db_name,
                                                                      db_charset)
        print(connect_str)
        egine = create_engine(connect_str, encoding="utf-8", pool_size=10, echo=False, pool_recycle=7200)
        return egine
    except OperationalError as e:
        db_logger.error(e)


def create_db():
    connect_str = "{}+pymysql://{}:{}@{}:{}".format(db_type, db_user, db_pwd,
                                                    db_host, db_port, db_charset)
    mysql_engine = create_engine(connect_str, echo=True)
    sql_str = "CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARSET utf8mb4;".format(db_name)
    mysql_engine.execute(sql_str)


engine = get_engine()
Base = declarative_base()
metadata = MetaData(engine)
session_factory = sessionmaker(bind=engine, expire_on_commit=False)
Session = scoped_session(session_factory)


@contextmanager
def get_db_session():
    try:
        db_session = Session()
        try:
            yield db_session
        finally:
            db_session.close()
    except Exception as e:
        db_logger.error("get database session error {}".format(e))
