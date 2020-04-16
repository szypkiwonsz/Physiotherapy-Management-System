from django import forms

from .models import Appointment


class AppointmentForm(forms.ModelForm):
    date = forms.DateTimeField(label='Podaj datę wizyty:', input_formats=['%d.%m.%Y %H:%M'],
                               widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    choice = ['Konsultacja', 'Terapia manualna i indywidualna', 'Masaż', 'Fala uderzeniowa']

    choice = forms.ChoiceField(label='Choose a service', choices=[(choice[0], choice[0]),
                                                                  (choice[1], choice[1]),
                                                                  (choice[2], choice[2]),
                                                                  (choice[3], choice[3])])

    class Meta:
        model = Appointment
        fields = ['date', 'name', 'choice']


class AppointmentCancel(forms.Form):
    key = forms.CharField(label='Podaj numer wizyty aby potwierdzić odwołanie wizyty.')
