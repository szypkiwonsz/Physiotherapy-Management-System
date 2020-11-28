import locale

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import SetPasswordForm
from django.utils.translation import gettext as _

from applications.users.models import User, Profile, Office, UserPatient, OfficeDay
from applications.users.utils import get_days_of_week, get_hours_in_day
from applications.users.widgets import MyClearableFileInput
from utils.regex_validators import numeric_phone_number


class LoginForm(AuthenticationForm):
    """An inheriting class for the user's login form."""

    def __init__(self, *args, **kwargs):
        self.error_messages['invalid_login'] = 'Niepoprawny email lub hasło. Badź konto nie zostało jeszcze aktywowane.'
        super().__init__(*args, **kwargs)
        super(LoginForm, self).__init__(*args, **kwargs)


class OfficeSignUpForm(UserCreationForm):
    """Form class for user registration as an office."""
    name = forms.CharField()
    address = forms.CharField()
    city = forms.CharField()
    phone_number = forms.CharField(min_length=9, max_length=9, validators=[numeric_phone_number()], error_messages={
        'min_length': _('Numer powinien zawierać 9 cyfr.'),
        'max_length': _('Numer powinien składać się z maksymalnie 9 cyfr.')
    })
    email = forms.CharField(widget=forms.EmailInput)
    confirm_email = forms.CharField(widget=forms.EmailInput)
    website = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(OfficeSignUpForm, self).__init__(*args, **kwargs)

        label = ['Nazwa gabinetu', 'Adres', 'Miasto', 'Numer telefonu', 'Strona internetowa', 'Adres email',
                 'Potwierdź adres email', 'Hasło',
                 'Potwierdź hasło']
        for i, field_name in enumerate(['name', 'address', 'city', 'phone_number', 'website', 'email', 'confirm_email',
                                        'password1', 'password2']):
            self.fields[field_name].help_text = None
            self.fields[field_name].label = label[i]

    class Meta:
        model = User
        fields = ['name', 'address', 'city', 'phone_number', 'website', 'email', 'confirm_email', 'password1',
                  'password2']

    error_messages = {
        'email_mismatch': _('Podane emaile nie zgadzają się.'),
        'password_mismatch': _('Hasła nie pasują do siebie.'),
    }

    def clean(self):
        """Overriding the method to check if both entered e-mails are correct."""
        cleaned_data = super(OfficeSignUpForm, self).clean()
        email = cleaned_data.get("email")
        confirm_email = cleaned_data.get("confirm_email")
        if email and confirm_email and email != confirm_email:
            raise forms.ValidationError(
                self.error_messages['email_mismatch'],
                code='email_mismatch',
            )
        return cleaned_data


class PatientSignUpForm(UserCreationForm):
    """Form class for user registration as a patient."""
    email = forms.CharField(widget=forms.EmailInput)
    confirm_email = forms.CharField(widget=forms.EmailInput)
    phone_number = forms.CharField(
        required=False, min_length=9, max_length=9, validators=[numeric_phone_number()], error_messages={
            'min_length': _('Numer powinien zawierać 9 cyfr.'),
            'max_length': _('Numer powinien składać się z maksymalnie 9 cyfr.')
        })

    def __init__(self, *args, **kwargs):
        super(PatientSignUpForm, self).__init__(*args, **kwargs)

        label = ['Numer telefonu', 'Adres email', 'Potwierdź adres email', 'Hasło', 'Potwierdź hasło']
        for i, field_name in enumerate(['phone_number', 'email', 'confirm_email', 'password1', 'password2']):
            self.fields[field_name].help_text = None
            self.fields[field_name].label = label[i]

    class Meta:
        model = User
        fields = ['phone_number', 'email', 'confirm_email', 'password1', 'password2']

    error_messages = {
        'email_mismatch': _('Podane emaile nie zgadzają się.'),
        'password_mismatch': _('Hasła nie pasują do siebie.'),
    }

    def clean(self):
        """Overriding the method to check if both entered e-mails are correct."""
        cleaned_data = super(PatientSignUpForm, self).clean()
        email = cleaned_data.get("email")
        confirm_email = cleaned_data.get("confirm_email")
        if email and confirm_email and email != confirm_email:
            raise forms.ValidationError(
                self.error_messages['email_mismatch'],
                code='email_mismatch',
            )
        return cleaned_data


class NewSetPasswordForm(SetPasswordForm):
    """Form for setting a new user password."""
    new_password1 = forms.CharField(
        label=_("Nowe hasło"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label=_("Potwierdź nowe hasło"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )


class UsersUpdateForm(forms.ModelForm):
    """Class form for updating the user profile."""

    class Meta:
        model = User
        fields = ['email']


class OfficeDayUpdateForm(forms.ModelForm):
    """Class form for updating the office times of making appointments."""
    # changing the names of the days of the week to Polish
    locale.setlocale(locale.LC_ALL, 'pl_PL')
    DAY_CHOICES = get_days_of_week()
    HOUR_CHOICES = get_hours_in_day()
    day = forms.ChoiceField(choices=DAY_CHOICES)
    earliest_appointment_time = forms.ChoiceField(choices=HOUR_CHOICES)
    latest_appointment_time = forms.ChoiceField(choices=HOUR_CHOICES)

    def __init__(self, *args, **kwargs):
        super(OfficeDayUpdateForm, self).__init__(*args, **kwargs)
        self.fields['day'].required = False
        self.fields['day'].widget.attrs['disabled'] = "disabled"

        label = ['Dzień', 'Najwcześniejsza godzina wizyty', 'Najpóźniejsza godzina wizyty']
        for i, field_name in enumerate(['day', 'earliest_appointment_time', 'latest_appointment_time']):
            self.fields[field_name].help_text = None
            self.fields[field_name].label = label[i]

    def clean_day(self):
        """Overriding the clean method, because the filed with disabled attr will post blank data."""
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.day
        else:
            return self.cleaned_data.get('day', None)

    class Meta:
        model = OfficeDay
        fields = ['day', 'earliest_appointment_time', 'latest_appointment_time']


class OfficeUpdateForm(forms.ModelForm):
    """Class form for updating the office-user data."""
    website = forms.CharField(required=False)
    phone_number = forms.CharField(min_length=9, validators=[numeric_phone_number()], error_messages={
        'min_length': _('Numer powinien zawierać 9 cyfr.'),
        'max_length': _('Numer powinien składać się z maksymalnie 9 cyfr.')
    })

    def __init__(self, *args, **kwargs):
        super(OfficeUpdateForm, self).__init__(*args, **kwargs)

        label = ['Nazwa', 'Adres', 'Miasto', 'Numer telefonu', 'Strona internetowa']
        for i, field_name in enumerate(['name', 'address', 'city', 'phone_number', 'website']):
            self.fields[field_name].help_text = None
            self.fields[field_name].label = label[i]

    class Meta:
        model = Office
        fields = ['name', 'address', 'city', 'phone_number', 'website']


class PatientUpdateForm(forms.ModelForm):
    """Class form for updating the user-patient data."""
    phone_number = forms.CharField(label='Numer telefonu', validators=[numeric_phone_number()], required=False,
                                   min_length=9, error_messages={
            'min_length': _('Numer powinien zawierać 9 cyfr.'),
            'max_length': _('Numer powinien składać się z maksymalnie 9 cyfr.')
        })

    class Meta:
        model = UserPatient
        fields = ['phone_number']


class ProfileUpdateForm(forms.ModelForm):
    """Class form for updating the user data."""
    image = forms.ImageField(label="Zmień swoje zdjęcie profilowe:", widget=MyClearableFileInput)

    class Meta:
        model = Profile
        fields = ['image']
