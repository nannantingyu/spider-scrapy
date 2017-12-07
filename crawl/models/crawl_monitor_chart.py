# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, SmallInteger, Date
from crawl.models.util import Base

class MonitorChart(Base):
    __tablename__ = 'crawl_monitor_chart'

    id = Column(Integer, primary_key=True)
    monitor_name = Column(String(32))
    time = Column(DateTime)
    value = Column(String(10))
    type = Column(String(5))
    day = Column(DateTime)
    site = Column(String(32))
    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())