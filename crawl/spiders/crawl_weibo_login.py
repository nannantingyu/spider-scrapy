# -*- coding: utf-8 -*-
import scrapy, datetime, json
from selenium import webdriver
import sys, time
reload(sys)
sys.setdefaultencoding("utf-8")

class CrawlWeiboLoginSpider(scrapy.Spider):
    name = 'crawl_weibo_login'
    allowed_domains = ['weibo.cn', 'weibo.com']
    start_urls = ['http://weibo.cn/']

    custom_settings = {
        'LOG_FILE': 'logs/weibo_login_{dt}.log'.format(dt=datetime.datetime.now().strftime('%Y%m%d'))
    }

    def __init__(self):
        self.cookie_file = "weibo.json"
        self.base_url = "https://d.weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=102803_ctg1_1760_-_ctg1_1760&pagebar=0&tab=home&current_page={current_page}&pre_page={pre_page}&page={page}&pl_name=Pl_Core_NewMixFeed__3&id=102803_ctg1_1760_-_ctg1_1760&script_uri=/&feed_type=1&domain_op=102803_ctg1_1760_-_ctg1_1760&__rnd={time}"
        self.page = self.current_page = self.pre_page = 1

    def get_url(self):
        timestr = str(int(time.time()) * 1000)
        return self.base_url.format(page=self.page, current_page=self.current_page, pre_page=self.pre_page, time=timestr)

    def start_requests(self):
        return [scrapy.Request(self.get_url(),
                               meta={'cookiejar': self.name, 'dont_redirect': True,
                                   'handle_httpstatus_list': [301, 302, 403], 'PhantomJS': True, "cookiefile": self.cookie_file},
                               callback=self.parse_cookie)]

    def parse_cookie(self, response):
        print response.status
        with open("weibo.html", "w") as fs:
            fs.write(response.body)

        html = response.body.replace(u"\u200b", "").replace("\r", "").replace("\n", "").replace(u"\xfb", "").replace(u"\xf1", "")
        print html