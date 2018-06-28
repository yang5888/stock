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
from web.app.main import overview, rise_stop
import json

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    cal = overview.overview()
    table1 = json.loads(cal.table1())
    chart1 = cal.chart1()
    chart1_key,chart1_value1,chart1_value2,chart1_value3,chart1_value4 = [], [], [], [], []
    for i in list(range(len(json.loads(chart1)))):
        chart1_key.append(json.loads(chart1)[i]['stat_date'])
        chart1_value1.append(json.loads(chart1)[i]['rise_stop'])
        chart1_value2.append(json.loads(chart1)[i]['fall_stop'])
        chart1_value3.append(json.loads(chart1)[i]['rise'])
        chart1_value4.append(json.loads(chart1)[i]['fall'])
    return render_template('overview.html', table1=table1, chart1_key=chart1_key, chart1_value1=chart1_value1, chart1_value2 = chart1_value2, chart1_value3 = chart1_value3, chart1_value4 = chart1_value4)

@app.route('/overview')
def overview_page():
    return index()

@app.route('/rise_stop')
def rise_stop_page():
    cal = rise_stop.rise_stop()
    table1 = json.loads(cal.table1())
    table2 = json.loads(cal.table2())
    return render_template('rise_stop.html', table1=table1, table2=table2)

@app.route('/test')
def test():
    cal = rise_stop.rise_stop()
    data = cal.table1()
    return data


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

