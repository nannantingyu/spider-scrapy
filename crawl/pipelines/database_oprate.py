# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging, datetime, sys
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_, or_, func
from crawl.models.util import db_connect, create_news_table
from crawl.models.crawl_china_time import ChinaTime
from crawl.models.crawl_error_top import ErrorTop
from crawl.models.crawl_monitor_area_stastic import MonitorAreaStastic
from crawl.models.crawl_monitor_chart import MonitorChart
from crawl.models.crawl_monitor_province import MonitorProvince
from crawl.models.crawl_monitor_stastic import MonitorStastic
from crawl.models.crawl_monitor_type import MonitorType
from crawl.models.crawl_province_time import ProvinceTime
from crawl.models.crawl_type_time import TypeTime
from crawl.models.crawl_baidu_tongji import BaiduTongji
from crawl.models.crawl_zhanzhang import CrawlZhanzhang
from crawl.models.crawl_ibrebates import Ibrebates
from crawl.models.crawl_baidu_rate import BaiduRate
from crawl.models.crawl_cgse import Cgse
from crawl.common.util import session_scope
import crawl.items as items
reload(sys)
sys.setdefaultencoding('utf-8')

class OpratePipeline(object):
    def __init__(self):
        engine = db_connect()
        create_news_table(engine)
        self.sess = sessionmaker(bind=engine)
        self.recent_newsid = None

    def open_spider(self, spider):
        """This method is called when the spider is opened."""
        logging.info('Oprate pipeline open spider')

    def process_item(self, item, spider):
        """process news item"""
        if spider.name in ["crawl_jiankongbao", "crawl_jiankongbao_tongji"]:
            self.process_jiankongbao(item)
        elif spider.name in ['baidu_tongji_nologin', 'crawl_baidu_tongji']:
            self.process_baidutongji(item)
        elif spider.name in ['crawl_zhanzhang']:
            self.parse_zhanzhang(item)
        elif spider.name in ['ibrebates']:
            self.parse_ibrebates(item)
        elif spider.name in ['crawl_baidu_rate']:
            self.parse_baidu_rate(item)
        elif spider.name in ['crawl_cgse']:
            self.parse_cgse(item)
        else:
            return item

    def parse_cgse(self, item):
        print item
        with session_scope(self.sess) as session:
            cgse = Cgse(**item)
            query = session.query(Cgse.id).filter(and_(
                Cgse.idr == cgse.idr
            )).one_or_none()

            if query:
                up_item = {}
                for k in item:
                    if item[k]:
                        up_item[k] = item[k]

                session.query(Cgse).filter(
                    Cgse.id == query[0]
                ).update(up_item)
            else:
                session.add(cgse)

    def parse_baidu_rate(self, item):
        with session_scope(self.sess) as session:
            baiduRate = BaiduRate(**item)
            query = session.query(BaiduRate.id).filter(and_(
                BaiduRate.source_id == baiduRate.source_id,
                BaiduRate.site == baiduRate.site
            )).one_or_none()

            if query:
                up_item = {}
                for k in item:
                    if item[k]:
                        up_item[k] = item[k]

                session.query(BaiduRate).filter(
                    BaiduRate.id == query[0]
                ).update(up_item)
            else:
                session.add(baiduRate)

    def parse_zhanzhang(self, item):
        all_data = [CrawlZhanzhang(**item[it]) for it in item]
        with session_scope(self.sess) as session:
            session.add_all(all_data)

    def process_jiankongbao(self, item):
        if isinstance(item, items.ChinaTimeItem):
            chinaTime = ChinaTime(**item)
            with session_scope(self.sess) as session:
                session.add(chinaTime)

        elif isinstance(item.values()[0], items.ErrorTopItem):
            all_items = []
            for it in item.values():
                all_items.append(ErrorTop(**it))
            with session_scope(self.sess) as session:
                session.add_all(all_items)

        elif isinstance(item.values()[0], items.MonitorAreaStasticItem):
            all_items = []
            for it in item.values():
                all_items.append(MonitorAreaStastic(**it))

            with session_scope(self.sess) as session:
                session.add_all(all_items)

        elif isinstance(item.values()[0], items.MonitorChartItem):
            all_items = []
            for it in item.values():
                all_items.append(MonitorChart(**it))
            with session_scope(self.sess) as session:
                for db_item in all_items:
                    query = session.query(MonitorChart.id).filter(and_(
                        MonitorChart.time == db_item.time,
                        MonitorChart.type == db_item.type,
                        MonitorChart.site == db_item.site,
                        MonitorChart.monitor_name == db_item.monitor_name
                    )).one_or_none()

                    if query is None:
                        session.add(db_item)
                    else:
                        data = {}
                        if db_item.value is not None:
                            data['value'] = db_item.value

                        if data:
                            session.query(MonitorChart).filter(
                                MonitorChart.id == query[0]).update(data)

        elif isinstance(item.values()[0], items.MonitorProvinceItem):
            all_items = []
            for it in item.values():
                all_items.append(MonitorProvince(**it))
            with session_scope(self.sess) as session:
                session.add_all(all_items)

        elif isinstance(item.values()[0], items.MonitorStasticItem):
            all_items = []
            for it in item.values():
                all_items.append(MonitorStastic(**it))
            with session_scope(self.sess) as session:
                session.add_all(all_items)

        elif isinstance(item.values()[0], items.MonitorTypeItem):
            all_items = []
            for it in item.values():
                all_items.append(MonitorType(**it))
            with session_scope(self.sess) as session:
                session.add_all(all_items)

        elif isinstance(item.values()[0], items.ProvinceTimeItem):
            all_items = []
            for it in item.values():
                all_items.append(ProvinceTime(**it))
            with session_scope(self.sess) as session:
                session.add_all(all_items)

        elif isinstance(item.values()[0], items.TypeTimeItem):
            all_items = []
            for it in item.values():
                all_items.append(TypeTime(**it))
            with session_scope(self.sess) as session:
                    session.add_all(all_items)

    def process_baidutongji(self, item):
        all_data = []
        with session_scope(self.sess) as session:
            baiduTongji = BaiduTongji(**item)

            query = session.query(BaiduTongji.id).filter(and_(
                BaiduTongji.user_id == baiduTongji.user_id,
                BaiduTongji.access_time == baiduTongji.access_time
            )).one_or_none()

            if query is None:
                all_data.append(baiduTongji)
            else:
                data = {}
                if baiduTongji.area is not None:
                    data['area'] = baiduTongji.area
                if baiduTongji.keywords is not None:
                    data['keywords'] = baiduTongji.keywords
                if baiduTongji.entry_page is not None:
                    data['entry_page'] = baiduTongji.entry_page
                if baiduTongji.ip is not None:
                    data['ip'] = baiduTongji.ip
                if baiduTongji.visit_time is not None:
                    data['visit_time'] = baiduTongji.visit_time
                if baiduTongji.visit_pages is not None:
                    data['visit_pages'] = baiduTongji.visit_pages
                if baiduTongji.visitorType is not None:
                    data['visitorType'] = baiduTongji.visitorType
                if baiduTongji.visitorFrequency is not None:
                    data['visitorFrequency'] = baiduTongji.visitorFrequency
                if baiduTongji.lastVisitTime is not None:
                    data['lastVisitTime'] = baiduTongji.lastVisitTime
                if baiduTongji.endPage is not None:
                    data['endPage'] = baiduTongji.endPage
                if baiduTongji.deviceType is not None:
                    data['deviceType'] = baiduTongji.deviceType
                if baiduTongji.fromType is not None:
                    data['fromType'] = baiduTongji.fromType
                if baiduTongji.fromurl is not None:
                    data['fromurl'] = baiduTongji.fromurl
                if baiduTongji.fromAccount is not None:
                    data['fromAccount'] = baiduTongji.fromAccount
                if baiduTongji.isp is not None:
                    data['isp'] = baiduTongji.isp
                if baiduTongji.os is not None:
                    data['os'] = baiduTongji.os
                if baiduTongji.osType is not None:
                    data['osType'] = baiduTongji.osType
                if baiduTongji.browser is not None:
                    data['browser'] = baiduTongji.browser
                if baiduTongji.browserType is not None:
                    data['browserType'] = baiduTongji.browserType
                if baiduTongji.language is not None:
                    data['language'] = baiduTongji.language
                if baiduTongji.resolution is not None:
                    data['resolution'] = baiduTongji.resolution
                if baiduTongji.color is not None:
                    data['color'] = baiduTongji.color
                if baiduTongji.accessPage is not None:
                    data['accessPage'] = baiduTongji.accessPage
                if baiduTongji.antiCode is not None:
                    data['antiCode'] = baiduTongji.antiCode

                if data:
                    session.query(BaiduTongji).filter(
                        baiduTongji.id == query[0]).update(data)


            if len(all_data) > 0:
                session.add_all(all_data)

    def parse_ibrebates(self, item):
        ibrebates = Ibrebates(**item)
        with session_scope(self.sess) as session:
            query = session.query(Ibrebates.id).filter(and_(
                Ibrebates.name == ibrebates.name
            )).one_or_none()

            if query is None:
                session.add(ibrebates)
            else:
                data = {}
                update_field = ["description", "spread_type", "om_spread", "gold_spread", "offshore", "a_share", "regulatory_authority", "trading_varieties", "platform_type", "account_type", "scalp", "hedging", "min_transaction", "least_entry", "maximum_leverage", "maximum_trading", "deposit_method", "entry_method", "commission_fee", "entry_fee", "account_currency", "rollovers", "explosion_proportion", "renminbi"]
                for field in update_field:
                    try:
                        attr_value = getattr(ibrebates, field)
                        data[field] = attr_value
                    except AttributeError as err:
                        pass

                if data:
                    session.query(Ibrebates).filter(Ibrebates.id == query[0]).update(data)

    def close_spider(self, spider):
        """close spider"""
        logging.info('Oprate pipeline close spider')