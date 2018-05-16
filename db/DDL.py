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


if __name__ == '__main__':
    # sql = '''CREATE TABLE if not exists stock(
	# symbol text NOT NULL,
	# name text NOT NULL,
	# PRIMARY KEY (symbol));'''
    sql = '''create table if not exists stock_market(
	stat_date NUMERIC not null,
	symbol text not null,
	code text not null,
	close_price REAL,
	last_close_price REAL,
	percentage REAL,
	change REAL,
	open_price REAL,
	high REAL,
	low REAL,
	high52week REAL,
	low52week REAL,
	marketCapital REAL,
	eps REAL,
	pe_ttm REAL,
	pe_lyr REAL,
	rise_stop REAL,
	fall_stop REAL,
	amount REAL,
	lot_volume REAL,
	float_market_capital REAL,
	primary key (stat_date,symbol)
)'''
    c = DDL()
    c.ddl('stock.db',sql)