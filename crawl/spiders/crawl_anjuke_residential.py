# -*- coding: utf-8 -*-
import scrapy, datetime, re, sys
reload(sys)
sys.setdefaultencoding("utf-8")

class CrawlAnjukeResidentialSpider(scrapy.Spider):
    name = 'crawl_anjuke_residential'
    allowed_domains = ['anjuke.com']
    start_urls = ['http://anjuke.com/']

    custom_settings = {
        'LOG_FILE': 'logs/anjuke_residential_{dt}.log'.format(dt=datetime.datetime.now().strftime('%Y%m%d'))
    }

    def __init__(self, *args, **kwargs):
        super(CrawlAnjukeResidentialSpider, self).__init__(*args, **kwargs)
        self.url = "https://tianjin.anjuke.com/community/{area}/p{page}/"
        self.area = 0
        self.areas = [
            { "name": "北辰区", "code": "beichenqu", "page": 1 },
            { "name": "和平区", "code": "hepingc", "page": 1 },
            { "name": "河西区", "code": "hexi", "page": 1 },
            { "name": "宝坻区", "code": "baodiqu", "page": 1 },
            { "name": "南开区", "code": "nankai", "page": 1 },
            { "name": "蓟县", "code": "jizhouqujixian", "page": 1 },
            { "name": "静海", "code": "jinghaiqujinghaixian", "page": 1 },
            { "name": "宁河", "code": "ninghequninghexian", "page": 1 },
            { "name": "河北", "code": "hebei", "page": 1 },
            { "name": "河东", "code": "hedong", "page": 1 },
            { "name": "红桥", "code": "hongqiaob", "page": 1 },
            { "name": "滨海新区", "code": "binhaixinqu", "page": 1 },
            { "name": "西青", "code": "xiqing", "page": 1 },
            { "name": "津南", "code": "jinnan", "page": 1 },
            { "name": "东丽", "code": "dongli", "page": 1 },
            { "name": "武清", "code": "wuqingqu", "page": 1 },
            { "name": "天津周边", "code": "tianjinzhoubian", "page": 1 },
        ]

    def get_next_url(self):
        if self.area < len(self.areas):
            area = self.areas[self.area]
            url = self.url.format(area=area['code'], page=area['page'])

            print area['name'].encode("gbk"), area['page'], url
            area['page'] += 1

            return url

        return None

    def start_requests(self):
        url = self.get_next_url()
        return [scrapy.Request(url,
                               meta={'cookiejar': self.name, 'platform': 'pc'},
                               callback=self.get_residential)]

    def get_residential(self, response):
        divs = response.xpath(".//div[@id='list-content']//div[@class='li-info']")
        for div in divs:
            name = div.xpath(".//h3/a/text()").extract_first()
            residential_url = div.xpath(".//h3/a/@href").extract_first()
            residential_id = residential_url.split("/")[-1]
            build_year = div.xpath(".//p[@class='date']/text()").extract_first()
            try:
                build_year_re = re.compile(r"\d+")
                build_year = build_year_re.findall(build_year)
                build_year = build_year[0] if len(build_year) > 0 else 0
            except Exception, e:
                print "无法获取年份"

            print name, residential_url, residential_id, build_year
            yield {
                "residential": name,
                "residential_url": residential_url,
                "residential_id": residential_id,
                "build_year": build_year,
                "area": self.areas[self.area]['name']
            }

        next_page = response.xpath(".//div[@class='multi-page']/a[@class='aNxt']/text()").extract_first()
        if next_page is None and self.area < len(self.areas) - 1:
            self.area += 1

        url = self.get_next_url()
        if url:
            yield scrapy.Request(url, meta={'cookiejar': self.name, 'platform': 'pc'},
                                   callback=self.get_residential)