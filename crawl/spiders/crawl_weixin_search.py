# -*- coding: utf-8 -*-
import scrapy


class CrawlWeixinSearchSpider(scrapy.Spider):
    name = 'crawl_weixin_search'
    allowed_domains = ['sogou.com']
    start_urls = ['http://sogou.com/']

    def parse(self, response):
        pass
