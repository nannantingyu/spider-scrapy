# -*- coding: utf-8 -*-
import scrapy
import datetime
from bs4 import BeautifulSoup

class CrawlWeiboHotSpider(scrapy.Spider):
    name = 'crawl_weibo_hot'
    allowed_domains = ['weibo.com']
    start_urls = ['http://weibo.com/']

    custom_settings = {
        'LOG_FILE': 'logs/weibo_hot_{dt}.log'.format(dt=datetime.datetime.now().strftime('%Y%m%d'))
    }

    def start_requests(self):
        return [scrapy.Request("https://weibo.com/?category=99991",
                               meta={'cookiejar': self.name, 'handle_httpstatus_list': [301, 302, 403], 'PhantomJS': True},
                               callback=self.parse_content)]

    def parse_content(self, response):
        divs = response.xpath(".//div[@id='PCD_pictext_i_v5']/ul/div[@class='UG_list_b']")

        for div in divs:
            pic = div.xpath(".//div[@class='pic W_piccut_v']/img/@src").extract_first()
            content = div.xpath(".//div[@class='list_des']/h3/div").extract()

            author_info = div.xpath(".//div[@class='list_des']/div[@class='subinfo_box clearfix']")
            author_img = author_info.xpath("./a[1]//img/@src").extract_first()
            author_name = author_info.xpath("./a[2]/span/text()").extract_first()
            author_link = author_info.xpath("./a[1]/@href").extract_first()
            if author_link is not None and not author_link.starts_with("http"):
                author_link = "https://weibo.com" + author_link

            pub_time = author_info.xpath(".//span[@class='subinfo S_txt2']/text()").extract_first()

            print "pic", pic
            print "content", content
            print "author_img", author_img
            print "author_name", author_name
            print "author_link", author_link
            print "pub_time", pub_time
            print "\n\n"