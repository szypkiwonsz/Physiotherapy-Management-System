from django import forms
from django.utils.translation import gettext as _

from applications.office_panel.models import Patient


class PatientForm(forms.ModelForm):
    address = forms.CharField(required=False)
    pesel = forms.CharField(required=False, min_length=11, error_messages={
        'min_length': _('Pesel powinien zawierać 11 cyfr.'),
        'max_length': _('Pesel powinien składać się z maksymalnie 11 cyfr. ')
    })
    phone_number = forms.CharField(min_length=9, error_messages={
        'min_length': _('Numer powinien zawierać 9 cyfr.'),
        'max_length': _('Numer powinien składać się z maksymalnie 9 cyfr.')
    })

    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)

        label = ['Imię', 'Nazwisko', 'Adres email', 'Adres zamieszkania', 'Pesel', 'Numer telefonu']
        for i, field_name in enumerate(['first_name', 'last_name', 'email', 'address', 'pesel', 'phone_number']):
            self.fields[field_name].help_text = None
            self.fields[field_name].label = label[i]

    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'email', 'address', 'pesel', 'phone_number']
