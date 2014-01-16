__author__ = 'rui'
#coding=utf-8

import sys
import codecs
import re
import pygtk
from collections import Counter

pygtk.require("2.0")
import gtk
import gtk.glade

maxWordLen = 2


def countWord(s):
    dict = {}
    s = str(s)
    words = s.split()
    for w in words:
        if w in dict:
            dict[w] += 1
        else:
            dict[w] = 1
    return prettyPrint(dict, True)


def splitWord(w, allwords):
    for i in range(len(w)):
        if (i + maxWordLen) <= len(w):
            if w[i:i + maxWordLen] in allwords:
                allwords[w[i:i + maxWordLen]] += 1
            else:
                allwords[w[i:i + maxWordLen]] = 1
    return allwords


def countFile():
    from time import clock

    start = clock()
    words = []
    allwords = {}
    with codecs.open("res/songci.txt", 'r', 'utf-8') as f:
        for line in f:
            if len(line) > 10 and len(line) < 500:
                word = re.split(u'[,!?.，！？。]', line)
                words.extend(word)
    words = filter(lambda x: len(x) > 0, words)
    #prettyPrintArray(words)
    for wd in words:
        splitWord(wd, allwords)
    maxCount = 30
    result = ""
    for key, valve in sorted(allwords.iteritems(), key=lambda e: e[1], reverse=True):
        if (maxCount > 0):
            maxCount -= 1
            result += key + ":" + str(valve) + "\n"
    print(result)
    return result


def prettyPrintArray(arr):
    for k in arr:
        print(k)


def prettyPrint(wcDict, sort=False):
    result = ""
    if (sort):
        for key, valve in sorted(wcDict.iteritems(), key=lambda e: e[1], reverse=True):
            result += key + ":" + str(valve) + "\n"
    else:
        for k, v in wcDict.items():
            result += k + ":" + str(v) + "\n"
    return result


def doGo(widget):
    text_buffer = tvInput.get_buffer()
    result = text_buffer.get_text(text_buffer.get_start_iter(), text_buffer.get_end_iter())
    if (len(result) > 0):
        lbResult.set_text(str(countWord(result)))
    else:
        lbResult.set_text(str(countFile()))
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
    #tvInput.get_buffer().set_text(u"Count Words in a String – Counts the number of individual words in a string. For added complexity read these strings in from a text file and generate a summary.")
    lbResult = builder.get_object('lbResult')
    builder.connect_signals(handlers)
    if mainWindow:
        mainWindow.connect('destroy', gtk.main_quit)
        mainWindow.set_title("单词出现次数")
        mainWindow.show_all()
    gtk.main()