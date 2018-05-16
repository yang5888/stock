#-*- coding:utf-8 _*-  
""" 
@version: 
@author:yang 
@time: 2018/05/14 
@file: get_stock_list.py 
@Project : stock
@Software: PyCharm
@function: 
@modify: 
"""

from spiders import readconf
import json
from db import DML
from spiders import spider

class GetStockList:
    def __init__(self):
        r = readconf.ReadConf('../stock.conf')
        self.__agent = r.getUserAgent()
        self.__cookie = r.getCookie()

    def run(self):
        getstocklist = spider.Spider()
        page = '1'
        size = '100'
        url = 'https://xueqiu.com/stock/cata/stocklist.json?page=' + page + '&size=' + size + '&order=desc&orderby=percent&type=11%2C12&_=1525762043577'
        header = {'User-Agent': self.__agent, 'Cookie': self.__cookie}
        total = json.loads(getstocklist.spider(url, header))['count']['count']
        for page in list(range(1, int(total / int(size)) + 2)):
            url = 'https://xueqiu.com/stock/cata/stocklist.json?page=' + str(
                page) + '&size=' + size + '&order=desc&orderby=percent&type=11%2C12&_=1525762043577'
            data = json.loads(getstocklist.spider(url, header))
            for sub_index in list(range(len(data['stocks']))):
                record = "\"" + data['stocks'][sub_index]['symbol'] + "\"" + "," + "\"" + data['stocks'][sub_index]['name'] + "\""
                replace_data = DML.DML()
                replace_data.ReplacetData('../db/stock.db','stock',record)


if __name__ == "__main__":
    r = GetStockList()
    r.run()
