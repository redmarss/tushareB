#!/usr/bin/env python
#-*-coding:utf8-*-
#数据库操作类

import pymysql

class SingletonModel:
    #数据库连接对象
    __db = None
    #游标对象
    __cursor = None

    def __new__(self, *args, **kwargs):
        if not hasattr(self,'_instance'):
            self._instance = super().__new__(self)
            host = 'host' in kwargs and kwargs['host'] or 'localhost'
            port ='port' in kwargs and kwargs['port'] or '3306'
            user ='user' in kwargs and kwargs['user'] or 'root'
            passwd ='passwd' in kwargs and kwargs['passwd'] or '123456'
            db = 'db' in kwargs and kwargs['db'] or 'test'
            charset = 'charset' in kwargs and kwargs['charset'] or 'utf8'

            #打开数据库连接
            print('连接数据库')
            self.__db = pymysql.connect(host=host,port=int(port),user=user,passwd=passwd,db=db,charset=charset)

            #创建一个游标对象
            self.__cursor = self.__db.cursor(cursor=pymysql.cursors.DictCursor)
        return self._instance

    #返回执行execute()方法后影响的行数
    def execute(self,sql):
        self.__cursor.execute(sql)
        rowcount = self.__cursor.rowcount
        return rowcount

    #增->返回新增ID
    def insert(self,**kwargs):
        table=kwargs['table']       #取出参数中table名称
        kwargs.pop('table')         #将参数中table删除，方便后续操作
        sql = 'insert into %s set '%table
        for k,v in kwargs.items():
            sql += "'%s'='%s',"
        sql=sql.rstrip(',')
        print(sql)
        try:
            #执行SQL语句
            self.__cursor.execute(sql)
            self.__db.commit()
            res = self.__cursor.lastrowid   #获取最后一行自增id
        except:
            #发生错误时回滚
            self.__db.rollback()
        return res

    #删->返回影响的行数
    def delete(self,**kwargs):
        table = kwargs['table']
        where = kwargs['where']
        sql = 'delete from %s where %s'%(table,where)
        print(sql)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            rowcount = self.__cursor.rowcount   #返回影响的行数
        except:
            #发生错误时回滚
            self.__db.rollback()
        return rowcount

    #改->返回影响的行数
    def update(self,**kwargs):
        #表名称
        table = kwargs['table']
        kwargs.pop('table')

        #where条件
        where = kwargs['where']
        kwargs.pop('where')

        sql = 'update %s set '%table
        for k,v in kwargs.items():
            sql += "'%s'='%s',"%(k,v)
        sql = sql.rstrip(',')
        sql += ' where %s'%where
        print(sql)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            rowcount = self.__cursor.rowcount
        except:
            self.__db.rollback()
        return rowcount

    #查->单条数据
    def fetchone(self,**kwargs):
        table = kwargs['table']
        #字段
        field = 'field' in kwargs and kwargs['field'] or '*'

        #where条件
        where = 'where' in kwargs and 'where '+kwargs['where'] or ''

        #order条件
        order = 'order' in kwargs and 'order by '+kwargs['order'] or ''

        sql = 'select %s from %s %s %s limit 1'%(field,table,where,order)
        print(sql)

        try:
            self.__cursor.execute(sql)
            data=self.__cursor.fetchone()
        except:
            self.__db.rollback()
        return data

    #查->多条数据
    def fetchall(self,**kwargs):
        table = kwargs['table']
        #字段
        field = 'field' in kwargs and kwargs['field'] or '*'
        #where条件
        where = 'where' in kwargs and 'where '+kwargs['where'] or ''
        #order
        order = 'order' in kwargs and 'order by '+kwargs['order'] or ''
        #limit
        limit = 'limit' in kwargs and 'limit '+kwargs['limit'] or ''

        sql = 'select %s from %s %s %s %s'%(field,table,where,order,limit)
        print(sql)

        try:
            self.__cursor.execute(sql)
            data = self.__cursor.fetchall()
        except:
            self.__db.rollback()
        return data

    def __del__(self):
        #关闭数据库连接
        self.__db.close()
        print('关闭数据库连接')

