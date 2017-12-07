# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, Date
from crawl.models.util import Base

class Cgse(Base):
    __tablename__ = 'crawl_cgse'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    idr = Column(Integer)
    executive_manager = Column(String(64))
    executive_manager_ex = Column(String(64))
    register_number = Column(String(32))
    company_number = Column(String(32))
    business_status = Column(String(32))
    registe_address = Column(String(128))
    website = Column(String(356))
    tel = Column(String(32))
    fax = Column(String(32))

    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())