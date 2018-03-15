# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, SmallInteger
from crawl.models.util import Base

class Crawl_Cryptomiso(Base):
    """微信新闻类"""
    __tablename__ = 'crawl_cryptomiso'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=True)
    rank = Column(Integer)
    commit = Column(Integer)

    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())