import calendar
import datetime

import pandas as pd

from applications.users.models import OfficeDay, UserOffice
from utils.add_zero import add_zero


def get_number_of_days_in_month(year, month):
    """
    A function that returns a list of the number of days in a month.
    """
    num_days = calendar.monthrange(year, month)[1]
    days = [datetime.date(year, month, day).day for day in range(1, num_days + 1)]
    return days


def get_hours_in_day(earliest_time, latest_time, office_id):
    """A function that returns a list of hours between two given hours."""
    split_by = UserOffice.objects.values_list(
        'appointment_time_interval', flat=True).filter(pk=office_id).first()
    hours = []
    for i in range(earliest_time, latest_time):
        for j in range(0, 60, split_by):
            hours.append(f'{i}:{add_zero(j)}')
    return hours


def get_dates_in_month(office_id, days_in_month, month, year):
    """The function returns all possible dates of making an appointment to the office with the hours."""
    dates_in_month = []
    for day in days_in_month:
        dates = []
        date = datetime.datetime(int(year), int(month), int(day))
        office_day = OfficeDay.objects.get(office=office_id, day=date.weekday())
        hours_in_day = get_hours_in_day(
            earliest_time=int(office_day.earliest_appointment_time.split(':')[0]),
            latest_time=int(office_day.latest_appointment_time.split(':')[0]),
            office_id=office_id
        )
        for hour in hours_in_day:
            date = f'{add_zero(day)}.{add_zero(month)}.{year} {hour}'
            dates.append(date)
        dates_in_month.append(dates)
    return dates_in_month
