__author__ = 'rui'
#coding=utf-8
#学习一下yield的用法
factor = [2, 3, 5, 7]


def GetNextPrime():
    yield 2
    yield 3
    yield 5
    yield 7
    nextPrime = 11
    while (True):
        for i in range(2, nextPrime):
            if (i * i > nextPrime):
                nextPrime += 1
                yield nextPrime - 1
                break
            if (i * i <= nextPrime and nextPrime % i == 0):
                nextPrime += 1
                break


if __name__ == "__main__":
    primeIter = GetNextPrime()
    for i in range(300):
        print(primeIter.next())