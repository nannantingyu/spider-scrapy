# -*- coding: utf-8 -*-
import scrapy
import datetime, redis, json
from crawl.Common.Util import util
from crawl.items import CrawlEconomicJieduItem

class CrawlJin10CalendarJieduSpider(scrapy.Spider):
    name = 'crawl_jin10_calendar_jiedu'
    allowed_domains = ['jin10.com']
    start_urls = ['https://www.jin10.com/']
    url_format = "https://rili.jin10.com/datas/jiedu/{dataid}.json?ori={ori}"
    index = 1

    custom_settings = {
        'LOG_FILE': 'logs/jin10_calendar_jiedu_{dt}.log'.format(dt=datetime.datetime.now().strftime('%Y%m%d'))
    }

    def __init__(self):
        self.util = util()
        self.r = redis.Redis(host='127.0.0.1')

    def start_requests(self):
        url = self.next_url()
        return [scrapy.Request(url, meta={"cookiejar": self.name, 'dont_redirect': True},
                               callback=self.parse_jiedu)]

    def next_url(self):
        url = None
        while True:
            id = self.r.spop("jin10:jiedu")

            if id:
                ids = id.split("_")
                crawled_key = 'jin10:jiedu_%s' % ids[0]
                if len(self.r.keys(crawled_key)) == 0:
                    self.r.set(crawled_key, ids[0])
                    self.r.expire(crawled_key, 3600*24*10)

                    url = self.url_format.format(dataid=ids[1], ori=ids[0])
                    break
            else:
                break

        return url

    def parse_jiedu(self, response):
        url = response.url
        params = self.util.get_url_param(url)

        data = json.loads(response.body)
        item = CrawlEconomicJieduItem()
        item['next_pub_time'] = data['publictime']
        item['pub_agent'] = data['institutions']
        item['pub_frequency'] = data['frequency']
        item['count_way'] = data['method']
        item['data_influence'] = data['impact']
        item['data_define'] = data['paraphrase']
        item['funny_read'] = data['focus']
        item['dataname_id'] = params['ori']

        yield item

        url = self.next_url()
        if url:
            yield scrapy.Request(url, meta={"cookiejar": self.name, 'dont_redirect': True},
                                 callback=self.parse_jiedu)