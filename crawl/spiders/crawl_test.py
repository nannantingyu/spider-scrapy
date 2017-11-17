# -*- coding: utf-8 -*-
import scrapy


class CrawlTestSpider(scrapy.Spider):
    name = 'crawl_test'
    allowed_domains = ['baidu.com']
    start_urls = ['http://baidu.com/']

    def parse(self, response):
        pass
