# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, Date, SmallInteger
from crawl.models.util import Base

class CrawlAnjukeResidential(Base):
    __tablename__ = 'crawl_anjuke_residential'

    id = Column(Integer, primary_key=True)
    residential = Column(String(64))
    residential_id = Column(Integer)
    residential_url = Column(String(256))
    build_year = Column(SmallInteger)
    area = Column(String(32))

    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())