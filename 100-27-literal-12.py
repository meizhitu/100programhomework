__author__ = 'rui'
#coding=utf-8

import pygtk

pygtk.require("2.0")
import gtk
import urllib2
import re


class FortuneTellerWindow:
    def __init__(self, title=""):
        self.gladeFile = "res/fortuneteller.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(self.gladeFile)
        self.mainWindow = self.builder.get_object('demoWindow')
        self.lbFortune = self.builder.get_object('labelFortune')
        self.buttons = []
        self.horoscope = '白羊座,金牛座,双子座,巨蟹座,狮子座,处女座,天秤座,天蝎座,射手座,摩羯座,水瓶座,双鱼座'.split(',')
        for i in range(1, 13):
            btn = self.builder.get_object('button' + str(i))
            btn.set_label(self.horoscope[i - 1])
            btn.connect('clicked', self.on_buttonDo_clicked, i)
            self.buttons.append(btn)
        self.builder.connect_signals(self)
        self.count = 0
        if self.mainWindow:
            self.mainWindow.connect('destroy', gtk.main_quit)
            self.mainWindow.set_title(title)
            self.mainWindow.show_all()

    def on_buttonDo_clicked(self, *args):
        index = args[1]
        horoscopeUrl = 'http://act1.astro.women.sohu.com/yuncheng_xingzuo_new.php?type=d&xingzuo=' + str(index)
        print horoscopeUrl
        content = urllib2.urlopen(horoscopeUrl).read()
        m = re.search("<td class=wz12_3B07>(.+?</td>)", content, re.DOTALL)
        horoscopeText = str(m.groups()[0]).replace('</td>', '').replace('<br />', '\r\n')
        self.lbFortune.get_buffer().set_text(horoscopeText.decode('gb2312'))


if __name__ == '__main__':
    w = FortuneTellerWindow(title="星座运程")
    gtk.main()