__author__ = 'rui'
#coding=utf-8

#计算个人所得税及年终奖
#学习一下gtk
import sys
import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade

class TaxGtk:
    def __init__(self):
        self.gladefile="res/tax.glade"
        #self.wTree = gtk.glade.XML(self.gladefile)
        self.glade = gtk.Builder()
        self.glade.add_from_file(self.gladefile)
        dic = {"onCalcClicked":self.onCalcClicked,
               "onMainDestroy":gtk.main_quit}
        self.glade.connect_signals(self)
        self.glade.get_object("taxWindow").show_all()
        #self.glade.signal_autoconnect(dic)
    def onCalcClicked(self, *args):
        print("click")
    def onMainDestroy(self,*args):
        gtk.main_quit()
        print("close")

if __name__ == "__main__":
    tax = TaxGtk()
    gtk.main()