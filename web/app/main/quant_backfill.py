# -*- coding:utf-8 _*-
""" 
@version: 
@author:yang 
@time: 2018/06/26 
@file: quant_backfill.py
@Project : stock
@Software: PyCharm
@function: 
@modify: 
"""

from db import DML
import json
import math
import numpy


class quant(object):
    def __init__(self):
        self.__db = '../../../db/stock.db'
        self.__last_deal_price = ''

    def dealfee(self, trade_type, feerate, amount):
        if trade_type == 'buy':
            if amount * feerate >= 5:
                return math.floor(float(amount * feerate) * 100) / 100
            else:
                return 5
        elif trade_type == 'sell':
            if amount * feerate >= 5:
                return math.floor(float(amount * feerate) * 100) / 100 + math.floor(float(amount * 0.001) * 100) / 100
            else:
                return 5 + math.floor(float(amount * 0.001) * 100) / 100

    def init_grid(self, backfill_start_date, symbol, inital_fund, first_buy_price):
        sel = DML.DML()
        avg_amplitude = json.loads(sel.SelectData(self.__db,
                                                  'select avg((high-low)/open) avg_amplitude from stock_history where symbol=\'' + symbol + '\' and stat_date<\'' + backfill_start_date + '\' group by symbol'))[
            0]['avg_amplitude']
        grid_width = math.floor(float(avg_amplitude) * 100) / 100
        grid_amount = math.floor(float(first_buy_price) * grid_width * 100) / 100
        min = float(first_buy_price) - grid_amount * 10
        max = float(first_buy_price) + grid_amount * 10
        down_grid = numpy.arange(float(first_buy_price), min, -grid_amount)
        up_grid = numpy.arange(float(first_buy_price), max, grid_amount)
        price_grid = numpy.unique(numpy.append(down_grid, up_grid))
        deal_grid = []
        deal_amount = inital_fund / len(price_grid)
        for i in range(len(price_grid)):
            deal_grid.append(int(deal_amount / price_grid[i] / 100) * 100)
        return (deal_grid, price_grid, grid_width)

    def backfill(self, start_date, end_date, symbol, inital_fund):
        self.__start_date = start_date
        self.__end_date = end_date
        self.__symbol = symbol
        self.__inital_fund = inital_fund
        self.__dealfee = [0]
        self.__holdamount = [0]
        self.__holdstock = [0]
        self.__freeamount = [inital_fund]
        self.__grid_flag = 0
        self.__yield_rate = []
        sel = DML.DML()
        deal_day = sel.SelectData(self.__db,
                                  'select distinct stat_date from stock_history where stat_date>=\'' + self.__start_date + '\' and stat_date<=\'' + self.__end_date + '\' and symbol=\'' + self.__symbol + '\'')
        for day in json.loads(deal_day):
            # print(day['stat_date'])
            # print(str(self.__holdstock))
            # print(str(self.__holdamount))
            # print(str(self.__freeamount))
            ma10 = json.loads(sel.SelectData(self.__db,
                                             'select avg(close) ma10 from (select close from stock_history where stat_date<\'' +
                                             day[
                                                 'stat_date'] + '\' and symbol=\'' + self.__symbol + '\' order by stat_date desc limit 10)a'))[
                0]['ma10']
            ma30 = json.loads(sel.SelectData(self.__db,
                                             'select avg(close) ma30 from (select close from stock_history where stat_date<\'' +
                                             day[
                                                 'stat_date'] + '\' and symbol=\'' + self.__symbol + '\' order by stat_date desc limit 30)a'))[
                0]['ma30']
            day_max = json.loads(sel.SelectData(self.__db, 'select high from stock_history where stat_date=\'' + day[
                'stat_date'] + '\' and symbol=\'' + self.__symbol + '\''))[0]['high']
            day_min = json.loads(sel.SelectData(self.__db, 'select low from stock_history where stat_date=\'' + day[
                'stat_date'] + '\' and symbol=\'' + self.__symbol + '\''))[0]['low']
            day_close = json.loads(sel.SelectData(self.__db, 'select close from stock_history where stat_date=\'' + day[
                'stat_date'] + '\' and symbol=\'' + self.__symbol + '\''))[0]['close']
            day_open = json.loads(sel.SelectData(self.__db, 'select open from stock_history where stat_date=\'' + day[
                'stat_date'] + '\' and symbol=\'' + self.__symbol + '\''))[0]['open']
            day_ratio = json.loads(sel.SelectData(self.__db, 'select ratio from stock_history where stat_date=\'' + day[
                'stat_date'] + '\' and symbol=\'' + self.__symbol + '\''))[0]['ratio']
            last_close_price = int(float(day_close) / (1 + float(day_ratio) / 100) * 100) / 100

            if ma10 > ma30:
                if self.__grid_flag == 0:
                    (deal_grid, price_grid, grid_width) = self.init_grid(day['stat_date'], self.__symbol,
                                                                         self.__freeamount[len(self.__freeamount) - 1],
                                                                         float(day_open))
                    self.__grid_flag = 1
                if float(day_max) < last_close_price:
                    day_max = last_close_price
                if float(day_min) > last_close_price:
                    day_min = last_close_price
                for i in range(len(price_grid)):
                    if float(price_grid[i]) > float(day_min) and float(price_grid[i]) < float(day_max):
                        if int(self.__holdstock[len(self.__holdstock) - 1]) == 0:
                            day_first_deal = 0.0
                            stock = 0
                            for j in range(len(price_grid) - i):
                                day_first_deal = day_first_deal + price_grid[j] * deal_grid[j]
                                stock = stock + deal_grid[j]
                            self.__holdstock.append(stock)
                            self.__holdamount.append(stock * float(day_close))
                            self.__dealfee.append(
                                self.__dealfee[len(self.__dealfee) - 1] + self.dealfee('buy', 0.0005, day_first_deal))
                            self.__freeamount.append(self.__freeamount[len(self.__freeamount) - 1] - day_first_deal)
                            hold_level = i
                            break
                        else:
                            if i > hold_level:
                                sell = 0.0
                                fee = 0.0
                                stock = 0
                                for k in range(hold_level, i):
                                    sell = sell + deal_grid[k - 1] * price_grid[k]
                                    stock = stock + deal_grid[k - 1]
                                    fee = fee + self.dealfee('sell', 0.0005, deal_grid[k - 1] * price_grid[k])
                                hold_level = i
                                self.__holdstock.append(self.__holdstock[len(self.__holdstock) - 1] - stock)
                                self.__holdamount.append(
                                    self.__holdstock[len(self.__holdstock) - 1] * float(day_close))
                                self.__dealfee.append(self.__dealfee[len(self.__dealfee) - 1] + fee)
                                self.__freeamount.append(self.__freeamount[len(self.__freeamount) - 1] + sell)
                                break
                            elif i < hold_level:
                                buy = 0.0
                                fee = 0.0
                                stock = 0
                                for k in range(i, hold_level):
                                    buy = buy + price_grid[k] * deal_grid[k]
                                    stock = stock + deal_grid[k]
                                    fee = fee + self.dealfee('buy', 0.0005, price_grid[k] * deal_grid[k])
                                hold_level = i
                                self.__holdstock.append(self.__holdstock[len(self.__holdstock) - 1] + stock)
                                self.__holdamount.append(
                                    self.__holdstock[len(self.__holdstock) - 1] * float(day_close))
                                self.__dealfee.append(self.__dealfee[len(self.__dealfee) - 1] + fee)
                                self.__freeamount.append(self.__freeamount[len(self.__freeamount) - 1] - buy)
                                break
                            else:
                                self.__holdstock.append(self.__holdstock[len(self.__holdstock) - 1])
                                self.__holdamount.append(
                                    self.__holdstock[len(self.__holdstock) - 1] * float(day_close))
                                self.__dealfee.append(self.__dealfee[len(self.__dealfee) - 1])
                                self.__freeamount.append(self.__freeamount[len(self.__freeamount) - 1])
                                break
                    else:
                        if i == len(price_grid) - 1:
                            self.__holdstock.append(self.__holdstock[len(self.__holdstock) - 1])
                            self.__holdamount.append(
                                self.__holdstock[len(self.__holdstock) - 1] * float(day_close))
                            self.__dealfee.append(self.__dealfee[len(self.__dealfee) - 1])
                            self.__freeamount.append(self.__freeamount[len(self.__freeamount) - 1])
            else:
                self.__holdamount.append(0)
                self.__freeamount.append(self.__freeamount[len(self.__freeamount) - 1] + self.__holdstock[
                    len(self.__holdstock) - 1] * float(day_open))
                self.__holdstock.append(0)
                fee = self.dealfee('sell', 0.0005, self.__holdstock[len(self.__holdstock) - 1] * float(day_open))
                self.__dealfee.append(self.__dealfee[len(self.__dealfee) - 1] + fee)
                self.__grid_flag = 0
            print(self.__freeamount[len(self.__freeamount) - 1])
            print(self.__holdamount[len(self.__holdamount) - 1])
            print(self.__dealfee[len(self.__dealfee) - 1])
            print(price_grid)
            print(day_close)
            print(day_open)
            self.__yield_rate.append(str(int((((self.__freeamount[len(self.__freeamount) - 1] + self.__holdamount[
            len(self.__holdamount) - 1] - self.__dealfee[len(
            self.__dealfee) - 1]) / self.__inital_fund - 1) * 100) * 100) / 100) + "%")
        print("股票代码:" + symbol)
        print("回测区间:" + self.__start_date + "~" + self.__end_date)
        # print("网格宽度（%）:" + str(grid_width) + "%")
        # print("价格网格（元）:" + str(price_grid))
        # print("交易网格（股）:" + str(deal_grid))
        print("累计手续费（元）:" + str(self.__dealfee[len(self.__dealfee) - 1]))
        # print("策略收益率（%）:" + str(int((((self.__freeamount[len(self.__freeamount) - 1] + self.__holdamount[
        #     len(self.__holdamount) - 1] - self.__dealfee[len(
        #     self.__dealfee) - 1]) / self.__inital_fund - 1) * 100) * 100) / 100) + "%")
        print("策略收益率（%）:" + str(self.__yield_rate))
        print(str(self.__holdstock))


if __name__ == "__main__":
    q = quant()
    q.backfill('2015-06-16', '2015-06-17', 'SZ002382', 200000.0)
    # q.backfill('2015-06-16', '2018-01-01', 'SZ002382', 200000.0)
    # q.backfill('2018-01-01', '2018-06-29', 'SH600621', 200000.0)
    # q.init_grid('2015-01-01','SH600621',200000, 12.61)
