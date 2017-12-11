# -*- coding: utf-8 -*-
import scrapy
import datetime, json, random, redis, urllib, time
from crawl.common.util import util, Verify

class CrawlBaiduCookieSpider(scrapy.Spider):
    name = 'crawl_baidu_cookie'
    cookie_name = 'crawl_baidu'
    allowed_domains = ['baidu.com']
    handle_httpstatus_list = [404, 500, 302, 301]
    start_urls = ['http://tongji.baidu.com/']

    custom_settings = {
        'LOG_FILE': 'logs/baidu_tongji_{dt}.log'.format(dt=datetime.datetime.now().strftime('%Y%m%d'))
    }

    def __init__(self):
        self.util = util()
        self.verify_tool = Verify()
        self.r = redis.Redis(host='127.0.0.1')
        self.login_url = 'https://cas.baidu.com/?action=login'
        self.verify_url = 'http://cas.baidu.com/?action=image&key={rand}'
        self.page_now = 1
        self.max_page = 51
        self.sites_map = {
            '8918649': {'name': 'm.91pme.com', 'page_now': 1},
            '7802984': {'name': '91pme.com', 'page_now': 1},
            '8918810': {'name': 'mm.91pme.com', 'page_now': 1}
        }
        self.formdata = {
            "siteId": "7802984",
            "order": "start_time,desc",
            "offset": "0",
            "pageSize": "100",
            "tab": "visit",
            "timeSpan": "14",
            "indicators": "start_time,area,source,access_page,searchword,visitorId,ip,visit_time,visit_pages",
            "reportId": "4",
            "method": "trend/latest/a",
            "queryId": ""
        }

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
            for site in self.sites_map:
                site_id = site
                site_page = self.sites_map[site]['page_now']
                offset = str((int(site_page) - 1) * 100)

                form_dt = {}
                form_dt.update(self.formdata)
                form_dt['siteId'] = site_id
                form_dt['offset'] = offset

                yield scrapy.FormRequest(url="https://tongji.baidu.com/web/24229627/ajax/post",
                                         meta={'cookiejar': self.name, 'site_id': site_id},
                                         formdata=form_dt,
                                         callback=self.parseData)

    def check_verify(self, response):
        verify_img = "verify.jpg"
        with open(verify_img, "wb") as fs:
            fs.write(response.body)

        verify_code = self.verify_tool.parse_verify(verify_img)
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
        print "login success"
