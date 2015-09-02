#encoding:utf8

import math
import time
'''
本息计算
'''

def EqualBoth(loan, month_rate, N):
    return loan * month_rate * pow(1+month_rate, N) / (pow(1+month_rate, N) - 1)

def EqualBoth_Test():
    loan = 10000
    month_rate = 0.0861/12
    N = 12
    month_pay = EqualBoth(loan, month_rate, N)
    print month_pay

def CalTotalPayWithInterest(month_pay, month_rate, N):
    pay_sum = 0.0
    for i in range(N):
        pay_sum += month_pay * pow(1 + month_rate, i)
    return pay_sum

def CalRate(month_pay, loan, N):
    a = loan * N - loan
    b = loan * N - 2 * loan
    c = month_pay * N - loan - month_pay
    result1 = (-b + math.sqrt(pow(b, 2) - 4*a*c)) / (2 * a)
    return result1

'''
A: 贷款额度
x: 每月还款额
N：还款期数
r：初始月利率
'''
def partial(A, x, N, r):
    return A * pow(1+r, N) + A * r * N * pow(1 + r, N - 1) - x * pow(1+r, N-1) * N

'''
等额本息
最后参数 应该满足 差值为0 的时候
'''
def valuate(A, x, N, r):
    return A * r * pow(1+r, N) - x * (pow(1+r, N) -1)

'''
给定贷款额度，每日还款额，初始利率，计算实际的利率
'''
def cal_fee_rate(A, x, N, init_r, f):
    '''
    init_r : initiate value of rate
    '''
    n = 0
    r = init_r
    while 1:
        gradient = partial(A, x, N, r)
        value = f(A, x, N, r)
        rate =  0.01
        last_r = r
        r = r - rate * value / gradient

        n += 1
        print ">>", r, gradient, value
        if abs(value) < 0.001:
            break
    return r

def linspace(start, end, number):
    space = (end - start) * 1.0 / (number - 1)
    item = start
    items = [item]
    for i in range(number - 1):
        item = item + space
        items.append(item)
    return items

def test():
	'''
    loan = 100000
    month_rate = 0.1/12
    N = 12
    month_pay = EqualBoth(loan, month_rate, N)
    platform_fee = 1650
    print "month pay: ", month_pay
    total_pay_with_interest = CalTotalPayWithInterest(month_pay, month_rate, N)
    print "total pay with interest: ", total_pay_with_interest
    total2 = CalTotalPayWithInterest(month_pay+platform_fee, month_rate, N)
    print "total pay with platform: ", total2

    #real_rate = CalRate(month_pay + platform_fee, loan, N)
    #print "real rate: ", real_rate
    print "real payed month: ", month_pay+platform_fee
    result = solution(loan, month_pay+platform_fee, N, 0.04, valuate)
    print "result : ", result
    for r in linspace(0.00, 0.02, 20):
        #print r, valuate(loan, month_pay+platform_fee, N, r)
        print r, valuate(loan, month_pay+platform_fee, N, r)
	'''
	loan = 100000.0
	other_fee = 0.02
	platform_fee_rate = 0.85 / 100
	N = 12.0
	month_pay = loan / N
	rate = solution(loan*(1-other_fee), month_pay+platform_fee_rate*loan, N, 0.01, valuate)  # 0.0185290393264
	

#test()

