# -*- coding: utf-8 -*-
import scrapy
import datetime, redis, json, re
from crawl.items import CrawlEconomicCalendarItem, CrawlEconomicEventItem, CrawlEconomicHolidayItem

class CrawlJin10CalendarSpider(scrapy.Spider):
    name = 'crawl_jin10_calendar'
    allowed_domains = ['jin10.com']
    start_urls = ['http://rili.jin10.com/']

    date_now = datetime.datetime.now()
    max_days = None
    after_days = 60
    date_end = None

    r = redis.Redis(host="127.0.0.1", port=6379, db=0)
    custom_settings = {
        'LOG_FILE': 'logs/jin10_calendar_{dt}.log'.format(dt=datetime.datetime.now().strftime('%Y%m%d'))
    }

    def __init__(self, *args, **kwargs):
        super(CrawlJin10CalendarSpider, self).__init__(*args, **kwargs)
        if 'args' in kwargs:
            params = {x[0]: x[1] for x in [[l for l in m.split(":")] for m in kwargs['args'].split(",")]}

            if "start" in params:
                try:
                    date_pat = re.compile(r"\d{4}\-\d{2}\-\d{2}")
                    if len(date_pat.findall(params['start'])) == 0:
                        timedelta = datetime.timedelta(days=int(params['start']))
                        date_start = datetime.datetime.now() + timedelta
                    else:
                        date_start = datetime.datetime.strptime(params['start'], "%Y-%m-%d")

                    self.date_now = date_start
                except ValueError as error:
                    print params['start'] + ' 不是正确格式的时间，已默认从今天开始抓取'

            if "max" in params:
                try:
                    self.max_days = int(params['max'])
                except ValueError as err:
                    print params['max'] + ' 不是正确的抓取天数，已默认抓取全部数据'

            if "after" in params:
                try:
                    self.after_days = int(params['after'])
                except ValueError as err:
                    print params['after'] + ' 不是正确的向后抓取天数，已默认抓取今天之后60天的数据'

            if "jiedu" in params:
                self.jiedu = params['jiedu']

            if self.max_days is not None:
                date_diff = datetime.timedelta(days=int(self.max_days))
                self.date_end = self.date_now + date_diff
            else:
                date_diff = datetime.timedelta(days=int(self.after_days))
                self.date_end = datetime.datetime.now() + date_diff

    def start_requests(self):
        return [scrapy.Request("https://rili.jin10.com/", meta={'cookiejar': self.name},
                               callback=self.parse_cookie)]

    def parse_cookie(self, response):
        yield scrapy.Request(
            'https://ucenter.jin10.com/info?jsonpCallback=jQuery111106577188087567758_1502096954188&_=1502096954189',
            meta={"cookiejar": response.meta['cookiejar'], 'dont_redirect': True,
                  'handle_httpstatus_list': [301, 302]}, callback=self.parse_index)

    def parse_index(self, response):
        yield scrapy.Request(
            'https://rili.jin10.com/datas/{year}/{monthday}/economics.json'.format(year=self.date_now.year,
                                                                                   monthday=self.date_now.strftime(
                                                                                       "%m%d")),
            meta={"cookiejar": response.meta['cookiejar'], 'dont_redirect': True},
            callback=self.parse_calendar)

    def parse_calendar(self, response):
        data = json.loads(response.body)
        all_item = {}
        index = 0
        for dt in data:
            item = CrawlEconomicCalendarItem()
            item['country'] = dt['country']
            item['quota_name'] = dt['title']
            item['pub_time'] = dt['publictime']
            item['importance'] = dt['star']
            item['former_value'] = dt['previous']
            item['predicted_value'] = dt['consensus']
            item['published_value'] = dt['actual']
            item['influence'] = dt['status_name']
            item['source_id'] = dt['dataId']
            item['dataname'] = dt['dataname']
            item['datename'] = dt['datename']
            item['dataname_id'] = dt['datanameId']
            item['unit'] = dt['unit']

            self.r.sadd('jin10:jiedu', "%s_%s"%(item['dataname_id'], item['source_id']))
            all_item[index] = item
            index += 1
        yield all_item

        # 抓取财经事件
        yield scrapy.Request("https://rili.jin10.com/datas/{year}/{monthday}/event.json".format(year=self.date_now.year,
                                                                                                monthday=self.date_now.strftime(
                                                                                                    "%m%d")),
                             meta={"cookiejar": response.meta['cookiejar'],
                                   'dont_redirect': True},
                             callback=self.parse_event)

    def parse_event(self, response):
        data = json.loads(response.body)
        time_re = re.compile(r"^\d{2}:\d{2}")
        all_event_item = {}
        index_event = 0
        for dt in data:
            item = CrawlEconomicEventItem()
            dt_time = dt['public_time']
            if len(time_re.findall(dt_time)) > 0:
                dt_time = self.date_now.strftime("%Y-%m-%d {ori}:00".format(ori=dt_time))

            item['time'] = dt_time
            item['country'] = dt['country']
            item['city'] = dt['city']
            item['importance'] = dt['star']
            item['event'] = dt['eventcontent']
            item['date'] = self.date_now
            item['source_id'] = dt['id']

            all_event_item[index_event] = item
            index_event += 1
        yield all_event_item

        yield scrapy.Request(
            "https://rili.jin10.com/datas/{year}/{monthday}/holiday.json".format(year=self.date_now.year,
                                                                                 monthday=self.date_now.strftime("%m%d")),
                meta={"cookiejar": response.meta['cookiejar'], 'dont_redirect': True}, callback=self.parse_holiday)

    def parse_holiday(self, response):
        data = json.loads(response.body)
        all_holiday_items = {}
        index_holiday = 0
        for dt in data:
            item = CrawlEconomicHolidayItem()
            item['time'] = dt['date'][0:10]
            item['country'] = dt['country']
            item['market'] = dt['exchangename']
            item['holiday_name'] = dt['holidayname']
            item['detail'] = dt['note']
            item['date'] = self.date_now.strftime("%Y-%m-%d")
            item['source_id'] = dt['id']

            all_holiday_items[index_holiday] = item
            index_holiday += 1

        yield all_holiday_items

        dtadd = datetime.timedelta(days=1)
        self.date_now = self.date_now + dtadd

        if self.date_now < self.date_end:
            yield scrapy.Request(
                'https://rili.jin10.com/datas/{year}/{monthday}/economics.json'.format(year=self.date_now.year,
                                                                                       monthday=self.date_now.strftime("%m%d")),
                meta={"cookiejar": response.meta['cookiejar'], 'dont_redirect': True},
                callback=self.parse_calendar)