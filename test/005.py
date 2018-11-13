#!/bin/usr/env python
# -*- coding:utf-8 -*-
#第 0005 题： 你有一个目录，装了很多照片，把它们的尺寸变成都不大于 iPhone5 分辨率(1136*640)的大小。

import os
from PIL import Image

ext = ['jpg','jpeg','png']
path='./pic/'
files = os.listdir(path)

def process_image(filename, mwidth=640, mheigt=1136):
    image =Image.open(path+filename)
    w, h = image.size
    if w <= mwidth and h <= mheigt:
        print(filename, 'is OK.')
        return
    if 1.0*w/mwidth >1.0*h/mheigt:
        scale = 1.0*w/mwidth
        new_im = image.resize((int(w/scale), int(h/scale)), Image.ANTIALIAS)
    else:
        scale = 1.0*h/mheigt
        new_im = image.resize((int(w/scale), int(h/scale)),Image.ANTIALIAS)
    new_im.save(path+'new-'+filename)
    new_im.close

for file in files:
    if file.split('.')[-1].lower() in ext:
        process_image(file)