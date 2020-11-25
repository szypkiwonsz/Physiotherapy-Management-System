import datetime
from datetime import date

from django import template

register = template.Library()


@register.filter
def index(value, i):
    """Returns the index of the given value."""
    return value[i]


@register.filter
def len_str(list_of_values):
    """Returns the length of the list of values ​​as a string."""
    return str(len(list_of_values))


@register.filter
def split(string_to_split, separator):
    """Returns the list of strings divided by the separator."""
    return string_to_split.split(separator)


@register.filter
def remove_zero(value):
    """Removes 0 from string if string is 0."""
    if value == '0':
        value = ''
    return value


@register.filter
def add_zero(value):
    """Returns a string appended with 0 if the value is less than 10."""
    if int(value) < 10:
        value = '0' + str(value)
    return value


@register.filter
def is_past_due(str_date):
    """Returns bool value if the entered date is earlier than today."""
    return date.today() > datetime.datetime.strptime(str_date.split(' ')[0], "%d.%m.%Y").date()
