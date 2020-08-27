from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import SetPasswordForm
from django.core.validators import RegexValidator
from django.utils.translation import gettext as _

from users.widgets import MyClearableFileInput
from .models import User, Profile, Office, UserPatient

numeric_phone_number = RegexValidator('^[0-9]*$', 'Jako numer telefonu, możesz podać jedynie cyfry.')


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        self.error_messages['invalid_login'] = 'Niepoprawny email lub hasło. Badź konto nie zostało jeszcze aktywowane.'
        super().__init__(*args, **kwargs)
        super(LoginForm, self).__init__(*args, **kwargs)

        label = ['Email', 'Hasło']
        for i, field_name in enumerate(['username', 'password']):
            self.fields[field_name].help_text = None
            self.fields[field_name].label = label[i]


class OfficeSignUpForm(UserCreationForm):
    error_messages = {
        'email_mismatch': _('Podane emaile nie zgadzają się.'),
        'password_mismatch': _('Hasła nie pasują do siebie.'),
    }

    name = forms.CharField()
    address = forms.CharField()
    city = forms.CharField()
    phone_number = forms.CharField(min_length=9, max_length=9, validators=[numeric_phone_number], error_messages={
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

    def clean_confirm_email(self):
        email = self.cleaned_data.get("email")
        confirm_email = self.cleaned_data.get("confirm_email")
        if email and confirm_email and email != confirm_email:
            raise forms.ValidationError(
                self.error_messages['email_mismatch'],
                code='email_mismatch',
            )
        return confirm_email


class PatientSignUpForm(UserCreationForm):
    error_messages = {
        'email_mismatch': _('Podane emaile nie zgadzają się.'),
        'password_mismatch': _('Hasła nie pasują do siebie.'),
    }

    email = forms.CharField(widget=forms.EmailInput)
    confirm_email = forms.CharField(widget=forms.EmailInput)
    phone_number = forms.CharField(
        required=False, min_length=9, max_length=9, validators=[numeric_phone_number], error_messages={
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

    def clean_confirm_email(self):
        email = self.cleaned_data.get("email")
        confirm_email = self.cleaned_data.get("confirm_email")
        if email and confirm_email and email != confirm_email:
            raise forms.ValidationError(
                self.error_messages['email_mismatch'],
                code='email_mismatch',
            )
        return confirm_email


class NewSetPasswordForm(SetPasswordForm):
    error_messages = {
        'password_mismatch': _('Hasła nie pasują do siebie.'),
    }
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
    class Meta:
        model = User
        fields = ['email']


class OfficeUpdateForm(forms.ModelForm):
    website = forms.CharField(required=False)
    phone_number = forms.CharField(min_length=9, error_messages={
        'min_length': _('Numer powinien zawierać 9 cyfr.')
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
    phone_number = forms.CharField(label='Numer telefonu', required=False, min_length=9, error_messages={
        'min_length': _('Numer powinien zawierać 9 cyfr.')
    })

    class Meta:
        model = UserPatient
        fields = ['phone_number']


class ProfileUpdateForm(forms.ModelForm):
    image = forms.ImageField(label="Zmień swoje zdjęcie profilowe:", widget=MyClearableFileInput)

    class Meta:
        model = Profile
        fields = ['image']
