#!/usr/bin/env python
#encoding:utf8
import pdb

'''
optimization methods for optimized problems
'''

MIN_FLOAT = 1E-06
''' solve optimized problems f(args, vars) = 0 with Newton Gradient Method
Given:
    value_func : the valuation function, saying f
    partial_func: the partial funciton of f
    args_dict: other arguments in f, should be const in solving processing
    wanted_args_init_dict: the wanted arguments dict, should be given initiated values

    threshold: when abs(f) is below, the iteration should be stopped
    learn_rate: the learn rate
    max_iter: the maximum iteration number, if set to 0, then no limitation

    print_info: wheather to print the iteration info

Return:
    (wanted_args_init_dict, code, info)
    code: 0 is ok. other number is not ok and see the info

Example:
    given the problem to compute rate of average capital and interest, which satisfied
        A * (1 + r)^N  = X * [(1 + r)^N - 1] / r
    then :
        value_func = A * r * pow(1+r, N) - x * (pow(1+r, N) -1)
        patial_func = A * pow(1+r, N) + A * r * N * pow(1 + r, N - 1) - x * pow(1+r, N-1) * N
        args_dict = {"A": loan, "N": period, "x": monthly_payment}
        wanted_args_init_dict = {"r": init_r}
    result = GradientMethod(valuate, partial, args_dict, wanted_args_init_dict, print_info=True)

'''
def GradientMethod(value_func, partial_func, args_dict, wanted_args_init_dict, 
    threshold = 0.001, learn_rate= 0.01, max_iter = 0, print_info = False):
    n = 0
    #pdb.set_trace()
    while 1:
        n += 1
        args_dict.update(wanted_args_init_dict)
        gradient = partial_func(**args_dict)
        value = value_func(**args_dict)
        if abs(gradient) < MIN_FLOAT:
            return (wanted_args_init_dict, 1, "The gradient is ZERO at iteration {0}".format(n))
        if abs(value) < threshold:
            return (wanted_args_init_dict, 0, "Threshold is satisfied below {0} at iteration {1}".format(threshold, n))
        for k in wanted_args_init_dict:
            wanted_args_init_dict[k] = wanted_args_init_dict[k] - learn_rate * value / gradient

        if max_iter > 0 and n >= max_iter:
            return (wanted_args_init_dict, 2, "The gradient is ZERO at iteration {0}".format(n))
        if print_info:
            print "DEBUG>> {0}, VALUE:{1}, GRADIENT:{2}, WANTED:{3}".format(n, 
                value, gradient, wanted_args_init_dict)
            print args_dict
    return (wanted_args_init_dict, -1, "Abnormal Processing Occur!")

def TestGradientMethod():
    def valuate(A, x, N, r, **args):
        return A * r * pow(1+r, N) - x * (pow(1+r, N) -1)
    def partial(A, x, N, r, **args):
        return A * pow(1+r, N) + A * r * N * pow(1 + r, N - 1) - x * pow(1+r, N-1) * N
    args_dict = {"A": 98000.0, "N": 12.0, "x": 100000.0/12.0+850}
    wanted_args_init_dict = {"r": 0.01}
    result = GradientMethod(valuate, partial, args_dict, wanted_args_init_dict, print_info=True)
    print result
#TestGradientMethod()



