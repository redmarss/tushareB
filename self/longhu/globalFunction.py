#!/usr/bin/env python
# -*- coding:utf8 -*-
from tushare.stock import cons as ct
import self.longhu.mysqlConn as msql
import datetime
import re
import csv
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request



#判断是否涨停板
def IsLimit(open,close):
    if close>=round(1.1*open):
        return True
    else:
        return False

#判断股票涨或跌
def RaiseOrFall(open,close):
    if open<close:
        return True
    else:
        return False

#返回上一交易日（字符串格式）
def lastTddate(strdate):
    date=None
    try:
        date = datetime.datetime.strptime(strdate, "%Y-%m-%d").date()
        while is_holiday(str(date))==True:
            date=date-datetime.timedelta(days=1)
        return str(date)
    except:
        print("日期输入有误")

def is_holiday(date):
    '''
            判断是否为交易日，返回True or False
            1、接口地址：http://api.goseek.cn/Tools/holiday?date=数字日期，支持https协议。
            2、返回数据：工作日对应结果为 0, 休息日对应结果为 1, 节假日对应的结果为 2
            3、节假日数据说明：本接口包含2017年起的中国法定节假日数据，数据来源国务院发布的公告，每年更新1次，确保数据最新
            4、示例：
            http://api.goseek.cn/Tools/holiday?date=20170528
            https://api.goseek.cn/Tools/holiday?date=20170528
            返回数据：
            {"code":10001,"data":2}

    '''

    apiUrl="http://api.goseek.cn/Tools/holiday?date="+str(date)
    request = Request(apiUrl)
    try:
        response=urlopen(request)
    except Exception as e:
        print(e)
    else:
        response_data=response.read()


    if str(response_data)[-3]=='0':
        return False
    else:
        return True

#输入一个日期及天数，返回该日期加上/减去该数量的交易日的结果
def diffDay(strdate,day=0):
    date=None
    try:
        date = datetime.datetime.strptime(strdate,"%Y-%m-%d").date()
        if day>0:
            while(day>0):
                date=date+datetime.timedelta(days=1)
                if is_holiday(date)==False:
                    day=day-1
        else:
            while(day<0):
                date=date+datetime.timedelta(days=-1)
                if is_holiday(date)==False:
                    day=day+1
        return str(date)
    except:
        print("日期或天数输入有误")

#将byte数据Post至jar服务中
def postData(textByte,urlPost,code=None):
    if isinstance(textByte,str):
        textByte=bytes(textByte,encoding='utf8')
    elif isinstance(textByte,bytes):
        pass
    else:
        print('输入文件格式错误')
        return None
    try:
        req=Request(urlPost)
        req.add_header('Content-Type','application/json;charset=utf-8')
        req.add_header('Content-Length',len(textByte))
        response=urlopen(req,textByte)
        if response.status==200:
            if code is None:
                print("龙虎榜数据完成")
            else:
                print("%s完成"%code)
    except Exception as e:
        if e.code==500:
            print("%s或已退市"%code)
        else:
            print(e)

#获取所有股票代码
def getAllStockCode():
    stock_CodeUrl="http://quote.eastmoney.com/stocklist.html"
    allCodeList=[]
    csvFileSH=open(r"H:\github\tushareB\self\longhu\SHALIST.csv","r")
    readerSH=csv.reader(csvFileSH)
    for item in readerSH:
        if readerSH.line_num==1:
            continue
        allCodeList.append(item[0])

    csvFileSZ=open(r"H:\github\tushareB\self\longhu\SZALIST.csv","r")
    readerSZ=csv.reader(csvFileSZ)
    for item in readerSZ:
        if readerSZ.line_num==1:
            continue
        allCodeList.append(item[0])
    return allCodeList
    # try:
    #     request=Request(stock_CodeUrl)
    #     html=urlopen(request,timeout=10).read()
    #     html=html.decode('gbk')
    #     s=r'<li><a target="_blank" href="http://quote.eastmoney.com/\S\S(.*?).html">'
    #     pat=re.compile(s)
    #     code=pat.findall(html)
    # except Exception as e:
    #     print(e)
    #     return None
    # for item in code:
    #     if item[0] == '6' or item[0] == '3' or item[0] == '0':
    #
    #         allCodeList.append(item)

#获取某股票N个交易日内的所有数据,返回元组
def getStockPrice(code,startdate=None,days=7):
    code = ct._code_to_symbol(code)
    if startdate==None:
        startdate=str(datetime.datetime.today().date())
    enddate=diffDay(startdate,days)

    sql="select * from stock_trade_history_info where stock_code='%s' and ts_date between '%s' and '%s'"%(code,startdate,enddate)
    try:
        t=msql.selectSqlAll(sql)
        return t
    except:
        print("code或startdate错误")
        return None

#取得数据库中所有机构代码及名称,返回列表
def getAllBrokerInfo():
    sql="select broker_code,broker_name from broker_buy_summary"
    t=msql.selectSqlAll(sql)
    #去除t中重复值
    list_temp=list(t)
    set_temp=set(list_temp)
    return list(set_temp)

#生成所需要的随机数
def _random(n=13):
    from random import randint
    start = 10**(n-1)
    end = (10**n)-1
    return str(randint(start, end))
