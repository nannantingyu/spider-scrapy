# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, Date
from crawl.models.util import Base

class ChinaTime(Base):
    __tablename__ = 'crawl_china_time'

    id = Column(Integer, primary_key=True)
    value = Column(String(10))
    type = Column(String(10))
    day = Column(DateTime)
    site = Column(String(32))
    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())