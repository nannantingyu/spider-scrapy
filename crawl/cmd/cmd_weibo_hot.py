# -*- coding: utf-8 -*-
import scrapy
import sys, redis
reload(sys)
sys.setdefaultencoding('utf-8')
from selenium import webdriver

r = redis.Redis(host='127.0.0.1', port=6379)
driver = webdriver.PhantomJS()
driver.get("http://s.weibo.com/top/summary?Refer=top_hot&topnav=1&wvr=6")
tds = driver.find_elements_by_xpath(".//table[@id='realtimehot']//tr//td[@class='td_02']")

for td in tds:
    keywords = td.text.strip() if td.text is not None else None
    if keywords:
        r.sadd("weixin_hot_keywords", keywords)
        r.sadd("weibo_hot_keywords", keywords)
        print keywords