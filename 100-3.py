__author__ = 'rui'
#coding=utf-8
#因式分解
def PrimeFactorization(n):
    factor=[]
    if (n <=3):
        factor.append(n)
        return factor
    while (n%2 == 0):
            factor.append(2)
            n = n/2
    for i in range(3,n,2):
        if (i*i >n):
            break
        while (n%i == 0):
            factor.append(i)
            n = n/i
    if n != 1:
        factor.append(n)
    return factor

if __name__ == "__main__":
    print(PrimeFactorization(13579))
    for n in range(30):
        print(PrimeFactorization(n))