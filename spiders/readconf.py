#-*- coding:utf-8 _*-  
""" 
@version: 
@author:yang 
@time: 2018/05/15 
@file: readconf.py 
@Project : stock
@Software: PyCharm
@function: 
@modify: 
"""

import configparser

class ReadConf(object):
    def __init__(self,conf):
        self.__conf = conf
        cf = configparser.ConfigParser()
        cf.read(self.__conf)
        self.__agent = cf.get("spiders", "User-Agent")
        self.__cookie = cf.get("spiders", "Cookie")

    def getCookie(self):
        return self.__cookie

    def getUserAgent(self):
        return self.__agent

if __name__ == '__main__':
    r = ReadConf('../etc/stock.conf')
    r.getUserAgent()