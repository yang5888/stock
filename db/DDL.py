#-*- coding:utf-8 _*-  
""" 
@version: 
@author:yang 
@time: 2018/05/14 
@file: DDL.py 
@Project : stock
@Software: PyCharm
@function: 
@modify: 
"""

import sqlite3

class DDL(object):
    def __init__(self):
        pass

    def ddl(self,db,ddl):
        self.__ddl = ddl
        self.__db = db
        conn = sqlite3.connect(self.__db)
        conn.cursor().execute(self.__ddl)
        conn.close()
