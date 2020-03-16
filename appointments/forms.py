from django import forms

from .models import Appointment


class AppointmentForm(forms.ModelForm):
    date = forms.DateTimeField(label='Provide date of visit:', input_formats=['%d.%m.%Y %H:%M'])
    choice_first = 'Consultation'
    choice_second = 'Manual and individual therapy'
    choice_third = 'Massage'
    choice_fourth = 'Shock wave'

    choice = forms.ChoiceField(label='Choose a service', choices=[(choice_first, choice_first),
                                                                  (choice_second, choice_second),
                                                                  (choice_third, choice_third),
                                                                  (choice_fourth, choice_fourth)])

    class Meta:
        model = Appointment
        fields = ['date', 'name', 'choice']


class AppointmentCancel(forms.Form):
    key = forms.CharField(label='Enter the visit number to confirm your cancellation:')
