# -*- coding: utf-8 -*-
# 2017/10/20 
"""
-------------------------------------------------------------------------------
Function:   
Version:    1.0
Author:     Louis Song
Contact:    slysly759@gmail.com 

code is far away from bugs with the god animal protecting
               ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
-------------------------------------------------------------------------------
"""
import pymysql
con=pymysql.connections.Connection(host='localhost', port=3308, user='root', password='root',charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cur=con.cursor()
sql=''.join(open('db-start.sql',encoding='utf8').readlines())
print(sql)
cur.execute(sql)
con.commit()

