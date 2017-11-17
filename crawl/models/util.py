# -*- encoding: utf-8 -*-
"""
定义数据库模型实体
"""

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from crawl.settings import DATABASE

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**DATABASE), echo=False)

def create_news_table(engine):
    """
    create news table
    """
    Base.metadata.create_all(engine)

Base = declarative_base()
