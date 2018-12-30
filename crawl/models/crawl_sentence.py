# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, Date
from crawl.models.util import Base

class Sentence(Base):
    __tablename__ = 'crawl_sentence'

    id = Column(Integer, primary_key=True)
    content = Column(String(64))
    source_id = Column(String(32))
    favor = Column(Integer, default=0)

    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())