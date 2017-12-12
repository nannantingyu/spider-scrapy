# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, SmallInteger
from crawl.models.util import Base

class Crawl_Weibo_Hotkey(Base):
    """微信新闻类"""
    __tablename__ = 'crawl_baidu_hotkey'

    id = Column(Integer, primary_key=True)
    time = Column(DateTime, nullable=True)
    keyword = Column(String(64), nullable=True)
    order = Column(SmallInteger)
    state = Column(SmallInteger, default=1)

    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())