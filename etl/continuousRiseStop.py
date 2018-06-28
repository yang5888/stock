#-*- coding:utf-8 _*-  
""" 
@version: 
@author:yang 
@time: 2018/06/11 
@file: continuousRiseStop.py 
@Project : stock
@Software: PyCharm
@function: 
@modify: 
"""

from db import DML
import time
import json

class ContinuousRiseStop:
    def __init__(self):
        pass

    def run(self):
        stat_date = time.strftime("%Y-%m-%d", time.localtime())
        print(stat_date)
        sel = DML.DML()
        data = sel.SelectData('../db/stock.db', "select symbol from stock_market where rise_stop not in ('999999.99','99999.999','','0.0') and close_price=rise_stop and rise_stop<>fall_stop and stat_date='" + stat_date + "'")
        last_stat_date = json.loads(sel.SelectData('../db/stock.db','select stat_date from stock_market where stat_date<"' + stat_date + '" order by stat_date desc limit 1'))[0]['stat_date']
        for symbol_index in list(range(len(json.loads(data)))):
            symbol = json.loads(data)[symbol_index]['symbol']
            last_rise_stop_data = json.loads(sel.SelectData('../db/stock.db','select symbol,risestopnum from rise_stop_analysis where symbol="' + symbol + '" and stat_date="' + last_stat_date + '"'))
            if last_rise_stop_data:
                risestopnum = last_rise_stop_data[0]['risestopnum']
                risestopnum = float(risestopnum) + 1
            else:
                risestopnum = 1
            record = "'" + str(symbol) + "','" + str(stat_date) + "','" + str(risestopnum) + "'"
            print(record)
            sel.ReplacetData('../db/stock.db', 'rise_stop_analysis', record)

if __name__ == "__main__":
    s = ContinuousRiseStop()
    s.run()