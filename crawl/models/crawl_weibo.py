# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, SmallInteger
from crawl.models.util import Base

class Crawl_Weibo(Base):
    """微信新闻类"""
    __tablename__ = 'crawl_weibo'

    id = Column(Integer, primary_key=True)
    pub_time = Column(DateTime, nullable=True)
    content = Column(Text, nullable=True)
    author_name = Column(String(32))
    author_link = Column(String(256))
    author_img = Column(String(256))
    source_url = Column(String(32))
    source_id = Column(String(32))
    images = Column(Text)

    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())