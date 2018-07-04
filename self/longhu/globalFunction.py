#!/usr/bin/env python
# -*- coding:utf8 -*-
import datetime
from tushare.util import dateu as du

#返回上一交易日（字符串格式）
def lastTddate(strdate):
    date=None
    try:
        date = datetime.datetime.strptime(strdate, "%Y-%m-%d").date()
        while du.is_holiday(str(date))==True:
            date=date-datetime.timedelta(days=1)
        return str(date)
    except:
        print("日期输入有误")