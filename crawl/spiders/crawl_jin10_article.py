# -*- coding: utf-8 -*-
import scrapy
import redis, random, json, datetime, os, time, re
from crawl.items import ArticleItem
from crawl.common.util import util

class CrawlJin10ArticleSpider(scrapy.Spider):
    name = 'crawl_jin10_article'
    allowed_domains = ['news.jin10.com']
    start_urls = ['http://news.jin10.com/']

    crawl_all_page = False

    r = redis.Redis(host="127.0.0.1", port=6379, db=0)
    detail_pages = []
    categories = [
        { 'id': '4', 'name': '原油', 'page_count': 0, 'page_index': 1 },
        { 'id': 'thinktank', 'name': '午读', 'page_count': 0, 'page_index': 1 },
        { 'id': '5', 'name': '贵金属', 'page_count': 0, 'page_index': 1 },
        { 'id': '7', 'name': '外汇', 'page_count': 0, 'page_index': 1 },
        { 'id': '19', 'name': '行情', 'page_count': 0, 'page_index': 1 },
        { 'id': '13', 'name': '独家', 'page_count': 0, 'page_index': 1 },
        { 'id': 'trading', 'name': '交易智慧', 'page_count': 0, 'page_index': 1 }
    ]

    cat_index = 0
    detail_url = 'https://news.jin10.com/details.html?id={id}'
    detail_json_url = 'https://news.jin10.com/datas/details/{id}.json'

    custom_settings = {
        'LOG_FILE': 'logs/jin10_article_{dt}.log'.format(dt=datetime.datetime.now().strftime('%Y%m%d'))
    }

    def __init__(self, *args, **kwargs):
        self.util = util()
        super(CrawlJin10ArticleSpider, self).__init__(*args, **kwargs)
        if kwargs and "all" in kwargs:
            self.crawl_all_page = bool(kwargs['all'])

    def start_requests(self):
        # 保存cookie，同时模拟浏览器访问过程，设置refer
        return [scrapy.Request("https://news.jin10.com/", meta={'cookiejar': self.name}, callback=self.parse_cookie)]

    def parse_cookie(self, response):
        yield scrapy.Request("https://news.jin10.com/list.html?cate=4&p=1",
                             meta={'cookiejar': self.name}, callback=self.set_refer)

    def set_refer(self, response):
        yield scrapy.Request(
            "https://news.jin10.com/datas/cate/{cat}/main.json".format(cat=self.categories[self.cat_index]['id']),
            meta={'cookiejar': self.name}, callback=self.parse_list)

    def parse_list(self, response):
        json_data = json.loads(response.body)
        self.categories[self.cat_index]['page_count'] = int(json_data['totalPage'])
        cat_now = self.categories[self.cat_index]
        list_url = self.get_list_url(cat_now)

        yield scrapy.Request(
            list_url,
            meta={'cookiejar': self.name}, callback=self.parse_info)

    def parse_info(self, response):
        json_data = json.loads(response.body)

        for index,dt in enumerate(json_data):
            if not dt['redirect_url']:
                image = os.path.basename(dt['thumb'])
                image_path = self.util.downfile(dt['thumb'], image)
                source_url = self.detail_json_url.format(id=dt['id'])

                item = {
                    'title': dt['title'],
                    'image': image_path,
                    'description': dt['desc'],
                    'keywords': dt['keyword'],
                    'publish_time': dt['time_show'],
                    'type': self.categories[self.cat_index]['name'],
                    'source_url': source_url,
                    'source_site': 'jin10',
                    'source_id': self.util.get_sourceid(source_url)
                }

                yield item
                self.r.sadd('jin10:page', item['source_url'])

        self.categories[self.cat_index]['page_index'] += 1
        cat_now = self.categories[self.cat_index]

        if self.crawl_all_page and cat_now['page_index'] <= cat_now['page_count']:
            list_url = self.get_list_url(cat_now)

            yield scrapy.Request(list_url,
                meta={'cookiejar': self.name}, callback=self.parse_info)

        elif self.cat_index < len(self.categories) - 1:
            self.cat_index += 1
            cat_now = self.categories[self.cat_index]
            main_url = "https://news.jin10.com/datas/cate/{cat}/main.json"
            if not cat_now['id'].isdigit():
                main_url = "https://news.jin10.com/datas/tags/{cat}/main.json"

            yield scrapy.Request(
                main_url.format(cat=self.categories[self.cat_index]['id']),
                meta={'cookiejar': self.name}, callback=self.parse_list)
        else:
            details_first = self.get_detail_page()
            if details_first:
                yield scrapy.Request(details_first, meta={'cookiejar': self.name}, callback=self.parse_body)

    def get_list_url(self, cat_now):
        print ('crawl cat %s, page %s' % (cat_now['name'], cat_now['page_index'])).encode('gbk')
        list_url = "https://news.jin10.com/datas/cate/{cat}/p{page}.json"
        if not cat_now['id'].isdigit():
            list_url = "https://news.jin10.com/datas/tags/{cat}/p{page}.json"

        return list_url.format(cat=cat_now['id'], page=(cat_now['page_count'] + 1 - cat_now['page_index']))

    def get_detail_page(self):
        page = self.r.spop('jin10:page')
        return page

    def parse_body(self, response):
        body = json.loads(response.body)
        if 'text' in body:
            item = {}

            item['source_id'] = self.util.get_sourceid(response.url)
            item['source_url'] = response.url
            item['body'] = self.util.handle_body(body['text'])

            yield item

        detail_page = self.get_detail_page()
        if detail_page:
            yield scrapy.Request(detail_page, meta={'cookiejar': self.name}, callback=self.parse_body)