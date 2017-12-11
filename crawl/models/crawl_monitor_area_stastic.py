# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, SmallInteger, Date
from crawl.models.util import Base

class MonitorAreaStastic(Base):
    __tablename__ = 'crawl_monitor_area_stastic'

    id = Column(Integer, primary_key=True)
    monitor_name = Column(String(32))
    type = Column(String(5))
    province = Column(String(32))
    area = Column(String(10))
    mid = Column(Integer)
    day = Column(DateTime)
    site = Column(String(32))
    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())