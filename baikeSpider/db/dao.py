"""
@Author:lichunhui
@Time:   
@Description: 
"""

from sqlalchemy.exc import IntegrityError as SqlalchemyIntegrityError, InternalError
from pymysql.err import IntegrityError as PymysqlIntegrityError
from sqlalchemy.exc import InvalidRequestError

from ..logger import db_logger
from .basic import get_db_session

__all__ = ['CommandOperate']


class CommandOperate:
    @classmethod
    def add_one(cls, data):
        with get_db_session() as db_session:
            try:
                db_session.add(data)
                db_session.commit()
            except (InternalError, SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError) as e:
                db_session.rollback()
                db_logger.error("exception '{}' happened when add data".format(e))

    @classmethod
    def add_all(cls, datas):
        with get_db_session() as db_session:
            try:
                db_session.add_all(datas)
                db_session.commit()
            except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError):
                for data in datas:
                    cls.add_one(data)
