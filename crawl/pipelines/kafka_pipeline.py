# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from kafka import KafkaProducer
import json

class KafkaPipeline(object):
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers='192.168.100.122',
                                      value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    def process_item(self, item, spider):
        print "get item in kafka %s" % spider.name
        if spider.name in ['crawl_jin10_article', 'crawl_fx678_article', 'crawl_jin10_calendar', 'crawl_jin10_calendar_jiedu',
                           'crawl_fx678_calendar', 'crawl_fx678_calendar_jiedu', 'crawl_cgse', 'crawl_jin10_ssi_trends',
                           'crawl_jin10_ssi_trends_today', 'crawl_zhanzhang', 'crawl_jiankongbao', 'crawl_baidu_tongji',
                           'crawl_jiankongbao_tongji', 'crawl_ibrebates']:
            self.producer.send(spider.name, item)

    def close_spider(self, spider):
        """close spider"""
        print "close"