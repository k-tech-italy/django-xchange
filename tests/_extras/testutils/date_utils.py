import datetime as dt


def _dt(x):
    if '-' in x:
        return dt.datetime.strptime(x, '%Y-%m-%d').date()
    return dt.datetime.strptime(x, '%Y/%m/%d').date()
