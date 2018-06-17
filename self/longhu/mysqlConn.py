#!/usr/bin/env python
# -*- conding：utf8 -*-
import pymysql
import pandas as pd
from sqlalchemy import create_engine

# 数据库连接参数
config = {
    'host': "127.0.0.1",
    'database': "longhu",
    'user': "root",
    'password': "123456",
    'port': 3306,
    'charset': 'utf8',
}
dbconn = pymysql.connect(**config)

# 根据sql语句查询所有数据，返回类型为元组
def selectSqlAll(sql):
    try:
        with dbconn.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            print(config['user'])
        return result
        dbconn.commit()
    except:
        print("sql语句有误，请重新输入")
    finally:
        dbconn.close()

# 增删改均可用此函数，先确保sql语句正确(要设定mysql:SET SQL_SAFE_UPDATES = 0)
def OperateSql(sql):
    try:
        with dbconn.cursor() as cursor:
            cursor.execute(sql)
            print("操作成功")
        return True
    except:
        print("操作失败，请重试")
        return False
    finally:
        dbconn.close()

#将一个DataFrame存入mysql的table表中
def DataframeToSql(df,table):
    strEngine="mysql+pymysql://"+config['user']+':'+config['password']+'@'+config['host']+':'+str(config['port'])+'/'+config['database']+'?charset='+config['charset']

    engine = create_engine(strEngine)
    try:
        pd.io.sql.to_sql(df, table, engine, if_exists='append')
        print("成功")
    except:
        print("重复")