from django.forms import ClearableFileInput


class MyClearableFileInput(ClearableFileInput):
    initial_text = 'Aktualne'
    input_text = 'Zmień tutaj'
