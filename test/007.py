#!/bin/usr/env python
# #-*- coding:utf-8 -*-
#有个目录，里面是你自己写过的程序，统计一下你写过多少行代码。包括空行和注释，但是要分别列出来。
import os

code_lines = list()
notation_lines = list()
blank_lines = list()

def process_file(filename):
    global code_lines
    global notation_lines
    global blank_lines
    with open(filename,'r') as f:
        for line in f.readline():
            _line = line.strip()
            if not _line:
                blank_lines.append(_line)
            elif _line.startswith('#'):
                notation_lines.append(_line)
            else:
                code_lines.append(_line)


def show_result():
    global code_lines
    global notation_lines
    global blank_lines
    print('-'*20)
    print('code:',len(code_lines))
    for line in code_lines:
        print(line)
    print('-'*20)
    print('notation:',len(notation_lines))
    for line in notation_lines:
        print(line)
    print('-'*20)
    print('blank:',blank_lines)
    code_lines.clear()
    notation_lines.clear()
    blank_lines.clear()

def process_files(path=r'\007file'):
    files = os.listdir(path)
    for file in files:
        if file.endswith('.py'):
            print('='*30)
            print('current file:',os.path.join(path,file))
            process_file(os.path.join(path,file))
            show_result()

process_file(r'\007file')

