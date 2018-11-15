#!/bin/usr/env python
# -*- coding:utf-8 -*-
#第 0008 题： 一个HTML文件，找出里面的正文。

import urllib.request
from bs4 import BeautifulSoup

url = "https://www.google.co.in"
page = urllib.request.urlopen(url).read()

soup = BeautifulSoup(page)
#print(soup.body.text)

#找到所有链接
links =soup.findAll('a')
for link in links:
    print(link['href'])