__author__ = 'rui'
#coding=utf-8

__author__ = 'rui'
#coding=utf-8

import pygtk

pygtk.require("2.0")
import gtk


class DemoWindow:
    def __init__(self, title="", inputText=u""):
        self.gladeFile = "res/demo.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(self.gladeFile)
        self.mainWindow = self.builder.get_object('demoWindow')
        self.tvInput = self.builder.get_object('tvInput')
        self.tvInput.get_buffer().set_text(inputText)
        self.lbResult = self.builder.get_object('lbResult')
        self.builder.connect_signals(self)
        if self.mainWindow:
            self.mainWindow.connect('destroy', gtk.main_quit)
            self.mainWindow.set_title(title)
            self.mainWindow.show_all()

    def on_buttonDo_clicked(self, *args):
        text_buffer = self.tvInput.get_buffer()
        result = text_buffer.get_text(text_buffer.get_start_iter(), text_buffer.get_end_iter())
        self.lbResult.set_text(str(self.doGo(result)))

    def doGo(self,result):
        return ""


