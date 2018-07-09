#!/usr/bin/env python
# -*- coding:utf8 -*-
import datetime
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request


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

