#-*- coding:utf-8 _*-
"""
@version:
@author:yang
@time: 2018/05/15
@file: get_stock_info.py
@Project : stock
@Software: PyCharm
@function:
@modify:
"""

import json
from db import DML
from spiders import readconf
from spiders import spider
import time
from spiders import tools

class GetStockInfo(object):
    def __init__(self):
        r = readconf.ReadConf('../etc/stock.conf')
        self.__agent = r.getUserAgent()
        self.__cookie = r.getCookie()

    def run(self):
        stat_date = time.strftime("%Y-%m-%d", time.localtime())
        getstocklist = spider.Spider()
        sql = 'select symbol from stock'
        query = DML.DML()
        str = query.SelectData('../db/stock.db',sql)
        for symbol_index in list(range(len(json.loads(str)))):
            symbol = json.loads(str)[symbol_index]['symbol']
            url = "https://xueqiu.com/v4/stock/quote.json?code=" + symbol
            header = {'User-Agent': self.__agent, 'Cookie': self.__cookie}
            tool = tools.tools()
            record = "\"" + stat_date + "\""
            columns = ["symbol","code","close","last_close","percentage","change","open","high","low","high52week","low52week","marketCapital","eps","pe_ttm","pe_lyr","rise_stop","fall_stop","amount","lot_volume","float_market_capital"]
            context = json.loads(getstocklist.spider(url, header))[symbol]
            for column in columns:
                record = tool.strcat(record, context[column])
            replace_data = DML.DML()
            print(record)
            replace_data.ReplacetData('../db/stock.db','stock_market',record)


if __name__ == "__main__":
    r = GetStockInfo()
    r.run()
