# -*- coding: utf-8 -*-
import scrapy
import datetime

class CrawlTestSpider(scrapy.Spider):
    name = 'crawl_test'
    allowed_domains = ['lianjia.com']
    start_urls = ['http://tj.lianjia.com/']
    custom_settings = {'LOG_FILE': 'logs/test_{dt}.log'.format(dt=datetime.datetime.now().strftime('%Y%m%d'))}

    def parse(self, response):
        pass
