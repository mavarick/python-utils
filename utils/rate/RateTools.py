#!/usr/bin/env python
#encoding:utf8
import pdb

''' Rate compution tools, Given:

    A: total loan amount
    x: monthly payed amount
    N: payment period (unit: month)
    r: interest

    normimal_interest_annual_rate: 
    real_interest_annual_rate:

    platform_fee:  platform fee, could be computed by A*platform_fee
'''
from GradientMethod import GradientMethod

# average capital plus interest
class AbstractRateWrap(object):
    # given loan and monthly pay, compute the rate 
    @staticmethod
    def calc_rate(loan, monthly_pay, period): pass
    # given loan, period, annual_rate, calculate the monthly_pay
    @staticmethod
    def calc_monthly_payment(loan, period, annual_rate): pass


class AvgCapitalAndInterestRateWrap(AbstractRateWrap):
    # evaluation function 
    @classmethod
    def valuate(cls, A, x, N, r, **args):
        return A * r * pow( 1+r, N) - x * (pow(1+r, N) -1)

    # partial function for rate computation
    @classmethod
    def partial(cls, A, x, N, r, **args):
        return A * pow(1+r, N) + A * r * N * pow(1 + r, N - 1) - x * pow(1+r, N-1) * N
        
    @staticmethod
    def calc_monthly_payment(loan, period, monthly_rate):
        return loan * monthly_rate * pow(1+monthly_rate, period) / (pow(1+monthly_rate, period) - 1)

    @staticmethod
    def calc_month_rate(loan, monthly_pay, period, init_r, **args):
        args_dict = {"A": loan * 1.0, "x": monthly_pay * 1.0, "N": period * 1.0}
        wanted_args_init_dict = {"r": init_r}
        result_dict, code, info = GradientMethod(
            AvgCapitalAndInterestRateWrap.valuate, 
            AvgCapitalAndInterestRateWrap.partial, 
            args_dict, 
            wanted_args_init_dict,
            **args)
        if code != 0:
            print info
        return result_dict.get("r")
    

    @staticmethod
    def calc_month_rate_approximate(loan, period, monthly_pay):
        ''' calculate the rate using approximate formula, given loan, period and monthly_payment
        which should be :
        r*N = (tN - 1) / (1 - (N-1)/2 * t)
        in which, t = monthly_pay / loan, and
        r is the approximate rate
        '''
        t = monthly_pay * 1.0 / loan
        return (t * period - 1) / (1 - (period - 1) * t / 2) / period

    
    @staticmethod
    def calc_month_rate_simplify(platform_fee, monthly_fee_rate, period):
        ''' given platform_fee and monthly_fee_rate, calculate the approximate interest
        whose formula is :
        r = 2 * (platform_fee + monthly_fee_rate * N) / (N + 1)
            r is the monthly_rate
        @return  the approximate monthly rate
        '''
        return 2 * (platform_fee + monthly_fee_rate * period) / (period + 1)


# average capital
class AvgCapitalRateWrap(AbstractRateWrap):
    @staticmethod
    def calc_monthly_payment(loan, N, monthly_rate):
        monthly_pays = []
        left_loan = loan
        monthly_capital_pay = loan * 1.0 / N
        for period in range(N):
            interest = left_loan * monthly_rate
            monthly_pay = monthly_capital_pay + interest

            left_loan = left_loan - monthly_capital_pay
            monthly_pays.append(monthly_pay)
        return monthly_pays

    @staticmethod
    def calc_month_rate(loan, first_month_pay, period):
        first_month_capital_pay = loan * 1.0 / period2
        first_month_interest = first_month_pay - first_month_capital_pay
        return first_month_interest / loan

def WangShangLoan():
    # 网商贷 http://tjr.taojindi.com/detail_8.html#calc
    loan = 100000.0
    N = 12.0
    platform_fee = 0.04
    monthly_payment = 8986.24
    r = AvgCapitalAndInterestRateWrap.calc_month_rate(
        loan = loan * (1 - platform_fee),
        monthly_pay = monthly_payment,
        period = N, 
        init_r = 0.5,
        learn_rate = 0.001)
    print r, r * 12

def AliLoan():
    # 阿里贷款 http://www.quickloans.cn/news_196751371.html
    loan = 100000.0
    N = 12.0
    platform_fee = 0.00
    monthly_payment = 110016.0/12
    r = AvgCapitalAndInterestRateWrap.calc_month_rate(
        loan = loan * (1 - platform_fee),
        monthly_pay = monthly_payment,
        period = N, 
        init_r = 0.9,
        learn_rate = 0.001)
    print r, r * 12, pow((1+r), 12) -1

def YiRenLoan():
    # 宜人贷  
    loan = 100000.0
    N = 12.0
    platform_fee = 0.00
    monthly_payment = 0.78 / 100 * loan + loan / 12.0
    r = AvgCapitalAndInterestRateWrap.calc_month_rate(
        loan = loan * (1 - platform_fee),
        monthly_pay = monthly_payment,
        period = N, 
        init_r = 0.9,
        learn_rate = 0.001)
    print r, r * 12, pow((1+r), 12) -1

def PingAnLoan():
    # http://www.yinhang.com/jingying/d-8t9sht
    loan = 50000.0
    N = 36.0
    platform_fee = 0.00
    monthly_payment = 2531
    r = AvgCapitalAndInterestRateWrap.calc_month_rate(
        loan = loan * (1 - platform_fee),
        monthly_pay = monthly_payment,
        period = N, 
        init_r = 0.9,
        learn_rate = 0.001)
    print r, r * 12, pow((1+r), 12) -1
#PingAnLoan()

def TestMonthlyPayment():
    loan = 10000.0
    period = 12
    annual_rate = 0.12
    x = AvgCapitalAndInterestRateWrap.calc_monthly_payment(
        loan = loan,
        period = period,
        monthly_rate = annual_rate / 12
        )
    print x, x*12

#TestMonthlyPayment()

def RenRenLoan():
    loan = 50000
    period = 3
    platform_fee = 0.00
    monthly_fee_rate = 0.88 / 100
    monthly_payment = loan*1.0 / period +  loan * monthly_fee_rate
    r = AvgCapitalAndInterestRateWrap.calc_month_rate(
        loan = loan * (1 - platform_fee),
        monthly_pay = monthly_payment,
        period = period, 
        init_r = 0.9,
        learn_rate = 0.001)
    print r, r * 12, pow((1+r), 12) -1, (monthly_payment * period - loan) / loan

#RenRenLoan()

def Test():

    loan = 1500000.0
    platform_fee = 33.3 / 100
    N = 12.0
    monthly_fee_rate = 1.0 / 100

    monthly_pay = loan /  N  + monthly_fee_rate * loan 

    #pdb.set_trace()
    r = AvgCapitalAndInterestRateWrap.calc_month_rate(
        loan = loan * (1-platform_fee), 
        monthly_pay = monthly_pay, 
        period = N, init_r= 0.5,
        learn_rate = 0.001)
    print "monthly_payment: ", monthly_pay
    print "total payment  : ", monthly_pay * N, monthly_pay * N / loan
    print r , r * 12 # 0.0185290380407
    print ">> the simplified formula: r = 2*M/(N+1), M = platform_fee + monthly_fee_rate * N >>"
    sim_r = 2 * (platform_fee + monthly_fee_rate * N) / (N + 1)

    print sim_r, sim_r * 12


def instraments():
    # http://cc.cmbchina.com/Financing/Bill.aspx
    r = AvgCapitalAndInterestRateWrap.calc_month_rate(10000, 1741.67, 6, 0.3)
    print r, r * 12


def HouseDebt():
    month_pay = 1600000.0 / 360
    r = AvgCapitalAndInterestRateWrap.calc_month_rate(920000, month_pay, 360, 0.3)
    print month_pay, r, r * 12

def PublicHouseAccDebt():
    N = 10 * 12
    loan = 1000000
    month_rate = 0.06 / 12
    month_pay = month_rate * loan 
    month_pay = AvgCapitalAndInterestRateWrap.calc_monthly_payment(loan, N, month_rate)
    print month_pay, month_pay * N


#instraments()
#HouseDebt()
PublicHouseAccDebt()




