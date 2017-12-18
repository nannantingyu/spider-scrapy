# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, SmallInteger
from crawl.models.util import Base

class Crawl_Weixin_Search(Base):
    """微信新闻类"""
    __tablename__ = 'crawl_weixin_article'

    id = Column(Integer, primary_key=True)
    publish_time = Column(DateTime, nullable=True)
    title = Column(String(255), nullable=True)
    description = Column(String(512), nullable=True)
    favor = Column(Integer, nullable=True, default=0)
    disfavor = Column(Integer, nullable=True, default=0)
    type = Column(String(64), nullable=True)
    state = Column(SmallInteger, nullable=True, default=0)
    image = Column(String(255), nullable=True)
    source_url = Column(String(255))
    source_id = Column(String(50))
    author = Column(String(64))
    hits = Column(Integer)
    key_state = Column(SmallInteger, default=0)

    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())