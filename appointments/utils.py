from datetime import datetime


def database_old_datetime_format_to_new(datetime_string):
    """
    The function changes the date string with dashes to the correct form of a string separated by dots.
    :param datetime_string: <string> -> String-Date in format: '%Y-%m-%d %H:%M:%S'
    :return: <string> -> String-Date in format: '%d.%m.%Y %H:%M'
    """
    new_datetime = datetime.strptime(datetime_string.split('+')[0], '%Y-%m-%d %H:%M:%S')
    return datetime.strftime(new_datetime, '%d.%m.%Y %H:%M')


def add_zero(number):
    """
    # Add zero before number if number is smaller than 10.
    :param number: <string> -> number
    :return: <string> -> number
    """
    if int(number) < 10:
        number = '0' + str(number)
    else:
        pass
    return number
