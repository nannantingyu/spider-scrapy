# -*- coding: utf-8 -*-
import scrapy
import datetime, json, random, redis, urllib, time, math, os, json
from crawl.common.util import util, Verify
from crawl.items import CrawlBaiduRateItem
import crawl.settings as settings

class CrawlBaiduRateSpider(scrapy.Spider):
    name = 'crawl_baidu_rate'
    cookie_name = 'crawl_baidu'
    allowed_domains = ['baidu.com']
    handle_httpstatus_list = [404, 500, 302, 301]
    start_urls = ['http://tongji.baidu.com/']

    custom_settings = {
        'LOG_FILE': 'logs/baidu_rate_{dt}.log'.format(dt=datetime.datetime.now().strftime('%Y%m%d'))
    }

    def __init__(self):
        self.all = []
        self.data_name = 'baidu_rate_%d' % int(time.time())
        self.util = util()
        self.verify_tool = Verify()
        self.verify_save_name = 'verify.jpg'
        self.r = redis.Redis(host='127.0.0.1')
        self.login_url = 'https://cas.baidu.com/?action=login'
        self.verify_url = 'http://cas.baidu.com/?action=image&key={rand}'
        self.page_now = 0
        self.sites_map = {
            '8918649': {'name': 'm.91pme.com', 'page_now': 1},
            '7802984': {'name': '91pme.com', 'page_now': 1},
        }

        self.formdata = {
            "productId" : "fcWord,0",
            "fcPlanId" : "-1",
            "fcUnitId" : "-1",
            "siteId" : "8918649",
            "st" : "1512489600000",
            "et" : "1512489600000",
            "indicators" : "",
            "order" : "bounce_ratio,desc",
            "offset" : "0",
            "target" : "-1",
            "flag" : "fcWord",
            "userId" : "0",
            "fcWordType" : "fcSearchWord",
            "clientDevice" : "all",
            "reportId" : "6",
            "method" : "pro/product/a",
            "queryId" : ""
        }

        self.indicators = [
            "show_count", "clk_count", "cost_count", "ctr", "cpm", "pv_count", "visit_count", "visitor_count",
            "new_visitor_count", "new_visitor_ratio", "in_visit_count", "bounce_ratio", "avg_visit_time",
            "avg_visit_pages", "arrival_ratio", "trans_count", "trans_ratio", "avg_trans_cost", "income", "profit",
            "roi"
        ]


    def start_requests(self):
        # 看用既有的cookie能否成功登录
        return [scrapy.Request("https://tongji.baidu.com/web/24229627/trend/latest?siteId=8918649",
                               meta={'cookiejar': self.cookie_name},
                               callback=self.checkState)]

    def checkState(self, response):
        if response.status == 302:
            verify_url = self.verify_url.format(rand=random.randint(1500000000, 1511111111))
            yield scrapy.Request(verify_url, meta={'cookiejar': response.meta['cookiejar']}, callback=self.check_verify)
        else:
            for site_id in self.sites_map:
                form_dt = {}
                form_dt.update(self.formdata)
                form_dt['siteId'] = site_id
                form_dt['st'] = form_dt['et'] = str(int(time.time()) * 1000)

                for i in range(int(math.ceil(float(len(self.indicators)) / 6))):
                    start = i * 6
                    end = start + 6
                    form_dt['indicators'] = ",".join(self.indicators[start:end])

                    # print i, start, end,  ",".join(self.indicators[start:end])
                    print form_dt['indicators']
                    yield scrapy.FormRequest(url="https://tongji.baidu.com/web/24229627/ajax/post",
                                             meta={'cookiejar': self.cookie_name, 'site_id': site_id},
                                             formdata=form_dt,
                                             callback=self.parseData)

    def check_verify(self, response):
        with open(os.path.join(settings.Tmp_Dir, self.verify_save_name), "wb") as fs:
            fs.write(response.body)

        verify_code = self.verify_tool.parse_verify(self.verify_save_name)
        print verify_code
        if verify_code and len(verify_code) == 4:
            form_data = {
                "entered_login": "18513788638",
                "entered_password": "Jj8@ops...",
                "appid": "12",
                "entered_imagecode": verify_code,
                "charset": "utf-8",
                "fromu": "https://tongji.baidu.com/web/24229627/trend/latest?siteId=8918649",
                "selfu": "https://tongji.baidu.com/web/welcome/login",
                "senderr": "1"
            }

            yield scrapy.FormRequest(
                url=self.login_url,
                formdata=form_data,
                meta={"cookiejar": response.meta['cookiejar'], 'dont_redirect': True,
                      'handle_httpstatus_list': [301, 302]},
                callback=self.login
            )
        else:
            verify_url = self.verify_url.format(rand=random.randint(1500000000, 1511111111))
            yield scrapy.Request(verify_url, meta={'cookiejar': response.meta['cookiejar']}, callback=self.check_verify)

    def login(self, response):
        login_back = response.xpath("//script").re(r'var\surl="(.+)";')
        if login_back and len(login_back) > 0:
            login_back = urllib.unquote(str(login_back[0])).decode("utf-8")

            params = self.util.get_url_param(login_back)
            if 'errno' in params and params['errno'] == '131':
                time.sleep(5)
                verify_url = self.verify_url.format(rand=random.randint(1500000000, 1511111111))
                yield scrapy.Request(verify_url, meta={'cookiejar': response.meta['cookiejar']},
                                     callback=self.check_verify)
            else:
                yield scrapy.Request(login_back,
                                     meta={'cookiejar': response.meta['cookiejar'],
                                           'dont_redirect': True,
                                           'handle_httpstatus_list': [301, 302]},
                                     callback=self.parse_check)

    def parse_check(self, response):
        if "Location" in response.headers:
            yield scrapy.Request(response.headers['Location'],
                                 meta={'cookiejar': response.meta['cookiejar'],
                                       'dont_redirect': True,
                                       'handle_httpstatus_list': [301, 302]},
                                 callback=self.parse_loginback)

    def parse_loginback(self, response):
        yield scrapy.Request("https://tongji.baidu.com/web/24229627/homepage/index",
                             meta={'cookiejar': response.meta['cookiejar']}, callback=self.parse_visit)

    def parse_visit(self, response):
        print response.status, response.status == 302
        with open("body.html", 'w') as fs:
            fs.write(response.body)
            
        page_title = response.xpath(".//div[@class='sub-wrapper']//h2[@class='title']/text()").extract_first()
        if response.status == 302 or (page_title and page_title == '密保验证'.encode('utf-8')):
            form_dt = {
                'qid': '100000000',
                'answer': '18513788638'
            }

            yield scrapy.FormRequest(url="https://aq.baidu.com/hold/quesverify/verify",
                                     meta={'cookiejar': self.cookie_name},
                                     formdata=form_dt,
                                     callback=self.parse_redirect)
        else:
            for site_id in self.sites_map:
                form_dt = {}
                form_dt.update(self.formdata)
                form_dt['siteId'] = site_id
                form_dt['st'] = form_dt['et'] = str(int(time.time()) * 1000)

                print "site: ", self.sites_map[site_id]['name']
                for i in range(int(math.ceil(float(len(self.indicators)) / 6))):
                    start = i * 6
                    end = start + 6
                    print i, start, end
                    form_dt['indicators'] = ",".join(self.indicators[start:end])
                    print form_dt['indicators']

                    yield scrapy.FormRequest(url="https://tongji.baidu.com/web/24229627/ajax/post",
                                             meta={'cookiejar': self.cookie_name, 'site_id': site_id},
                                             formdata=form_dt,
                                             callback=self.parseData)

    def parse_redirect(self, response):
        print "verify phone", response.status, response.url
        yield scrapy.Request('http://tongji.baidu.com', meta={'cookiejar': self.cookie_name}, callback=self.parse_index_page)

    def parse_index_page(self, response):
        for site_id in self.sites_map:
            form_dt = {}
            form_dt.update(self.formdata)
            form_dt['siteId'] = site_id
            form_dt['st'] = form_dt['et'] = str(int(time.time()) * 1000)

            print "site: ", self.sites_map[site_id]['name']
            for i in range(int(math.ceil(float(len(self.indicators)) / 6))):
                start = i * 6
                end = start + 6
                print i, start, end
                form_dt['indicators'] = ",".join(self.indicators[start:end])
                print form_dt['indicators']

                yield scrapy.FormRequest(url="https://tongji.baidu.com/web/24229627/ajax/post",
                                     meta={'cookiejar': self.cookie_name, 'site_id': site_id},
                                     formdata=form_dt,
                                     callback=self.parseData)
        pass

    def parseData(self, response):
        data = json.loads(response.body)
        self.all.append(data)
        with open("body.json", 'w') as fs:
            json.dump(self.all, fs)

        # print response.status, response.request.meta, response.request.meta['site_id']

        fields = data['data']['fields'][1:]
        sum = data['data']['sum']
        item = CrawlBaiduRateItem()

        for index,field in enumerate(fields):
            item[field] = sum[0][index]

        item['ctime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item['site'] = self.sites_map[response.request.meta['site_id']]['name']
        item['source_id'] = self.data_name

        yield item


