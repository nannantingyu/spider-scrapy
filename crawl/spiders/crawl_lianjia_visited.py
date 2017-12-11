# -*- coding: utf-8 -*-
import scrapy
import datetime, redis, json, time
from crawl import settings
from crawl.common.util import util

class CrawlLianjiaVisitedSpider(scrapy.Spider):
    name = 'crawl_lianjia_visited'
    allowed_domains = ['lianjia.com']
    start_urls = ['http://lianjia.com/']
    custom_settings = {
        'LOG_FILE': 'logs/lianjia_visited_{dt}.log'.format(dt=datetime.datetime.now().strftime('%Y%m%d'))}

    def __init__(self):
        self.util = util()
        self.house_id = None
        self.baseurl = 'https://tj.lianjia.com/ershoufang/houseseerecord?id={id}'
        self.r = redis.Redis(host=settings.REDIS['host'], port=settings.REDIS['port'])

    def start_requests(self):
        url = self.next_url()
        if url is not None:
            return [scrapy.Request(url, meta={'cookiejar': self.name, 'platform': 'pc'}, callback=self.parse_feedback)]

    def parse_feedback(self, response):
        data = json.loads(response.body)
        data = data['data']

        recordList = data['seeRecord']
        all_datas = {}
        for index, record in enumerate(recordList):
            item = {}
            item['visited_time'] = record['seeTime']
            item['agent_id'] = record['agentId']
            item['house_id'] = self.house_id
            item['see_count'] = record['seeCnt']

            all_datas[index] = data

        print all_datas

        agentList = data['agentInfo']
        all_agent = {}
        for index, agent in enumerate(agentList):
            item = {}
            item['name'] = agent['agentName']
            item['agent_id'] = agent['agentUcid']
            item['reason'] = data['reason']
            item['agent_url'] = agent['agent_url']
            item['agent_level'] = data['agent_level']
            item['agent_photo'] = self.util.downfile(agent['agent_photo'])
            item['feedback_good_rate'] = data['feedbackGoodRate'][0:-1]
            item['comment_count'] = agent['commentCount']
            item['total_comment_score'] = data['totalCommentScore']
            item['agent_phone'] = agent['agent_phone']

            all_agent[index] = data

        print all_agent
        url = self.next_url()
        if url is not None:
            yield scrapy.Request(url, meta={'cookiejar': self.name, 'platform': 'pc'}, callback=self.parse_feedback)

    def next_url(self):
        house_id = self.r.spop('lianjia:visited')
        if house_id is not None:
            self.house_id = house_id
            self.r.sadd('lianjia:visited:all', house_id)
            return self.baseurl.format(id=house_id)

        return None