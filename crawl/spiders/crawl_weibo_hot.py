# -*- coding: utf-8 -*-
import scrapy
import datetime, time, json, re
from scrapy.selector import Selector
from crawl.Common.Util import Nth, util, Email
from crawl.items import CrawlWeibo
from crawl.Cmd.Cmd_weibo_login import CmdWeiboLogin

class CrawlWeiboHotSpider(scrapy.Spider):
    name = 'crawl_weibo_hot'
    allowed_domains = ['weibo.com', 'd.weibo.com']
    start_urls = ['http://weibo.com/']

    custom_settings = {
        'LOG_FILE': 'logs/weibo_hot_{dt}.log'.format(dt=datetime.datetime.now().strftime('%Y%m%d'))
    }

    def __init__(self):
        self.base_url = "https://d.weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=102803_ctg1_1760_-_ctg1_1760&pagebar=0&tab=home&current_page={current_page}&pre_page={pre_page}&page={page}&pl_name=Pl_Core_NewMixFeed__3&id=102803_ctg1_1760_-_ctg1_1760&script_uri=/&feed_type=1&domain_op=102803_ctg1_1760_-_ctg1_1760&__rnd={time}"
        self.page = self.current_page = self.pre_page = 1
        self.util = util()
        self.login_time = 0
        self.login_cmd = CmdWeiboLogin()

    def get_url(self):
        timestr = str(int(time.time()) * 1000)
        return self.base_url.format(page=self.page, current_page=self.current_page, pre_page=self.pre_page, time=timestr)

    def start_requests(self):
        return [scrapy.Request(self.get_url(),
                               meta={'cookiejar': 'crawl_weibo_login', 'dont_redirect': True,
                                   'handle_httpstatus_list': [301, 302, 403]},
                               callback=self.parse_cookie)]

    def parse_cookie(self, response):
        print response.status
        if response.status == 200:
            data = json.loads(response.body)
            html = data['data'].replace(u"\u200b", "").replace("\r", "").replace("\n", "").replace(u"\xfb", "").replace(
                u"\xf1", "")

            with open("weibo_index.html", "w") as fs:
                fs.write(html)

            st = Selector(text=html, type='html')
            divs = st.xpath(".//div[contains(@class, 'WB_cardwrap WB_feed_type S_bg2')]")

            for div in divs:
                info = div.xpath(".//div[@class='WB_feed_detail clearfix']")
                author = info.xpath(".//div[@class='WB_face W_fl']/div[@class='face']/a")
                author_link = author.xpath("./@href").extract_first()
                author_img = author.xpath("./img/@src").extract_first()

                if author_link is not None and not author_link.startswith("http"):
                    author_link = "https:" + author_link
                if author_img is not None and not author_img.startswith("http"):
                    author_img = "https:" + author_img

                detail = div.xpath(".//div[@class='WB_detail']")
                author_name = detail.xpath("./div[@class='WB_info']/a/text()").extract_first()
                author_name = author_name.strip() if author_name is not None else None

                pub_time = detail.xpath(".//div[@class='WB_from S_txt2']/a[1]/@title").extract_first()
                if pub_time is not None:
                    pub_time = datetime.datetime.strptime(pub_time, "%Y-%m-%d %H:%M")

                content = detail.xpath(".//div[@class='WB_text W_f14']").extract_first()
                content = content.replace(u"\xa0", "") if content is not None else ""

                images = detail.xpath(".//div[@class='media_box']/ul/li/img/@src").extract()
                for i,img in enumerate(images):
                    images[i] = "http:" + img

                source_id = div.xpath("./@mid").extract_first()

                content_img_pat = re.compile(r'src="(.*?)"')
                all_img = content_img_pat.findall(content)
                replaced_imgs = []
                for img in all_img:
                    img = "http:" + img
                    img_src = self.util.downfile(img, fix_path=True, need_down=True)
                    print img, img_src
                    replaced_imgs.append(img_src)

                content = content_img_pat.sub(Nth(replaced_imgs), content)

                try:
                    print "images", images
                    print "content", content
                    print "author_img", author_img
                    print "author_name", author_name
                    print "author_link", author_link
                    print "pub_time", pub_time
                    print "source_id", source_id
                    print "\n\n"
                except Exception, e:
                    print e

                item = CrawlWeibo()
                item['images'] = ",".join(images)
                item['content'] = content
                item['author_img'] = author_img
                item['author_name'] = author_name
                item['author_link'] = author_link
                item['pub_time'] = pub_time
                item['source_id'] = source_id

                yield item

        else:
            if self.login_time < 5:
                self.login_cmd.start()
                self.login_time += 1
            else:
                Email.send("登录微博失败5次，请查看日志", ['939259192@qq.com'], subject="爬虫失败提醒")

