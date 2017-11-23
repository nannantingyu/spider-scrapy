# -*- coding: utf-8 -*-
import scrapy
import datetime, redis, json
from crawl.settings import REDIS
import logging
from crawl.items import LianjiaResidentialItem, LianjiaAgentItem
from crawl.common.util import util

class CrawlLianjiaResidentialSpider(scrapy.Spider):
    name = 'crawl_lianjia_residential'
    allowed_domains = ['lianjia.com']
    start_urls = ['http://lianjia.com/']
    custom_settings = {'LOG_FILE': 'logs/lianjia_residentail_{dt}.log'.format(dt=datetime.datetime.now().strftime('%Y%m%d'))}

    def __init__(self):
        self.base_url = "https://tj.lianjia.com/ershoufang/housestat?hid={house_id}&rid={residential_id}"
        self.r = redis.Redis(host=REDIS['host'])
        self.util = util()
        self.residential_id = None

    def start_requests(self):
        url = self.next_url()
        if url is not None:
            return [scrapy.Request(url, meta={'cookiejar': self.name, 'platform': 'pc'}, callback=self.parse_residential)]

    def parse_residential(self, response):
        # try:
            data = json.loads(response.body)
            data = data['data']

            item = LianjiaResidentialItem()

            item['residential_id'] = self.residential_id
            item['name'] = data['resblockCard']['name']
            item['build_year'] = data['resblockCard']['buildYear']
            item['build_num'] = data['resblockCard']['buildNum']
            item['build_type'] = data['resblockCard']['buildType']
            item['unit_price'] = data['resblockCard']['unitPrice']
            item['sell_num'] = data['resblockCard']['sellNum']
            item['rent_num'] = data['resblockCard']['rentNum']

            resblockPosition = data['resblockPosition'].split(",")
            item['longitude'] = resblockPosition[0]
            item['latitude'] = resblockPosition[1]

            print item
            yield item

            agents = data['agentInfo']
            for a in agents:
                agent = agents[a]
                agent_item = LianjiaAgentItem()
                agent_item['agent_id'] = agent['agentUcid']
                agent_item['reason'] = agent['reason']
                agent_item['name'] = agent['agentName']
                agent_item['agent_url'] = self.util.downfile(agent['agent_url'])
                agent_item['agent_level'] = agent['agent_level']
                agent_item['agent_photo'] = agent['agent_photo']
                agent_item['feedback_good_rate'] = agent['feedbackGoodRate']
                agent_item['comment_count'] = agent['commentCount']
                agent_item['total_comment_score'] = agent['totalCommentScore']
                agent_item['agent_phone'] = agent['agent_phone']

                yield agent_item


            url = self.next_url()
            if url is not None:
                yield scrapy.Request(url, meta={'cookiejar': self.name, 'platform': 'pc'}, callback=self.parse_residential)

        # except Exception, e:
        #     logging.error(e)

    def next_url(self):
        url = None
        residential_id = self.r.spop('lianjia:residential')
        if residential_id is not None:
            self.residential_id = residential_id
            house_id = self.r.get('lianjia:residential:%s' % residential_id)
            url = self.base_url.format(house_id=house_id, residential_id=residential_id)

        print url
        return url

