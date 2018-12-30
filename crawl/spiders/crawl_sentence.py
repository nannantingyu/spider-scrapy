# -*- coding: utf-8 -*-
import scrapy, datetime
from crawl.Common.Util import util

class CrawlSentenceSpider(scrapy.Spider):
    name = 'crawl_sentence'
    allowed_domains = ['www.59xihuan.cn']
    start_urls = ['http://http://www.59xihuan.cn//']

    custom_settings = {'LOG_FILE': 'logs/sentence_{dt}.log'.format(dt=datetime.datetime.now().strftime('%Y%m%d'))}

    def __init__(self):
        self.base_url = "http://www.59xihuan.cn/jingdianyulu_10_{page}.html"
        self.page_now = 200
        self.max_page = 400

    def get_next(self):
        url = None
        if self.page_now < self.max_page:
            url = self.base_url.format(page=self.page_now)
            self.page_now += 1

        return url

    def start_requests(self):
        return [scrapy.Request(self.get_next(), meta={'cookiejar': self.name}, callback=self.parse_list)]

    def parse_list(self, response):
        contents = response.xpath("//div[@class='main']/div[@class='mLeft']/div[@class='post']/div[@class='mixed1']/div[@class='pic_text1']/text()").extract()

        for content in contents:
            content = content.strip().replace("\n", "").replace("\r", "") if content else ""
            if content is not None and content != '':
                item = {
                    "content": content,
                    "source_id": util.get_sourceid(content)
                }

                yield item
                print content

        url = self.get_next()
        if url:
            yield scrapy.Request(self.get_next(), meta={'cookiejar': self.name}, callback=self.parse_list)
