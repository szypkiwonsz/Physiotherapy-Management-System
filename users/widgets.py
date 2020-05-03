from django.forms import ClearableFileInput


# Profile picture label text.
class MyClearableFileInput(ClearableFileInput):
    initial_text = 'Aktualne'
    input_text = 'Zmień tutaj'
