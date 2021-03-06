from django import forms
from django.utils.translation import gettext as _

from applications.office_panel.models import Patient


class PatientForm(forms.ModelForm):
    """Form class for office patient."""
    address = forms.CharField(required=False)
    pesel = forms.CharField(required=False, min_length=11, error_messages={
        'min_length': _('Pesel powinien zawierać 11 cyfr.'),
        'max_length': _('Pesel powinien składać się z maksymalnie 11 cyfr. ')
    })
    phone_number = forms.CharField(min_length=9, error_messages={
        'min_length': _('Numer powinien zawierać 9 cyfr.'),
        'max_length': _('Numer powinien składać się z maksymalnie 9 cyfr.')
    })
    email = forms.EmailField(required=False)

    def __init__(self, *args, **kwargs):
        # user pk from view
        self.user = kwargs.pop('user', None)
        self.patient = kwargs.pop('patient', None)
        super(PatientForm, self).__init__(*args, **kwargs)

        label = ['Imię', 'Nazwisko', 'Adres email', 'Adres zamieszkania', 'Pesel', 'Numer telefonu']
        for i, field_name in enumerate(['first_name', 'last_name', 'email', 'address', 'pesel', 'phone_number']):
            self.fields[field_name].help_text = None
            self.fields[field_name].label = label[i]

    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'address', 'pesel']

    error_messages = {
        'email_unique_mismatch': _('Podany email jest już zajęty.'),
        'pesel_unique_mismatch': _('Ten numer pesel jest już przypisany do innego pacjenta.')
    }

    def clean(self):
        """Overriding the method to check if email or pesel is unique."""
        cleaned_data = super(PatientForm, self).clean()
        email = cleaned_data.get('email')
        pesel = cleaned_data.get('pesel')
        patient_by_email = Patient.objects.filter(email=email, owner=self.user).first()
        patient_by_pesel = Patient.objects.filter(pesel=pesel, owner=self.user).first()
        if patient_by_email and email and self.patient != patient_by_email.pk:
            raise forms.ValidationError(
                self.error_messages['email_unique_mismatch'],
                code='email_unique_mismatch'
            )
        elif patient_by_pesel and pesel and self.patient != patient_by_pesel.pk:
            raise forms.ValidationError(
                self.error_messages['pesel_unique_mismatch'],
                code='pesel_unique_mismatch'
            )
        return cleaned_data
