__author__ = 'rui'
#coding=utf-8

def CostCoverFloor():
    w = input("输入W：")
    h = input("输入H：")
    cost = input("输入单价：")
    print("Cost Cover Floor:"+ str(w*h*cost))

if __name__ == "__main__":
    CostCoverFloor()