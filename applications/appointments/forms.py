from django import forms
from django.utils.translation import gettext as _

from Physiotherapy_Management_System import settings
from applications.appointments.models import Appointment
from applications.office_panel.models import Patient


class AppointmentPatientMakeForm(forms.ModelForm):
    date = forms.DateTimeField(
        label='Data wizyty:',
        input_formats=settings.DATE_INPUT_FORMATS,
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )
    first_name = forms.CharField(label='Imię')
    last_name = forms.CharField(label='Nazwisko')
    phone_number = forms.CharField(label='Numer telefonu', min_length=9, error_messages={
        'min_length': _('Numer powinien zawierać 9 cyfr.'),
        'max_length': _('Numer powinien składać się z maksymalnie 9 cyfr.')
    })
    choices = ['Konsultacja', 'Terapia manualna i indywidualna', 'Masaż', 'Fala uderzeniowa']
    choice = forms.ChoiceField(
        label='Usługa',
        choices=[(choices[0], choices[0]),
                 (choices[1], choices[1]),
                 (choices[2], choices[2]),
                 (choices[3], choices[3])]
    )

    class Meta:
        model = Appointment
        fields = ['date', 'first_name', 'last_name', 'phone_number', 'choice']


class AppointmentOfficeMakeForm(AppointmentPatientMakeForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.date = kwargs.pop('date', None)
        super(AppointmentOfficeMakeForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = forms.HiddenInput()
        self.fields['phone_number'].widget = forms.HiddenInput()
        self.fields['owner'] = forms.ModelChoiceField(queryset=Patient.objects.filter(owner=self.user), required=False)
        self.fields['owner'].label = 'Pacjent'
        self.fields['date'].widget = forms.TextInput(attrs={'value': str(self.date), 'readonly': 'true'})


class AppointmentOfficeUpdateForm(forms.ModelForm):
    date = forms.DateTimeField(
        label='Data wizyty:',
        input_formats=settings.DATE_INPUT_FORMATS,
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )
    confirmed = forms.BooleanField(required=False, label='Potwierdzona')

    class Meta:
        model = Appointment
        fields = ['date', 'confirmed']
