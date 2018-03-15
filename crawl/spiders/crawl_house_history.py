# -*- coding: utf-8 -*-
import scrapy, datetime, re, json, sys
reload(sys)
sys.setdefaultencoding("utf-8")

class CrawlHouseHistorySpider(scrapy.Spider):
    name = 'crawl_house_history'
    allowed_domains = ['anjuke.com']
    start_urls = ['http://www.anjuke.com/']

    custom_settings = {
        'LOG_FILE': 'logs/house_history_{dt}.log'.format(dt=datetime.datetime.now().strftime('%Y%m%d'))
    }

    def __init__(self, *args, **kwargs):
        super(CrawlHouseHistorySpider, self).__init__(*args, **kwargs)
        self.url_residential = "https://tianjin.anjuke.com/community/?kw={residential_name}"
        self.url = "https://www.anjuke.com/fangjia/tianjin{year}/xq{residential_id}/"

        if 'args' in kwargs:
            params = {x[0]: x[1] for x in [[l for l in m.split(":")] for m in kwargs['args'].split(",")]}

            if "name" in params:
                self.residential_name = params['name'].decode("gbk").encode("utf-8")

            if "id" in params:
                self.residential_id = params['id']

            if "year" in params:
                self.year = params['year']
            else:
                self.year = datetime.datetime.now().year

            self.year += 1

            print ("将开始抓取%s，从%s开始的房价走势" % (self.residential_name, str(self.year))).decode("utf-8").encode("gbk")

    def start_requests(self):
        return [scrapy.Request(self.url_residential.format(residential_name=self.residential_name),
                               meta={'cookiejar': self.name, 'platform': 'pc'},
                               callback=self.get_residential_id)]


    def get_residential_id(self, response):
        with open("index.html", "w") as fs:
            fs.write(response.body)

        residential = response.xpath(".//div[@class='li-info']/h3/a[@title='%s']" % unicode(self.residential_name, "utf-8"))
        title = residential.xpath("./text()").extract_first()
        href = residential.xpath("./@href").extract_first()
        build_year = residential.xpath("./parent::h3/parent::div[@class='li-info']/p[@class='date']/text()").extract_first()
        try:
            build_year_re = re.compile(r"\d+")
            build_year = build_year_re.findall(build_year)
            build_year = build_year[0]
        except Exception,e:
            print "无法获取年份"

        self.house_url = href
        self.build_year = build_year
        self.residential_id = href.split("/")[-1]

        self.item = {
            "residential": self.residential_name,
            "house_url": href,
            "build_year": build_year,
            "residential_id": self.residential_id
        }

        print self.item
        yield scrapy.Request(self.get_next_year(),
                               meta={'cookiejar': self.name},
                               callback=self.parse_house)

    def parse_house(self, response):
        data = response.xpath(".//script").re(r"window\.drawChart\(([\s\S]*?)\);")
        if data:
            data = data[0].replace("\r", "").replace("\n", "").replace("\t", "")
            comment_re = re.compile(r"(\/\/.*?\]\}\])\}")
            data_comment = comment_re.findall(data)
            if len(data_comment) > 0:
                data = data.replace(data_comment[0], "")

        try:
            xdata_re = re.compile(r"xyear\:\s*(.*),ydata")
            xdata = xdata_re.findall(data)
            xdata = json.loads(xdata[0])
            year_month = []
            for x in xdata:
                print x, xdata[x]
                year_month.append((int(xdata[x].replace("年", "")), int(x.replace("月", ""))))

            year_month = sorted(year_month)

            ydata_re = re.compile(r"ydata\:\s*\[(.*)\]\}")
            ydata = ydata_re.findall(data)
            ydata = json.loads(ydata[0])

            for i, dt in enumerate(ydata['data']):
                item = {
                    "year": year_month[i][0],
                    "month": year_month[i][1],
                    "price": dt
                }

                item.update(self.item)
                yield item
        except Exception, e:
            print e
        else:
            next_url = self.get_next_year()
            if next_url:
                yield scrapy.Request(next_url,
                                       meta={'cookiejar': self.name},
                                       callback=self.parse_house)

    def get_next_year(self):
        if self.year >= 2006:
            self.year -= 1
        else:
            return None

        print ("抓取%s小区%d年的历史价格" % (self.residential_name, self.year)).encode("gbk")
        url = self.url.format(year=self.year, residential_id=self.residential_id)
        return url