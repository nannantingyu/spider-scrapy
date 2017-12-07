# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, SmallInteger, DECIMAL, Date
from crawl.models.util import Base

class BaiduTongji(Base):
    __tablename__ = 'crawl_baidu_tongji'

    id = Column(Integer, primary_key=True)
    access_time = Column(DateTime)
    area = Column(String(64))
    keywords = Column(String(64))
    entry_page = Column(String(512))
    ip = Column(String(15))
    user_id = Column(String(32))
    visit_time = Column(String(32))
    visit_pages = Column(Integer)
    visitorType = Column(String(16))
    visitorFrequency = Column(Integer)
    lastVisitTime = Column(DateTime)
    endPage = Column(String(255))
    deviceType = Column(String(16))
    fromType = Column(String(255))
    fromurl = Column(String(255))
    fromAccount = Column(String(255))
    isp = Column(String(255))
    os = Column(String(255))
    osType = Column(String(32))
    browser = Column(String(64))
    browserType = Column(String(64))
    language = Column(String(64))
    resolution = Column(String(32))
    color = Column(String(32))
    accessPage = Column(String(255))
    antiCode = Column(String(32))
    site = Column(String(64))
    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())