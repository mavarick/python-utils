#!/usr/bin/env python
"""parse rules like:
    ((((A=a)|(B=b)|(C=c))&(D=d)&(E=e))|(F=f))
NOTICE: the basic rule are 'A=a', A is field, a is value
"""

import json

def parse_rule(rule):
    #if len(rule) < 1:
    #    raise Exception("length error")
    data = []
    idx = 0
    while idx < len(rule):
        c = rule[idx]
        if c == "(":
            idx_end = find_respond_end(rule, idx)
            _rule = parse_rule(rule[(idx+1):(idx_end)])
            
            data.append(_rule)
            idx = idx_end + 1
        elif c == "|":
            data.append("|")
            idx += 1
        elif c == "&":
            data.append("&")
            idx += 1
        else:
            data.append(rule)
            break
    return data
        

def find_respond_end(rule, start_idx):
    n = 0
    for idx, c in enumerate(rule[start_idx:]):
        if c == "(":
            n += 1
        if c == ")":
            n -= 1
        if n == 0:
            return start_idx + idx
             

def main():
    r = "((((A=a)|(B=b)|(C=c))&(D=d)&(E=e))|(F=f))"
    #r = "(A=a)"
    print r
    data = parse_rule(r)
    print data


if __name__ == "__main__":
    main()



