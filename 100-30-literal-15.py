__author__ = 'rui'
#coding=utf-8


def textToHtml(txt):
    txt = str(txt).replace("&", "&amp;")
    txt = str(txt).replace("<", "&lt;")
    txt = str(txt).replace(">", "&gt;")
    txt = str(txt).replace("\r\n", "<br>")
    txt = str(txt).replace("\r", "<br>")
    txt = str(txt).replace("\n", "<br>")
    return txt


if __name__ == '__main__':
    print(textToHtml("只是&\r\n<>天地玄黄"))
