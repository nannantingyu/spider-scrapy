# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, SmallInteger, DECIMAL, Date
from crawl.models.util import Base

class CrawlFx678EconomicHoliday(Base):
    __tablename__ = 'crawl_fx678_economic_holiday'

    id = Column(Integer, primary_key=True)
    country = Column(String(64))
    time = Column(String(512))
    market = Column(String(32))
    holiday_name = Column(String(24))
    detail = Column(String(32))
    date = Column(Date)
    source_id = Column(String(32))
    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())