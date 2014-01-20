__author__ = 'rui'
#coding=utf-8
import pygtk

pygtk.require("2.0")
import gtk

class PostItWindow:
    def __init__(self):
        self.gladeFile = "res/postit.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(self.gladeFile)
        self.mainWindow = self.builder.get_object('postItWindow')
        self.tvInput = self.builder.get_object('tvInput')
        self.builder.connect_signals(self)
        if self.mainWindow:
            self.mainWindow.connect('destroy', gtk.main_quit)
            self.mainWindow.set_title("即时贴")
            self.mainWindow.show_all()

    def on_buttonDo_clicked(self, *args):
        pass


if __name__ == "__main__":
    w = PostItWindow()
    gtk.main()