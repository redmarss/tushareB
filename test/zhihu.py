#!/bin/usr/env python
# -*- coding:utf-8 -*-

#python爬虫：使用账号、密码和验证码登录知乎网页

import re
from bs4 import BeautifulSoup
import gzip
import urllib.request
import urllib.parse
import http.cookiejar
import ssl
import time

def get_opener(heads):
    cj = http.cookiejar.CookieJar()
    pro = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(pro)
    header = []
    for key, value in heads.items():
        header.append((key, value))
    opener.addheaders = header
    return opener

def ungzip(data):
    try:
        print("正在解压...")
        data = gzip.decompress(data)
        print("解压完成")
    except:
        print("无需解压")
    return data

if __name__ == "__main__":
    ssl._create_default_https_context = ssl._create_unverified_context      #解决弹出可信站点问题
    heads={
        "Accept": "*/*",
        "AcceptLanguage": "zh-CN,zh;q=0.9",
        "User-Angent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
        "Accept-Encoding":"gzip, deflate",
        "Host": "www.zhihu.com",
        "DNT": "1",
        "Connection": "Keep-Alive"
    }
    opener = get_opener(heads)
    url = "https://www.zhihu.com"
    op = opener.open(url)
    data1 = op.read()
    data1 = ungzip(data1).decode('utf-8')

    soup = BeautifulSoup(data1, "html.parser")
    _xsrf = soup.find("input", {'type':'tel'})
    _xsrf = _xsrf.get("value")
    password = "wuxianwuxian1"
    phone_num = "redmarss@sohu.com"
    captcha_url = "https://www.zhihu.com/captcha.gif?r=%d&type=login"% (time.time() * 1000)
    captchadata = opener.open(captcha_url).read()
    with open("1.gif", 'wb') as f:
        f.write(captchadata)
    yanzhengma = input("captcha:")
    postdata={
        "_xsrf":_xsrf,
        "password":password,
        "phone_num":phone_num,
        "captcha":yanzhengma
    }
    postdata = urllib.parse.urlencode(postdata).encode()
    login_url = "https://www.zhihu.com/login/phone_num"
    op2 = opener.open(login_url, postdata)
    login_data = op2.read()
    data = ungzip(login_data).decode("utf-8")
    print(data)
    result = dict(eval(data))
    if result["r"] == 0:
        print("登录成功")
    else:
        print("登录失败")