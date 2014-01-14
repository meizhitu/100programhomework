__author__ = 'rui'
#coding=utf-8

import re
#信用卡相关验证
class CreditCard:
    cardMap = (["^(51|52|53|54|55)", 16, "MasterCard"],
               ["^(4)", 16, "VISA"],
               ["^(4)", 13, "VISA"],
               ["^(34|37)", 15, "Amex"],
               ["^(6011)", 16, "Discover"],
               ["^(300|301|302|303|304|305|36|38)", 14, "DinersClub"],
               ["^(3)", 16, "JCB"],
               ["^(2131|1800)", 15, "JCB"],
               ["^(2014|2149)", 15, "enRoute"]
    )

    def isCardNumberValid(self, cardNo):
        cardNo = "".join(cardNo.split())
        checkSum = 0
        cardNo = str(cardNo)
        for i in range(cardNo.__len__() - 1, -1, -2):
            checkSum += (ord(cardNo[i]) - ord('0'))
        for i in range(cardNo.__len__() - 2, -1, -2):
            val = (ord(cardNo[i]) - ord('0')) * 2
            while val > 0:
                checkSum += (val % 10)
                val /= 10
        return (checkSum % 10) == 0
    def getCardType(self,cardNo):
        cardNo = "".join(cardNo.split())
        for k in (self.cardMap):
            if (len(cardNo) == k[1] and re.match(k[0], cardNo)):
                return k[2]
        return "NOT_KNOWN"


if __name__ == "__main__":
    #http://www.e1114.cn/service/32.htm 信用卡号生成
    creditCard = CreditCard()
    print(creditCard.getCardType("4899162644752"))
    print(creditCard.isCardNumberValid("4899162644752"))
    print(creditCard.getCardType("3782 370460 72742"))
    print(creditCard.isCardNumberValid("3782 370460 72742"))
    print(creditCard.getCardType("30760 4386 73082"))
    print(creditCard.isCardNumberValid("30760 4386 73082"))
    print(creditCard.getCardType("3502 8815 8636 3012"))
    print(creditCard.isCardNumberValid("3502 8815 8636 3012"))
    print(creditCard.getCardType(" 5226 6084 7328 3817"))
    print(creditCard.isCardNumberValid(" 5226 6084 7328 3817"))

