# -*- coding: utf-8 -*-
import scrapy
import datetime
from crawl.common.util import util

class CrawlCgseSpider(scrapy.Spider):
    name = 'crawl_cgse'
    allowed_domains = ['www.cgse.com.hk']
    start_urls = ['http://www.cgse.com.hk/cn/member_01_1.php']
    base_url = 'http://www.cgse.com.hk/cn/'

    custom_settings = {
        'LOG_FILE': 'logs/cgse_{dt}.log'.format(dt=datetime.datetime.now().strftime('%Y%m%d'))
    }

    def __init__(self):
        self.util = util()

    def parse(self, response):
        trs = response.xpath(
            ".//table[1]//tr[1]/td[2]/table[1]//tr[4]/td[2]/table[1]//tr[3]/td[1]/table//tr[2]/td[1]/table//tr")

        datas = {}
        for index, tr in enumerate(trs[1:]):
            data = {}
            data['no'] = tr.xpath(".//td[1]/div/text()").extract_first()
            data['name'] = tr.xpath(".//td[2]/div/text()").extract_first()
            idr = tr.xpath(".//td[3]/div/a/@href").extract_first()
            idr = idr if idr.startswith('http') else '%s%s' % (self.base_url, idr[1:])

            data['idr'] = self.util.get_url_param(idr)['id']
            data['executive_manager'] = tr.xpath(".//td[4]/div/text()").extract_first()
            data['executive_manager_ex'] = tr.xpath(".//td[5]/div/text()").extract_first()
            data['register_number'] = tr.xpath(".//td[6]/div/text()").extract_first()
            data['company_number'] = tr.xpath(".//td[7]/div/text()").extract_first()
            data['business_status'] = tr.xpath(".//td[8]/div/text()").extract_first()
            if data['business_status'] is None:
                data['business_status'] = tr.xpath(".//td[8]/div/font/text()").extract_first()

            datas[index] = data
            yield scrapy.Request(idr, meta={"cookiejar": self.name,
                                            'dont_redirect': True}, callback=self.parse_detail)

        yield datas

    def parse_detail(self, response):
        trs = response.xpath(".//table//tr[1]/td[1]/table[1]//tr[1]/td[1]/table[1]/tr")
        data = {}
        data['registe_address'] = trs[3].xpath(".//td[2]/text()").extract_first()
        data['website'] = trs[4].xpath(".//td[2]/text()").extract_first()
        data['tel'] = trs[5].xpath(".//td[2]/text()").extract_first()
        data['fax'] = trs[6].xpath(".//td[2]/text()").extract_first()
        idr = self.util.get_url_param(response.url)['id']
        data['idr'] = idr

        yield data