# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, func, Index, Date, BIGINT, SmallInteger
from crawl.models.util import Base

class LianjiaFeedback(Base):
    __tablename__ = 'crawl_lianjia_feedback'

    id = Column(Integer, primary_key=True)
    agent_id = Column(BIGINT)
    comment = Column(String(512))
    hourse_id = Column(BIGINT)
    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())