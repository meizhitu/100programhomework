__author__ = 'rui'
#coding=utf-8
import re


def regexTest(pattern, input):
    #re.IGNORECASE|re.MULTILINE|re.LOCALE|re.UNICODE|re.DOTALL|re.VERBOSE
    regex = re.compile(pattern, re.DOTALL)
    m = regex.search(input)
    if m:
        print("search: ")
        print(m.groups())
    else:
        print('search: not match')
    m = regex.match(input)
    if m:
        print("match: ")
        print(m.groups())
    else:
        print('match: not match')
    m = regex.findall(input)
    if m:
        print("findall: ")
        print(m)
    else:
        print('findall: not match')


if __name__ == '__main__':
    regexTest("(\w+)", "Regex Query Tool – A tool that allows the user to enter a text string and then in a separate control enter a regex pattern. It will run the regular expression against the source text and return any matches or flag errors in the regular expression.\
")
