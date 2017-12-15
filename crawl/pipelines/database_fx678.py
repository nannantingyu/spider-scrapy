# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
from crawl.Common.Util import session_scope
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_, or_, func
from crawl.models.util import db_connect, create_news_table
from crawl.models.crawl_fx678_economic_calendar import CrawlFx678EconomicCalendar
from crawl.models.crawl_fx678_economic_event import CrawlFx678EconomicEvent
from crawl.models.crawl_fx678_economic_holiday import CrawlFx678EconomicHoliday
from crawl.models.crawl_fx678_economic_jiedu import CrawlFx678EconomicJiedu
from crawl.models.crawl_economic_calendar import CrawlEconomicCalendar
from crawl.models.crawl_economic_jiedu import CrawlEconomicJiedu
import crawl.items as items

class Fx678Pipeline(object):
    """保存文章到数据库"""

    def __init__(self):
        engine = db_connect()
        create_news_table(engine)
        self.sess = sessionmaker(bind=engine)
        self.recent_newsid = None

    def open_spider(self, spider):
        """This method is called when the spider is opened."""
        logging.info('Fx678 pipeline open spider')

    def process_item(self, item, spider):
        """process news item"""
        if spider.name in ['crawl_fx678_calendar']:
            self.parse_fx678_calendar(item)
        elif spider.name in ['crawl_fx678_calendar_jiedu']:
            self.parse_fx678_jiedu(item)
        else:
            return item

    def parse_fx678_jiedu(self, item):
        with session_scope(self.sess) as session:
            crawlFx678EconomicJiedu = CrawlFx678EconomicJiedu(**item)
            query = session.query(CrawlFx678EconomicJiedu.dataname_id).filter(and_(
                CrawlFx678EconomicJiedu.dataname_id == crawlFx678EconomicJiedu.dataname_id,
            )).one_or_none()

            if query:
                session.query(CrawlEconomicCalendar).filter(
                    CrawlEconomicCalendar.dataname_id == crawlFx678EconomicJiedu.dataname_id
                ).update({
                    'next_pub_time': crawlFx678EconomicJiedu.next_pub_time,
                    'pub_agent': crawlFx678EconomicJiedu.pub_agent,
                    'pub_frequency': crawlFx678EconomicJiedu.pub_frequency,
                    'count_way': crawlFx678EconomicJiedu.count_way,
                    'data_influence': crawlFx678EconomicJiedu.data_influence,
                    'data_define': crawlFx678EconomicJiedu.data_define,
                    'funny_read': crawlFx678EconomicJiedu.funny_read

                })
            else:
                session.add(crawlFx678EconomicJiedu)

    def parse_fx678_calendar(self, item):
        if item and len(item) > 0:
            if 0 in item and isinstance(item[0], items.CrawlFx678EconomicCalendarItem):
                with session_scope(self.sess) as session:
                    all_data = []
                    for ditem in item:
                        ditem = item[ditem]
                        crawlfx678EconomicCalendar = CrawlFx678EconomicCalendar(**ditem)

                        query = session.query(CrawlFx678EconomicCalendar.id).filter(and_(
                            CrawlFx678EconomicCalendar.source_id == crawlfx678EconomicCalendar.source_id,
                            # CrawlEconomicCalendar.pub_time == crawlEconomicCalendar.pub_time
                        )).one_or_none()

                        if query is not None:
                            data = {}
                            if crawlfx678EconomicCalendar.country is not None:
                                data['country'] = crawlfx678EconomicCalendar.country
                            if crawlfx678EconomicCalendar.pub_time is not None:
                                data['pub_time'] = crawlfx678EconomicCalendar.pub_time
                            if crawlfx678EconomicCalendar.quota_name is not None:
                                data['quota_name'] = crawlfx678EconomicCalendar.quota_name
                            if crawlfx678EconomicCalendar.importance is not None:
                                data['importance'] = crawlfx678EconomicCalendar.importance
                            if crawlfx678EconomicCalendar.former_value is not None:
                                data['former_value'] = crawlfx678EconomicCalendar.former_value
                            if crawlfx678EconomicCalendar.predicted_value is not None:
                                data['predicted_value'] = crawlfx678EconomicCalendar.predicted_value
                            if crawlfx678EconomicCalendar.published_value is not None:
                                data['published_value'] = crawlfx678EconomicCalendar.published_value
                            if crawlfx678EconomicCalendar.influence is not None:
                                data['influence'] = crawlfx678EconomicCalendar.influence
                            if crawlfx678EconomicCalendar.position is not None:
                                data['position'] = crawlfx678EconomicCalendar.position

                            if data:
                                session.query(CrawlFx678EconomicCalendar).filter(
                                    CrawlFx678EconomicCalendar.id == query[0]).update(data)

                        else:
                            all_data.append(crawlfx678EconomicCalendar)

                    if len(all_data) > 0:
                        session.add_all(all_data)

            elif 0 in item and isinstance(item[0], items.CrawlEconomicEventItem):
                all_data = []

                with session_scope(self.sess) as session:
                    for ditem in item:
                        ditem = item[ditem]
                        crawlEconomicEvent = CrawlFx678EconomicEvent(**ditem)
                        query = session.query(CrawlFx678EconomicEvent.id).filter(and_(
                            CrawlFx678EconomicEvent.source_id == crawlEconomicEvent.source_id,
                            # CrawlEconomicCalendar.pub_time == crawlEconomicCalendar.pub_time
                        )).one_or_none()

                        if query:
                            data = {}
                            if crawlEconomicEvent.country is not None:
                                data['country'] = crawlEconomicEvent.country
                            if crawlEconomicEvent.time is not None:
                                data['time'] = crawlEconomicEvent.time
                            if crawlEconomicEvent.city is not None:
                                data['city'] = crawlEconomicEvent.city
                            if crawlEconomicEvent.importance is not None:
                                data['importance'] = crawlEconomicEvent.importance
                            if crawlEconomicEvent.event is not None:
                                data['event'] = crawlEconomicEvent.event
                            if crawlEconomicEvent.date is not None:
                                data['date'] = crawlEconomicEvent.date

                            if data:
                                session.query(CrawlFx678EconomicEvent).filter(
                                    CrawlFx678EconomicEvent.id == query[0]).update(data)
                        else:
                            all_data.append(crawlEconomicEvent)

                    if len(all_data) > 0:
                        session.add_all(all_data)

            elif 0 in item and isinstance(item[0], items.CrawlEconomicHolidayItem):
                all_data = []

                with session_scope(self.sess) as session:
                    for ditem in item:
                        ditem = item[ditem]
                        crawlEconomicHoliday = CrawlFx678EconomicHoliday(**ditem)

                        query = session.query(CrawlFx678EconomicHoliday.id).filter(and_(
                            CrawlFx678EconomicHoliday.source_id == crawlEconomicHoliday.source_id,
                            # CrawlEconomicCalendar.pub_time == crawlEconomicCalendar.pub_time
                        )).one_or_none()

                        if query:
                            data = {}
                            if crawlEconomicHoliday.country is not None:
                                data['country'] = crawlEconomicHoliday.country
                            if crawlEconomicHoliday.time is not None:
                                data['time'] = crawlEconomicHoliday.time
                            if crawlEconomicHoliday.market is not None:
                                data['market'] = crawlEconomicHoliday.market
                            if crawlEconomicHoliday.holiday_name is not None:
                                data['holiday_name'] = crawlEconomicHoliday.holiday_name
                            if crawlEconomicHoliday.detail is not None:
                                data['detail'] = crawlEconomicHoliday.detail
                            if crawlEconomicHoliday.date is not None:
                                data['date'] = crawlEconomicHoliday.date

                            if data:
                                session.query(CrawlFx678EconomicHoliday).filter(
                                    CrawlFx678EconomicHoliday.id == query[0]).update(data)
                        else:
                            all_data.append(crawlEconomicHoliday)

                    if len(all_data) > 0:
                        session.add_all(all_data)

            elif 0 in item and isinstance(item[0], items.CrawlEconomicJieduItem):
                with session_scope(self.sess) as session:
                    crawlEconomicJiedu = CrawlEconomicJiedu(**item[0])

                    query = session.query(CrawlEconomicJiedu.dataname_id).filter(and_(
                        CrawlEconomicJiedu.dataname_id == crawlEconomicJiedu.dataname_id,
                        # CrawlEconomicCalendar.pub_time == crawlEconomicCalendar.pub_time
                    )).one_or_none()

                    if query:
                        data = {
                            'next_pub_time': crawlEconomicJiedu.next_pub_time,
                            'pub_agent': crawlEconomicJiedu.pub_agent,
                            'pub_frequency': crawlEconomicJiedu.pub_frequency,
                            'count_way': crawlEconomicJiedu.count_way,
                            'data_influence': crawlEconomicJiedu.data_influence,
                            'data_define': crawlEconomicJiedu.data_define,
                            'funny_read': crawlEconomicJiedu.funny_read
                        }

                        session.query(CrawlEconomicJiedu).filter(
                            CrawlEconomicJiedu.dataname_id == crawlEconomicJiedu.dataname_id).update(data)
                    else:
                        session.add(crawlEconomicJiedu)

    def close_spider(self, spider):
        """close spider"""
        logging.info('Fx678 pipeline close spider')