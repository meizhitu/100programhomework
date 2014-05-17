__author__ = 'rui'
#coding=utf-8
import string

import random

N = 16


def genKey():
    #TODO:写一个真正的实际的序列号生成器
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))


if __name__ == '__main__':
    print(genKey())
