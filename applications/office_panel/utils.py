import calendar
import datetime

from applications.users.models import OfficeDay
from utils.add_zero import add_zero


def get_number_of_days_in_month(year, month):
    num_days = calendar.monthrange(year, month)[1]
    days = [datetime.date(year, month, day).day for day in range(1, num_days + 1)]
    return days


def get_hours_in_day(hour_open, hour_close):
    hours = [f'{i}:00' for i in range(hour_open, hour_close + 1)]
    return hours


def get_dates_in_month(request, days_in_month, month, year):
    dates_in_month = []
    for day in days_in_month:
        dates = []
        day = add_zero(day)
        date = datetime.datetime(int(year), int(month), int(day))
        day_of_week = date.weekday()
        office_day = OfficeDay.objects.get(office=request.user.office, day=day_of_week)
        hours_in_day = get_hours_in_day(int(office_day.earliest_appointment_time.split(':')[0]),
                                        int(office_day.latest_appointment_time.split(':')[0]))
        for hour in hours_in_day:
            date = f'{day}.{month}.{year} {hour}'
            dates.append(date)
        dates_in_month.append(dates)
    return dates_in_month
