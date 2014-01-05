__author__ = 'rui'
#coding=utf-8

def ChangeReturn():
    """
    找零钱
    """
    price=input("应付：")
    receive=input("已付：")
    change=receive-price
    money=[100,50,20,10,5,2,1,0.5,0.2,0.1]
    changeC=[]
    print("找零：")
    for i in money:
        c  = int(change/i)
        changeC.append(c)
        change = change - c*i
    for i in range(money.__len__()):
        if (changeC[i] != 0):
            print(str(money[i])+" *"+ str(changeC[i]))
if __name__ == "__main__":
    ChangeReturn()