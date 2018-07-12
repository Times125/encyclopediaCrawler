"""
@Author:lichunhui
@Time:   
@Description: 
"""
from .basic import db_session
from sqlalchemy.exc import IntegrityError as SqlalchemyIntegrityError, InternalError
from pymysql.err import IntegrityError as PymysqlIntegrityError
from sqlalchemy.exc import InvalidRequestError


class CommandOperate:
    @classmethod
    def add_one(cls, data):
        try:
            db_session.add(data)
            db_session.commit()
        except (InternalError, SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError) as e:
            print('=============>', e, "<===============")
            db_session.rollback()

    @classmethod
    def add_all(cls, datas):
        try:
            db_session.add_all(datas)
            db_session.commit()
        except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError):
            for data in datas:
                cls.add_one(data)
