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
    __index=None
    __broker_code=None
    __broker_name=None
    __b_count=None
    __s_count=None
    __avr_2day=None
    __avr_3day=None
    __avr_5day=None
    __avr_7day=None
    __avr_10day=None
    __day2limit_count=None
    __maxlimit_count=None
    __score=None



    def __init__(self,list):
        if len(list)==13:
            self.list=list
            self.__index=list[0]
            self.__broker_code=list[1]
            self.__broker_name=list[2]
            self.__b_count=list[3]
            self.__s_count=list[4]
            self.__avr_2day=list[5]
            self.__avr_3day=list[6]
            self.__avr_5day=list[7]
            self.__avr_7day=list[8]
            self.__avr_10day=list[9]
            self.__day2limit_count=list[10]
            self.__maxlimit_count=list[11]
            self.__score=list[12]
        else:
            print("类参数输入错误")
            return

    @property
    def score_index(self):
        return self.__index
    @score_index.setter
    def score_index(self):
        pass

    @property
    def broker_code(self):
        return self.__broker_code
    @broker_code.setter
    def broker_code(self):
        pass

    @property
    def broker_name(self):
        return self.__broker_name
    @broker_name.setter
    def broker_name(self):
        pass

    @property
    def b_count(self):
        return self.__b_count
    @b_count.setter
    def b_count(self,value):
        self.__b_count=value

    @property
    def s_count(self):
        return self.__s_count
    @s_count.setter
    def s_count(self):
        pass

    @property
    def avr_2day(self):
        return self.__avr_2day
    @avr_2day.setter
    def avr_2day(self):
        pass

    @property
    def avr_3day(self):
        return self.__avr_3day
    @avr_3day.setter
    def avr_3day(self):
        pass

    @property
    def avr_5day(self):
        return self.__avr_5day
    @avr_5day.setter
    def avr_5day(self):
        pass

    @property
    def avr_7day(self):
        return self.__avr_7day
    @avr_7day.setter
    def avr_7day(self):
        pass

    @property
    def avr_10day(self):
        return self.__avr_10day
    @avr_10day.setter
    def avr_10day(self):
        pass

    @property
    def day2limit_count(self):
        return self.__day2limit_count
    @day2limit_count.setter
    def day2limit_count(self):
        pass

    @property
    def maxlimit_count(self):
        return self.__maxlimit_count
    @maxlimit_count.setter
    def maxlimit_count(self):
        pass

    @property
    def score(self):
        return self.__score
    @score.setter
    def score(self,value):
        self.__score=value

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
    #判断第一天状态
    def __day1(self):
        #机构买入后当天上涨
        if self.__stockPriceDay1.close>self.__stockPriceDay1.open:
            return True
        else:
            return False


    #处理第二天的分数
    def __day2(self):

        #第二天开盘涨停
        if gl.isLimit(self.__stockcode,self.__stockPriceDay1.close,self.__stockPriceDay2.open):
            #第二天最低价=最高价（一字涨停）
            if self.__stockPriceDay2.high==self.__stockPriceDay2.low:
                self.__score+=4            #加4分
            #最低价<最高价（高开低走）
            elif self.__stockPriceDay2.low<self.__stockPriceDay2.high:
                #加（收盘价-最低价）幅度*10
                self.__score=self.__score+gl.Range(self.__stockPriceDay1.close,self.__stockPriceDay2.low,self.__stockPriceDay2.close)*10*2
            #理论上不存在第三种可能
            else:
                print("参数输入错误")
                return
        #第二天开盘未涨停
        else:
            #收盘>开盘
            if self.__stockPriceDay2.close>self.__stockPriceDay2.open:
                #(最高价-最低价)幅度<0.02，加4分
                if gl.Range(self.__stockPriceDay1.close,self.__stockPriceDay2.low,self.__stockPriceDay2.high)<=0.02:
                    self.__score+=4
                # (最高价-最低价)幅度>0.02，加2分
                else:
                    self.__score+=2
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


    #第3-5天使用同一个函数
    def __day3to5(self,lastDay,today):
        #输入参数都为StockPrice类
        if isinstance(lastDay,StockPrice) and isinstance(today,StockPrice):
            # 开盘涨停，加3分
            if gl.isLimit(self.__stockcode,lastDay.close,today.open):
                self.__score+=3
            # 开盘未涨停，但涨幅大于5%，加2分
            elif gl.Range(lastDay.close,lastDay.close,today.open)>0.05:
                self.__score+=2
                # 开盘>5%,最高价涨停，附加1分
                if gl.isLimit(self.__stockcode,today.open,today.high):
                    self.__score+=1
                # 收盘<开盘，附减（开盘-收盘）幅度*10
                if today.close<=today.open:
                    self.__score=self.__score+gl.Range(lastDay.close,today.open,today.close)*10
            # 开盘未涨停，但涨幅大于0%,加1分，再附加（收盘-开盘）幅度*10
            elif gl.Range(lastDay.close,lastDay.close,today.open)>=0:
                self.__score+=1
                self.__score=self.__score+gl.Range(lastDay.close,today.open,today.close)*10
            #开盘涨幅<0%
            else:
                # 收盘>开盘,加（收盘-开盘）幅度*10
                if today.close>today.open:
                    self.__score=self.__score+gl.Range(lastDay.close,today.open,today.close)*10
                # 收盘<开盘，加（收盘-开盘）幅度*20
                else:
                    self.__score=self.__score+gl.Range(lastDay.close,today.open,today.close)*10*2

    #处理第三天的分数
    def __day3(self):
        self.__day3to5(self.__stockPriceDay2,self.__stockPriceDay3)

    #处理第四天的分数
    def __day4(self):
        self.__day3to5(self.__stockPriceDay3,self.__stockPriceDay4)

    #处理第五天的分数
    def __day5(self):
        self.__day3to5(self.__stockPriceDay4,self.__stockPriceDay5)



    #算总分
    def calcScore(self):
        if self.__day1():
            self.__day2()
            self.__day3()
            self.__day4()
            self.__day5()
        return self.score


