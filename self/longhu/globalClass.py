#!/usr/bin/env python
# -*- coding:utf8 -*-

import self.longhu.globalFunction as gl

#stockPrice类
#输入一个长度为8的元组作为参数，只读。参数分别是index,stock_code,tsdate,open,close,average
#输入参数从gl.getStockPrice()取【参数为code,date,day(某个股票某天后几天内的交易数据)，返回元组，再切片】
class StockPrice(object):
    def __init__(self,tuple):
        if len(tuple)==8:
            self.tuple=tuple
        else:
            print("类参数输入错误")
            return

    @property
    def stock_code(self):
        return self.tuple[1]
    @property
    def ts_date(self):
        return self.tuple[2]
    @property
    def open(self):
        return self.tuple[3]
    @property
    def close(self):
        return self.tuple[4]
    @property
    def high(self):
        return self.tuple[5]
    @property
    def low(self):
        return self.tuple[6]
    @property
    def volumne(self):
        return self.tuple[7]

#机构分数类
#输入一个长度为13的LIST作为参数，可读可写。参数为【index,broker_code,broker_name,b_count,s_count,avr_2day,avr_3day,avr_5day,avr_7day,avr_10day,2daylimit_count,maxlimit_count,score】
#输入参数从数据库broker_score中取
class BrokerScore(object):
    def __init__(self,list):
        if len(list)==13:
            self.list=list
        else:
            print("类参数输入错误")
            return

    @property
    def score_index(self):
        return self.list[0]
    @score_index.setter
    def score_index(self):
        pass

    @property
    def broker_code(self):
        return self.list[1]
    @broker_code.setter
    def broker_code(self):
        pass

    @property
    def broker_name(self):
        return self.list[2]
    @broker_name.setter
    def broker_name(self):
        pass

    @property
    def b_count(self):
        return self.list[3]
    @b_count.setter
    def b_count(self):
        pass

    @property
    def s_count(self):
        return self.list[4]
    @s_count.setter
    def s_count(self):
        pass

    @property
    def avr_2day(self):
        return self.list[5]
    @avr_2day.setter
    def avr_2day(self):
        pass

    @property
    def avr_3day(self):
        return self.list[6]
    @avr_3day.setter
    def avr_3day(self):
        pass

    @property
    def avr_5day(self):
        return self.list[7]
    @avr_5day.setter
    def avr_5day(self):
        pass

    @property
    def avr_7day(self):
        return self.list[8]
    @avr_7day.setter
    def avr_7day(self):
        pass

    @property
    def avr_10day(self):
        return self.list[9]
    @avr_10day.setter
    def avr_10day(self):
        pass

    @property
    def day2limit_count(self):
        return self.list[10]
    @day2limit_count.setter
    def day2limit_count(self):
        pass

    @property
    def maxlimit_count(self):
        return self.list[11]
    @maxlimit_count.setter
    def maxlimit_count(self):
        pass

    @property
    def score(self):
        return self.list[12]
    @score.setter
    def score(self):
        pass

#打分类
#输入一个长度不限的列表作为参数。
class Score(object):
    __score=0
    __stockcode=None
    __listStockPrice=[]
    __stockPriceDay1=None
    __stockPriceDay2=None
    __stockPriceDay3=None
    __stockPriceDay4=None
    __stockPriceDay5=None
    @property
    def score(self):
        return self.__score

    def __init__(self,list):
        #判断输入参数中每个元素必须是stockPrice类的对象
        flag=0
        for i in range(len(list)):
            if isinstance(list[i],StockPrice):
                flag+=1
        if flag==len(list):
            self.__listStockPrice=list
            self.__stockcode=list[0].stock_code[2:]
            self.__stockPriceDay1=list[0]
            self.__stockPriceDay2=list[1]
            self.__stockPriceDay3=list[2]
            self.__stockPriceDay4=list[3]
            self.__stockPriceDay5=list[4]

        else:
            print("error")

    #处理第二天的分数
    def __day2(self):
        #第二天开盘涨停

        if gl.isLimit(self.__stockcode,self.__stockPriceDay1.close,self.__stockPriceDay2.open)==True:
            #第二天最低价=最高价（一字涨停）
            if self.__stockPriceDay2.high==self.__stockPriceDay2.low:
                self.__score+=1             #加一分
            #最低价<最高价（高开低走）
            elif self.__stockPriceDay2.low<self.__stockPriceDay2.high:
                #加（收盘价-开盘价）幅度*10
                self.__score=self.__score+gl.Range(self.__stockPriceDay1.close,self.__stockPriceDay2.open,self.__stockPriceDay2.close)*10

        else:
            #收盘>开盘
            if self.__stockPriceDay2.close>self.__stockPriceDay2.open:
                #开盘不涨停，收盘>开盘，直接+4分
                self.__score+=4
                #收盘涨停，附加3分
                if gl.isLimit(self.__stockcode,self.__stockPriceDay2.open,self.__stockPriceDay2.close):
                    self.__score+=3
                #收盘不涨停，附加（收盘价-开盘价）幅度*10
                else:
                    self.__score=self.__score+gl.Range(self.__stockPriceDay1.close,self.__stockPriceDay2.open,self.__stockPriceDay2.close)*10

                #另一个条件：如果第二日收盘不如前一日收盘高，减去4分
                if self.__stockPriceDay2.close<=self.__stockPriceDay1.close:
                    self.__score-=4
            #收盘<=开盘,减去2分，再减去（收盘价-开盘价）幅度*10
            else:
                self.__score-=2
                self.__score=self.__score-gl.Range(self.__stockPriceDay1.close,self.__stockPriceDay2.open,self.__stockPriceDay2.close)*10

    #处理第三天的分数
    def __day3(self):
        pass

    #算总分
    def calcScore(self):
        self.__day2()
        print(self.__score)


