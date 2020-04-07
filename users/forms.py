from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.views import SetPasswordForm
from .models import User, Patient
from django.utils.translation import gettext as _


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        label = ['Email', 'Hasło']
        for i, field_name in enumerate(['username', 'password']):
            self.fields[field_name].help_text = None
            self.fields[field_name].label = label[i]


class OfficeSignUpForm(UserCreationForm):
    error_messages = {
        'password_mismatch': _('Podane hasła nie zgadzają się.'),
        'email_mismatch': _('Podane emaile nie zgadzają się.'),
    }

    name = forms.CharField()
    email = forms.CharField(widget=forms.EmailInput)
    confirm_email = forms.CharField(widget=forms.EmailInput)

    def __init__(self, *args, **kwargs):
        super(OfficeSignUpForm, self).__init__(*args, **kwargs)

        label = ['Nazwa gabinetu', 'Adres email', 'Potwierdź adres email', 'Hasło', 'Potwierdź hasło']
        for i, field_name in enumerate(['name', 'email', 'confirm_email', 'password1', 'password2']):
            self.fields[field_name].help_text = None
            self.fields[field_name].label = label[i]

    class Meta:
        model = User
        fields = ['name', 'email', 'confirm_email', 'password1', 'password2']

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
        'password_mismatch': _('Podane hasła nie zgadzają się.'),
        'email_mismatch': _('Podane emaile nie zgadzają się.'),
    }

    email = forms.CharField(widget=forms.EmailInput)
    confirm_email = forms.CharField(widget=forms.EmailInput)

    def __init__(self, *args, **kwargs):
        super(PatientSignUpForm, self).__init__(*args, **kwargs)

        label = ['Adres email', 'Potwierdź adres email', 'Hasło', 'Potwierdź hasło']
        for i, field_name in enumerate(['email', 'confirm_email', 'password1', 'password2']):
            self.fields[field_name].help_text = None
            self.fields[field_name].label = label[i]

    class Meta:
        model = User
        fields = ['email', 'confirm_email', 'password1', 'password2']

    def clean_confirm_email(self):
        email = self.cleaned_data.get("email")
        confirm_email = self.cleaned_data.get("confirm_email")
        if email and confirm_email and email != confirm_email:
            raise forms.ValidationError(
                self.error_messages['email_mismatch'],
                code='email_mismatch',
            )
        return confirm_email


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'email']


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
