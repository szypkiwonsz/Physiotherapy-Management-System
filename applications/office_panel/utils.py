import calendar
import datetime


def get_number_of_days_in_month(year, month):
    num_days = calendar.monthrange(year, month)[1]
    days = [datetime.date(year, month, day).day for day in range(1, num_days + 1)]
    return days


def get_hours_in_day(hour_open, hour_close):
    hours = [f'{i}:00' for i in range(hour_open, hour_close+1)]
    return hours
