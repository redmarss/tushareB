#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import datetime
from decimal import Decimal
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
    t_stock_price=((81, 'sh600000', datetime.date(2017, 5, 5), Decimal('11.24'), Decimal('11.25'), Decimal('11.26'), Decimal('10.91'), Decimal('401945.00')), (82, 'sh600000', datetime.date(2017, 5, 8), Decimal('11.17'), Decimal('11.33'), Decimal('11.33'), Decimal('11.10'), Decimal('435685.00')), (83, 'sh600000', datetime.date(2017, 5, 9), Decimal('11.04'), Decimal('11.09'), Decimal('11.15'), Decimal('11.02'), Decimal('192254.00')), (84, 'sh600000', datetime.date(2017, 5, 10), Decimal('11.09'), Decimal('10.98'), Decimal('11.16'), Decimal('10.94'), Decimal('283594.00')), (85, 'sh600000', datetime.date(2017, 5, 11), Decimal('10.95'), Decimal('11.09'), Decimal('11.12'), Decimal('10.94'), Decimal('273129.00')), (86, 'sh600000', datetime.date(2017, 5, 12), Decimal('11.09'), Decimal('11.43'), Decimal('11.45'), Decimal('11.07'), Decimal('457334.00')), (87, 'sh600000', datetime.date(2017, 5, 15), Decimal('11.48'), Decimal('11.48'), Decimal('11.60'), Decimal('11.39'), Decimal('299658.00')), (88, 'sh600000', datetime.date(2017, 5, 16), Decimal('11.45'), Decimal('11.48'), Decimal('11.49'), Decimal('11.33'), Decimal('248753.00')), (89, 'sh600000', datetime.date(2017, 5, 17), Decimal('11.45'), Decimal('11.43'), Decimal('11.47'), Decimal('11.33'), Decimal('334344.00')), (90, 'sh600000', datetime.date(2017, 5, 18), Decimal('11.35'), Decimal('11.28'), Decimal('11.38'), Decimal('11.24'), Decimal('306579.00')), (91, 'sh600000', datetime.date(2017, 5, 19), Decimal('11.30'), Decimal('11.29'), Decimal('11.33'), Decimal('11.21'), Decimal('286106.00')))

    if len(t_stock_price)==count_day+1:             #至少有count_day天的数据，否则可能是停牌或新股（会报边界错误）
        for i in range(len(t_stock_price)):
            list_stock_price.append(gc.StockPrice(t_stock_price[i]))
        calc=gc.Score(list_stock_price)
        calc.calcScore()
    else:
        print("股票天数长度不对")
        raise IndexError


















