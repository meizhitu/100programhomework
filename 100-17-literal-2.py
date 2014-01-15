__author__ = 'rui'
#coding=utf-8

"""
“Pig Latin”是一个英语儿童文字改写游戏，整个游戏遵从下述规则：
(1). 元音字母是‘a’、‘e’、‘i’、‘o’、‘u’。字母‘y’在不是第一个字母的情况下，也被视作元音字母。其他字母均为辅音字母。例如，单词“yearly”有三个元音字母（分别为‘e’、‘a’和最后一个‘y’）和三个辅音字母（第一个‘y’、‘r’和‘l’）。
(2). 如果英文单词以元音字母开始，则在单词末尾加入“hay”后得到“Pig Latin”对应单词。例如，“ask”变为“askhay”，“use”变为“usehay”。
(3). 如果英文单词以‘q’字母开始，并且后面有个字母‘u’，将“qu”移动到单词末尾加入“ay”后得到“Pig Latin”对应单词。例如，“quiet”变为“ietquay”，“quay”变为“ayquay”。
(4). 如果英文单词以辅音字母开始，所有连续的辅音字母一起移动到单词末尾加入“ay”后得到“Pig Latin”对应单词。例如，“tomato”变为“omatotay”， “school” 变为“oolschay”，“you” 变为“ouyay”，“my” 变为“ymay ”，“ssssh” 变为“sssshay”。
"""
vowels = ("a", "e", "i", "o", "u", "A", "E", "I", "O", "U","y","Y")
def getVowelPosition(word):
    if word.startswith("qu"):
        return 2
    for i in range(len(word)):
        if (i == 0 and (word[i] == 'y' or word[i] == 'Y')):
            continue
        if (word[i] in vowels):
            return i
    return -1

def pigLatinConverter(sentence):
    words = sentence.split()
    new_words = []
    for word in words:
        pos = getVowelPosition(word)
        if (pos == 0):
            new_words.append(word+"hay")
        elif(pos > 0):
            new_words.append(word[pos:]+word[:pos]+"ay")
        else:
            new_words.append(word+"ay")
    return " ".join(new_words)

if __name__ == "__main__":
    print(pigLatinConverter("Welcome to the Python world Are you ready"))