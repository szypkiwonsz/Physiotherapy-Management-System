class DateTime:

    @staticmethod
    # add zero before number if number is smaller than 10.
    def add_zero(number):
        if int(number) < 10:
            number = '0' + str(number)
        else:
            pass
        return number
