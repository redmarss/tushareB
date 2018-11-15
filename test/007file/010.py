#!/bin/usr/env python
#-*-coding:utf-8 -*-

#你有一个目录，放了你一个月的日记，都是 txt，为了避免分词的问题，假设内容都是英文，请统计出你认为每篇日记最重要的词。

import glob
from collections import Counter
import re

def list_txt():
    return glob.glob(r"006package/*.txt")

def wc(filename):
    datalist = []
    with open(filename, 'r') as f:
        for line in f:
            content = re.sub("\"|,|\.", "", line)
            datalist.extend(content.strip().split(' '))
    return Counter(datalist).most_common(1)

def most_comm():
    all_txt = list_txt()
    for txt in all_txt:
        print(wc(txt))

if __name__ == "__main__":
    most_comm()
    print(list(map(wc,list_txt())))
