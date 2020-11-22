import datetime
from datetime import date

from django import template

register = template.Library()


@register.filter
def index(value, i):
    return value[i]


@register.filter
def len_str(list_of_values):
    return str(len(list_of_values))


@register.filter
def split(string_to_split, separator):
    return string_to_split.split(separator)


@register.filter
def remove_zero(value):
    if value == '0':
        value = ''
    return value


@register.filter
def add_zero(value):
    if int(value) < 10:
        value = '0' + str(value)
    return value


@register.filter
def is_past_due(str_date):
    return date.today() > datetime.datetime.strptime(str_date.split(' ')[0], "%d.%m.%Y").date()
