# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, SmallInteger, DECIMAL, Date
from crawl.models.util import Base

class CrawlWeixinArticleDetail(Base):
    __tablename__ = 'crawl_weixin_article_detail'

    id = Column(Integer, primary_key=True)
    body = Column(Text(32))
    key_state = Column(SmallInteger, default=0)

    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())