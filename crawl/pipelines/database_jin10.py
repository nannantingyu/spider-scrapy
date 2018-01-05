# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging, datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_, or_, func
from crawl.models.util import db_connect, create_news_table
from crawl.models.crawl_economic_calendar import CrawlEconomicCalendar
from crawl.models.crawl_economic_event import CrawlEconomicEvent
from crawl.models.crawl_economic_holiday import CrawlEconomicHoliday
from crawl.models.crawl_economic_jiedu import CrawlEconomicJiedu
from crawl.models.crawl_article import CrawlArticle
from crawl.models.crawl_ssi_trend import CrawlSsiTrend
from crawl.models.crawl_ssi_trend_tb import *
from crawl.Common.Util import session_scope

import crawl.items as items
import datetime


class Jin10Pipeline(object):
    """保存文章到数据库"""

    def __init__(self):
        engine = db_connect()
        create_news_table(engine)
        self.sess = sessionmaker(bind=engine)
        self.recent_newsid = None

    def open_spider(self, spider):
        """This method is called when the spider is opened."""
        logging.info('Jin10 pipeline open spider')

    def process_item(self, item, spider):
        """process news item"""
        if spider.name in ['cj-calendar']:
            self.parse_calendar(item)
        elif spider.name in ['crawl_jin10_article', 'crawl_jin10_article_detail', 'weibo', 'weibo_article_detail', 'crawl_fx678_article']:
            self.parse_article(item)
        elif spider.name in ['crawl_jin10_ssi_trends']:
            self.parse_ssi_trends(item)
        elif spider.name in ['crawl_jin10_ssi_trends_today']:
            self.parse_ssi_trends_today(item)
        elif spider.name in ['crawl_jin10_calendar']:
            self.parse_calendar(item)
        elif spider.name in ['crawl_jin10_calendar_jiedu']:
            self.parse_jiedu(item)
        else:
            return item

    def parse_jiedu(self, item):
        with session_scope(self.sess) as session:
            crawlEconomicJiedu = CrawlEconomicJiedu(**item)
            query = session.query(CrawlEconomicJiedu.dataname_id).filter(
                CrawlEconomicJiedu.dataname_id == crawlEconomicJiedu.dataname_id
            ).one_or_none()

            if query:
                updata = {}
                for it in item:
                    if item[it]:
                        updata[it] = item
                session.query(CrawlEconomicJiedu).filter(CrawlEconomicJiedu.dataname_id == query[0]).update(updata)
            else:
                session.add(crawlEconomicJiedu)

    def parse_article(self, item):
        article = CrawlArticle(**item)
        with session_scope(self.sess) as session:
            query = session.query(CrawlArticle.id).filter(and_(
                CrawlArticle.source_id == article.source_id,
            )).one_or_none()

            if query is None:
                session.add(article)
            else:
                data = {}
                for it in item:
                    if item[it] is not None:
                        data[it] = item[it]

                if data:
                    session.query(CrawlArticle).filter(CrawlArticle.id == query[0]).update(data)

    def parse_calendar(self, item):
        if item and len(item) > 0:
            if 0 in item and isinstance(item[0], items.CrawlEconomicCalendarItem):
                with session_scope(self.sess) as session:
                    all_data = []
                    now_dataname_ids = []
                    for ditem in item:
                        ditem = item[ditem]
                        crawlEconomicCalendar = CrawlEconomicCalendar(**ditem)

                        now_dataname_ids.append(crawlEconomicCalendar.source_id)
                        query = session.query(CrawlEconomicCalendar.id).filter(and_(
                            CrawlEconomicCalendar.source_id == crawlEconomicCalendar.source_id,
                            # CrawlEconomicCalendar.pub_time == crawlEconomicCalendar.pub_time
                        )).one_or_none()

                        if query is not None:
                            data = {}
                            if crawlEconomicCalendar.country is not None:
                                data['country'] = crawlEconomicCalendar.country
                            if crawlEconomicCalendar.pub_time is not None:
                                data['pub_time'] = crawlEconomicCalendar.pub_time
                            if crawlEconomicCalendar.quota_name is not None:
                                data['quota_name'] = crawlEconomicCalendar.quota_name
                            if crawlEconomicCalendar.importance is not None:
                                data['importance'] = crawlEconomicCalendar.importance
                            if crawlEconomicCalendar.former_value is not None:
                                data['former_value'] = crawlEconomicCalendar.former_value
                            if crawlEconomicCalendar.predicted_value is not None:
                                data['predicted_value'] = crawlEconomicCalendar.predicted_value
                            if crawlEconomicCalendar.published_value is not None:
                                data['published_value'] = crawlEconomicCalendar.published_value
                            if crawlEconomicCalendar.influence is not None:
                                data['influence'] = crawlEconomicCalendar.influence

                            if data:
                                session.query(CrawlEconomicCalendar).filter(
                                    CrawlEconomicCalendar.id == query[0]).update(data)

                        else:
                            all_data.append(crawlEconomicCalendar)

                    if len(all_data) > 0:
                        session.add_all(all_data)

                    #删除昨天没有发布的
                    lastday = item[0]['pub_time']
                    lastday = datetime.datetime.strptime(lastday, "%Y-%m-%d %H:%M:%S")
                    print lastday.strftime('%Y-%m-%d 00:00:00'), lastday.strftime('%Y-%m-%d 23:59:59')
                    session.query(CrawlEconomicCalendar).filter(and_(
                        CrawlEconomicCalendar.pub_time.between(lastday.strftime('%Y-%m-%d 00:00:00'), lastday.strftime('%Y-%m-%d 23:59:59')),
                        ~CrawlEconomicCalendar.dataname_id.in_(now_dataname_ids)
                    )).delete(synchronize_session=False)

            elif 0 in item and isinstance(item[0], items.CrawlEconomicEventItem):
                all_data = []

                with session_scope(self.sess) as session:

                    for ditem in item:
                        ditem = item[ditem]
                        crawlEconomicEvent = CrawlEconomicEvent(**ditem)

                        query = session.query(CrawlEconomicEvent.id).filter(and_(
                            CrawlEconomicEvent.source_id == crawlEconomicEvent.source_id,
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
                                session.query(CrawlEconomicEvent).filter(
                                    CrawlEconomicEvent.id == query[0]).update(data)
                        else:
                            all_data.append(crawlEconomicEvent)

                    if len(all_data) > 0:
                        session.add_all(all_data)

            elif 0 in item and isinstance(item[0], items.CrawlEconomicHolidayItem):
                all_data = []

                with session_scope(self.sess) as session:
                    # crawlEconomicHoliday = CrawlEconomicHoliday(**item[0])
                    # session.query(CrawlEconomicHoliday).filter(CrawlEconomicHoliday.date == crawlEconomicHoliday.date).delete()

                    for ditem in item:
                        ditem = item[ditem]
                        crawlEconomicHoliday = CrawlEconomicHoliday(**ditem)

                        query = session.query(CrawlEconomicHoliday.id).filter(and_(
                            CrawlEconomicHoliday.source_id == crawlEconomicHoliday.source_id,
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
                                session.query(CrawlEconomicHoliday).filter(
                                    CrawlEconomicHoliday.id == query[0]).update(data)
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

    def parse_ssi_trends_today(self, item):
        with session_scope(self.sess) as session:
            all_item = []
            for it in item:
                crawlSSiTrend = CrawlSsiTrend(**item[it])
                all_item.append(crawlSSiTrend)

            if len(all_item) > 0:
                session.add_all(all_item)

    def parse_ssi_trends(self, item):
        with session_scope(self.sess) as session:
            CrawlSsiTrend = eval("CrawlSsiTrend_" + item[0]['platform'])
            query = session.query(func.max(CrawlSsiTrend.time).label("max_time")).filter(
                and_(
                    CrawlSsiTrend.type == item[0]['type'],
                    CrawlSsiTrend.platform == item[0]['platform'],
                )
            ).one_or_none()

            max_time = query[0] if query else None

            all_item = []
            for it in item:
                if max_time is None or item[it]['time'] > max_time.strftime('%Y-%m-%d %H:%M:%I'):
                    crawlSSiTrend = CrawlSsiTrend(**item[it])
                    all_item.append(crawlSSiTrend)

            if len(all_item) > 0:
                session.add_all(all_item)

    def close_spider(self, spider):
        """close spider"""
        logging.info('Jin10 pipeline close spider')