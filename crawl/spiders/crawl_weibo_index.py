# -*- coding: utf-8 -*-
import scrapy
import datetime

class CrawlWeiboIndexSpider(scrapy.Spider):
    name = 'crawl_weibo_index'
    allowed_domains = ['weibo.com', 'd.weibo.com']
    start_urls = ['http://weibo.com/']

    custom_settings = {
        'LOG_FILE': 'logs/weibo_index_{dt}.log'.format(dt=datetime.datetime.now().strftime('%Y%m%d'))
    }

    def start_requests(self):
        return [scrapy.Request("https://d.weibo.com",
                               meta={'cookiejar': 'crawl_weibo_login', 'dont_redirect': True,
                                   'handle_httpstatus_list': [301, 302, 403]},
                               callback=self.parse_cookie)]

    def parse_cookie(self, response):
        print response.status
        with open("weibo_index.html", "w") as fs:
            fs.write(response.body)
