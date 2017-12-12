# -*- coding: utf-8 -*-
import scrapy
import datetime, redis
from crawl.items import CrawlWexinArticleItem
from crawl.common.util import util
from crawl.common.weixin_util import weixin_body_parser

class CrawlWeixinDetailSpider(scrapy.Spider):
    name = 'crawl_weixin_detail'

    allowed_domains = ["weixin.sogou.com", "mp.weixin.qq.com"]
    start_urls = ['http://weixin.gogou.com/']
    custom_settings = {
        'LOG_FILE': 'logs/weixin_detail_{dt}.log'.format(dt=datetime.datetime.now().strftime('%Y%m%d'))
    }

    def __init__(self):
        self.util = util()
        self.r = redis.Redis(host="127.0.0.1", port=6379, db=0)
        self.item_index = 0

    def start_requests(self):
        detail_url = self.get_next_url()
        if detail_url is not None:
            return [scrapy.Request(detail_url, meta={'cookiejar': self.name, 'dont_redirect': True,
                                         'handle_httpstatus_list': [301, 302, 404]},
                                   callback=self.parse_detail)]

    def get_next_url(self):
        url = self.r.spop('weixin_url')
        return url

    def parse_detail(self, response):
        self.item_index += 1
        body = response.xpath(".//div[@id='js_content']").extract_first()
        item = CrawlWexinArticleItem()
        item['body'] = weixin_body_parser.parse(body) if body else body

        try:
            print item['body']
        except Exception, e:
            print e

        url_param = self.util.get_url_param(response.url)
        source_id = url_param['source_id']
        item['source_id'] = source_id

        if body:
            yield item

        detail_url = self.get_next_url()
        print detail_url
        if detail_url is not None:
            yield scrapy.Request(detail_url,
                                 meta={'cookiejar': self.name, 'dont_redirect': True,
                                       'handle_httpstatus_list': [301, 302, 404]},
                                 errback=self.parse_error,
                                 callback=self.parse_detail)

    def parse_error(self, failure):
        detail_url = self.get_next_url()
        if detail_url is not None:
            yield scrapy.Request(detail_url,
                                 meta={'cookiejar': self.name, 'dont_redirect': True,
                                       'handle_httpstatus_list': [301, 302, 404]},
                                 errback=self.parse_error, callback=self.parse_detail)
