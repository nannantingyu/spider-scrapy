# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, Date
from crawl.models.util import Base

class Ibrebates(Base):
    __tablename__ = 'crawl_ibrebates'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    description = Column(String(512))
    spread_type = Column(String(32))
    om_spread = Column(String(32))
    gold_spread = Column(String(32))
    offshore = Column(String(32))
    a_share = Column(String(32))
    regulatory_authority = Column(String(32))
    trading_varieties = Column(String(64))
    platform_type = Column(String(256))
    account_type = Column(String(32))
    scalp = Column(String(32))
    hedging = Column(String(32))
    min_transaction = Column(String(32))
    least_entry = Column(String(32))
    maximum_leverage = Column(String(32))
    maximum_trading = Column(String(32))
    deposit_method = Column(String(32))
    entry_method = Column(String(32))
    commission_fee = Column(String(32))
    entry_fee = Column(String(32))
    account_currency = Column(String(32))
    rollovers = Column(String(32))
    explosion_proportion = Column(String(32))
    renminbi = Column(String(32))
    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())