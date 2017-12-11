# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, func, Index, Date, BIGINT, SmallInteger
from crawl.models.util import Base

class LianjiaAgent(Base):
    __tablename__ = 'crawl_lianjia_agent'

    id = Column(Integer, primary_key=True)
    name = Column(String(16))
    agent_id = Column(BIGINT)
    reason = Column(String(128))
    agent_url = Column(String(256))
    agent_level = Column(String(64))
    agent_photo = Column(String(256))
    feedback_good_rate = Column(SmallInteger)
    comment_count = Column(Integer)
    total_comment_score = Column(String(5))
    agent_phone = Column(String(32))
    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())