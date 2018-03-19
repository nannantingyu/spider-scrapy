# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging, datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_, or_, func
from crawl.models.util import db_connect, create_news_table
from crawl.Common.Util import session_scope
from crawl.models.crawl_cryptomiso import Crawl_Cryptomiso
from crawl.items import CrawlWexinArticleItem

class CryptPipeline(object):

    def __init__(self):
        engine = db_connect()
        create_news_table(engine)
        self.sess = sessionmaker(bind=engine)
        self.recent_newsid = None

    def open_spider(self, spider):
        """This method is called when the spider is opened."""
        logging.info('Crypt pipeline open spider')

    def process_item(self, item, spider):
        """process news item"""
        if spider.name in ['crawl_cryptomiso']:
            self.parse_cryptomiso(item)
        else:
            return item

    def parse_cryptomiso(self, item):
        print item
        with session_scope(self.sess) as session:
            rank = Crawl_Cryptomiso(**item)
            session.add(rank)

    def close_spider(self, spider):
        """close spider"""
        logging.info('Crypt pipeline close spider')
