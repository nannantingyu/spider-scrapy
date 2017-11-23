# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, func, Index, Date, BIGINT, SmallInteger
from crawl.models.util import Base

class LianjiaResidential(Base):
    __tablename__ = 'crawl_lianjia_residential'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    build_year = Column(String(16))
    build_num = Column(String(16))
    build_type = Column(String(16))
    residential_id = Column(BIGINT)
    unit_price = Column(Integer)
    sell_num = Column(Integer)
    rent_num = Column(Integer)
    longitude = Column(Float)
    latitude = Column(Float)
    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())