# -*- coding: utf-8 -*-
import hashlib, os, datetime, time, random, logging, re, redis, pytesseract, sys
reload(sys)
sys.setdefaultencoding('utf-8')
import crawl.settings as setting
import jieba.analyse
from bs4 import BeautifulSoup
from crawl.settings import DATA_DIR

class RobitUtil(object):
    def __init__(self):
        jieba.load_userdict(os.path.join(DATA_DIR, "user_dict.txt"))
        self.r = redis.Redis(host=setting.REDIS['host'], port=setting.REDIS['port'])


    @classmethod
    def keywords_analyse(cls, text, strip_tag=False, topK=20, allowPos=('nr2', 'nr', 'n', 'ns', 'nsf', 'nt', 'nz', 'ng')):
        if strip_tag:
            soup = BeautifulSoup(text, "lxml")
            text = soup.getText()
            text = text.replace(u"\xa0", "").replace("\n", "")

        print text
        keywords = jieba.analyse.extract_tags(text, topK=topK, allowPOS=allowPos)

        return keywords
    @classmethod
    def word_split(cls, text, strip_tag=False):
        if strip_tag:
            soup = BeautifulSoup(text, "lxml")
            text = soup.getText()
            text = text.replace(u"\xa0", "").replace("\n", "")

        return jieba.cut(text)