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
    }

    def clean(self):
        """Overriding the method to check if email is unique."""
        cleaned_data = super(PatientForm, self).clean()
        email = cleaned_data.get("email")
        emails = Patient.objects.values_list('email', flat=True).filter(owner=self.user)
        if email in emails and email:
            raise forms.ValidationError(
                self.error_messages['email_unique_mismatch'],
                code='email_unique_mismatch'
            )
        return cleaned_data
