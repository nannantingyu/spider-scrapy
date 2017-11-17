# -*- coding: utf-8 -*-
import scrapy


class CrawlLianjiaResidentialSpider(scrapy.Spider):
    name = 'crawl_lianjia_residential'
    allowed_domains = ['lianjia.com']
    start_urls = ['http://lianjia.com/']

    def parse(self, response):
        pass
