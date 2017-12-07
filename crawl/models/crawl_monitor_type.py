# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, SmallInteger, DECIMAL, Date
from crawl.models.util import Base

class MonitorType(Base):
    __tablename__ = 'crawl_monitor_type'

    id = Column(Integer, primary_key=True)
    monitor_name = Column(String(32))
    province = Column(String(32))
    rate = Column(String(6))
    type_name = Column(String(3))
    catname = Column(String(5))
    day = Column(DateTime)
    site = Column(String(32))
    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())