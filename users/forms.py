from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User


class MultipleForm(forms.Form):
    action = forms.CharField(max_length=60, widget=forms.HiddenInput())


class OfficeSignUpForm(UserCreationForm, MultipleForm):

    email = forms.CharField(widget=forms.EmailInput)
    password1 = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(OfficeSignUpForm, self).__init__(*args, **kwargs)

        for field_name in ['email', 'password1', 'password2']:
            self.fields[field_name].help_text = None

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


class PatientSignUpForm(UserCreationForm, MultipleForm):

    email = forms.CharField(widget=forms.EmailInput)

    def __init__(self, *args, **kwargs):
        super(PatientSignUpForm, self).__init__(*args, **kwargs)

        for field_name in ['email', 'password1', 'password2']:
            self.fields[field_name].help_text = None

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
