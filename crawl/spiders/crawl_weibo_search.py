# -*- coding: utf-8 -*-
import scrapy, redis
from crawl.settings import REDIS, Tmp_Dir
import sys, datetime, re, urllib
from crawl.items import CrawlHotkey
from crawl.common.util import util
reload(sys)
sys.setdefaultencoding('utf-8')

class CrawlWeiboSearchSpider(scrapy.Spider):
    name = 'crawl_weibo_search'
    allowed_domains = ['weibo.com']
    start_urls = ['http://weibo.com/']

    custom_settings = {
        'LOG_FILE': 'logs/weibo_search_{dt}.log'.format(dt=datetime.datetime.now().strftime('%Y%m%d'))
    }

    def start_requests(self):
        self.r = redis.Redis(hosts=REDIS['host'], port=REDIS['port'])
        return [scrapy.Request("http://s.weibo.com/top/summary?Refer=top_hot&topnav=1&wvr=6",
                               meta={'cookiejar': self.name, 'handle_httpstatus_list': [301, 302, 403], 'PhantomJS': True}, callback=self.parse_content)]

    def parse_content(self, response):
        tds = response.xpath(".//table[@id='realtimehot']//tr//td[@class='td_02']//p[@class='star_name']/a/@href").extract()
        key_pat = re.compile(r"weibo\/(.*)\&")
        for index,td in enumerate(tds):
            keywords = td.strip() if td is not None else None

            if keywords:
                keywords = key_pat.findall(keywords)
                keywords = keywords[0] if len(keywords) > 0 else None

                if keywords is not None:
                    keywords = urllib.unquote(urllib.unquote(keywords))
                    print keywords
                    self.r.sadd("weixin_hot_keywords", keywords)
                    self.r.sadd("weibo_hot_keywords", keywords)

                    item = CrawlHotkey()
                    item['time'] = datetime.datetime.now()
                    item['keyword'] = keywords
                    item['order'] = index
                    item['source_id'] = util.get_sourceid(keywords)

                    yield item