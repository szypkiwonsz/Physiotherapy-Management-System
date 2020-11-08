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
