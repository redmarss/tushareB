#!/bin/usr/env python
# -*-coding:utf8-*-

import uuid
import self.myGlobal.mysqlCls as mysqlCls

def create_code(num,length):
    result=[]
    for i in range(num):
        uuid_id = uuid.uuid1()
        temp = str(uuid_id).replace('-','')[:length]
        if not temp in result:
            result.append(temp)
    return result

if __name__ == "__main__":
    r = create_code(200,20)

    dbObject = mysqlCls.SingletonModel(host="localhost", port=3306, user="root", passwd="redmarss", db="test", charset="utf8")
    # sql="""CREATE TABLE code(
    # id int(11) NOT NULL AUTO_INCREMENT,
    # code varchar(30) NOT NULL,
    # PRIMARY KEY (id)
    # ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='优惠券';
    # """
    # res = dbObject.execute(sql)
    for i in range(len(r)):
        dbObject.insert(table="code",code=r[i])