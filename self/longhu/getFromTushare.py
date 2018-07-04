#!/usr/bin/env python
# -*- coding:utf8 -*-

import self.longhu.globalFunction as gl
import tushare as ts
import pandas as pd



#获取每日龙虎榜信息，并修改成指定格式，返回一个dataframe
def getLastData(strdate):
    date=gl.lastTddate(strdate)
    dfLastTradeDay=ts.top_list(gl.lastTddate(date))

    strIndex=date.replace("-","")
    listIndex = []
    for i in range(len(dfLastTradeDay)):
        listIndex.append(strIndex + "{:0>2}".format(i))
    dfLastTradeDay.index = listIndex
    return dfLastTradeDay

#根据日期，获得龙虎榜上的股票代码，并根据股票代码返回每天前5的买卖机构,返回一个包含多个元组的list
def getCompany(strdate):
    #寻找上一个交易日
    date=gl.lastTddate(strdate)
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
