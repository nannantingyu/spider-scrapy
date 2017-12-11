# -*- coding: utf-8 -*-
import scrapy


class CrawlWeiboSearchSpider(scrapy.Spider):
    name = 'crawl_weibo_search'
    allowed_domains = ['weibo.com']
    start_urls = ['http://weibo.com/']

    def parse(self, response):
        pass
