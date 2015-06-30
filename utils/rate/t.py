from RateTools import AvgCapitalAndInterestRateWrap



loan = 10000.0
month_pay_rate = 0.01

period = 12

month_payment = AvgCapitalAndInterestRateWrap.calc_monthly_payment(loan, period, month_pay_rate * 12)

print month_payment * 12, month_payment

platform_fee = 0.065
monthly_fee_rete = 1.18 / 100 
period = 12

real_rate = AvgCapitalAndInterestRateWrap.calc_month_rate_simplify(platform_fee, monthly_fee_rete, period)
print real_rate, real_rate * 12

print "* " * 20

loan = 10000.0
period = 6
monthly_fee_rate = 1.18/100
monthly_pay = loan / period + loan * monthly_fee_rate

real_rate = AvgCapitalAndInterestRateWrap.calc_month_rate(loan * (1 - platform_fee), monthly_pay, period, 0.5)
simulate_real_rate = AvgCapitalAndInterestRateWrap.calc_month_rate_simplify(platform_fee, monthly_fee_rate, period)
print real_rate, real_rate* period, monthly_fee_rate * period * 2
print simulate_real_rate, simulate_real_rate * period
print monthly_pay * period
print platform_fee * loan
print monthly_fee_rate * loan * period, monthly_fee_rate * loan * period + platform_fee * loan


