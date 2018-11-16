#!/bin/usr/env python
# -*-coding:utf8 -*-

#用 Python 写一个爬图片的程序，爬http://tieba.baidu.com/p/2166231880 里面的图片

import requests
from pyquery import PyQuery
from urllib.request import urlopen

class DownLoadImage(object):

    def __init__(self):
        self.urls = list()
        self.url = 'http://tieba.baidu.com/p/2166231880'
        self.headers = {
            'Acccept': '*/*',
            'Accept-Encoding':'gzip,deflate',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
        }
        self.s =requests.session()
        self.s.headers.update(self.headers)

    def get_image_url(self):
        resp = self.s.get(self.url)
        doc = PyQuery(resp.content.decode())
        imgs = doc.find('img.BDE_Image')
        for img in imgs.items():
            self.urls.append(img.attr('src'))

    def save(self):
        for i in range(len(self.urls)):
            url = self.urls[i]
            print(url)
            resp = self.s.get(url)
            filename = './013img/'+'img' +str(i) +'.jpg'
            with open(filename,'wb') as f:
                f.write(resp.content)

    def download(self):
        self.get_image_url()
        self.save()


if __name__ == '__main__':
    d = DownLoadImage()
    d.download()
