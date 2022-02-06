from math import sin, cos, sqrt, atan2, radians, acos, asin, floor
import datetime

def rad(x):
    PI = 3.1415926535898
    return x * PI / 180.0

def dist_calculate(lat1, lon1, lat2, lon2):
    EARTH_RADIUS = 3440.0348679829
    radLat1 = rad(lat1)
    radLat2 = rad(lat2)
    a = radLat1 - radLat2
    b = rad(lon1) - rad(lon2)
    s = 2 * asin(sqrt(pow(sin(a / 2), 2) +
                                cos(radLat1) * cos(radLat2) * pow(sin(b / 2), 2)))
    s = s*EARTH_RADIUS
    return s

def time_calc(dep_time, arr_time):
    dateTimeA = datetime.datetime.combine(datetime.date.today(), dep_time)
    dateTimeB = datetime.datetime.combine(datetime.date.today(), arr_time)
    dateTimeDifference = dateTimeB - dateTimeA
    try:
        return datetime.datetime.strptime(str(dateTimeDifference), "%H:%M:%S").strftime("%H:%M")
    except:
        dateTimeDifference = dateTimeDifference + datetime.timedelta(days=1)
        return datetime.datetime.strptime(str(dateTimeDifference), "%H:%M:%S").strftime("%H:%M")