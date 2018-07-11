#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
#ABSPATH = os.path.abspath(os.path.realpath(os.path.dirname(__file__)))         #将本文件路径加入包搜索范围
sys.path.append("H:\\github\\tushareB\\")
import datetime

import tushare as ts
import self.longhu.globalFunction as globalFunction
import time
import json
from tushare.stock import ref_vars as rv
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

def brokerInfo(statrDate=None, endDate=None, pagesize=2000):
    urlPost="http://localhost:8080/broker/purchaseSummary"
    LHBYYBSBCS=LHBYYBSBCS="http://datainterface3.eastmoney.com/EM_DataCenter_V3/Api//LHBYYBSBCS/GetLHBYYBSBCS?tkn=eastmoney&mkt=&dateNum=&startDateTime=%s&endDateTime=%s&sortRule=1&sortColumn=JmMoney&pageNum=1&pageSize=%s&cfg=lhbyybsbcs"
    print(LHBYYBSBCS % (statrDate, endDate, pagesize))
    try:
        request=Request(LHBYYBSBCS%(statrDate,endDate,pagesize))
        text=urlopen(request,timeout=10).read()                     #type is byte
        req=Request(urlPost)
        req.add_header('Content-Type','application/json;charset=utf-8')
        req.add_header('Content-Length',len(text))
        response=urlopen(req,text)                                  # text一定要是byte
        print(response.status)
    except Exception as e:
        print(e)


#Main and Run
#将每日机构数据导入数据库
startDate=globalFunction.lastTddate(str(datetime.datetime.today().date()-datetime.timedelta(days=7)))
endDate=str(datetime.datetime.today().date())
brokerInfo(startDate,endDate,200000)


