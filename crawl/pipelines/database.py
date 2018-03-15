# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_, or_, func
from crawl.models.util import db_connect, create_news_table
from crawl.models.crawl_lianjia_house import LianjiaHouse
from crawl.models.crawl_lianjia_agent import LianjiaAgent
from crawl.models.crawl_lianjia_feedback import LianjiaFeedback
from crawl.models.crawl_lianjia_residential import LianjiaResidential
from crawl.models.crawl_lianjia_visited import LianjiaVisited
from crawl.models.crawl_house_history import CrawlHouseHistory
from crawl.models.crawl_anjuke_residentail import CrawlAnjukeResidential
from crawl.items import LianjiaResidentialItem
from crawl.Common.Util import session_scope
import logging

class DatabasePipeline(object):
    def __init__(self):
        engine = db_connect()
        create_news_table(engine)
        self.sess = sessionmaker(bind=engine)

    def open_spider(self, spider):
        """This method is called when the spider is opened."""
        logging.info('Database pipeline open spider')

    def process_item(self, item, spider):
        if spider.name in ['crawl_lianjia', 'crawl_lianjia_detail']:
            self.parse_lianjia_house(item)
        elif spider.name in ['crawl_lianjia_visited']:
            self.parse_lianjia_visited(item)
        elif spider.name in ['crawl_lianjia_feedback']:
            self.parse_lianjia_feedback(item)
        elif spider.name in ['crawl_house_history']:
            self.parse_house_history(item)
        elif spider.name in ['crawl_anjuke_residential']:
            self.parse_anjuke_residentail(item)
        elif spider.name in ['crawl_anjuke_lianjia_residential']:
            self.parse_anjuke_lianjia_residential(item)
        elif spider.name in ['crawl_lianjia_residential']:
            if isinstance(item, LianjiaResidentialItem):
                self.parse_lianjia_residential(item)
            else:
                self.parse_agent(item)
        else:
            return item

    def parse_anjuke_lianjia_residential(self, item):
        type = item['type']
        del item['type']
        if type == "residential":
            anjuke_id = item['anjuke_residential_id']
            del item['anjuke_residential_id']
            with session_scope(self.sess) as session:
                session.query(CrawlAnjukeResidential).filter(
                    and_(
                        CrawlAnjukeResidential.residential_id == anjuke_id
                    )
                ).update(item)
        elif type == 'agent':
            with session_scope(self.sess) as session:
                lianjiaAgent = LianjiaAgent(**item)
                query = session.query(LianjiaFeedback.id).filter(and_(
                    LianjiaAgent.agent_id == lianjiaAgent.agent_id
                )).one_or_none()

                if query is None:
                    session.add(lianjiaAgent)
                else:
                    session.query(LianjiaAgent).filter(LianjiaAgent.id == query[0]).update(item)

    def parse_anjuke_residentail(self, item):
        with session_scope(self.sess) as session:
            crawlAnjukeResidential = CrawlAnjukeResidential(**item)

            query = session.query(CrawlHouseHistory.id).filter(and_(
                crawlAnjukeResidential.residential_id == CrawlAnjukeResidential.residential_id,
            )).one_or_none()

            if query:
                session.query(CrawlAnjukeResidential).filter(
                    and_(
                        CrawlAnjukeResidential.residential_id == crawlAnjukeResidential.residential_id,
                    )
                ).update(item)
            else:
                session.add(crawlAnjukeResidential)

    def parse_house_history(self, item):
        with session_scope(self.sess) as session:
            houseHistory = CrawlHouseHistory(**item)

            query = session.query(CrawlHouseHistory.id).filter(and_(
                CrawlHouseHistory.year == houseHistory.year,
                CrawlHouseHistory.month == houseHistory.month,
                CrawlHouseHistory.residential_id == houseHistory.residential_id,
            )).one_or_none()

            if query:
                session.query(LianjiaHouse).filter(
                    and_(
                        CrawlHouseHistory.year == houseHistory.year,
                        CrawlHouseHistory.month == houseHistory.month,
                        CrawlHouseHistory.residential_id == houseHistory.residential_id,
                    )
                ).update(item)
            else:
                session.add(houseHistory)


    def parse_lianjia_house(self, item):
        with session_scope(self.sess) as session:
            lianjiaHouse = LianjiaHouse(**item)
            query = session.query(LianjiaHouse.id).filter(and_(
                LianjiaHouse.house_id == lianjiaHouse.house_id,
            )).one_or_none()

            if query:
                itemdata = {
                    'price': lianjiaHouse.price,
                    'layout': lianjiaHouse.layout,
                    'area': lianjiaHouse.area,
                    'direction': lianjiaHouse.direction,
                    'elevator': lianjiaHouse.elevator,
                    'residential_id': lianjiaHouse.residential_id,
                    'flood': lianjiaHouse.flood,
                    'images': lianjiaHouse.images,
                    'district': lianjiaHouse.district,
                    'apartment_structure': lianjiaHouse.apartment_structure,
                    'street': lianjiaHouse.street,
                    'address': lianjiaHouse.address,
                    'building_type': lianjiaHouse.building_type,
                    'ladder': lianjiaHouse.ladder,
                    'heating': lianjiaHouse.heating,
                    'property_term': lianjiaHouse.property_term,
                    'list_time': lianjiaHouse.list_time,
                    'ownership': lianjiaHouse.ownership,
                    'last_trade': lianjiaHouse.last_trade,
                    'purpose': lianjiaHouse.purpose,
                    'hold_years': lianjiaHouse.hold_years,
                    'mortgage': lianjiaHouse.mortgage,
                    'house_register': lianjiaHouse.house_register,
                    'core_point': lianjiaHouse.core_point,
                    'periphery': lianjiaHouse.periphery,
                    'traffic': lianjiaHouse.traffic,
                    'residential_desc': lianjiaHouse.residential_desc,
                    'layout_desc': lianjiaHouse.layout_desc,
                    'img_layout': lianjiaHouse.img_layout,
                    'layout_datas': lianjiaHouse.layout_datas,
                    'renovation': lianjiaHouse.renovation,
                    'state': lianjiaHouse.state
                }

                updata = {}
                for key in itemdata:
                    if itemdata[key] is not None:
                        updata[key] = itemdata[key]

                session.query(LianjiaHouse).filter(
                    LianjiaHouse.house_id == lianjiaHouse.house_id
                ).update(updata)
            else:
                session.add(lianjiaHouse)

    def parse_lianjia_residential(self, item):
        with session_scope(self.sess) as session:
            lianjiaResidential = LianjiaResidential(**item)
            query = session.query(LianjiaResidential.id).filter(and_(
                LianjiaResidential.residential_id == lianjiaResidential.residential_id,
            )).one_or_none()

            if query is None:
                session.add(lianjiaResidential)
            else:
                session.query(LianjiaResidential).filter(LianjiaResidential.id == query[0]).update(item)

    def parse_lianjia_visited(self, item):
        with session_scope(self.sess) as session:
            lianjiaVisited = LianjiaVisited(**item)
            query = session.query(LianjiaVisited.id).filter(and_(
                LianjiaVisited.agent_id == lianjiaVisited.agent_id,
                LianjiaVisited.visited_time == lianjiaVisited.visited_time
            )).one_or_none()

            if query is None:
                session.add(item)
            else:
                session.query(LianjiaVisited).filter(LianjiaVisited.id == query[0]).update(item)

    def parse_lianjia_feedback(self, item):
        with session_scope(self.sess) as session:
            lianjiaFeedback = LianjiaFeedback(**item)
            query = session.query(LianjiaFeedback.id).filter(and_(
                LianjiaFeedback.agent_id == lianjiaFeedback.agent_id,
                LianjiaFeedback.hourse_id == lianjiaFeedback.hourse_id
            )).one_or_none()

            if query is None:
                session.add(item)
            else:
                session.query(LianjiaFeedback).filter(LianjiaFeedback.id == query[0]).update(item)

    def parse_agent(self, item):
        with session_scope(self.sess) as session:
            lianjiaAgent = LianjiaAgent(**item)
            query = session.query(LianjiaFeedback.id).filter(and_(
                LianjiaAgent.agent_id == lianjiaAgent.agent_id
            )).one_or_none()

            if query is None:
                session.add(lianjiaAgent)
            else:
                session.query(LianjiaAgent).filter(LianjiaAgent.id == query[0]).update(item)

    def close_spider(self, spider):
        """close spider"""
        logging.info("Database pipeline close")