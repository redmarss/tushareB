#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
#ABSPATH = os.path.abspath(os.path.realpath(os.path.dirname(__file__)))         #将本文件路径加入包搜索范围
sys.path.append("H:\\github\\tushareB\\")
import self.longhu.mysqlConn as msql


def anaylzeLonghu(broker_code,date):
    #根据机构代码、日期筛选出当日购买的股票代码
    sql_broker="select id from broker_buy_summary where broker_code='%s' and ts_date='%s'"%(broker_code,date)
    result=msql.selectSqlAll(sql_broker)
    broker_buy_summary_id=result[0][0]
    sql_stock="select stock_code from broker_buy_stock_info where broker_buy_summary_id=%i"%(broker_buy_summary_id)
    result_stock=msql.selectSqlAll(sql_stock)

    code_list=[]
    for i in range(len(result_stock)):                      #将该机构当日买的股票代码存入code_list
        code_list.append(result_stock[i][0][:6])

