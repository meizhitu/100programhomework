__author__ = 'rui'
#coding=utf-8
from pylab import *
import urllib
import re
import json
mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

def get_stock_hexun(stock_num):
    url = 'http://bdcjhq.hexun.com/quote?s2=%s'%(stock_num)
    values = urllib.urlopen(url).read()
    # 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
    match = re.search(u'\{".+\}\}',values)
    jsonData = {}
    if match:
        # 使用Match获得分组信息
        data =  match.group()
        print(data)
        print(json.loads(str(data),'GBK'))
        jsonData = json.loads(str(data),'GBK')["002041.sz"]
    return jsonData

def get_stock_info(stock_num):
    flag = 'l1c1va2xj1b4j4dyekjm3m4rr5p5p6s7n'
    url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (stock_num, flag)
    values = urllib.urlopen(url).read().strip().split(',')
    print(values)
    data = {}
    data['price'] = values[0]
    data['change'] = values[1]
    data['volume'] = values[2]
    data['avg_daily_volume'] = values[3]
    data['stock_exchange'] = values[4]
    data['market_cap'] = values[5]
    data['book_value'] = values[6]
    data['ebitda'] = values[7]
    data['dividend_per_share'] = values[8]
    data['dividend_yield'] = values[9]
    data['earnings_per_share'] = values[10]
    data['52_week_high'] = values[11]
    data['52_week_low'] = values[12]
    data['50day_moving_avg'] = values[13]
    data['200day_moving_avg'] = values[14]
    data['price_earnings_ratio'] = values[15]
    data['price_earnings_growth_ratio'] = values[16]
    data['price_sales_ratio'] = values[17]
    data['price_book_ratio'] = values[18]
    data['short_ratio'] = values[19]
    data['name'] = values[20]
    return data

def quote_track(stock_num):
    from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY
    from matplotlib.finance import quotes_historical_yahoo, candlestick,plot_day_summary
    from matplotlib.font_manager import FontProperties

    font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=18)
    # 定义起始、终止日期和股票代码
    date2 = datetime.date.today()
    date1 = date2 - datetime.timedelta(days=30)
    # 定义日期格式
    mondays = WeekdayLocator(MONDAY)
    alldays = DayLocator()
    weekFormatter = DateFormatter('%b %d')
    # 获取股票数据
    quotes = quotes_historical_yahoo(stock_num, date1, date2)
    if len(quotes) == 0:
        raise SystemExit
    print(quotes)
    # 绘制蜡烛线或美国线
    fig = figure()
    fig.subplots_adjust(bottom=0.2)
    ax = fig.add_subplot(111)
    ax.xaxis.set_major_locator(mondays)
    ax.xaxis.set_minor_locator(alldays)
    ax.xaxis.set_major_formatter(weekFormatter)
    #注释掉下面的其中一行，可以得到蜡烛线或美国线
    candlestick(ax, quotes, width=0.6)
    #plot_day_summary(ax, quotes, ticksize=3)
    ax.xaxis_date()
    ax.autoscale_view()
    setp(gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    stockdata = get_stock_hexun(stock_num)
    title(u'%s %s 昨收盘：%s 今开盘：%s 当前价：%s'%(stock_num,stockdata['na'],stockdata['pc'],stockdata['op'],stockdata['la']), fontproperties=font)
    show()


if __name__ == "__main__":
    #get_stock_hexun("002041.sz")
    quote_track("002041.sz")
