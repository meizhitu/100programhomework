#coding=utf-8
import re


def getZipCity(code):
    pattern = re.compile(code)
    for i, line in enumerate(open('zipcode.csv')):
        for match in re.finditer(pattern, line):
            return line


def getZipCode(city):
    pattern = re.compile(city)
    for i, line in enumerate(open('zipcode.csv')):
        for match in re.finditer(pattern, line):
            return line


if __name__ == '__main__':
    print(getZipCity("110105"))
    print(getZipCode("武汉"))
