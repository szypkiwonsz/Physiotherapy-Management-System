from django import forms

from Physiotherapy_Management_System import settings
from .models import Appointment


class AppointmentForm(forms.ModelForm):
    date = forms.DateTimeField(
        label='Data wizyty:',
        input_formats=settings.DATE_INPUT_FORMATS,
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )
    name = forms.CharField(label='Imię')
    phone_number = forms.CharField(label='Numer telefonu')
    choice = ['Konsultacja', 'Terapia manualna i indywidualna', 'Masaż', 'Fala uderzeniowa']

    choice = forms.ChoiceField(
        label='Usługa',
        choices=[(choice[0], choice[0]),
                 (choice[1], choice[1]),
                 (choice[2], choice[2]),
                 (choice[3], choice[3])]
    )

    class Meta:
        model = Appointment
        fields = ['date', 'name', 'phone_number', 'choice']


class AppointmentOfficeUpdateForm(forms.ModelForm):
    date = forms.DateTimeField(
        label='Data wizyty:',
        input_formats=settings.DATE_INPUT_FORMATS,
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )
    confirmed = forms.BooleanField(required=False)

    class Meta:
        model = Appointment
        fields = ['date', 'confirmed']


class AppointmentCancel(forms.Form):
    key = forms.CharField(label='Podaj numer wizyty aby potwierdzić odwołanie wizyty.')
