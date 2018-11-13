#!/bin/usr/env python
# -*-coding:utf-8 -*-

#第 0004 题： 任一个英文的纯文本文件，统计其中的单词出现的个数。第 0004 题： 任一个英文的纯文本文件，统计其中的单词出现的个数。
from collections import Counter
import string

#simply extend word like: it's => it is
def extend_word(text):
    if text.find('\'')>0:
        old2new = dict()
        words = text.split()
        for word in words:
            if word.find('\'') > 0:
                parts = word.split('\'')
                if parts[1] == 'm':
                    parts[1] = 'am'
                elif parts[1] == 's':
                    parts[1] = 'is'
                elif parts[1] == 're':
                    parts[1] = 'are'
                elif parts[1] == 't':
                    parts[1] = 'not'
                elif parts[1] == 've':
                    parts[1] = 'have'
                elif parts[1] == 'll':
                    parts[1] = "will"
                elif parts[1] == 'd':
                    if words[words.index(word)+1] == 'better':
                        parts[1] = 'had'
                    else:
                        parts[1] = 'would'
                if parts[0].endswith('n'):              #ex:doesn't
                    parts[0] = parts[0][:-1]
                old2new[word] = ' '.join(parts)
        _text = text
        for old_word in old2new.keys():
            _text = _text.replace(old_word, old2new[old_word])
        return _text


def return_order_key(record):
    return record[1]


def show_in_order(records):
    items = sorted(records.items(), key=lambda record:record[1] , reverse=True)
    for item in items:
        print(item[0], item[1])


if __name__ == "__main__":
    with open('004_file','r') as file:
        article = file.read()
        no_pun_text = article
        _punctuation = string.punctuation.replace('\'', '')     #punctuation函数为找出字符串中所有标点
        for pun in _punctuation:
            no_pun_text = no_pun_text.replace(pun,'')
        complete_text = extend_word(no_pun_text)
        records = dict()
        for word in complete_text.lower().split():
            records[word] = records.get(word, 0) + 1
        show_in_order(records)


