#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
#ABSPATH = os.path.abspath(os.path.realpath(os.path.dirname(__file__)))         #将本文件路径加入包搜索范围
sys.path.append("H:\\github\\tushareB\\")
import datetime

import tushare as ts
import self.longhu.globalFunction as gl
import self.longhu.getFromTushare as gt
import time
import json
from tushare.stock import ref_vars as rv
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request



#根据日期取出机构交易数据并调用postData函数至数据库
def brokerInfo(statrDate=None, endDate=None, pagesize=2000):
    urlPost="http://localhost:8080/broker/purchaseSummary"
    LHBYYBSBCS=LHBYYBSBCS="http://datainterface3.eastmoney.com/EM_DataCenter_V3/Api//LHBYYBSBCS/GetLHBYYBSBCS?tkn=eastmoney&mkt=&dateNum=&startDateTime=%s&endDateTime=%s&sortRule=1&sortColumn=JmMoney&pageNum=1&pageSize=%s&cfg=lhbyybsbcs"
    try:
        request=Request(LHBYYBSBCS%(statrDate,endDate,pagesize))
        text=urlopen(request,timeout=10).read()                     #type is byte
        gl.postData(text,urlPost)
    except Exception as e:
        print(e)


def getAllStockData():
    li = []
    for key in gl.getAllStockCode():
        li.append(key)
    urlPost = 'http://localhost:8080/stock/tradeHistory'
    for i in li:
        textByte = gt.getDayData(i, startDate, endDate)
        gl.postData(textByte, urlPost, i)



#Main and Run

startDate=gl.lastTddate(str(datetime.datetime.today().date()-datetime.timedelta(days=7)))
endDate=str(datetime.datetime.today().date())

#将每日机构数据导入数据库
brokerInfo(startDate,endDate,200000)

#将每日交易数据导入数据库
getAllStockData()


