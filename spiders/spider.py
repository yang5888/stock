#-*- coding:utf-8 _*-  
""" 
@version: 
@author:yang 
@time: 2018/05/15 
@file: spider.py 
@Project : stock
@Software: PyCharm
@function: 
@modify: 
"""

import urllib
from urllib import error
from urllib import request

class Spider(object):
    def __init__(self):
        pass

    def spider(self, url, header):
        try:
            req = request.Request(url, headers=header)
            res = request.urlopen(req).read()
            return res
        except error.HTTPError as e:
            print(e.code)
        except error.URLError as e:
            print(str(e))