#-*- coding:utf-8 _*-  
""" 
@version: 
@author:yang 
@time: 2018/05/14 
@file: run.py 
@Project : stock
@Software: PyCharm
@function: 
@modify: 
"""

from spiders.get_stock_list import GetStockList
from spiders.get_stock_info import GetStockInfo

def run():
    stock_list = GetStockList()
    stock_list.run()
    stock_info = GetStockInfo()
    stock_info.run()

if __name__ == "__main__":
    run()