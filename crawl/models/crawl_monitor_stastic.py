# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, SmallInteger, DECIMAL, Date
from crawl.models.util import Base

class MonitorStastic(Base):
    __tablename__ = 'crawl_monitor_stastic'

    id = Column(Integer, primary_key=True)
    mid = Column(Integer)
    day = Column(DateTime)
    min = Column(DECIMAL)
    max = Column(DECIMAL)
    avg = Column(DECIMAL)
    time_st = Column(String(10))
    all_time = Column(Integer)
    site = Column(String(32))
    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())