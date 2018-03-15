# -*- coding: utf-8 -*-
import scrapy, datetime, redis
from crawl.items import CrawlHotkey
from crawl.Common.Util import util
from crawl.settings import REDIS

class CrawlBaiduSearchSpider(scrapy.Spider):
    name = 'crawl_baidu_search'
    allowed_domains = ['baidu.com']
    start_urls = ['http://top.baidu.com/buzz?b=1&fr=topindex']

    custom_settings = {
        'LOG_FILE': 'logs/baidu_search_{dt}.log'.format(dt=datetime.datetime.now().strftime('%Y%m%d'))
    }

    def __init__(self):
        self.r = redis.Redis(host=REDIS['host'], port=REDIS['port'])

    def parse(self, response):
        trs = response.xpath(".//div[@class='mainBody']//table[@class='list-table']/tr")
        for index,tr in enumerate(trs):
            data = tr.xpath("./td[@class='keyword']/a[1]/text()").extract_first()

            if data:
                print data
                if not self.r.sismember("old_hot_keywords", data):
                    self.r.sadd("weixin_hot_keywords", data)
                    self.r.sadd("weibo_hot_keywords", data)

                    item = CrawlHotkey()
                    item['time'] = datetime.datetime.now()
                    item['keyword'] = data
                    item['order'] = index
                    item['source_id'] = util.get_sourceid(data)

                    yield item
