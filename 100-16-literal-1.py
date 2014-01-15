__author__ = 'rui'
#coding=utf-8

def reverseString(s):
    return s[::-1]

def reverseString2(s):
    slen = len(s)
    if slen<=1:
        return s
    return reverseString2(s[1:])+s[0]

if __name__ == "__main__":
    print reverseString("hello world")
    print reverseString2(u"精灵入世，双鹤齐飞。 孤亭独立，单鹤静候。 独凿山石，枝叶单飞。 炭黑如墨，苔似牙月。")