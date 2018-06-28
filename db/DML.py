#-*- coding:utf-8 _*-  
""" 
@version: 
@author:yang 
@time: 2018/05/14 
@file: DML.py
@Project : stock
@Software: PyCharm
@function:
@modify:
"""

import sqlite3

class DML(object):
    def __init__(self):
        pass

    def InsertData(self,db,tb,data):
        self.__data = data
        self.__db = db
        self.__tb = tb
        conn = sqlite3.connect(self.__db)
        conn.cursor().execute("INSERT INTO "+ self.__tb +" VALUES(" + self.__data + ")")
        conn.commit()
        conn.close()

    def ReplacetData(self,db,tb,data):
        self.__data = data
        self.__db = db
        self.__tb = tb
        conn = sqlite3.connect(self.__db)
        conn.cursor().execute("REPLACE INTO "+ self.__tb +" VALUES(" + self.__data + ")")
        conn.commit()
        conn.close()

    def TruncateData(self,db,tb):
        self.__db = db
        self.__tb = tb
        conn = sqlite3.connect(self.__db)
        conn.cursor().execute("DELETE from "+ self.__tb)
        conn.commit()
        conn.close()


    def SelectData(self,db,sql):
        self.__db = db
        self.__sql = sql
        conn = sqlite3.connect(self.__db)
        col_name_list = [tuple[0] for tuple in conn.cursor().execute(self.__sql).description]
        data = ''
        for row in conn.cursor().execute(self.__sql):
            record = '"' + str(col_name_list[0])  + '"' + ":" + '"' + str(row[0]) + '"'
            for length in list(range(1,len(row))):
                record = record + "," + '"' + str(col_name_list[length])  + '"' + ":" + '"' + str(row[length]) + '"'
            record = "{" + record + "}"
            if data == '':
                data = data + record
            else:
                data = data + "," + record
        data = "[" + data + "]"
        conn.close()
        return data
