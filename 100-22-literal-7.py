__author__ = 'rui'
#coding=utf-8

import codecs
import re
import pygtk

pygtk.require("2.0")
import gtk
from Demo import DemoWindow

class RssFeedCreator(DemoWindow):

    def doGo(self,result):
        return "not implement"

if __name__ == "__main__":
    crreator = RssFeedCreator("RSS Feed生成","")
    gtk.main()