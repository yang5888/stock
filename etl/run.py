#-*- coding:utf-8 _*-  
""" 
@version: 
@author:yang 
@time: 2018/06/12 
@file: run.py 
@Project : stock
@Software: PyCharm
@function: 
@modify: 
"""

import os, sys
sys.path.append(os.path.abspath(os.path.pardir))

from etl.continuousRiseStop import ContinuousRiseStop


def run():
    rise_stop_analysis = ContinuousRiseStop()
    rise_stop_analysis.run()

if __name__ == "__main__":
    run()