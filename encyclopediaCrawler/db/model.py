"""
@Author:lichunhui
@Time:   
@Description: 
"""
import json
from .basic import Base
from ..config import db_args
from .tables import (encyclopedia, encyclopedia_expand)

__all__ = ['EncyclopediaItemData', 'EncyclopediaItemDataExpand']


class BaseInfo:
    __table_args__ = {
        'mysql_charset': db_args['db_charset'],
        'mysql_engine': db_args['db_engine'],
    }


class EncyclopediaItemData(BaseInfo, Base):
    __table__ = encyclopedia


class EncyclopediaItemDataExpand(BaseInfo, Base):
    __table__ = encyclopedia_expand
