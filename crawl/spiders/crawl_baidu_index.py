# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from PIL import Image
import pytesseract
import re
import subprocess
import MySQLdb
import os

class CrawlBaiduIndexSpider(scrapy.Spider):
    name = 'crawl_baidu_index'
    allowed_domains = ['index.baidu.com']
    start_urls = ['http://index.baidu.com/']

    def parse(self, response):
        pass
