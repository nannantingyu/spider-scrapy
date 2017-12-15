# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, SmallInteger
from crawl.models.util import Base

class Crawl_keywords_map(Base):
    """文章关键词分类"""
    __tablename__ = 'crawl_keywords_map'

    id = Column(Integer, primary_key=True)
    keyword = Column(String(12))
    s_id = Column(Integer)
    tb = Column(String(32))

    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())