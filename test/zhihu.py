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
from selenium import webdriver

def get_login_cookie():
    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_argument('headless')              #配置参数使chrome后台运行
    driver = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\chromedriver.exe', chrome_options=chrome_option)     #配置参数chrome_options=
    driver.get('https://www.zhihu.com/signup?next=%2F')
    locad_butter = driver.find_element_by_css_selector('#root > div > main > div > div > div > div.SignContainer-inner > div.SignContainer-switch > span')
    locad_butter.click()
    time.sleep(2)               #等待2s
    username = driver.find_element_by_css_selector('#root > div > main > div > div > div > div.SignContainer-inner > div.Login-content > form > div.SignFlow-account > div.SignFlowInput.SignFlow-accountInputContainer > div.SignFlow-accountInput.Input-wrapper > input')
    print(username.tag_name)
    return username


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
    cookies_value = get_login_cookie()

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