# -*- coding: utf-8 -*-
import scrapy
import datetime, redis

class CrawlFx678CalendarJieduSpider(scrapy.Spider):
    name = 'crawl_fx678_calendar_jiedu'
    allowed_domains = ['fx678.com']
    start_urls = ['http://fx678.com/']

    url_format = "http://rl.fx678.com/id/{dataname_id}.html"
    index = 1
    id_x = None

    custom_settings = {
        'LOG_FILE': 'logs/fx678_calendar_jiedu_{dt}.log'.format(dt=datetime.datetime.now().strftime('%Y%m%d'))
    }

    def __init__(self):
        self.r = redis.Redis(host='127.0.0.1')

    def start_requests(self):
        url = self.next_url()
        return [scrapy.Request(url, meta={"cookiejar": self.name, 'dont_redirect': True},
                               callback=self.parse_jiedu)]

    def next_url(self):
        id = self.r.spop("fx678_jiedu")
        url = None

        if id:
            self.id_x = id
            self.r.sadd("fx678_jiedu_ori", id)
            url = self.url_format.format(dataname_id=id)

        return url

    def parse_jiedu(self, response):
        lis = response.xpath(".//div[@class='choose_add_1_two']/ul/li")
        item = {}
        item['next_pub_time'] = lis[3].xpath("./text()").extract_first()
        item['pub_agent'] = lis[1].xpath("./text()").extract_first()
        item['pub_frequency'] = lis[2].xpath("./text()").extract_first()
        item['count_way'] = ""
        item['data_influence'] = lis[0].xpath("./text()").extract_first()

        data_info = response.xpath(".//div[@class='choose_add_1_top']")
        item['data_define'] = data_info[0].xpath("./text()").extract_first()
        item['funny_read'] = data_info[1].xpath("./text()").extract_first()
        item['dataname_id'] = self.id_x

        yield item

        url = self.next_url()
        if url:
            yield scrapy.Request(url, meta={"cookiejar": self.name, 'dont_redirect': True},
                                 callback=self.parse_jiedu)