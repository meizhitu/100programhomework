__author__ = 'rui'
#coding=utf-8

import pygtk

pygtk.require("2.0")
import gtk


def checkPalindrome(s):
    print(s.decode('utf-8')[::-1])
    print(s)
    return str(s) == str(s).decode('utf-8')[::-1]


def doGo(widget):
    text_buffer = tvInput.get_buffer()
    result = text_buffer.get_text(text_buffer.get_start_iter(), text_buffer.get_end_iter())
    lbResult.set_text(str(checkPalindrome(result)))
    return


handlers = {
    "onDeleteWindow": gtk.main_quit,
    "on_buttonDo_clicked": doGo
}
if __name__ == "__main__":
    gladeFile = "res/demo.glade"
    builder = gtk.Builder()
    builder.add_from_file(gladeFile)
    mainWindow = builder.get_object('demoWindow')
    tvInput = builder.get_object('tvInput')
    tvInput.get_buffer().set_text(u"莺啼岸柳弄春晴 柳弄春晴夜月明 明月夜晴春弄柳 晴春弄柳岸啼莺")
    lbResult = builder.get_object('lbResult')
    builder.connect_signals(handlers)
    if mainWindow:
        mainWindow.connect('destroy', gtk.main_quit)
        mainWindow.set_title("判断回文字符串")
        mainWindow.show_all()
    gtk.main()