# -*- coding: utf-8 -*-
import hashlib, os, datetime, time, random, logging, re, redis, pytesseract, sys
reload(sys)
sys.setdefaultencoding('utf-8')
import crawl.settings as setting

class weixin_body_parser:
    @classmethod
    def parse(self, body):
        htmlcontent = body

        # 视频地址处理
        video_src_pat = re.compile(r'\sdata\-src="(https?:\/\/v\.qq.*?)"')
        htmlcontent = video_src_pat.sub(' src="\g<1>" ', htmlcontent)
        htmlcontent = htmlcontent.replace('https://v.qq.com/iframe/preview.html', 'http://v.qq.com/iframe/player.html').replace("width=500", "width=345")

        # 图片地址处理
        # 将图片地址改为经过服务器的链接（加自己的前缀）
        img_src_pat = re.compile(r'\sdata\-src="(https?:\/\/mmbiz.*?)"')

        uuids = []
        for _, match in enumerate(img_src_pat.finditer(htmlcontent)):
            img_src = match.group(1)
            uuids.append("/image?ori=" + img_src)

        htmlcontent = img_src_pat.sub(" src=\"\g<1>\" data-src=\"\g<1>\"", htmlcontent)
        src_pat = re.compile(r'\ssrc="(https?:\/\/mmbiz.+?)"')
        htmlcontent = src_pat.sub(Nth(uuids), htmlcontent)

        # css背景图片地址处理
        img_backgroud_pat = re.compile(r'url\("(https?:\/\/mmbiz.*?)"\)')
        uuids_background = []
        for _, match in enumerate(img_backgroud_pat.finditer(htmlcontent)):
            img_src = match.group(1)
            uuids_background.append("/image?ori=" + img_src)

        htmlcontent = img_backgroud_pat.sub(Nth(uuids_background, 'url("%s")'), htmlcontent)

        return htmlcontent

class Nth(object):
    def __init__(self, uuids, replace_pat=" src=\"%s\" "):
        self.uuids = uuids
        self.calls = 0
        self.replace_pat = replace_pat

    def __call__(self, matchobj):
        strreplace = self.replace_pat % self.uuids[self.calls]
        self.calls += 1
        return strreplace