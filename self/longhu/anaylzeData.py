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



#根据日期显示Top100的出现次数，返回dataframe('broker_code','broker_name','b_count','score')
def Last3MonthTrade(startdate="2017-01-01"):
    df=pd.DataFrame(columns=('broker_code','broker_name','b_count','score'))
    #先从broker_score表中将分数前100名的机构取出
    sql1="SELECT broker_code,score FROM tushare.broker_score order by score desc LIMIT 0, 100"
    t=msql.selectSqlAll(sql1)

    for i in range(len(t)):
        sql2='SELECT count(*),broker_name FROM broker_buy_summary as a,broker_buy_stock_info as b where a.id=b.broker_buy_summary_id and ts_date>="%s" and broker_code="%s"'%(startdate,t[i][0])
        t2=msql.selectSqlAll(sql2)
        df.loc[i]=[t[i][0],t2[0][1],t2[0][0],t[i][1]]
    return df


#根据机构代码、交易日期计算该机构近5次交易的明细
def Last5TradeScore(broker_code,ts_date):
    #根据机构代码，交易日期，取出该机构在上榜前（至多10次）买入的股票
    select_str="broker_code,broker_name,ts_date,stock_code,stock_name"
    #check_date=gl.diffDay(ts_date,-7)
    check_date="2018-04-18"
    sql="select %s from broker_buy_stock_info as a,broker_buy_summary as b where a.broker_buy_summary_id=b.id and b.broker_code='%s' and b.ts_date<'%s' order by ts_date desc LIMIT 0,10"%(select_str,broker_code,check_date)
    t=msql.selectSqlAll(sql)
    for i in range(len(t)):
        list_stock_price = []
        last_ts_date = t[i][2]
        last_stock_code=t[i][3][:6]
        t1=gl.getStockPrice(last_stock_code,last_ts_date,7)
        for j in range(len(t1)):
            list_stock_price.append(gc.StockPrice(t1[j]))
        calc=gc.Score(list_stock_price)
        score=calc.calcScore()
        print(score)


    
















