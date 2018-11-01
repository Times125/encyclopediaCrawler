"""
@Author:lichunhui
@Time:   
@Description: 
"""
from .basic import Base
from .tables import (baidu, baike, wiki_zh, wiki_en)

__all__ = ['BaiduItemData', 'BaikeItemData', 'WikiENItemData', 'WikiZHItemData']


class BaiduItemData(Base):
    __table__ = baidu


class BaikeItemData(Base):
    __table__ = baike


class WikiZHItemData(Base):
    __table__ = wiki_zh


class WikiENItemData(Base):
    __table__ = wiki_en
