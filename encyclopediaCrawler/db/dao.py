"""
@Author:lichunhui
@Time:   
@Description: 
"""
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError as SqlalchemyIntegrityError, InternalError, IntegrityError
from pymysql.err import IntegrityError as PymysqlIntegrityError
from sqlalchemy.exc import InvalidRequestError
from .model import (EncyclopediaItemDataExpand, EncyclopediaItemData)
from ..logger import db_logger
from .basic import get_db_session

__all__ = ['CommandOperate']


class CommandOperate:
    @classmethod
    def add_one(cls, data):
        res = 0
        with get_db_session() as db_session:
            try:
                db_session.add(data)
                db_session.commit()
                res = 1
                return res
            except (InternalError, SqlalchemyIntegrityError, PymysqlIntegrityError) as e:
                db_session.rollback()
                db_logger.error("exception '{}' happened when add data".format(e))
                return res

    @classmethod
    def add_batches(cls, datas):
        with get_db_session() as db_session:
            try:
                db_session.add_all(datas)
                db_session.commit()
            except (SqlalchemyIntegrityError, InvalidRequestError) as e:
                print("exception '{}' happened when add all data".format(e))
                db_logger.error("exception '{}' happened when add all data".format(e))
                db_session.rollback()
                for data in datas:
                    cls.add_one(data)
            except Exception as e:
                print("exception '{}' happened when query data".format(e))

    @classmethod
    def query(cls, name, rk_time):
        with get_db_session() as db_session:
            try:
                res = db_session.query(EncyclopediaItemData).filter(
                    and_(EncyclopediaItemData.name == name, EncyclopediaItemData.fetch_time == rk_time)).first()
                db_session.commit()
                return res
            except (InternalError, SqlalchemyIntegrityError, PymysqlIntegrityError) as e:
                db_session.rollback()
                db_logger.error("exception '{}' happened when query data".format(e))
                return None