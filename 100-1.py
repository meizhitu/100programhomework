__author__ = 'rui'
# coding=utf-8
#Find PI to the Nth Digit – Enter a number and have the program generate PI up to that many decimal places. Keep a limit to how far the program will go.
#http://pythonadventures.wordpress.com/2012/04/13/digits-of-pi-part-2/
def pi_digits():
    """生成PI"""
    q, r, t, k, n, l = 1, 0, 1, 1, 3, 3
    while True:
        if 4 * q + r - t < n * t:
            yield n
            q, r, t, k, n, l = (10 * q, 10 * (r - n * t), t, k, (10 * (3 * q + r)) / t - 10 * n, l)
        else:
            q, r, t, k, n, l = (q * k, (2 * q + r) * l, t * l, k + 1, (q * (7 * k + 2) + r * l) / (t * l), l + 2)


if __name__ == '__main__':
    digits = pi_digits()
    for i in range(30):
        print digits.next()
