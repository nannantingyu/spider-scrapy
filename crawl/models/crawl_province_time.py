# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, SmallInteger, DECIMAL, Date
from crawl.models.util import Base

class ProvinceTime(Base):
    __tablename__ = 'crawl_province_time'

    id = Column(Integer, primary_key=True)
    province_name = Column(String(32))
    value = Column(String(6))
    type = Column(String(5))
    day = Column(DateTime)
    site = Column(String(32))
    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())