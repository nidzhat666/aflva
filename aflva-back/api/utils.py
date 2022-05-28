def convert_hours(seconds):
    if seconds:
        hour = seconds // 3600
    else:
        hour = 0
    return hour


def timedelta_format(time):
    return ':'.join(str(time).split(':')[:2])
