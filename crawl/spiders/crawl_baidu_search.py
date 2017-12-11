# -*- coding: utf-8 -*-
import scrapy


class CrawlBaiduSearchSpider(scrapy.Spider):
    name = 'crawl_baidu_search'
    allowed_domains = ['weibo.com']
    start_urls = ['http://weibo.com/']

    def parse(self, response):
        pass
