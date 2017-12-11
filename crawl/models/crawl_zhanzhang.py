# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, SmallInteger, DECIMAL, Date
from crawl.models.util import Base

class CrawlZhanzhang(Base):
    __tablename__ = 'crawl_zhanzhang'

    id = Column(Integer, primary_key=True)
    keywords = Column(String(128))
    total_index = Column(String(32))
    pc_index = Column(String(32))
    mobile_index = Column(String(32))
    baidu_index = Column(String(32))
    shoulu_count = Column(String(64))
    shoulu_page = Column(String(512))
    shoulu_title = Column(String(256))
    site = Column(String(32))
    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())