#!/usr/bin/env python
# -*- coding:utf8 -*-

#stock类
class StockPrice(object):
    def __init__(self,tuple):
        self.tuple=tuple

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
    def average(self):
        return self.tuple[5]
    @property
    def volumne(self):
        return self.tuple[6]

#score类
class Score(object):
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