# -*- coding: utf-8 -*-
import scrapy
import datetime, re

class CrawlZhanzhangSpider(scrapy.Spider):
    name = 'crawl_zhanzhang'
    allowed_domains = ['chinaz.com']
    start_urls = ['http://seo.chinaz.com/www.91pme.com']

    url_format = "http://rank.chinaz.com/{site}-0--0-{page}"
    page_all = None
    page_index = 0

    allsite = ['www.91pme.com']
    site_index = 0

    custom_settings = {
        'LOG_FILE': 'logs/chinaz_{dt}.log'.format(dt=datetime.datetime.now().strftime('%Y%m%d'))
    }

    def start_requests(self):
        return [scrapy.Request(self.url_format.format(page=self.page_index, site=self.allsite[self.site_index]),
                               meta={'cookiejar': self.name},
                               callback=self.count_page)]

    def count_page(self, response):
        if self.page_all is None:
            page_div = response.xpath(
                ".//div[contains(@class, 'ToolPage')]/div[@class='ToolPage-right fr']/span[@class='col-gray02']/text()").extract_first()
            page_re = re.compile(r"(\d+).+")
            page = page_re.findall(page_div)

            if len(page) > 0:
                self.page_all = int(page[0])
                self.parse_item(response)
                self.page_index += 1

        if self.page_all is not None and self.page_index < self.page_all:
            yield scrapy.Request(self.url_format.format(page=self.page_index, site=self.allsite[self.site_index]),
                                 meta={'cookiejar': self.name, 'dont_redirect': True,
                                       'handle_httpstatus_list': [301, 302, 404, 403]},
                                 callback=self.parse_item)

    def parse_item(self, response):
        lis = response.xpath(".//ul[@class='ResultListWrap']/li[@class='ReListCent ReLists bor-b1s clearfix']")
        for li in lis:
            keywords = li.xpath(
                "./div[@class='w25-0 tl pl10 pr pbimg']/a[@class='ellipsis block']/text()").extract_first()
            all_index = li.xpath("./div[@class='w8-0']/a/text()").extract()
            total_index = all_index[0] if len(all_index) > 0 else 0
            pc_index = all_index[1] if len(all_index) > 1 else 0
            mobile_index = all_index[2] if len(all_index) > 2 else 0
            baidu_index = all_index[3] if len(all_index) > 3 else 0

            shoulu_count = li.xpath("./div[@class='w8-0 bor-r1s05']/a/text()").extract_first()
            shoulu_page = li.xpath("./div[@class='w25-0 tl pl10 pbimg']/a/@onclick").re(r"window\.open\('(.+)'\)")
            shoulu_title = li.xpath("./div[@class='w25-0 tl pl10 pbimg']/a/text()").extract_first()
            shoulu_page = "" if len(shoulu_page) == 0 else shoulu_page[0]
            item = {}
            item['keywords'] = keywords
            item['total_index'] = total_index
            item['pc_index'] = pc_index
            item['mobile_index'] = mobile_index
            item['baidu_index'] = baidu_index
            item['shoulu_count'] = shoulu_count
            item['shoulu_page'] = shoulu_page
            item['shoulu_title'] = shoulu_title
            item['site'] = self.allsite[self.site_index]

            yield item

        self.page_index += 1
        if self.page_index <= self.page_all:
            yield scrapy.Request(self.url_format.format(page=self.page_index, site=self.allsite[self.site_index]),
                                 meta={'cookiejar': self.name},
                                 callback=self.parse_item)
        elif self.site_index < len(self.allsite) - 1:
            self.site_index += 1
            self.page_index = 0
            self.page_all = None
            yield scrapy.Request(self.url_format.format(page=self.page_index, site=self.allsite[self.site_index]),
                                 meta={'cookiejar': self.name},
                                 callback=self.count_page)