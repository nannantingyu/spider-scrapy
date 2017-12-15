# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, SmallInteger, DECIMAL, Date
from crawl.models.util import Base

class CrawlArticle(Base):
    __tablename__ = 'crawl_article'

    id = Column(Integer, primary_key=True)
    title = Column(String(128))
    body = Column(Text(32))
    publish_time = Column(DateTime)
    author = Column(String(32))
    description = Column(String(512))
    image = Column(String(512))
    type = Column(String(32))
    keywords = Column(String(128))
    author = Column(String(25))
    source_id = Column(String(64))
    source_url = Column(String(512))
    source_site = Column(String(32))

    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())