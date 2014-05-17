__author__ = 'rui'
#coding=utf-8

import pygtk

pygtk.require("2.0")

MAX_KEY_SIZE = 26
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class CaesarCipher:
    def trans(self, mode, message, key):
        if mode[0] == 'd':
            key = -key
        translated = ''
        for symbol in message:
            if symbol.isalpha():
                num = ord(symbol)
                num += key
                if symbol.isupper():
                    if num > ord('Z'):
                        num -= 26
                    elif num < ord('A'):
                        num += 26
                elif symbol.islower():
                    if num > ord('z'):
                        num -= 26
                    elif num < ord('a'):
                        num += 26
                translated += chr(num)
            else:
                translated += symbol
        return translated

    def rudeDecode(self, message):
        entropies = []
        for key in range(0, 26):
            entropies.append(self.getEntropy(self.trans('d', message, key)))
        keyIndex = 0
        for i in range(1, len(entropies)):
            if entropies[i] < entropies[keyIndex]:
                keyIndex = i
        return self.trans('d', message, keyIndex)

    def getEntropy(self, deStr):
        result = 0
        englishFreqs = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 0.06966, 0.00153,
                        0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056,
                        0.02758, 0.00978, 0.02360, 0.00150, 0.01974, 0.00074]
        import math

        for i in range(0, len(deStr)):
            c = ord(deStr[i])
            if (c >= ord('A') and c <= ord('Z')):
                result += math.log(englishFreqs[c - ord('A')])
            elif (c >= ord('a') and c <= ord('z')):
                result += math.log(englishFreqs[c - ord('a')])
        return -result / math.log(2) / len(deStr)


class VigenereCipher:
    def trans(self, mode, message, key):
        translated = []
        keyIndex = 0
        key = key.upper()
        for symbol in message:
            num = LETTERS.find(symbol.upper())
            if num != -1:
                if (mode[0] == 'd'):
                    num -= LETTERS.find(key[keyIndex])
                else:
                    num += LETTERS.find(key[keyIndex])
                num %= len(LETTERS)
                if symbol.isupper():
                    translated.append(LETTERS[num])
                else:
                    translated.append(LETTERS[num].lower())
                keyIndex += 1
                if (keyIndex == len(key)):
                    keyIndex = 0
            else:
                translated.append(symbol)
        return ''.join(translated)

    def rudeDecode(self, message):
        #http://inventwithpython.com/vigenereHacker.py
        return "see http://inventwithpython.com/vigenereHacker.py"


class VernamCipher:
    def trans(self, message, key):
        translated = []
        keyIndex = 0
        for symbol in message:
            translated.append(chr(ord(symbol) ^ ord(key[keyIndex])))
        return ''.join(translated)

    def rudeDecode(self, message):
        return "not implement"


if __name__ == '__main__':
    cc = CaesarCipher()
    enResult = cc.trans('e',
                        "When we encrypt a message using a cipher, we will choose the key that is used to encrypt and decrypt this message",
                        13)
    print(enResult)
    deResult = cc.trans('d', enResult, 13)
    print(deResult)
    deResult = cc.rudeDecode(enResult)
    print(deResult)

    vc = VigenereCipher()
    enResult = vc.trans('e',
                        "When we encrypt a message using a cipher, we will choose the key that is used to encrypt and decrypt this message",
                        "April")
    print(enResult)
    deResult = vc.trans('d', enResult, "April")
    print(deResult)
    deResult = vc.rudeDecode(enResult)
    print(deResult)

    vec = VernamCipher()
    enResult = vec.trans(
        "When we encrypt a message using a cipher, we will choose the key that is used to encrypt and decrypt this message",
        "April")
    print(enResult)
    deResult = vec.trans(enResult, "April")
    print(deResult)
    deResult = vec.rudeDecode(enResult)
    print(deResult)
