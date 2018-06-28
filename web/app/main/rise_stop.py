#-*- coding:utf-8 _*-  
""" 
@version: 
@author:yang 
@time: 2018/06/08 
@file: rise_stop.py 
@Project : stock
@Software: PyCharm
@function: 
@modify: 
"""

from db import DML
import json
import time

class rise_stop(object):
    def __init__(self):
        sel = DML.DML()
        self.last_stat_date = json.loads(sel.SelectData('../../db/stock.db','select stat_date from stock_market order by stat_date desc limit 1'))[0]['stat_date']

    def table1(self):
        # stat_date = time.strftime("%Y-%m-%d", time.localtime())
        stat_date = self.last_stat_date
        sql = "select a.symbol,name,a.percentage,risestopnum,round((a.high-a.low)/a.last_close_price*100,2) amplitude,round(marketCapital/100000000,2) marketCapital,round(float_market_capital/100000000,2) float_market_capital from stock_market a join stock b on a.symbol=b.symbol left join rise_stop_analysis c on a.symbol=c.symbol and a.stat_date=c.stat_date where rise_stop not in ('999999.99','99999.999','','0.0') and close_price=rise_stop and rise_stop<>fall_stop and a.stat_date='" + stat_date + "' order by risestopnum desc,a.percentage desc"
        sel = DML.DML()
        d = sel.SelectData('../../db/stock.db', sql)
        return d

    def table2(self):
        # stat_date = time.strftime("%Y-%m-%d", time.localtime())
        stat_date = self.last_stat_date
        sql = "select risestopnum,count(*) cnt from rise_stop_analysis where stat_date='" + stat_date + "' group by risestopnum order by cnt desc"
        sel = DML.DML()
        d = sel.SelectData('../../db/stock.db', sql)
        return d
