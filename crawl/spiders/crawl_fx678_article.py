# -*- coding: utf-8 -*-
import scrapy
import redis, datetime, time, re
from crawl.common.util import util
from crawl.items import ArticleItem

class CrawlFx678ArticleSpider(scrapy.Spider):
    name = 'crawl_fx678_article'
    allowed_domains = ['brokers.fx678.com']
    start_urls = ['http://brokers.fx678.com/articlelist/10103/']

    r = redis.Redis(host="127.0.0.1", port=6379, db=0)

    type_maps = [
        { 'id': 10103, 'name': '成交观察', 'page': 0 },
        # { 'id': 101, 'name': '行业要闻', 'page': 0 },
        # { 'id': 10102, 'name': '经纪商动态', 'page': 0 },
        # { 'id': 10104, 'name': '行业相关', 'page': 0 }
    ]

    custom_settings = {
        'LOG_FILE': 'logs/fx678_article_{dt}.log'.format(dt=datetime.datetime.now().strftime('%Y%m%d'))
    }

    def __init__(self, *args, **kwargs):
        self.util = util()
        self.url_format = 'http://brokers.fx678.com/articlelist/{id}/{page}'
        self.type_index = 0
        self.page_index = 1
        self.max_page = 1

        super(CrawlFx678ArticleSpider, self).__init__(*args, **kwargs)
        if kwargs and "max" in kwargs:
            self.max_page = int(kwargs['max'])

    def start_requests(self):
        url = self.get_next()
        if url:
            return [scrapy.Request(url, meta={'cookiejar': self.name}, callback=self.parse_list)]

    def parse_list(self, response):
        type_now = self.type_maps[self.type_index]
        if type_now['page'] == 0:
            page_re = response.xpath('//ul[@id="showpage"]/li[@class="end"]/a/@href').re(r".*" + str(type_now['id']) + "\/(\d+)")
            type_now['page'] = int(page_re[0])

        lists = response.xpath("//div[@class='ym2_icon1 item clearfix']")
        for li in lists:
            info = li.xpath(".//p[@class='ym2_txt1']/a")
            title = info.xpath("./text()").extract_first()
            href = info.xpath("./@href").extract_first()

            img = li.xpath("./div[@class='clearfix ym2_ypi']/a/img/@src").extract_first()
            description = li.xpath("./div[@class='clearfix ym2_ypi']/p[@class='fl ym2_txt2']/a/text()").extract_first()
            pub_time = li.xpath("./div[@class='ym2_txt3 clearfix']/div[@class='fl ym2_ywxx']/text()").extract_first()

            img_name_pat = re.compile(r".*upload\/ht\/\d+\/(.*)")
            img_name = img_name_pat.findall(img)[0]
            img_path = self.util.downfile(img, img_name)

            href = href if href.startswith('http') else 'http://brokers.fx678.com' + href

            item = ArticleItem()
            item['title'] = title
            item['source_url'] = href
            item['image'] = img_path
            item['description'] = description
            item['publish_time'] = pub_time
            item['type'] = type_now['name']
            item['source_site'] = 'fx678'
            item['source_id'] = self.util.get_sourceid(href)

            yield item
            self.r.sadd('fx678:page', item['source_url'])

        self.move_next()
        url = self.get_next()

        if url:
            print url
            yield scrapy.Request(url, meta={'cookiejar': self.name}, callback=self.parse_list)

        else:
            detail_page = self.get_detail_page()
            if detail_page:
                yield scrapy.Request(detail_page, meta={'cookiejar': self.name}, callback=self.parse_detail)

    def parse_detail(self, response):
        body = response.xpath(".//div[@class='xw_l fl']/div[@class='xwl_ico3']/p").extract_first()
        publish_time = response.xpath(".//div[@class='xw_l fl']//div[@class='xwl_text clearfix']//div[@class='fl']/span/text()").extract_first()

        item = ArticleItem()

        item['publish_time'] = publish_time
        item['body'] = self.util.handle_body(body)
        item['source_site'] = 'fx678'
        item['source_id'] = self.util.get_sourceid(response.url)
        item['source_url'] = response.url

        yield item

        detail_page = self.get_detail_page()
        if detail_page:
            yield scrapy.Request(detail_page, meta={'cookiejar': self.name}, callback=self.parse_detail)

    def get_next(self):
        url = None
        if self.type_index < len(self.type_maps):
            type_now = self.type_maps[self.type_index]
            url = self.url_format.format(id=type_now['id'], page = self.page_index)

        return url

    def move_next(self):
        type_now = self.type_maps[self.type_index]
        if self.page_index < type_now['page'] and self.page_index < self.max_page:
            self.page_index += 1
        else:
            self.page_index = 1
            self.type_index += 1

    def get_detail_page(self):
        page = self.r.spop('fx678:page')
        return page