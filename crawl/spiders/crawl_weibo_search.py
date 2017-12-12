# -*- coding: utf-8 -*-
import scrapy, redis
from selenium import webdriver
from crawl.settings import REDIS, Tmp_Dir
import sys, datetime
reload(sys)
sys.setdefaultencoding('utf-8')

class CrawlWeiboSearchSpider(scrapy.Spider):
    name = 'crawl_weibo_search'
    allowed_domains = ['weibo.com']
    start_urls = ['http://weibo.com/']

    custom_settings = {
        'LOG_FILE': 'logs/weibo_search_{dt}.log'.format(dt=datetime.datetime.now().strftime('%Y%m%d'))
    }

    def start_requests(self):
        # r = redis.Redis(host=REDIS['host'], port=REDIS['port'])
        # driver = webdriver.PhantomJS()
        # driver.get("")
        # tds = driver.find_elements_by_xpath(".//table[@id='realtimehot']//tr//td[@class='td_02']")
        #
        # for td in tds:
        #     keywords = td.text.strip() if td.text is not None else None
        #     if keywords:
        #         r.sadd("weixin_hot_keywords", keywords)
        #         r.sadd("weibo_hot_keywords", keywords)
        #         print keywords

        return [scrapy.Request("http://s.weibo.com/top/summary?Refer=top_hot&topnav=1&wvr=6",
                               meta={'cookiejar': self.name, 'handle_httpstatus_list': [301, 302, 403], 'PhantomJS': True}, callback=self.parse_content)]

    def parse_content(self, response):
        with open(Tmp_Dir + "body.html", 'w') as fs:
            fs.write(response.body)