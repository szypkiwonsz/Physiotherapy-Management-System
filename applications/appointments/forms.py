from datetime import datetime

from django import forms
from django.utils.translation import gettext as _

from Physiotherapy_Management_System import settings
from applications.appointments.models import Appointment, Service
from applications.office_panel.models import Patient
from applications.office_panel.utils import get_dates_taken
from applications.users.models import OfficeDay


class AppointmentPatientMakeForm(forms.ModelForm):
    """Form for patient to make an appointment."""
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
    choice = forms.CharField(label='Usługa')

    def __init__(self, *args, **kwargs):
        self.office = kwargs.pop('office', None)
        self.appointment = kwargs.pop('appointment', None)
        self.date = kwargs.pop('date', None)
        self.service = kwargs.pop('service', None)
        super(AppointmentPatientMakeForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget = forms.TextInput(attrs={'value': str(self.date), 'readonly': 'true'})
        self.fields['choice'].widget = forms.TextInput(attrs={'value': str(self.service), 'readonly': 'true'})

    class Meta:
        model = Appointment
        fields = ['date', 'first_name', 'last_name', 'phone_number', 'choice']

    error_messages = {
        'appointment_date_taken': _('Wybrana data jest już zajęta.'),
        'appointment_default_time_error': _('Wybierz poprawną godzinę.'),
        'appointment_incorrect_date': _('Wybierz poprawną godzinę.')
    }

    def clean(self):
        """Validate appointment date provided to form."""
        cleaned_data = super(AppointmentPatientMakeForm, self).clean()
        dates_taken = Appointment.objects.filter(office=self.office)
        service = Service.objects.filter(name=self.service, office=self.office).first()
        appointment = Appointment.objects.filter(date=cleaned_data.get('date'), office=self.office).first()
        if service:
            dates_taken = get_dates_taken(dates_taken, service)
        else:
            dates_taken = []
        if cleaned_data.get('date'):
            weekday = cleaned_data.get('date').weekday()
        else:
            weekday = None
        day = OfficeDay.objects.filter(office=self.office, day=weekday).first()
        # if the user selected default hour time
        if cleaned_data.get('date') and cleaned_data.get('date').hour == 23 and cleaned_data.get('date').minute == 59:
            raise forms.ValidationError(
                self.error_messages['appointment_default_time_error'],
                code='appointment_default_time_error'
            )
        # if hour time selected is not correct with office hours
        elif day and int(day.earliest_appointment_time.split(':')[0]) > int(cleaned_data.get('date').hour) \
                or day and int(day.latest_appointment_time.split(':')[0]) < int(cleaned_data.get('date').hour):
            raise forms.ValidationError(
                self.error_messages['appointment_incorrect_date'],
                code='appointment_incorrect_date'
            )
        # if the date of the visit is already taken
        elif cleaned_data.get('date') and datetime.strftime(cleaned_data.get('date'), '%d.%m.%Y %H:%M') in dates_taken \
                and appointment and appointment.pk != self.appointment:
            raise forms.ValidationError(
                self.error_messages['appointment_date_taken'],
                code='appointment_date_taken'
            )
        return cleaned_data


class AppointmentOfficeMakeForm(AppointmentPatientMakeForm):
    """Form for office to make an appointment."""

    def __init__(self, *args, **kwargs):
        super(AppointmentOfficeMakeForm, self).__init__(*args, **kwargs)
        # removing unnecessary fields
        del self.fields['first_name']
        del self.fields['last_name']
        del self.fields['phone_number']
        self.fields['patient'] = forms.ModelChoiceField(queryset=Patient.objects.filter(owner__useroffice=self.office),
                                                        required=True)
        self.fields['patient'].label = 'Pacjent'


class AppointmentOfficeUpdateForm(AppointmentOfficeMakeForm):
    """Form for office to update an appointment."""
    confirmed = forms.BooleanField(required=False, label='Potwierdzona')

    def __init__(self, *args, **kwargs):
        super(AppointmentOfficeUpdateForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget = forms.TextInput()
        self.fields['choice'] = forms.ModelChoiceField(
            queryset=Service.objects.filter(office=self.office), required=True
        )
        self.fields['choice'].label = 'Usługa'
        del self.fields['patient']

    class Meta:
        model = Appointment
        fields = ['date', 'confirmed']


class AppointmentPatientUpdateForm(AppointmentOfficeUpdateForm):
    """Form for office to update an appointment."""

    def __init__(self, *args, **kwargs):
        super(AppointmentPatientUpdateForm, self).__init__(*args, **kwargs)
        del self.fields['confirmed']
        self.fields['first_name'] = forms.CharField(label='Imię')
        self.fields['last_name'] = forms.CharField(label='Nazwisko')
        self.fields['phone_number'] = forms.CharField(label='Numer telefonu', min_length=9, error_messages={
            'min_length': _('Numer powinien zawierać 9 cyfr.'),
            'max_length': _('Numer powinien składać się z maksymalnie 9 cyfr.')
        })

    class Meta:
        model = Appointment
        fields = ['first_name', 'last_name', 'phone_number', 'date']


class ServiceForm(forms.ModelForm):
    """Form for office to add and update an appointment."""

    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        self.fields['duration'].help_text = 'czas podany w minutach'

        label = ['Nazwa', 'Czas trwania']
        for i, field_name in enumerate(['name', 'duration']):
            self.fields[field_name].label = label[i]

    class Meta:
        model = Service
        fields = ['name', 'duration']
