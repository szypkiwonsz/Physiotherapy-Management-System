from django.core.validators import RegexValidator


def numeric_phone_number():
    return RegexValidator('^[0-9]*$', 'Jako numer telefonu, możesz podać jedynie cyfry.')


def numeric_pesel():
    return RegexValidator('^[0-9]*$', 'Jako pesel, możesz podać jedynie cyfry.')


def alphanumeric_first_name():
    return RegexValidator('^[A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ]*$', 'Imię nie może zawierać cyfr, ani znaków specjalnych.')


def alphanumeric_last_name():
    return RegexValidator('^[A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ]*$', 'Nazwisko nie może zawierać cyfr, ani znaków specjalnych.')
