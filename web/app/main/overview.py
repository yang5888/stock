#-*- coding:utf-8 _*-  
""" 
@version: 
@author:yang 
@time: 2018/05/23 
@file: overview.py
@Project : stock
@Software: PyCharm
@function: 
@modify: 
"""

from db import DML
import json
import time

class overview(object):
    def __init__(self):
        pass

    def table1(self):
        stat_date = time.strftime("%Y-%m-%d", time.localtime())
        sql = "select count(*) total,count(case when close_price=rise_stop and rise_stop<>fall_stop then code else null end) rise_stop,count(case when close_price=fall_stop and rise_stop<>fall_stop then code else null end) fall_stop,count(case when percentage>0 then code else null end) rise,count(case when percentage<0 then code else null end) fall,count(case when percentage=0 then code else null end) keep,count(case when percentage>7 then code else null end) rise_sev,count(case when percentage>5 then code else null end) rise_fiv,count(case when percentage>2 then code else null end) rise_two,count(case when percentage<-7 then code else null end) fall_sev,count(case when percentage<-5 then code else null end) fall_fiv,count(case when percentage<-2 then code else null end) fall_two,count(case when close_price=rise_stop and rise_stop<>fall_stop and high<>low then code else null end) nature_rise_stop,count(case when close_price=fall_stop and rise_stop<>fall_stop and high<>low then code else null end) nature_fall_stop,count(case when close_price<>rise_stop and rise_stop<>fall_stop and high=rise_stop then code else null end) touch_rise_stop from stock_market where rise_stop not in ('999999.99','99999.999','','0.0') and stat_date='" + stat_date + "'"
        sel = DML.DML()
        d = sel.SelectData('../../db/stock.db', sql)
        return json.loads(d)

    def chart1(self):
        sql = "select stat_date,count(case when close_price=rise_stop and rise_stop<>fall_stop then code else null end) rise_stop from stock_market group by stat_date"
        sel = DML.DML()
        d = sel.SelectData('../../db/stock.db', sql)
        return d

