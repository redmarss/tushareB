#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
#ABSPATH = os.path.abspath(os.path.realpath(os.path.dirname(__file__)))         #将本文件路径加入包搜索范围
sys.path.append("H:\\github\\tushareB\\")
import datetime
import self.longhu.globalFunction as gl
import self.longhu.getFromTushare as gt
# import tushare as ts
# import time
# import json
# from tushare.stock import ref_vars as rv
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request



#根据日期取出机构交易数据并调用postData函数至数据库
def brokerInfo(startDate=None, endDate=None, pagesize=2000):
    urlPost="http://localhost:8080/broker/purchaseSummary"
    LHBYYBSBCS="http://datainterface3.eastmoney.com/EM_DataCenter_V3/Api//LHBYYBSBCS/GetLHBYYBSBCS?tkn=eastmoney&mkt=&dateNum=&startDateTime=%s&endDateTime=%s&sortRule=1&sortColumn=JmMoney&pageNum=1&pageSize=%s&cfg=lhbyybsbcs"
    try:
        request=Request(LHBYYBSBCS%(startDate,endDate,pagesize))
        text=urlopen(request,timeout=10).read()                     #type is byte
        print(text)
        gl.postData(text,urlPost)
    except Exception as e:
        print(e)

#获取所有股票的交易信息
def getAllStockData(startDate=None, endDate=None):
    #将所有股票代码存入一个list
    li = []
    for key in gl.getAllStockCode():
        li.append(key)

    urlPost = 'http://localhost:8080/stock/tradeHistory'        #定义post至mvn的地址
    for i in li:
        textByte = gt.getDayData(i, start, end)                 #从网页获取交易信息
        gl.postData(textByte, urlPost, i)                       #post至mvn



#Main and Run
#将时间范围定义到（今天至14天前）
start=gl.lastTddate(str(datetime.datetime.today().date()-datetime.timedelta(days=14)))
end=str(datetime.datetime.today().date())

#将时间范围内的机构买卖信息导入数据库，重复的不导入
brokerInfo(start,end,200000)

#将时间范围内所有股票的交易数据导入数据库
getAllStockData(start,end)


