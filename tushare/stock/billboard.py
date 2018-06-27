#!/usr/bin/env python
# -*- coding:utf-8 -*- 
"""
龙虎榜数据
Created on 2015年6月10日
@author: Jimmy Liu
@group : waditu
@contact: jimmysoa@sina.cn
"""

import pandas as pd
from pandas.compat import StringIO
from tushare.stock import cons as ct
import numpy as np
import time
import json
import re
import lxml.html
from lxml import etree
from tushare.util import dateu as du
from tushare.stock import ref_vars as rv
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

def top_list(date = None, retry_count=3, pause=0.001):
    """
    获取每日龙虎榜列表
    Parameters
    --------
    date:string
                明细数据日期 format：YYYY-MM-DD 如果为空，返回最近一个交易日的数据
    retry_count : int, 默认 3
                 如遇网络等问题重复执行的次数 
    pause : int, 默认 0
                重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
    
    Return
    ------
    DataFrame
        code：代码
        name ：名称
        pchange：涨跌幅     
        amount：龙虎榜成交额(万)
        buy：买入额(万)
        bratio：占总成交比例
        sell：卖出额(万)
        sratio ：占总成交比例
        reason：上榜原因
        date  ：日期
    """
    if date is None:
        if du.get_hour() < 18:
            date = du.last_tddate()
        else:
            date = du.today() 
    else:
        if(du.is_holiday(date)):
            return None
    for _ in range(retry_count):
        time.sleep(pause)
        try:
            request = Request(rv.LHB_URL%(ct.P_TYPE['http'], ct.DOMAINS['em'], date, date))
            text = urlopen(request, timeout=10).read()
            text = text.decode('GBK')
            text = text.split('_1=')[1]
            text = eval(text, type('Dummy', (dict,), 
                                           dict(__getitem__ = lambda s, n:n))())    #将不规则json转换成规则的dict
            text = json.dumps(text)
            text = json.loads(text)
            df = pd.DataFrame(text['data'], columns=rv.LHB_TMP_COLS)
            df.columns = rv.LHB_COLS
            df = df.fillna(0)
            df = df.replace('', 0)
            df['buy'] = df['buy'].astype(float)
            df['sell'] = df['sell'].astype(float)
            df['amount'] = df['amount'].astype(float)
            df['Turnover'] = df['Turnover'].astype(float)
            df['bratio'] = df['buy'] / df['Turnover']
            df['sratio'] = df['sell'] /df['Turnover']
            df['bratio'] = df['bratio'].map(ct.FORMAT)
            df['sratio'] = df['sratio'].map(ct.FORMAT)
            df['date'] = date
            for col in ['amount', 'buy', 'sell']:
                df[col] = df[col].astype(float)
                df[col] = df[col] / 10000
                df[col] = df[col].map(ct.FORMAT)
            df = df.drop('Turnover', axis=1)
        except Exception as e:
            print(e)
        else:
            return df
    raise IOError(ct.NETWORK_URL_ERROR_MSG)



def cap_tops(days= 5, retry_count= 3, pause= 0.001):
    """
    获取个股上榜统计数据
    Parameters
    --------
        days:int
                  天数，统计n天以来上榜次数，默认为5天，其余是10、30、60
        retry_count : int, 默认 3
                     如遇网络等问题重复执行的次数 
        pause : int, 默认 0
                    重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
    Return
    ------
    DataFrame
        code：代码
        name：名称
        count：上榜次数
        bamount：累积购买额(万)     
        samount：累积卖出额(万)
        net：净额(万)
        bcount：买入席位数
        scount：卖出席位数
    """
    
    if ct._check_lhb_input(days) is True:
        ct._write_head()
        df =  _cap_tops(days, pageNo=1, retry_count=retry_count,
                        pause=pause)
        if df is not None:
            df['code'] = df['code'].map(lambda x: str(x).zfill(6))
            df = df.drop_duplicates('code')
        return df
    
    
def _cap_tops(last=5, pageNo=1, retry_count=3, pause=0.001, dataArr=pd.DataFrame()):   
    ct._write_console()
    for _ in range(retry_count):
        time.sleep(pause)
        try:
            request = Request(rv.LHB_SINA_URL%(ct.P_TYPE['http'], ct.DOMAINS['vsf'], rv.LHB_KINDS[0],
                                               ct.PAGES['fd'], last, pageNo))
            text = urlopen(request, timeout=10).read()
            text = text.decode('GBK')
            html = lxml.html.parse(StringIO(text))
            res = html.xpath("//table[@id=\"dataTable\"]/tr")
            if ct.PY3:
                sarr = [etree.tostring(node).decode('utf-8') for node in res]
            else:
                sarr = [etree.tostring(node) for node in res]
            sarr = ''.join(sarr)
            sarr = '<table>%s</table>'%sarr
            df = pd.read_html(sarr)[0]
            df.columns = rv.LHB_GGTJ_COLS
            dataArr = dataArr.append(df, ignore_index=True)
            nextPage = html.xpath('//div[@class=\"pages\"]/a[last()]/@onclick')
            if len(nextPage)>0:
                pageNo = re.findall(r'\d+', nextPage[0])[0]
                return _cap_tops(last, pageNo, retry_count, pause, dataArr)
            else:
                return dataArr
        except Exception as e:
            print(e)
            

def broker_tops(days= 5, retry_count= 3, pause= 0.001):
    """
    获取营业部上榜统计数据
    Parameters
    --------
    days:int
              天数，统计n天以来上榜次数，默认为5天，其余是10、30、60
    retry_count : int, 默认 3
                 如遇网络等问题重复执行的次数 
    pause : int, 默认 0
                重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
    Return
    ---------
    broker：营业部名称
    count：上榜次数
    bamount：累积购买额(万)
    bcount：买入席位数
    samount：累积卖出额(万)
    scount：卖出席位数
    top3：买入前三股票
    """
    if ct._check_lhb_input(days) is True:
        ct._write_head()
        df =  _broker_tops(days, pageNo=1, retry_count=retry_count,
                        pause=pause)
        return df


def _broker_tops(last=5, pageNo=1, retry_count=3, pause=0.001, dataArr=pd.DataFrame()):   
    ct._write_console()
    for _ in range(retry_count):
        time.sleep(pause)
        try:
            request = Request(rv.LHB_SINA_URL%(ct.P_TYPE['http'], ct.DOMAINS['vsf'], rv.LHB_KINDS[1],
                                               ct.PAGES['fd'], last, pageNo))
            text = urlopen(request, timeout=10).read()
            text = text.decode('GBK')
            html = lxml.html.parse(StringIO(text))
            res = html.xpath("//table[@id=\"dataTable\"]/tr")
            if ct.PY3:
                sarr = [etree.tostring(node).decode('utf-8') for node in res]
            else:
                sarr = [etree.tostring(node) for node in res]
            sarr = ''.join(sarr)
            sarr = '<table>%s</table>'%sarr
            df = pd.read_html(sarr)[0]
            df.columns = rv.LHB_YYTJ_COLS
            dataArr = dataArr.append(df, ignore_index=True)
            nextPage = html.xpath('//div[@class=\"pages\"]/a[last()]/@onclick')
            if len(nextPage)>0:
                pageNo = re.findall(r'\d+', nextPage[0])[0]
                return _broker_tops(last, pageNo, retry_count, pause, dataArr)
            else:
                return dataArr
        except Exception as e:
            print(e)
        

def inst_tops(days= 5, retry_count= 3, pause= 0.001):
    """
    获取机构席位追踪统计数据
    Parameters
    --------
    days:int
              天数，统计n天以来上榜次数，默认为5天，其余是10、30、60
    retry_count : int, 默认 3
                 如遇网络等问题重复执行的次数 
    pause : int, 默认 0
                重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
                
    Return
    --------
    code:代码
    name:名称
    bamount:累积买入额(万)
    bcount:买入次数
    samount:累积卖出额(万)
    scount:卖出次数
    net:净额(万)
    """
    if ct._check_lhb_input(days) is True:
        ct._write_head()
        df =  _inst_tops(days, pageNo=1, retry_count=retry_count,
                        pause=pause)
        df['code'] = df['code'].map(lambda x: str(x).zfill(6))
        return df 
 

def _inst_tops(last=5, pageNo=1, retry_count=3, pause=0.001, dataArr=pd.DataFrame()):   
    ct._write_console()
    for _ in range(retry_count):
        time.sleep(pause)
        try:
            request = Request(rv.LHB_SINA_URL%(ct.P_TYPE['http'], ct.DOMAINS['vsf'], rv.LHB_KINDS[2],
                                               ct.PAGES['fd'], last, pageNo))
            text = urlopen(request, timeout=10).read()
            text = text.decode('GBK')
            html = lxml.html.parse(StringIO(text))
            res = html.xpath("//table[@id=\"dataTable\"]/tr")
            if ct.PY3:
                sarr = [etree.tostring(node).decode('utf-8') for node in res]
            else:
                sarr = [etree.tostring(node) for node in res]
            sarr = ''.join(sarr)
            sarr = '<table>%s</table>'%sarr
            df = pd.read_html(sarr)[0]
            df = df.drop([2,3], axis=1)
            df.columns = rv.LHB_JGZZ_COLS
            dataArr = dataArr.append(df, ignore_index=True)
            nextPage = html.xpath('//div[@class=\"pages\"]/a[last()]/@onclick')
            if len(nextPage)>0:
                pageNo = re.findall(r'\d+', nextPage[0])[0]
                return _inst_tops(last, pageNo, retry_count, pause, dataArr)
            else:
                return dataArr
        except Exception as e:
            print(e)


def inst_detail(retry_count= 3, pause= 0.001):
    """
    获取最近一个交易日机构席位成交明细统计数据
    Parameters
    --------
    retry_count : int, 默认 3
                 如遇网络等问题重复执行的次数 
    pause : int, 默认 0
                重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
                
    Return
    ----------
    code:股票代码
    name:股票名称     
    date:交易日期     
    bamount:机构席位买入额(万)     
    samount:机构席位卖出额(万)     
    type:类型
    """
    ct._write_head()
    df =  _inst_detail(pageNo=1, retry_count=retry_count,
                        pause=pause)
    if len(df)>0:
        df['code'] = df['code'].map(lambda x: str(x).zfill(6))
    return df  
 

def _inst_detail(pageNo=1, retry_count=3, pause=0.001, dataArr=pd.DataFrame()):   
    ct._write_console()
    for _ in range(retry_count):
        time.sleep(pause)
        try:
            request = Request(rv.LHB_SINA_URL%(ct.P_TYPE['http'], ct.DOMAINS['vsf'], rv.LHB_KINDS[3],
                                               ct.PAGES['fd'], '', pageNo))
            text = urlopen(request, timeout=10).read()
            text = text.decode('GBK')
            html = lxml.html.parse(StringIO(text))
            res = html.xpath("//table[@id=\"dataTable\"]/tr")
            if ct.PY3:
                sarr = [etree.tostring(node).decode('utf-8') for node in res]
            else:
                sarr = [etree.tostring(node) for node in res]
            sarr = ''.join(sarr)
            sarr = '<table>%s</table>'%sarr
            df = pd.read_html(sarr)[0]
            df.columns = rv.LHB_JGMX_COLS
            dataArr = dataArr.append(df, ignore_index=True)
            nextPage = html.xpath('//div[@class=\"pages\"]/a[last()]/@onclick')
            if len(nextPage)>0:
                pageNo = re.findall(r'\d+', nextPage[0])[0]
                return _inst_detail(pageNo, retry_count, pause, dataArr)
            else:
                return dataArr
        except Exception as e:
            print(e)

            
def _f_rows(x):
    if '%' in x[3]:
        x[11] = x[6]
        for i in range(6, 11):
            x[i] = x[i-5]
        for i in range(1, 6):
            x[i] = np.NaN
    return x

#self
def lhb_detail(code=None, date=None, retry_count=3, pause=0.001):
    """
    获取个股龙虎榜明细数据
    Parameters
    --------
        code:str
                股票代码
        date:str
                日期
        retry_count : int, 默认 3
                     如遇网络等问题重复执行的次数
        pause : int, 默认 0
                    重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
    Return
    ------
    tuple(DataFrame1,DateFrame2)
    DataFrame
        code:股票代码
        date:日期
        broker：营业部名称
        count：上榜次数
        probability：买入后上涨概率
        buy：买入金额(万)
        buy_prop:买入额占总成交比
        sell：卖出金额(万)
        sell_prop：卖出额占总成交比
        net：净额(万)
        buysellflag:买入卖出标记
    """
    df1 = None
    df2 = None
    for _ in range(retry_count):
        time.sleep(pause)
        try:
            request = Request(rv.LHB_DETAIL % (date, code))
            text = urlopen(request, timeout=10).read()
            text = text.decode('GBK')
            html = lxml.html.parse(StringIO(text))
            res = html.xpath("//tbody")
            if ct.PY3:
                sarr = [etree.tostring(node).decode('utf-8') for node in res]
            else:
                sarr = [etree.tostring(node) for node in res]
            sarr.pop(0)                     #舍弃无用的第一个元素
            sarr = ''.join(sarr)
            sarr = sarr.replace('tbody', 'table')   #规范格式
            list_sarr = pd.read_html(sarr)          #由于有两个<table>,所以得到两个dataframe

            for i in range(len(list_sarr)):
                df=list_sarr[i]

            #处理dataframe
                # 删除卖出表的最后一行统计数据
                if df.iloc[:,0].size==6:                #只保留5行数据
                    df.drop([5],inplace=True,axis=0)

                # 删除第一列无用的序号
                df.drop([0],inplace=True,axis=1)

                #处理机构那一列，拆分成三列
                df[1]=df[1].map(lambda x: str(x).split("  "))   #引号里为两个空格
                try:                                            #将原有列拆分成三个新的Series
                    ser1=df[1].map(lambda x:x[0])
                    ser2 = df[1].map(lambda x: x[1])
                    ser3 = df[1].map(lambda x: x[2])
                except Exception as e:
                    pass
                df.drop(1,inplace=True,axis=1)                  #删除原有列
                df.insert(0, 'broker', ser1)
                df.insert(1, 'count', ser2)
                df.insert(2, 'per', ser3)

                #在最前面增加code与date两列
                df.insert(0,'code',str(code))
                df.insert(1,'date',str(date))

                #在最后面加上买卖标记
                if i==0:
                    df.insert(len(df.columns),'buysellflag','buy')
                elif i==1:
                    df.insert(len(df.columns), 'buysellflag', 'sell')

                #判断如果字段个数，若一致，则套用表头
                if len(df.columns)==11:
                    df.columns = rv.LHB_DETAIL_COLS
                elif len(df.columns)==10:        #若只有10列，说明没有买入卖出机构：
                    #如何处理
                    df.insert(5,'None',None)
                    df.columns = rv.LHB_DETAIL_COLS
                    df.loc[0]=[code,date,'没有买入或卖出机构','None','None','None','None','None','None','None','None']

                #赋值
                if i==0:
                    df1=df
                elif i==1:
                    df2=df
            list1=[df1,df2]
            return pd.concat(list1)
        except Exception as e:
            print(e)

