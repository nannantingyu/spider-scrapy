# -*- coding: utf-8 -*-
import scrapy
import json, datetime, re

class CrawlJin10SsiTrendsTodaySpider(scrapy.Spider):
    name = 'crawl_jin10_ssi_trends_today'
    allowed_domains = ['jin10.com', 'cdn.jin10.com']
    start_urls = ['https://datacenter.jin10.com/get_dc_second_data?type=dc_ssi_shark_fx_current']

    custom_settings = {
        'LOG_FILE': 'logs/jin10_ssi_trends_today_{dt}.log'.format(dt=datetime.datetime.now().strftime('%Y%m%d'))
    }

    def parse(self, response):
        d_pat = re.compile(r"\((.*)\)")
        all_data = d_pat.findall(response.body)
        data = all_data[0] if len(all_data) > 0 else ''
        data = json.loads(data)
        pairs = data['data']['pairs']

        for index, trends in enumerate(pairs):
            for k, broker in enumerate(pairs[trends]):
                if 'oip' != broker:
                    item = {}
                    item['platform'] = broker
                    item['type'] = trends.lower()
                    item['long_position'] = pairs[trends][broker]
                    item['time'] = data['time']

                    yield item