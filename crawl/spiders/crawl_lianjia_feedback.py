# -*- coding: utf-8 -*-
import scrapy
import datetime, redis, json, time
from crawl import settings

class CrawlLianjiaFeedbackSpider(scrapy.Spider):
    name = 'crawl_lianjia_feedback'
    allowed_domains = ['lianjia.com']
    start_urls = ['http://lianjia.com/']
    custom_settings = {'LOG_FILE': 'logs/lianjia_feedback_{dt}.log'.format(dt=datetime.datetime.now().strftime('%Y%m%d'))}

    def __init__(self):
        self.page_now = 1
        self.page_all = 0
        self.house_id = None
        self.baseurl = 'https://tj.lianjia.com/ershoufang/showcomment?isContent=1&page={page}&order=0&id={id}&_={timestamp}'
        self.r = redis.Redis(host=settings.REDIS['host'], port=settings.REDIS['port'])

    def start_requests(self):
        url = self.next_url()
        if url is not None:
            return [scrapy.Request(url, meta={'cookiejar': self.name}, callback=self.parse_feedback)]

    def parse_feedback(self, response):
        data = json.loads(response.body)
        data = data['data']

        print data
        if self.page_all == 0:
            self.page_all = int(data['totalPageNum'])

        agentList = data['agentList']
        all_datas = {}
        for index,agent in enumerate(agentList):
            item = {}
            item['comment'] = agent['comment']
            item['agent_id'] = agent['agentUcid']
            item['house_id'] = data['houseCode']

            all_datas[index] = data

        print all_datas

        url = self.next_url()
        if url is not None:
            yield scrapy.Request(url, meta={'cookiejar': self.name}, callback=self.parse_feedback)

    def next_url(self):
        if self.house_id == None or self.page_now == self.page_all:
            self.page_now = 1
            self.page_all = 0
            house_id = self.r.spop('lianjia:feedback')
            if house_id is not None:
                self.house_id = house_id
                self.r.sadd('lianjia:feedback:all', house_id)
                return self.baseurl.format(id=house_id, page=self.page_now, timestamp=int(time.time()))
        else:
            self.page_now += 1
            return self.baseurl.format(id=self.house_id, page=self.page_now, timestamp=int(time.time()))

        return None