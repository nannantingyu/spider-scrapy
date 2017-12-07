# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, SmallInteger, DECIMAL, Date
from crawl.models.util import Base

class CrawlSsiTrend_alpari(Base):
    __tablename__ = 'crawl_jin10_ssi_trends_alpari'

    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    platform = Column(String(32))
    type = Column(String(32))
    long_position = Column(DECIMAL)

    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())

class CrawlSsiTrend_dukscopy(Base):
    __tablename__ = 'crawl_jin10_ssi_trends_dukscopy'

    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    platform = Column(String(32))
    type = Column(String(32))
    long_position = Column(DECIMAL)

    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())

class CrawlSsiTrend_fiboforx(Base):
    __tablename__ = 'crawl_jin10_ssi_trends_fiboforx'

    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    platform = Column(String(32))
    type = Column(String(32))
    long_position = Column(DECIMAL)

    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())

class CrawlSsiTrend_forxfact(Base):
    __tablename__ = 'crawl_jin10_ssi_trends_forxfact'

    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    platform = Column(String(32))
    type = Column(String(32))
    long_position = Column(DECIMAL)

    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())

class CrawlSsiTrend_ftroanda(Base):
    __tablename__ = 'crawl_jin10_ssi_trends_ftroanda'

    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    platform = Column(String(32))
    type = Column(String(32))
    long_position = Column(DECIMAL)

    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())

class CrawlSsiTrend_fxcm(Base):
    __tablename__ = 'crawl_jin10_ssi_trends_fxcm'

    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    platform = Column(String(32))
    type = Column(String(32))
    long_position = Column(DECIMAL)

    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())

class CrawlSsiTrend_instfor(Base):
    __tablename__ = 'crawl_jin10_ssi_trends_instfor'

    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    platform = Column(String(32))
    type = Column(String(32))
    long_position = Column(DECIMAL)

    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())

class CrawlSsiTrend_myfxbook(Base):
    __tablename__ = 'crawl_jin10_ssi_trends_myfxbook'

    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    platform = Column(String(32))
    type = Column(String(32))
    long_position = Column(DECIMAL)

    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())

class CrawlSsiTrend_saxobank(Base):
    __tablename__ = 'crawl_jin10_ssi_trends_saxobank'

    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    platform = Column(String(32))
    type = Column(String(32))
    long_position = Column(DECIMAL)

    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())