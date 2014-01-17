__author__ = 'rui'
#coding=utf-8
def MortgageCalculator():
    '''贷款计算，等额本息
    '''
    #贷款本金 X	月利率×[（1+月利率）^ 还款月数 ]
    #----------------------------------
    #[（1+月利率）^ 还款月数 ] - 1
    total = input("贷款总额：")
    interest = input("贷款年利率：") / 100.0 / 12
    print(interest)
    years = input("贷款时间（多少个月）：")
    monthLoan = total * interest * ((1 + interest) ** years) / ((1 + interest) ** years - 1)
    print("每月还款额(等额本息)：%.2f" % (monthLoan))
    pass


if __name__ == "__main__":
    MortgageCalculator()