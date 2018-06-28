#-*- coding:utf-8 _*-  
""" 
@version: 
@author:yang 
@time: 2018/05/16 
@file: tools.py 
@Project : stock
@Software: PyCharm
@function: 
@modify: 
"""

class tools(object):
    def __init__(self):
        pass

    def strcat(self, str_init, str_add):
        if str_init == '':
            __str = "\"" + str_add + "\""
        else:
            __str = str_init + "," + "\"" + str_add + "\""
        return __str