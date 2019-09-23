#encoding:utf8

from pandas import DataFrame, Series

def dist_range(ser, points):
    total_size = ser.size
    data = []
    
    items = [0]
    items.extend(points)
    ts = zip(items[0:-1], items[1:])
    for p in ts:
        ser_p = ((ser > p[0]) & (ser <= p[1])).sum()
        ratio_p = ser_p * 1.0 / total_size
        data.append((p, ser_p, ratio_p))
        print p, ser_p, ratio_p
    ser_p = (ser > points[-1]).sum()
    ratio_p = ser_p * 1.0 / total_size
    data.append((p, ser_p, ratio_p))
    print points[-1], ser_p, ratio_p

    print
    return data


def dist_range_cumsum(ser, points):
    total_size = ser.size
    data = []
    for p in points:
        ser_p = (ser <= p).sum()
        ratio_p = ser_p * 1.0 / total_size
        data.append((p, ser_p, ratio_p))
        print p, ser_p, ratio_p
    print
    return data

