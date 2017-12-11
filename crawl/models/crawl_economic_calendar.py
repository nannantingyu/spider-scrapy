# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, SmallInteger, DECIMAL, Date
from crawl.models.util import Base

class CrawlEconomicCalendar(Base):
    __tablename__ = 'crawl_economic_calendar'

    id = Column(Integer, primary_key=True)
    country = Column(String(64))
    quota_name = Column(String(512))
    pub_time = Column(String(32))
    importance = Column(String(24))
    former_value = Column(String(32))
    predicted_value = Column(String(32))
    published_value = Column(String(32))
    influence = Column(String(64))
    source_id = Column(Integer)
    dataname = Column(String(256))
    datename = Column(String(64))
    dataname_id = Column(Integer)
    unit = Column(String(32))
    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())