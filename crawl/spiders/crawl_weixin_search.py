# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from crawl.common.util import util
from crawl.items import CrawlWexinArticleItem
import redis, json, urllib, datetime, scrapy, time
from crawl.settings import REDIS

class CrawlWeixinSearchSpider(scrapy.Spider):
    name = "crawl_weixin_search"
    allowed_domains = ["weixin.sogou.com", "mp.weixin.qq.com"]
    start_urls = [
        'http://weixin.sogou.com/weixin?usip=&query=%E5%A4%A7%E7%B1%B3&ft=&tsn=1&et=&interation=&type=2&wxid=&page=2&ie=utf8']

    custom_settings = {
        'LOG_FILE': 'logs/weixin_search_{dt}.log'.format(dt=datetime.datetime.now().strftime('%Y%m%d'))
    }

    def __init__(self, *args, **kwargs):
        super(CrawlWeixinSearchSpider, self).__init__(*args, **kwargs)
        self.util = util()
        self.r = redis.Redis(host=REDIS['host'], port=REDIS['port'])
        self.page_url = "http://weixin.sogou.com/weixin?usip=&query={query}&ft=&tsn=1&et=&interation=&type=2&wxid=&page={page}&ie=utf8"
        self.type_index = 0
        self.type = [ {'name': '五常大米', 'page_now': 1, 'page_all': 2} ]
        self.only_hot = False

        if 'args' in kwargs:
            params = {x[0]: x[1] for x in [[l for l in m.split(":")] for m in kwargs['args'].split(",")]}

            if "hot" in params:
                self.only_hot = True
                print "Only crawl hot keywords"

    def start_requests(self):
        # 种cookie
        return [scrapy.Request('http://weixin.sogou.com/websearch/wexinurlenc_sogou_profile.jsp',
                               meta={'cookiejar': self.name, 'handle_httpstatus_list': [301, 302, 403]},
                               callback=self.parse_cookie)]

    def parse_cookie(self, response):
        yield scrapy.Request(
            'http://weixin.sogou.com/weixin?type=2&query={query}&ie=utf8&s_from=input&_sug_=n&_sug_type_=&w=01015002&oq=&ri=0&sourceid=sugg&sut=375&sst0=1502699460309&lkt=1%2C1502699460207%2C1502699460207'.format(
                query=urllib.quote(self.type[self.type_index]['name'])),
            meta={'cookiejar': self.name, 'dont_redirect': True, 'handle_httpstatus_list': [301, 302, 403]},
            callback=self.parse_referer)

    def parse_referer(self, response):
        url = self.get_next_page()
        if url:
            yield scrapy.Request(url, meta={'cookiejar': self.name, 'dont_redirect': True,
                                   'handle_httpstatus_list': [301, 302, 400]},
                             callback=self.parse)

    def get_next_page(self):
        ret = None

        if self.type_index < len(self.type) and not self.only_hot:
            type_now = self.type[self.type_index]
            self.type[self.type_index]['page_now'] += 1
            if type_now['page_now'] > type_now['page_all']:
                self.type_index += 1

                return self.get_next_page()

            if self.type_index < len(self.type):
                ret = self.page_url.format(query=urllib.quote(type_now['name']),
                                           page=type_now['page_now'])
                self.typename = type_now['name']
        else:
            # 从redis读取热门搜索词
            keywords = self.r.spop("weixin_hot_keywords")
            if keywords:
                ret = self.page_url.format(query=urllib.quote(keywords), page=1)
                self.typename = keywords

        return ret

    def parse(self, response):
        if response.status != 400:
            lis = response.xpath("//ul[@class='news-list']/li")
            all_items = {}

            page_all = response.xpath("//div[@id='pagebar_container']/a/text()").extract()
            if not self.only_hot and self.type[self.type_index]['page_all'] == 0:
                if len(page_all) > 1:
                    page_all = int(page_all[-2]) if str(page_all[-2]).isdigit() else 1
                    if self.type[self.type_index]['page_all'] > page_all:
                        self.type[self.type_index]['page_all'] = page_all

            for item_index, li in enumerate(lis):
                img = li.xpath(".//div[@class='img-box']/a/img/@src").extract()

                source_url = li.xpath(".//div[@class='txt-box']/h3/a/@href").extract_first()
                if not source_url.startswith("http"):
                    continue

                print source_url
                title = BeautifulSoup(li.xpath(".//div[@class='txt-box']/h3/a").extract_first(), 'lxml')
                title = title.find('a').getText()
                description = li.xpath(".//div[@class='txt-box']/p[@class='txt-info']").extract_first()
                description = BeautifulSoup(description, "lxml")
                description = description.find("p").getText()
                img_d = li.xpath(".//div[@class='txt-box']/div[@class='img-d']/a/span/img/@src").extract()
                img.extend(img_d)

                imgs = []
                for _img in img:
                    _img_name = self.util.downfile(_img)
                    imgs.append(_img_name)

                time.localtime()
                img = json.dumps(imgs)
                from_user = li.xpath(".//div[@class='txt-box']//div[@class='s-p']/a/text()").extract_first()
                source_id = self.util.get_sourceid(str(from_user) + str(title))

                publish_time = li.xpath(".//div[@class='txt-box']//div[@class='s-p']/span[@class='s2']/script").re(
                    r"\w+Convert\('(.+?)'\)")
                publish_time = datetime.datetime.now() if len(publish_time) == 0 else datetime.datetime.strptime(
                    time.strftime("%Y-%m-%d", time.localtime(int(publish_time[0]))), "%Y-%m-%d")

                item = CrawlWexinArticleItem()
                item['title'] = title
                item['source_url'] = str(source_url)
                item['source_id'] = source_id
                item['description'] = description
                item['image'] = img
                item['from_user'] = from_user
                item['type'] = self.typename
                item['publish_time'] = publish_time

                if not self.r.sismember("crawl_source_id", source_id):
                    self.r.sadd("crawl_source_id", source_id)
                    self.r.sadd("weixin_url", "{url}&source_id={source_id}".format(url=source_url, source_id=source_id))

                    all_items[item_index] = item

            yield all_items

        next_url = self.get_next_page()
        if next_url:
            yield scrapy.Request(next_url, meta={'cookiejar': self.name, 'dont_redirect': True,
                                       'handle_httpstatus_list': [301, 302, 400]},
                                 callback=self.parse)