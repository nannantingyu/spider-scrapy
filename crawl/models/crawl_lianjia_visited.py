# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, func, Index, Date, BIGINT, SmallInteger
from crawl.models.util import Base

class LianjiaVisited(Base):
    __tablename__ = 'crawl_lianjia_visited'

    id = Column(Integer, primary_key=True)
    agent_id = Column(BIGINT)
    visited_time = Column(Date)
    build_type = Column(String(16))
    hourse_id = Column(BIGINT)
    see_count = Column(Integer)
    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())