#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import time
#ABSPATH = os.path.abspath(os.path.realpath(os.path.dirname(__file__)))         #将本文件路径加入包搜索范围
sys.path.append("H:\\github\\tushareB\\")
import self.longhu.mysqlConn as msql
import tushare as ts
import self.longhu.globalFunction as gl
import self.longhu.globalClass as gc
import pandas as pd

def ScoreBroker(broker_code=None,stock_code=None,ts_date=None):
#取出数据库机构Score信息并存入BrokerScore的实例对象中
    sql="select * from broker_score where broker_code='%s'"%broker_code
    clsBrokerScore=None
    try:
        list_broker_info=list(msql.selectSqlAll(sql)[0])            #只取第一条结果，也只应有一条
        clsBrokerScore=gc.BrokerScore(list_broker_info)
    except:
        print("broker_code Error")

#更新BrokerScoker信息
    #该机构在ts_date买入stock_code后十天的表现，每天的价格存入StockPrice类中，每个类Append至list_stock_price中
    count_day=10                        #计数天数
    t_stock_price=gl.getStockPrice(stock_code,ts_date,count_day)
    list_stock_price=[]

    if len(t_stock_price)==count_day+1:             #至少有count_day天的数据，否则可能是停牌或新股（会报边界错误）
        for i in range(len(t_stock_price)):
            list_stock_price.append(gc.StockPrice(t_stock_price[i]))
        gc.Score(list_stock_price)
    else:
        print("股票天数长度不对")
        raise IndexError


















