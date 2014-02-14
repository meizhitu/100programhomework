__author__ = 'rui'
#coding=utf-8

import pygtk

pygtk.require("2.0")
import gtk
import urllib2
from BeautifulSoup import BeautifulSoup
import re
import urllib, math
from datetime import datetime


class NewsTickerWindow:
    def __init__(self, title=""):
        self.gladeFile = "res/newsticker.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(self.gladeFile)
        self.mainWindow = self.builder.get_object('demoWindow')
        self.lbnews = self.builder.get_object('labelNews')
        self.lbgame = self.builder.get_object('labelGame')
        self.builder.connect_signals(self)
        self.count = 0
        if self.mainWindow:
            self.mainWindow.connect('destroy', gtk.main_quit)
            self.mainWindow.set_title(title)
            self.mainWindow.show_all()
        gtk.timeout_add(20000, self.delayrun)
        self.delayrun()

    def delayrun(self):
        self.count += 1
        #self.lbgame.set_text(str(self.count))
        content = urllib2.urlopen("http://roll.news.sina.com.cn/").read()
        soup = BeautifulSoup(content)
        self.lbnews.set_label(soup.li.span.a.string)
        self.lbnews.set_uri(soup.li.span.a['href'])
        #content = urllib2.urlopen("http://bdcjhq.hexun.com/quote?s2=000001.sh").read()
        #soup = BeautifulSoup(content)
        #print(content)
        #m = re.search('pc:"([^"]+)"', content)
        #self.lbgame.set_text(m.groups()[0])
        #print(m.groups()[0])
        t = datetime.now()
        h = t.hour
        m = t.minute
        s = math.floor(t.second / 10) * 10
        arg = "%02d%02d%02d" % (h, m, s)
        params = urllib.urlencode({"stocklist": "000001_1|399001_2", "time": arg})
        f = urllib2.urlopen("http://quote.tool.hexun.com/hqzx/getstock.aspx?%s" % params)
        content = f.read()
        m = re.search("(\['[^\]]+\])", content)
        print(m.groups()[0])
        arr = eval(m.groups()[0])
        print(arr[3])
        self.lbgame.set_text("上证指数：" + str(arr[3]))
        return True


if __name__ == '__main__':
    w = NewsTickerWindow(title="滚动新闻")
    gtk.main()