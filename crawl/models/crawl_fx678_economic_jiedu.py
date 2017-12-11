# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, SmallInteger, DECIMAL, Date
from crawl.models.util import Base

class CrawlFx678EconomicJiedu(Base):
    __tablename__ = 'crawl_fx678_economic_jiedu'

    dataname_id = Column(Integer, primary_key=True)
    next_pub_time = Column(String(64))
    pub_agent = Column(String(64))
    pub_frequency = Column(String(64))
    count_way = Column(String(64))
    data_influence = Column(String(512))
    data_define = Column(String(512))
    funny_read = Column(String(512))
    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())