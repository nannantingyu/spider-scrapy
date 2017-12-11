# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, SmallInteger, DECIMAL, Date
from crawl.models.util import Base

class BaiduRate(Base):
    __tablename__ = 'crawl_baidu_rate'

    id = Column(Integer, primary_key=True)
    show_count = Column(String(12))
    clk_count = Column(String(12))
    cost_count = Column(String(12))
    ctr = Column(String(12))
    cpm = Column(String(12))
    pv_count = Column(String(12))
    visit_count = Column(String(12))
    visitor_count = Column(String(12))
    new_visitor_count = Column(String(12))
    new_visitor_ratio = Column(String(12))
    in_visit_count = Column(String(12))
    bounce_ratio = Column(String(12))
    avg_visit_time = Column(String(12))
    avg_visit_pages = Column(String(12))
    arrival_ratio = Column(String(12))
    trans_count = Column(String(12))
    trans_ratio = Column(String(12))
    avg_trans_cost = Column(String(12))
    income = Column(String(12))
    profit = Column(String(12))
    roi = Column(String(12))
    ctime = Column(DateTime)
    site = Column(String(32))
    source_id = Column(String(32))
    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())