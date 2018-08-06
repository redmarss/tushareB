#!/usr/bin/env python
# -*-coding:utf8-*-

import self.longhu.globalFunction as gl
import self.longhu.mysqlConn as msql
import time
import pandas as pd

def CreateScoreTable():
    start=time.clock()
    list_broker=gl.getAllBrokerInfo()
    df_broker=pd.DataFrame(list_broker)
    for i in range(2,12):                       #在原有的code,name后再增加11列全0的数字
        df_broker.insert(i,str(i),0)
    list_broker_title=['broker_code','broker_name','b_count','s_count','avr_2day','avr_3day','avr_5day','avr_7day','avr_10day','2daylimit_count','maxlimit_count','score']
    df_broker.columns=list_broker_title
    msql.DataframeToSql(df_broker,'broker_score')
    end=time.clock()
    print("耗时%s秒"%(end-start))

