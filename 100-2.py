__author__ = 'rui'
#coding=utf-8
#Fibonacci Sequence – Enter a number and have the program generate the Fibonacci sequence to that number or to the Nth number.
def Fib(n):
    if n == 1 or n == 2: return 1
    fib1 = 1
    fib2 = 1
    for i in range(2, n):
        fib1, fib2 = fib2, fib1 + fib2
    return fib2


def AcmFib(n):
    #SICP的练习1-19里面则提到一个O(log(n))的巧妙算法：将计算fibonacci的每次迭代 (a, b) <- (a + b, a) 表示为一个变换T[p=0, q=1]，具体表示为（似乎是用矩阵乘法倒推过来的）
    #矩阵
    #|0 1|*[a b]=[b a+b]
    #|1 1|
    def iter(a, b, p, q, n):
        if n == 0:
            return b;
        elif n % 2 == 0:
            return iter(a, b, p * p + q * q, 2 * p * q + q * q, n / 2)
        else:
            return iter(a * (p + q) + b * q, a * q + b * p, p, q, n - 1)

    return iter(1, 0, 0, 1, n)


if __name__ == '__main__':
    for i in range(1, 30):
        print(Fib(i))
        print(AcmFib(i))
