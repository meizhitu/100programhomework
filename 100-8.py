__author__ = 'rui'
#coding=utf-8

def BinOctDecHex():
    inputStr = raw_input()
    arr = inputStr.split(" ")
    s1 = arr[0]
    base1 = int(arr[1])
    base2 = int(arr[2])
    sum = 0
    for i in s1:
        sum *= base1
        if (i <= '9' and i >= '0'):
            sum += ord(i) - ord('0')
        else:
            sum += ord(i) + 10 - ord('A')
    print("十进制：" + str(sum))
    s2 = ""
    while (sum != 0):
        yushu = sum % base2
        if (yushu <= 9):
            s2 += chr(yushu + ord('0'))
        else:
            s2 += chr(yushu + ord('A') - 10)
        sum /= base2
    print(s2[::-1])
    return s2[::-1]


if __name__ == "__main__":
    print("2 二进制 8 八进制 10 十进制 16 16进制")
    print("输入格式：数字 原进制 要转换的进制。比如 189 10 16")
    BinOctDecHex()