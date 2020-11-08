from datetime import datetime


def database_old_datetime_format_to_new(datetime_string):
    """
    The function changes the date string with dashes to the correct form of a string separated by dots.
    :param datetime_string: <string> -> String-Date in format: '%Y-%m-%d %H:%M:%S'
    :return: <string> -> String-Date in format: '%d.%m.%Y %H:%M'
    """
    new_datetime = datetime.strptime(datetime_string.split('+')[0], '%Y-%m-%d %H:%M:%S')
    return datetime.strftime(new_datetime, '%d.%m.%Y %H:%M')
