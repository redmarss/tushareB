#!/usr/bin/env python
# -*-coding:utf8-*-

import self.longhu.globalFunction as gl
import self.longhu.globalClass as gc
import self.longhu.mysqlConn as msql
import time
import pandas as pd


#建立Broker_score表，所有数据均为0
def CreateScoreTable():
    start=time.clock()
    list_broker=gl.getAllBrokerInfo()
    df_broker=pd.DataFrame(list_broker)
    for i in range(1,11):                       #在原有的code,name后再增加11列全0的数字
        df_broker.insert(i,str(i),0)
    list_broker_title=['broker_code','b_count','s_count','avr_2day','avr_3day','avr_5day','avr_7day','avr_10day','2daylimit_count','maxlimit_count','score']
    df_broker.columns=list_broker_title
    msql.DataframeToSql(df_broker,'broker_score')
    end=time.clock()
    print("成功，耗时%s秒"%(end-start))

#根据机构代码，买入股票代码，买入股票日期（一次行为），更新数据库Score表中信息
def ScoreBroker(broker_code=None,stock_code=None,ts_date=None):
    brokerScoreCls=None
    count_day=10    #计数天数（10天）
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
        calc=gc.Score(list_stock_price)             #创建Score类实例
        today_score=calc.calcScore()                #返回两位小数点的float
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
