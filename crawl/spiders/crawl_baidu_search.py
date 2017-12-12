# -*- coding: utf-8 -*-
import scrapy


class CrawlBaiduSearchSpider(scrapy.Spider):
    name = 'crawl_baidu_search'
    allowed_domains = ['baidu.com']
    start_urls = ['http://top.baidu.com/buzz?b=1&fr=topindex']

    def parse(self, response):
        trs = response.xpath(".//div[@class='mainBody']//table[@class='list-table']/tr")
        for tr in trs:
            data = tr.xpath("./td[@class='keyword']/a[1]/text()").extract_first()
            print data
