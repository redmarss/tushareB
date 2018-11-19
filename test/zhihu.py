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
    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_argument('headless')              #配置参数使chrome后台运行
    driver = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\chromedriver.exe')     #配置参数chrome_options=
    driver.get('https://www.zhihu.com/signup?next=%2F')
    locad_butter = driver.find_element_by_css_selector('#root > div > main > div > div > div > div.SignContainer-inner > div.SignContainer-switch > span')
    locad_butter.click()
    time.sleep(1)               #等待1s
    username = driver.find_element_by_css_selector('#root > div > main > div > div > div > div.SignContainer-inner > div.Login-content > form > div.SignFlow-account > div.SignFlowInput.SignFlow-accountInputContainer > div.SignFlow-accountInput.Input-wrapper > input')
    username.send_keys('redmarss@sohu.com')
    passwd = driver.find_element_by_css_selector('#root > div > main > div > div > div > div.SignContainer-inner > div.Login-content > form > div.SignFlow-password > div.SignFlowInput > div.Input-wrapper > input.Input')
    passwd.send_keys('wuxianwuxian1')
    time.sleep(2)
    driver.find_element_by_css_selector(
        '#root > div > main > div > div > div > div.SignContainer-inner > div.Login-content > form > button').click()
    try:
        captcha_input = driver.find_element_by_css_selector('#root > div > main > div > div > div > div > div > form > div.Captcha.SignFlow-captchaContainer > div > div.SignFlowInput > div.Input-wrapper > input.Input')
        captcha = driver.find_element_by_css_selector('#root > div > main > div > div > div > div > div > form > div.Captcha.SignFlow-captchaContainer > div > span.Captcha-englishImage > div.Captcha-englishContainer > img.Captcha-englishImg')
        captcha_url = captcha.get_attribute('src')
        captchadata = opener.open(captcha_url).read()
        with open("1.jpg", 'wb') as f:
            f.write(captchadata)
        yanzhengma = input("captcha:")
        captcha_input.send_keys(yanzhengma)

        driver.find_element_by_css_selector(
            '#root > div > main > div > div > div > div.SignContainer-inner > div.Login-content > form > button').click()
        print("登录成功")
    except:
        print("验证码获取失败，请稍后重试")
        return





def get_opener(heads):
    cj = http.cookiejar.CookieJar()
    pro = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(pro)
    header = []
    for key, value in heads.items():
        header.append((key, value))
    opener.addheaders = header
    return opener



if __name__ == "__main__":

    cookies_value = get_login_cookie()
