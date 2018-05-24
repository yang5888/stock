#-*- coding:utf-8 _*-  
""" 
@version: 
@author:yang 
@time: 2018/05/14 
@file: manage.py
@Project : stock
@Software: PyCharm
@function: 
@modify: 
"""

import os, sys
sys.path.append(os.path.abspath(os.path.pardir))

from spiders.get_stock_list import GetStockList
from spiders.get_stock_info import GetStockInfo



def run():
    stock_list = GetStockList()
    stock_list.run()
    stock_info = GetStockInfo()
    stock_info.run()

if __name__ == "__main__":
    run()