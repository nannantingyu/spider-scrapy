# -*- coding: utf-8 -*-
import hashlib, os, datetime, time, random, logging, re, redis, pytesseract, sys
reload(sys)
sys.setdefaultencoding('utf-8')
import crawl.settings as setting
from contextlib import contextmanager
from urlparse import urlparse
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = 'E:\\Tool\\Python\\Lib\\site-packages\\pytesser\\tesseract.exe'

class util(object):
    def __init__(self):
        self.r = redis.Redis(host=setting.REDIS['host'], port=setting.REDIS['port'])

    @classmethod
    def get_url_param(cls, url):
        if "?" not in url:
            return None

        url = url.split("?")[-1]
        params = {}
        for param in url.split("&"):
            pa = param.split("=")
            params[pa[0]] = pa[1]

        return params

    @classmethod
    def get_sourceid(cls, url):
        md5 = hashlib.md5()
        md5.update(url)
        return md5.hexdigest()

    @classmethod
    def sleep(cls, sleep_time=None):
        sleep_time = sleep_time if sleep_time is not None else random.randint(1, 5)
        time.sleep(sleep_time)

    def downfile(self, full_img_url, img_name=None, need_down=False):
        """
        将要下载的文件放到redis列表中，可以进行分布式下载
        :param full_img_url: 要下载的文件的url地址
        :param img_name: 下载的文件名称
        :return: 下载之后的文件路径
        """
        if img_name is None:
            img_name = os.path.basename(full_img_url)

        now = datetime.datetime.now()
        img_urlpath = "%d/%d/%d" % (now.year, now.month, now.day)
        img_path = os.path.join(setting.IMAGES_STORE, img_urlpath)

        full_img_path = os.path.join(img_path, img_name).replace("\\", "/")

        down_topic = "downfile_queue_ex" if need_down else "downfile_queue"
        self.r.sadd(down_topic, "%s_____%s" % (full_img_url, full_img_path))

        return os.path.join(setting.URL_PREFIX, img_urlpath, img_name).replace("\\", "/")

    def handle_body(self, htmlcontent, src_pat=r'\ssrc="(.*?)"'):
        img_src_pat = re.compile(src_pat)

        now = datetime.datetime.now()
        img_urlpath = "%d/%d/%d" % (now.year, now.month, now.day)

        img_save_path = os.path.join(setting.IMAGES_STORE, img_urlpath)
        is_exists = os.path.exists(img_save_path)
        if not is_exists:
            os.makedirs(img_save_path)

        uuids = []
        for _, match in enumerate(img_src_pat.finditer(htmlcontent)):
            img_src = match.group(1)
            img_name = os.path.basename(urlparse(img_src).path)

            if img_name == '' or '.' not in img_name:
                img_name = "{name}.{sufix}".format(name=str(int(time.time())), sufix='jpg')

            if not img_src.startswith('http'):
                img_src = 'http:/' + img_src

            full_img_path = self.downfile(img_src, img_name)
            uuids.append(full_img_path)

        htmlcontent = img_src_pat.sub(Nth(uuids), htmlcontent)

        # 删除文章中的链接
        a_pat = re.compile("<a.*?>(.*)<\/a>")
        htmlcontent = a_pat.sub("\g<1>", htmlcontent)

        return htmlcontent

class Nth(object):
    def __init__(self, uuids):
        self.uuids = uuids
        self.calls = 0

    def __call__(self, matchobj):
        strreplace = " src=\"" + setting.URL_PREFIX + self.uuids[self.calls] + "\""

        self.calls += 1
        return strreplace

class Verify(object):
    def __init__(self, threshold=140):
        self.threshold = self.ori_threshold = threshold
        self.saving_path = setting.Tmp_Dir

    def parse_verify(self, name):
        letter_range = [chr(c) for c in range(ord('A'), ord('Z') + 1)]
        letter_range.extend([chr(c) for c in range(ord('0'), ord('9') + 1)])

        while self.threshold > 100:
            table = self.image_split()
            im = Image.open(os.path.join(self.saving_path, name))
            imgry = im.convert('L')
            imgry.save(os.path.join(self.saving_path, 'g' + name))

            out = imgry.point(table, '1')
            out.save(os.path.join(self.saving_path, 'b' + name))

            text = pytesseract.image_to_string(out)
            text = text.strip()
            text = text.upper()

            passed = True
            if len(text) != 4:
                passed = False
            else:
                for c in text:
                    if c not in letter_range:
                        passed = False
                        break

            if text and passed:
                return text
            else:
                self.threshold -= 1

        self.threshold = self.ori_threshold
        print "cannot decode"

    def image_split(self):
        table = []
        for i in range(256):
            if i < self.threshold:
                table.append(0)
            else:
                table.append(1)

        return table

@contextmanager
def session_scope(session):
    sess = session()
    try:
        yield sess
        sess.commit()
    except:
        sess.rollback()
        raise
    finally:
        sess.close()