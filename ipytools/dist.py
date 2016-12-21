#encoding:utf8


def dist_range(ser, points):
    total_size = ser.size
    data = []
    for p in points:
        ser_p = (ser == p).sum()
        ratio_p = ser_p * 1.0 / total_size
        data.append((p, ser_p, ratio_p))
        print p, ser_p, ratio_p
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

