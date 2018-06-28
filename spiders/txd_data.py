#-*- coding:utf-8 _*-  
""" 
@version: 
@author:yang 
@time: 2018/06/25 
@file: txd_data.py 
@Project : stock
@Software: PyCharm
@function: 
@modify: 
"""

#!/usr/bin/python

import struct
import os
from db import DML
import time


replace_data = DML.DML()
def exactStock(fileName, code):
    ofile = open(fileName, 'rb')
    buf = ofile.read()
    ofile.close()
    num = len(buf)
    no = num / 32
    b = 0
    e = 32
    items = list()
    writefile = 'D:\\new_tdx\\vipdoc\\sh\\lday\\data.csv'
    ff = open(writefile, 'a')
    for i in range(int(no)):
        a = struct.unpack('IIIIIfII', buf[b:e])
        year = int(a[0] / 10000);
        m = int((a[0] % 10000) / 100);
        month = str(m);
        if m < 10:
            month = "0" + month;
        d = (a[0] % 10000) % 100;
        day = str(d);
        if d < 10:
            day = "0" + str(d);
        dd = str(year) + "-" + month + "-" + day
        openPrice = a[1] / 100.0
        high = a[2] / 100.0
        low = a[3] / 100.0
        close = a[4] / 100.0
        amount = a[5] / 10.0
        vol = a[6]
        unused = a[7]
        if i == 0:
            preClose = close
        ratio = round((close - preClose) / preClose * 100, 2)
        preClose = close
        # item = [code, dd, str(openPrice), str(high), str(low), str(close), str(ratio), str(amount), str(vol)]
        record = "\"" + dd + "\",\"SZ" + code + "\",\"" + code + "\",\"" + str(openPrice) + "\",\"" + str(high) + "\",\"" + str(low) + "\",\"" + str(close) + "\",\"" + str(ratio) + "\",\"" + str(amount) + "\",\"" + str(vol) + "\""
        # replace_data.ReplacetData('../db/stock.db', 'stock_history', record)
        ff.write(record)
        ff.write("\n")
        items.append(record)
        b = b + 32
        e = e + 32

    ff.close()
    return items


pathdir='D:\\new_tdx\\vipdoc\\sz\\lday'
listfile=os.listdir(pathdir)
for f in listfile:
    file = 'D:\\new_tdx\\vipdoc\\sz\\lday\\' + f
    code = f[2:8]
    print(file)
    print(time.asctime(time.localtime(time.time())))
    exactStock(file, code)
