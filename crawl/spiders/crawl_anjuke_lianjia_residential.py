# -*- coding: utf-8 -*-
import scrapy, datetime, json, sys, re
reload(sys)
sys.setdefaultencoding("utf-8")

class CrawlAnjukeLianjiaResidentialSpider(scrapy.Spider):
    name = 'crawl_anjuke_lianjia_residential'
    allowed_domains = ['lianjia.com']
    start_urls = ['http://lianjia.com/']

    custom_settings = {
        'LOG_FILE': 'logs/anjuke_lianjia_residential_{dt}.log'.format(dt=datetime.datetime.now().strftime('%Y%m%d'))
    }

    def __init__(self, *args, **kwargs):
        super(CrawlAnjukeLianjiaResidentialSpider, self).__init__(*args, **kwargs)
        self.url_search = "https://tj.lianjia.com/xiaoqu/rs{residential_name}/"
        self.url_info = "https://tj.lianjia.com/ershoufang/housestat?hid={house_id}&rid={residential_id}"
        self.residential_name = None

        if 'args' in kwargs:
            params = {x[0]: x[1] for x in [[l for l in m.split(":")] for m in kwargs['args'].split(",")]}

            if "name" in params:
                self.residential_name = params['name'].decode("gbk").encode("utf-8")

            if "id" in params:
                self.anjuke_residential_id = params['id']

            print ("将开始抓取【%s】的链家详情" % self.residential_name).decode("utf-8")

    def start_requests(self):
        if self.residential_name:
            return [scrapy.Request(self.url_search.format(residential_name=self.residential_name),
                                   meta={'cookiejar': self.name, 'platform': 'pc'},
                                   callback=self.parse_residential_search)]
        else:
            print "Please input residential name"

    def parse_residential_search(self, response):
        href = response.xpath(".//ul[@class='listContent']/li/a/@href").extract_first()
        self.residential_id = href.split("/")[-2]
        print href, self.residential_id

        yield scrapy.Request(href, meta={'cookiejar': self.name, 'platform': 'pc'},
                             callback=self.get_residential_house_id)

    def get_residential_house_id(self, response):
        house_ids = response.xpath(".//div[@class='m-content']//a/@href").re(r"\/ershoufang\/(\d+)\.")
        print house_ids
        if len(house_ids) < 1:
            print "Nothing ershoufang got"
            house_ids = response.xpath(".//div[@class='m-content']//a/@href").re(r"\/chengjiao\/(\d+)\.")

        self.house_id = house_ids[0]

        yield scrapy.Request(self.url_info.format(house_id=self.house_id, residential_id=self.residential_id),
                             meta={'cookiejar': self.name, 'platform': 'pc'},
                             callback=self.get_parse_residential_info)


    def get_parse_residential_info(self, response):
        data = json.loads(response.body)
        data = data['data']

        item = {}

        item['lianjia_id'] = self.residential_id
        item['build_year'] = data['resblockCard']['buildYear']
        num_re = re.compile(r"(\d+)")
        build_year = num_re.findall(item['build_year'])
        item['build_year'] = build_year[0] if len(build_year) > 0 else 0

        item['build_num'] = data['resblockCard']['buildNum']
        build_num = num_re.findall(item['build_num'])
        item['build_num'] = build_num[0] if len(build_num) > 0 else 0

        item['build_type'] = data['resblockCard']['buildType']
        item['unit_price'] = data['resblockCard']['unitPrice']
        item['sell_num'] = data['resblockCard']['sellNum']
        item['rent_num'] = data['resblockCard']['rentNum']

        resblockPosition = data['resblockPosition'].split(",")
        item['longitude'] = resblockPosition[0]
        item['latitude'] = resblockPosition[1]
        item_agent = []

        agents = data['agentInfo']
        for a in agents:
            agent = agents[a]
            agent_item = {}
            agent_item['agent_id'] = agent['agentUcid']
            agent_item['reason'] = agent['reason']
            agent_item['name'] = agent['agentName']
            agent_item['agent_url'] = agent['agent_url']
            agent_item['agent_level'] = agent['agent_level']
            agent_item['agent_photo'] = agent['agent_photo']
            agent_item['feedback_good_rate'] = agent['feedbackGoodRate']
            agent_item['comment_count'] = agent['commentCount']
            agent_item['total_comment_score'] = agent['totalCommentScore']
            agent_item['agent_phone'] = agent['agent_phone']
            agent_item['type'] = 'agent'

            yield agent_item
            item_agent.append(agent['agentUcid'])

        item['agent'] = ",".join(item_agent)
        item['type'] = 'residential'
        item['anjuke_residential_id'] = self.anjuke_residential_id

        print item
        yield item