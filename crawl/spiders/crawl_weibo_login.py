# -*- coding: utf-8 -*-
import scrapy, datetime
from selenium import webdriver

class CrawlWeiboLoginSpider(scrapy.Spider):
    name = 'crawl_weibo_login'
    allowed_domains = ['weibo.cn']
    start_urls = ['http://weibo.cn/']

    custom_settings = {
        'LOG_FILE': 'logs/weibo_login_{dt}.log'.format(dt=datetime.datetime.now().strftime('%Y%m%d'))
    }

    def start_requests(self):
        obj = webdriver.PhantomJS(executable_path="F://bat/phantomjs.exe")
        obj.set_page_load_timeout(5)
        try:
            obj.get('https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349')
            print obj.find_element_by_id("changeVerifyCode").text  # 获取元素的文本信息
            # obj.find_element_by_id('kw').clear()  # 用于清除输入框的内容
            # obj.find_element_by_id('kw').send_keys('Hello')  # 在输入框内输入Hello
            # obj.find_element_by_id('su').click()  # 用于点击按钮
            # obj.find_element_by_id('su').submit()  # 用于提交表单内容
        except Exception as e:
            print e

        return []
