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

#根据机构代码，买入股票代码，买入股票日期，更新数据库Score表中信息
def ScoreBroker(broker_code=None,stock_code=None,ts_date=None):
    brokerScoreCls=None
    count_day=10    #计数天数
#取出机构分数数据并存入BrokerScore类实例中，方便修改
    sql=r"select * from broker_score where broker_code='%s'"%broker_code
    try:
        list_broker_info=list(msql.selectSqlAll(sql)[0])            #只取第一条结果，也只应有一条
        brokerScoreCls=gc.BrokerScore(list_broker_info)
    except:
        print("没有找到相应机构数据")


#更新BrokerScoker信息
#1.计算此笔交易的Score
    #该机构在ts_date买入stock_code后十天的表现，每天的价格存入StockPrice类中，每个类Append至list_stock_price中
    t_stock_price=gl.getStockPrice(stock_code,ts_date,count_day)
    list_stock_price=[]
    if len(t_stock_price)==count_day:             #至少有count_day天的数据，否则可能是停牌或新股（会报边界错误）
        for i in range(len(t_stock_price)):
            list_stock_price.append(gc.StockPrice(t_stock_price[i]))
        calc=gc.Score(list_stock_price)
        today_score=calc.calcScore()
    else:
        print("股票价格的长度不对(%s,%s,%s)"%(stock_code,ts_date,broker_code))
        return
#2.计算平均score,更新b_count次数
    avr_scroe=(brokerScoreCls.score*brokerScoreCls.b_count+today_score)/(brokerScoreCls.b_count+1)
    b_count_temp=brokerScoreCls.b_count
    b_count_temp+=1
    brokerScoreCls.b_count=b_count_temp
    brokerScoreCls.score=float('%.2f'%avr_scroe)

#将ScoreBroker类实例存入数据库（调用类函数）
    brokerScoreCls.updateMysql()

#输入起始、结束日期，计算broker_buy_stock_info中所有交易的“得分”
def RunScore(startdate='2017-01-01',enddate='2018-12-31'):
    sql="SELECT broker_code,stock_code,ts_date,broker_buy_summary_id FROM broker_buy_summary as a,broker_buy_stock_info as b where a.id=b.broker_buy_summary_id and score_flag=0 and ts_date between '%s' and '%s' "%(startdate,enddate)
    t=msql.selectSqlAll(sql)
    for i in range(len(t)):
        ScoreBroker(t[i][0],t[i][1][0:6],str(t[i][2]))
        sql="update broker_buy_stock_info set score_flag=1 where broker_buy_summary_id='%s'"%t[i][3]
        msql.OperateSql(sql)

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


#根据机构代码、交易日期计算该机构近5次交易的“得分”
def Last5TradeScore(broker_code,ts_date):
    
















