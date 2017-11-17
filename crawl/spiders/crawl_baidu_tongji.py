# -*- coding: utf-8 -*-
import scrapy
import datetime, json, random, redis, urllib, time
from crawl.common.util import util, Verify

class CrawlBaiduTongjiSpider(scrapy.Spider):
    name = 'crawl_baidu_tongji'
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
        self.lastest_access_time = {}

    def start_requests(self):
        for site in self.sites_map:
            sname = self.sites_map[site]['name']
            self.lastest_access_time[sname] = self.r.get('baidutongji:%s'%sname)

        # 看用既有的cookie能否成功登录
        return [scrapy.Request("https://tongji.baidu.com/web/24229627/trend/latest?siteId=8918649",
                               meta={'cookiejar': self.name},
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
        yield scrapy.Request("https://tongji.baidu.com/web/24229627/homepage/index",
                             meta={'cookiejar': response.meta['cookiejar']}, callback=self.parse_visit)

    def parse_visit(self, response):
        for site_id in self.sites_map:
            site_page = self.sites_map[site_id]['page_now']
            offset = str((int(site_page) - 1) * 100)

            form_dt = {}
            form_dt.update(self.formdata)
            form_dt['siteId'] = site_id
            form_dt['offset'] = offset

            print form_dt

            yield scrapy.FormRequest(url="https://tongji.baidu.com/web/24229627/ajax/post",
                                     meta={'cookiejar': self.name, 'site_id': site_id},
                                     formdata=form_dt,
                                     callback=self.parseData)

    def parseData(self, response):
        print response.request.headers
        site_id = response.request.meta['site_id']
        site_name = self.sites_map[site_id]['name']
        page_now = self.sites_map[site_id]['page_now']

        new_time = None
        try:
            json_data = json.loads(response.body)
            data = json_data['data']
            for index, item in enumerate(data['items'][0]):
                for subitem in item:
                    item = {}
                    detail = subitem['detail']
                    sub_detail = data['items'][1][index]

                    item['visitorType'] = detail['visitorType']
                    item['visitorFrequency'] = detail['visitorFrequency']
                    item['lastVisitTime'] = detail['lastVisitTime']
                    item['endPage'] = detail['endPage']
                    item['deviceType'] = detail['deviceType']
                    item['fromType'] = detail['fromType']['fromType'] if 'fromType' in detail['fromType'] else ""
                    item['fromurl'] = detail['fromType']['url'] if 'url' in detail['fromType'] else ""
                    item['fromAccount'] = detail['fromType']['fromAccount'] if 'fromAccount' in detail[
                        'fromType'] else ""
                    item['isp'] = detail['isp']
                    item['os'] = detail['os']
                    item['osType'] = detail['osType']
                    item['browser'] = detail['browser']
                    item['browserType'] = detail['browserType']
                    item['language'] = detail['language']
                    item['resolution'] = detail['resolution']
                    item['color'] = detail['color']
                    item['accessPage'] = detail['accessPage']
                    item['antiCode'] = detail['antiCode'] if "antiCode" in detail else ""

                    item['visit_pages'] = sub_detail[8]
                    item['access_time'] = sub_detail[0]
                    item['user_id'] = sub_detail[6]
                    item['visit_time'] = sub_detail[7]
                    item['area'] = sub_detail[1]
                    item['ip'] = sub_detail[5]

                    if site_name == "mm.91pme.com":
                        item['keywords'] = sub_detail[4]
                        item['entry_page'] = sub_detail[3]
                    else:
                        item['keywords'] = sub_detail[3]
                        item['entry_page'] = sub_detail[4]

                    item['site'] = site_name
                    yield item

            new_time = data['items'][1][0][0]
            self.sites_map[site_id]['page_now'] += 1

        except Exception as e:
            print e
        finally:
            if self.sites_map[site_id]['page_now'] < self.max_page and \
                    (self.lastest_access_time is None or site_name not in self.lastest_access_time
                     or self.lastest_access_time[site_name] is None or
                             new_time > self.lastest_access_time[site_name]):
                if self.lastest_access_time is not None:
                    print new_time, self.lastest_access_time[site_name], site_name, page_now
                form_dt = {}
                form_dt.update(self.formdata)
                form_dt['siteId'] = site_id
                form_dt['offset'] = str((self.sites_map[site_id]['page_now'] - 1) * 100)

                yield scrapy.FormRequest(url="https://tongji.baidu.com/web/24229627/ajax/post",
                                         meta={'cookiejar': self.name, 'site_id': site_id},
                                         formdata=form_dt,
                                         callback=self.parseData)