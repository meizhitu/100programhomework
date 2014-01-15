__author__ = 'rui'
#coding=utf-8

import sys
import pygtk

pygtk.require("2.0")
import gtk
import gtk.glade

vowel = ("a", "e", "i", "o", "u")

def countVowels(s):
    countV = {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0}
    for c in s:
        if c.lower() in vowel:
            countV[c.lower()] += 1
    return countV

def doGo(widget):
    text_buffer = tvInput.get_buffer()
    result = text_buffer.get_text(text_buffer.get_start_iter(), text_buffer.get_end_iter())
    lbResult.set_text(str(countVowels(result)))
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
    tvInput.get_buffer().set_text(" Count Vowels – Enter a string and the program counts the number of vowels in the text. For added complexity have it report a sum of each vowel found.")
    lbResult = builder.get_object('lbResult')
    builder.connect_signals(handlers)
    if mainWindow:
        mainWindow.connect('destroy', gtk.main_quit)
        mainWindow.set_title("元音字母计数")
        mainWindow.show_all()
    gtk.main()