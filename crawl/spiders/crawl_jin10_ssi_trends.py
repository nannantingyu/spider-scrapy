# -*- coding: utf-8 -*-
import scrapy
import datetime, json, re

class CrawlJin10SsiTrendsSpider(scrapy.Spider):
    name = 'crawl_jin10_ssi_trends'
    allowed_domains = ['jin10.com', 'cdn.jin10.com']
    start_urls = ['http://datacenter.jin10.com/reportType/dc_ssi_trends/']

    trends = [
        'audjpy', 'audusd', 'euraud', 'eurjpy', 'eurusd', 'gbpjpy', 'gbpusd', 'nzdusd', 'usdcad', 'usdchf', 'usdjpy',
        'xauusd', 'usdx'
    ]

    brokers = [
        'forxfact', 'saxobank', 'myfxbook', 'instfor', 'ftroanda', 'fiboforx', 'dukscopy', 'alpari', 'fxcm'
    ]

    url_pat = 'https://cdn.jin10.com/dc/reports/dc_real_time_data_{trend}_{broker}_{date}.js'
    custom_settings = {
        'LOG_FILE': 'logs/jin10_ssi_trends_{dt}.log'.format(dt=datetime.datetime.now().strftime('%Y%m%d'))
    }

    trend_index = 0
    broker_index = 0
    date_start = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d")

    def __init__(self, *args, **kwargs):
        super(CrawlJin10SsiTrendsSpider, self).__init__(*args, **kwargs)
        if 'args' in kwargs:
            params = {x[0]: x[1] for x in [[l for l in m.split(":")] for m in kwargs['args'].split(",")]}

            if "start" in params:
                try:
                    self.date_start = datetime.datetime.strptime(params['start'], "%Y%m%d")
                except ValueError as error:
                    print params['start'] + ' 不是正确格式的时间，已默认抓取昨天'

    def start_requests(self):
        return [scrapy.Request(self.start_urls[0], meta={'cookiejar': self.name}, callback=self.parse_url)]

    def next_url(self):
        url = None

        if self.broker_index < len(self.brokers):
            url = self.url_pat.format(trend=self.trends[self.trend_index], broker=self.brokers[self.broker_index],
                                      date=self.date_start)

        if self.trend_index < len(self.trends) - 1:
            self.trend_index += 1
        else:
            self.trend_index = 0
            self.broker_index += 1

        return url

    def parse_url(self, response):
        url = self.next_url()
        print url
        if url is not None:
            yield scrapy.Request(url, meta={'cookiejar': self.name, 'handle_httpstatus_list': [301, 302, 404]},
                                 callback=self.parse_page)

    def parse_page(self, response):
        print response.status, response.url
        if response.status != 404:
            r_url = response.url

            para_pat = re.compile(r"dc_real_time_data_(\w+)_(\w+)_(\w+).js")
            params = para_pat.findall(r_url)

            data = response.body.replace('var dc_real_time_data = ', '')
            data = json.loads(data)

            all_items = {}
            for no, line in enumerate(data['data']):
                item = {}
                item['platform'] = params[0][1]
                item['type'] = params[0][0]
                item['time'] = line['time']
                item['long_position'] = line['data']
                all_items[no] = item

            yield all_items

        url = self.next_url()
        if url is not None:
            yield scrapy.Request(url, meta={'cookiejar': self.name, 'handle_httpstatus_list': [301, 302, 404]},
                                 callback=self.parse_page)