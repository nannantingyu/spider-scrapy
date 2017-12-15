# -*- coding: utf-8 -*-
import scrapy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import datetime, redis, re, json
import crawl.settings as settings
from crawl.Common.Util import util
from crawl.items import LianjiaHouseItem

class CrawlLianjiaSpider(scrapy.Spider):
    name = 'crawl_lianjia'
    allowed_domains = ['lianjia.com']
    start_urls = ['http://tj.lianjia.com/ershoufang/rs/']

    custom_settings = { 'LOG_FILE': 'logs/lianjia_{dt}.log'.format(dt=datetime.datetime.now().strftime('%Y%m%d'))}

    def __init__(self, *args, **kwargs):
        self.areas = [
            {"name": "heping", "page": 0, "now": 1},
            {"name": "nankai", "page": 0, "now": 1},
            {"name": "hexi", "page": 0, "now": 1},
            {"name": "hebei", "page": 0, "now": 1},
            {"name": "hedong", "page": 0, "now": 1},
            {"name": "hongqiao", "page": 0, "now": 1},
            {"name": "xiqing", "page": 0, "now": 1},
            {"name": "beichen", "page": 0, "now": 1},
            {"name": "dongli", "page": 0, "now": 1},
            {"name": "jinnan", "page": 0, "now": 1},
            {"name": "tanggu", "page": 0, "now": 1},
            {"name": "kaifaqu", "page": 0, "now": 1},
            {"name": "diyidajie", "page": 0, "now": 1},
            {"name": "dierdajie", "page": 0, "now": 1},
            {"name": "disandajie", "page": 0, "now": 1},
            {"name": "disidajie", "page": 0, "now": 1},
            {"name": "diwudajie", "page": 0, "now": 1}
        ]

        self.area_now = 0
        self.util = util()
        self.list_url = 'https://tj.lianjia.com/ershoufang/{area}/pg{page}/'
        self.r = redis.Redis(host=settings.REDIS['host'], port=settings.REDIS['port'])

        super(CrawlLianjiaSpider, self).__init__(*args, **kwargs)
        if kwargs and "page" in kwargs:
            try:
                self.page_all = int(kwargs['page'])
            except TypeError, e:
                self.page_all = 100

        if 'args' in kwargs:
            params = {x[0]: x[1] for x in [[l for l in m.split(":")] for m in kwargs['args'].split(",")]}
            if "start" in params:
                try:
                    self.page_now = int(params['start'])
                except Exception as error:
                    self.page_now = 1

            if "page" in params:
                try:
                    self.page_all = int(params['page'])
                except Exception as err:
                    self.page_now = self.page_now + 1


    def start_requests(self):
        url = self.next_url()
        if url is not None:
            return [scrapy.Request(url, meta={'cookiejar': self.name}, callback=self.parse_list)]

    def parse_list(self, response):
        area = self.areas[self.area_now]
        if area['page'] == 0:
            page = response.xpath(".//div[@class='page-box house-lst-page-box']/@page-data").extract_first()
            if page is not None and "totalPage" in page:
                page = json.loads(page)
                page = page['totalPage']
            else:
                page = 1

            print page
            self.areas[self.area_now]['page'] = page


        lis = response.xpath("//div[@class='leftContent']/ul[@class='sellListContent']/li")
        for li in lis:
            href = li.xpath("./a[contains(@class, 'img')]/@href").extract_first() #链接

            self.r.sadd("lianjia:detail", href)
            source_id = util.get_sourceid(href)
            house_id_pat = re.compile(r"ershoufang\/(\d+)\.html")
            house_id = house_id_pat.findall(href)
            house_id = house_id[0] if len(house_id) > 0 else None
            print href, house_id

            img_desc = li.xpath("./a[contains(@class, 'img')]/img/@src").extract_first()  #缩略图
            img_desc = self.util.downfile(img_desc)

            info = li.xpath("./div[contains(@class, 'info')]")
            title = info.xpath("./div[@class='title']/a/text()").extract_first()   #标题
            house_info = info.xpath("./div[@class='address']/div[@class='houseInfo']")
            hinfo = house_info.xpath("./text()").extract_first()
            residential = house_info.xpath("./a/text()").extract_first()   #小区
            hinfo = hinfo.split("|") if hinfo is not None else []
            direction = hinfo[3] if len(hinfo) > 3 else ""  #朝向

            related_name = info.xpath("./div[@class='flood']/div[@class='positionInfo']/a/text()").extract_first()  #相关搜索
            related_href = info.xpath(
                "./div[@class='flood']/div[@class='positionInfo']/a/@href").extract_first()  # 相关搜索链接

            followInfo = info.xpath("./div[@class='followInfo']/text()").extract_first()
            followInfo = followInfo.split("/") if followInfo is not None else []
            followed = followInfo[0].replace('人关注', '') if len(followInfo) > 0 else ""
            visited = followInfo[1].replace('共', '').replace('次带看', '') if len(followInfo) > 1 else ""
            pub_time = followInfo[2] if len(followInfo) > 2 else ""

            tag = info.xpath("./div[@class='tag']/span/text()").extract()

            price = info.xpath("./div[@class='priceInfo']/div[@class='totalPrice']/span/text()").extract_first()
            unit_price = info.xpath("./div[@class='priceInfo']/div[@class='unitPrice']/span/text()").extract_first()
            unit_price = unit_price.replace('单价', '').replace('元/平米', '') if unit_price is not None else ""

            if house_id is not None:
                item = LianjiaHouseItem()
                item['source_url'] = href
                item['source_id'] = source_id
                item['house_id'] = house_id
                item['img_desc'] = img_desc
                item['title'] = title
                item['residential'] = residential
                item['direction'] = direction
                item['followed'] = followed
                item['visited'] = visited
                item['pub_time'] = pub_time
                item['related_name'] = related_name
                item['related_href'] = related_href
                item['tag'] = ",".join(tag)
                item['price'] = price
                item['unit_price'] = unit_price

                yield item

        next_url = self.next_url()
        if next_url is not None:
            yield scrapy.Request(next_url, meta={'cookiejar': self.name}, callback=self.parse_list)

    def next_url(self):
        url = None
        area = self.areas[self.area_now]
        if area['now'] <= area['page'] or area['page'] == 0:
            url = self.list_url.format(area=area['name'], page=area['now'])
            self.areas[self.area_now]['now'] += 1
        elif self.area_now < len(self.areas):
            self.area_now += 1
            return self.next_url()

        print url
        return url