# -*- coding: utf-8 -*-
import scrapy, datetime

class CrawlBtc123Spider(scrapy.Spider):
    name = 'crawl_btc123'
    allowed_domains = ['btc123.com']
    start_urls = ['http://btc123.com/']

    custom_settings = {
        'LOG_FILE': 'logs/btc123_{dt}.log'.format(dt=datetime.datetime.now().strftime('%Y%m%d'))
    }

    def __init__(self):
        self.url = "https://btc123.com/ajaxNewsList?page={page}&typeId=0"
        self.page_now = 1

    def get_next_url(self):
        url = self.url.format(page=str(self.page_now))
        self.page_now += 1
        return url

    def start_requests(self):
        return scrapy.Request(self.get_next_url(), meta={'cookiejar': self.name}, callback=self.parse_list)

    def parse_list(self, response):
        lis = response.xpath("li")
        for li in lis:
            title = li.xpath(".//div[@class='newsrd']/h3/a/text()").extract_first()
            print title