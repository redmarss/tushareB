#!/usr/bin/env python
# -*- coding:utf8 -*-
import self.longhu.globalFunction as gl
import datetime

import tushare as ts
import self.longhu.getFromTushare
import time
import json
from tushare.stock import ref_vars as rv
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

def brokerInfo(statrDate=None, endDate=None, pagesize=2000):
    urlPost="http://localhost:8080/broker/purchaseSummary"
    try:
        print(rv.LHBYYBSBCS%(statrDate,endDate,pagesize))
        request=Request(rv.LHBYYBSBCS%(statrDate,endDate,pagesize))
        text=urlopen(request,timeout=10).read()                     #type is byte
        req=Request(urlPost)
        req.add_header('Content-Type','application/json;charset=utf-8')
        req.add_header('Content-Length',len(text))
        response=urlopen(req,text)                                  # text一定要是byte
    except Exception as e:
        print(e)


#Main and Run
#将每日机构数据导入数据库
startDate=gl.lastTddate(str(datetime.datetime.today().date()-datetime.timedelta(days=1)))
endDate=str(datetime.datetime.today().date())
brokerInfo(startDate,endDate,2000)

