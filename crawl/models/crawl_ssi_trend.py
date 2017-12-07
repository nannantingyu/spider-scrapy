# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, SmallInteger, DECIMAL, Date
from crawl.models.util import Base

class CrawlSsiTrend(Base):
    __tablename__ = 'crawl_jin10_ssi_trends'

    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    platform = Column(String(32))
    type = Column(String(32))
    long_position = Column(DECIMAL)

    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())