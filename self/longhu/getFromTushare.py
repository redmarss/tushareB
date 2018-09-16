#!/usr/bin/env python
# -*- coding:utf8 -*-

import self.longhu.globalFunction as globalFunction
import tushare as ts
from tushare.stock import cons as ct
from tushare.util import dateu as du
import pandas as pd
import re
import time
import json
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

#获取每日龙虎榜信息，并修改成指定格式，返回一个dataframe
def getLastData(strdate):
    date=globalFunction.lastTddate(strdate)
    dfLastTradeDay=ts.top_list(globalFunction.lastTddate(date))

    strIndex=date.replace("-","")
    listIndex = []
    for i in range(len(dfLastTradeDay)):
        listIndex.append(strIndex + "{:0>2}".format(i))
    dfLastTradeDay.index = listIndex
    return dfLastTradeDay

#根据日期，获得龙虎榜上的股票代码，并根据股票代码返回每天前5的买卖机构,返回一个包含多个元组的list
def getCompany(strdate):
    #寻找上一个交易日
    date=globalFunction.lastTddate(strdate)
    #将该日期所有上榜的股票代码放入listCode中
    df=getLastData(date)
    listCode=[]
    listLast=[]
    for i in df['code']:
        if i not in listCode:
            listCode.append(str(i))
    for j in listCode:
        t=ts.lhb_detail(j,date)
        listLast.append(t)
    return listLast

#获取股票日线数据
def getDayData(code=None,start="2017-01-01",end="2018-12-31"):
    symbol = ct._code_to_symbol(code)       #将代码转换成标准格式
    url = 'http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayqfq2017&param=%s,day,%s,%s,640,qfq'%(symbol,start,end)
    try:
        request=Request(url)
        lines=urlopen(request,timeout=10).read()
        if len(lines)<100:  #no data
            return None
    except Exception as e:
        print(e)
    else:
        lines=lines.decode('utf-8') if ct.PY3 else lines
        lines = lines.split('=')[1]
        reg = re.compile(r',{"nd.*?}')
        lines = re.subn(reg, '', lines)
        reg=re.compile(r',"qt":{.*?}')
        lines = re.subn(reg, '', lines[0])
        reg=r',"mx_price".*?"version":"4"'
        lines = re.subn(reg, '', lines[0])
        reg=r',"mx_price".*?"version":"12"'
        lines = re.subn(reg, '', lines[0])
        #将str格式转换成byte
        textByte=bytes(lines[0],encoding='utf-8')



    return textByte
    raise IOError(ct.NETWORK_URL_ERROR_MSG)

#获取所有股票的日线数据，并Post至java jar中
def getAllStockData():
    list1=globalFunction.getAllStockCode()
    for code in list1:
        textByte=getDayData(code)
        urlPost='http://localhost:8080/stock/tradeHistory'
        globalFunction.postData(textByte,urlPost,code)

# code="600145"
# textByte = getDayData(code)
# urlPost = 'http://localhost:8080/stock/tradeHistory'
# globalFunction.postData(textByte, urlPost, code)