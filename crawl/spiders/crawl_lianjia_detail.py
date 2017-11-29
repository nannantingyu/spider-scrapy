# -*- coding: utf-8 -*-
import scrapy
import datetime, re, redis, json, time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import crawl.settings as settings
from crawl.common.util import util
from bs4 import BeautifulSoup
from crawl.items import LianjiaHouseItem

class CrawlLianjiaDetailSpider(scrapy.Spider):
    name = 'crawl_lianjia_detail'
    allowed_domains = ['lianjia.com']
    handle_httpstatus_list = [404, 500, 302, 301]
    start_urls = ['http://tj.lianjia.com/ershoufang/rs/']
    custom_settings = {'LOG_FILE': 'logs/lianjia_detail_{dt}.log'.format(dt=datetime.datetime.now().strftime('%Y%m%d'))}

    def __init__(self):
        self.util = util()
        self.r = redis.Redis(host=settings.REDIS['host'], port=settings.REDIS['port'])
        self.property_map = {
            "房屋户型": 'layout',
            "所在楼层": 'flood',
            "建筑面积": 'area',
            "户型结构": 'apartment_structure',
            "建筑类型": 'building_type',
            "装修情况": 'renovation',
            "梯户比例": 'ladder',
            "供暖方式": 'heating',
            "产权年限": 'property_term',
            "交易权属": 'ownership',
            "挂牌时间": 'list_time',
            "上次交易": 'last_trade',
            "房屋朝向": 'direction',
            "房屋用途": 'purpose',
            "房屋年限": 'hold_years',
            "抵押信息": 'mortgage',
            "房本备件": 'house_register',
            "核心卖点": 'core_point',
            "周边配套": 'periphery',
            "交通出行": 'traffic',
            "小区介绍": 'residential_desc',
            "户型介绍": 'layout_desc',
            "配备电梯": 'elevator'
        }

    def next_url(self):
        while True:
            house_href = self.r.spop('lianjia:detail')
            if house_href is None:
                return None

            house_id_pat = re.compile(r"ershoufang\/(\d+)\.html")
            house_id = house_id_pat.findall(house_href)
            house_id = house_id[0] if len(house_id) > 0 else None

            if house_id is None or self.r.get("lianjia:house:%s"%house_id) is None:
                print house_href
                return house_href
            else:
                print house_href, " all ready crawled."

    def start_requests(self):
        url = self.next_url()
        if url is not None:
            return [scrapy.Request(url, meta={'cookiejar': self.name}, callback=self.parse_detail)]

    def parse_detail(self, response):
        if response.status == 200:
            item = LianjiaHouseItem()
            images = response.xpath(".//ul[@class='smallpic']/li/img/@src").extract()
            all_img = []
            for img in images:
                img = img.replace("120x80", "900x600")
                all_img.append(self.util.downfile(img))

            item['images'] = ','.join(all_img)
            item['state'] = 1
            residential_id = response.xpath(".//div[@class='intro clear']/div[@class='container']/div[@class='fl l-txt']/a/@href").extract()
            # residential_id = residential_id[-1].re().extract_first()
            re_pat = re.compile(r"ershoufang\/c(\d+)")
            residential_id = re_pat.findall(residential_id[-1]) if len(residential_id) > 0 else []
            residential_id = residential_id[0] if len(residential_id) > 0 else None

            price = response.xpath(".//div[@class='overview']/div[@class='content']/div[@class='price ']/span[@class='total']/text()").extract_first()
            if price is None:
                price = response.xpath(".//div[@class='overview']/div[@class='content']/div[@class='price isRemove']/span[@class='total']/text()").extract_first()
                item['state'] = 0

            item['price'] = price

            around_info = response.xpath(".//div[@class='aroundInfo']/div[@class='areaName']/span[@class='info']")
            district = around_info.xpath(".//a[1]/text()").extract_first()
            street = around_info.xpath(".//a[2]/text()").extract_first()
            address_info = response.xpath("//div[@class='aroundInfo']/div[@class='areaName']/span[@class='info']").extract_first()
            house_id = response.xpath(".//div[@class='aroundInfo']/div[@class='houseRecord']/span[@class='info']/text()").extract_first()
            house_id = house_id.strip() if house_id is not None else None

            if residential_id is not None:
                item['residential_id'] = residential_id
                self.r.sadd('lianjia:residential', residential_id)
                self.r.set('lianjia:residential:%s'%residential_id, house_id)

            if address_info is not None:
                soup = BeautifulSoup(address_info, 'lxml')
                strs = []
                [strs.append(str.replace(u'\xa0', '')) if str.strip() else '' for str in soup.strings]
                address = strs[-1] if len(strs) > 0 else ""
                item['address'] = address

            self.r.sadd("lianjia:visited", house_id)
            self.r.sadd("lianjia:feedback", house_id)

            baseinfo = response.xpath(".//div[@class='introContent']//div[@class='content']/ul/li")
            for li in baseinfo:
                property_name = li.xpath("./span/text()").extract_first()
                property_value = li.xpath("./text()").extract_first()
                if property_value is None:
                    property_value = li.xpath("./span[2]/text()").extract_first()

                property_value = property_value.strip() if property_value is not None else None
                if property_name.encode("utf-8") in self.property_map:
                    item[self.property_map[property_name.encode("utf-8")]] = property_value

            character = response.xpath(".//div[@class='newwrap baseinform']//div[@class='baseattribute clear']")
            for ba in character:
                property_name = ba.xpath(".//div[@class='name']/text()").extract_first()
                property_value = ba.xpath(".//div[@class='content']/text()").extract_first()
                property_value = property_value.strip() if property_value is not None else ""

                if property_name.encode("utf-8") in self.property_map:
                    item[self.property_map[property_name.encode("utf-8")]] = property_value

            layout_info = response.xpath(".//div[@id='layout']//div[@class='content']")
            img_layout = layout_info.xpath(".//div[@class='imgdiv']/img/@src").extract_first()
            img_layout = img_layout.replace("240x180", "900x600") if img_layout else None

            if img_layout:
                img_layout = self.util.downfile(img_layout)
                item['img_layout'] = img_layout

            layout_list = layout_info.xpath(".//div[@id='infoList']/div[@class='row']")
            layout_datas = []
            for row in layout_list:
                l = {}
                l['name'] = row.xpath("./div[@class='col'][1]/text()").extract_first()
                l['area'] = row.xpath("./div[@class='col'][2]/text()").extract_first()
                l['direct'] = row.xpath("./div[@class='col'][3]/text()").extract_first()
                l['window'] = row.xpath("./div[@class='col'][4]/text()").extract_first()
                layout_datas.append(l)

            item['district'] = district
            item['street'] = street
            item['house_id'] = house_id
            item['layout_datas'] = json.dumps(layout_datas)

            if 'property_term' in item:
                item['property_term'] = item['property_term'].replace('年', '') if item['property_term'] is not None else ""
            if 'area' in item:
                item['area'] = item['area'].replace('㎡', '') if item['area'] is not None else ""

            redis_id = "lianjia:house:%s" % item["house_id"]
            self.r.set(redis_id, time.time())
            self.r.expire(redis_id, 3600*24*7)
            yield item

        url = self.next_url()
        if url is not None:
            yield scrapy.Request(url, meta={'cookiejar': self.name}, callback=self.parse_detail)

def myp(coup):
    for c in coup:
        print c.replace(u'\xa0', "") if c is not None else "Null"