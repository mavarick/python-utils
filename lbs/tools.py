#encoding:utf8
import math


EARTH_RADIUS = 6378.137
PI=3.1415926535


def get_sphere_distance(lon1, lat1, lon2, lat2):
    # 返回单位:km
    d1 = rad(lon1) - rad(lon2)

    lat_rad1 = rad(lat1)
    lat_rad2 = rad(lat2)
    d2 = lat_rad1 - lat_rad2

    s = 2 * math.asin(math.sqrt(math.pow(math.sin(d2/2), 2) +
                      math.cos(lat_rad1) * math.cos(lat_rad2) * math.pow(math.sin(d1/2.0), 2)))
    return s * EARTH_RADIUS


def rad(ang):
    # 度 -> 球面角度
    return ang * PI / 180.0



def test():
    lat1, lon1 = 40.0706,116.588717
    lat2, lon2 = 40.070917,116.588684
    print get_sphere_distance(lon1, lat1, lon2, lat2)

    print get_sphere_distance(100, 30, 101, 30)

if __name__ == "__main__":
    test()


