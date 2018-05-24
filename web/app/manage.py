#-*- coding:utf-8 _*-  
""" 
@version: 
@author:yang 
@time: 2018/05/21 
@file: manage.py
@Project : stock
@Software: PyCharm
@function: 
@modify: 
"""

from flask_bootstrap import Bootstrap
from flask import Flask, render_template
from web.app.main import overview
import json

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    cal = overview.overview()
    table1 = cal.table1()
    chart1 = cal.chart1()
    print(len(list(chart1)))
    print(json.loads(str(chart1))[0]['stat_date'])
    return render_template('overview.html', table1=table1)

@app.route('/overview')
def overview_page():
    return index()

@app.route('/detail')
def detail():
    return render_template('detail.html')


if __name__ == '__main__':
    app.run(debug=True)

