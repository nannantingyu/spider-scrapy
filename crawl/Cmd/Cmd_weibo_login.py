#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time, base64, rsa, binascii, requests, re, random, json, os
from PIL import Image
from crawl.settings import Cookie_Dir
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from urllib import quote_plus


class CmdWeiboLogin:
    def __init__(self):
        agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0'
        self.headers = {
            'User-Agent': agent
        }

        self.cookie_file_path = os.path.join(Cookie_Dir, "weibo.json")
        self.session = requests.session()

    def start(self):
        index_url = "http://weibo.com/login.php"
        try:
            index_cookie = self.session.get(index_url, headers=self.headers, timeout=2)
            self.save_cookie(index_cookie.cookies)
        except:
            index_cookie = self.session.get(index_url, headers=self.headers)
            self.save_cookie(index_cookie.cookies)

        self.login("nannantingyu@hotmail.com", "wait12345")

    def save_cookie(self, cookie):
        data = []
        maps = {}
        for (key, value) in cookie.iteritems():
            c = {
                "name": key,
                "value": value,
                "domain": ".weibo.com",
                "path": "/"
            }

            maps[key] = value
            data.append(c)

        cookie_file = None
        if data and len(data) > 0:
            if os.path.exists(self.cookie_file_path):
                with open(self.cookie_file_path, "r") as fs:
                    cookie_file = json.load(fs)

                    for c in cookie_file:
                        c["value"] = maps[c['name']] if c['name'] in maps else c["value"]

            cookie_file = cookie_file if cookie_file is not None else data
            with open(self.cookie_file_path, "w") as wfs:
                json.dump(cookie_file, wfs)

            cookie_file_login = os.path.join(Cookie_Dir, "cookie_crawl_weibo_login.pkl")
            cookie_login_file = {}
            if os.path.exists(cookie_file_login):
                with open(cookie_file_login, "r") as fs:
                    cookie_login_file = json.load(fs)

            cookie_login_file = cookie_login_file.update(maps)
            with open(cookie_file_login, "w") as wfs:
                json.dump(cookie_login_file, wfs)

    def get_su(self, username):
        """
        对 email 地址和手机号码 先 javascript 中 encodeURIComponent
        对应 Python 3 中的是 urllib.parse.quote_plus
        然后在 base64 加密后decode
        """
        username_quote = quote_plus(username)
        username_base64 = base64.b64encode(username_quote.encode("utf-8"))
        return username_base64.decode("utf-8")

    # 预登陆获得 servertime, nonce, pubkey, rsakv
    def get_server_data(self, su):
        pre_url = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su="
        pre_url = pre_url + su + "&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)&_="
        pre_url = pre_url + str(int(time.time() * 1000))
        pre_data_res = self.session.get(pre_url, headers=self.headers)
        self.save_cookie(pre_data_res.cookies)

        sever_data = eval(pre_data_res.content.decode("utf-8").replace("sinaSSOController.preloginCallBack", ''))

        return sever_data

    def get_password(self, password, servertime, nonce, pubkey):
        rsaPublickey = int(pubkey, 16)
        key = rsa.PublicKey(rsaPublickey, 65537)  # 创建公钥
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)  # 拼接明文js加密文件中得到
        message = message.encode("utf-8")
        passwd = rsa.encrypt(message, key)  # 加密
        passwd = binascii.b2a_hex(passwd)  # 将加密信息转换为16进制。
        return passwd

    def get_cha(self, pcid):
        cha_url = "http://login.sina.com.cn/cgi/pin.php?r="
        cha_url = cha_url + str(int(random.random() * 100000000)) + "&s=0&p="
        cha_url = cha_url + pcid
        cha_page = self.session.get(cha_url, headers=self.headers)
        self.save_cookie(cha_page.cookies)

        with open("cha.jpg", 'wb') as f:
            f.write(cha_page.content)
            f.close()
        try:
            im = Image.open("cha.jpg")
            im.show()
            im.close()
        except:
            print(u"请到当前目录下，找到验证码后输入")

    def login(self, username, password):
        # su 是加密后的用户名
        su = self.get_su(username)
        sever_data = self.get_server_data(su)
        servertime = sever_data["servertime"]
        nonce = sever_data['nonce']
        rsakv = sever_data["rsakv"]
        pubkey = sever_data["pubkey"]
        showpin = sever_data["showpin"]
        password_secret = self.get_password(password, servertime, nonce, pubkey)

        postdata = {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'useticket': '1',
            'pagerefer': "http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl",
            'vsnf': '1',
            'su': su,
            'service': 'miniblog',
            'servertime': servertime,
            'nonce': nonce,
            'pwencode': 'rsa2',
            'rsakv': rsakv,
            'sp': password_secret,
            'sr': '1366*768',
            'encoding': 'UTF-8',
            'prelt': '115',
            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'META'
        }

        login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
        if showpin == 0:
            login_page = self.session.post(login_url, data=postdata, headers=self.headers)
        else:
            pcid = sever_data["pcid"]
            self.get_cha(pcid)
            postdata['door'] = input(u"请输入验证码")
            login_page = self.session.post(login_url, data=postdata, headers=self.headers)

        self.save_cookie(login_page.cookies)

        login_loop = (login_page.content.decode("GBK"))
        pa = r'location\.replace\([\'"](.*?)[\'"]\)'
        loop_url = re.findall(pa, login_loop)[0]
        # 还可以加上一个是否登录成功的判断，下次改进的时候写上
        login_index = self.session.get(loop_url, headers=self.headers)
        self.save_cookie(login_index.cookies)

        uuid = login_index.text
        uuid_pa = r'"uniqueid":"(.*?)"'
        uuid_res = re.findall(uuid_pa, uuid, re.S)[0]
        web_weibo_url = "http://weibo.com/%s/profile?topnav=1&wvr=6&is_all=1" % uuid_res
        weibo_page = self.session.get(web_weibo_url, headers=self.headers)
        self.save_cookie(weibo_page.cookies)

        weibo_pa = r'<title>(.*?)</title>'
        # print(weibo_page.content.decode("utf-8"))
        userID = re.findall(weibo_pa, weibo_page.content.decode("utf-8", 'ignore'), re.S)[0]
        print(u"欢迎你 %s, 你在正在使用模拟登录微博" % userID)
        self.save_cookie(weibo_page.cookies)

class __redirection__:
    def __init__(self):
        self.__console__ = sys.stdout

    def write(self, output_stream):
        self.__console__.write(output_stream.decode('utf-8').encode('gbk'))

    def reset(self):
        sys.stdout = self.__console__
