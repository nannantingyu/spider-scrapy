# -*- coding: utf-8 -*-
import scrapy, datetime, json
from selenium import webdriver

class CrawlWeiboLoginSpider(scrapy.Spider):
    name = 'crawl_weibo_login'
    allowed_domains = ['weibo.cn', 'weibo.com']
    start_urls = ['http://weibo.cn/']

    custom_settings = {
        'LOG_FILE': 'logs/weibo_login_{dt}.log'.format(dt=datetime.datetime.now().strftime('%Y%m%d'))
    }

    def start_requests(self):
        with open("cookies/cookie.json", "r") as fs:
            cookies = json.load(fs)

        print cookies
        return [scrapy.Request("https://d.weibo.com/", meta={'cookiejar': self.name, 'dont_redirect': True,
                                   'handle_httpstatus_list': [301, 302, 403], 'PhantomJS': True}, callback=self.parse_cookie)]

    def parse_cookie(self, response):
        print response.status
        with open("weibo.html", "w") as fs:
            fs.write(response.body)
