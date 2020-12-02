from django import forms

from applications.appointments.models import Appointment
from applications.medical_history.models import MedicalHistory
from applications.office_panel.models import Patient


class MedicalHistoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # user pk from view.
        self.user = kwargs.pop('user', None)
        super(MedicalHistoryForm, self).__init__(*args, **kwargs)

        self.fields['appointment'] = forms.ModelChoiceField(
            queryset=Appointment.objects.filter(office__user=self.user), required=True
        )
        self.fields['patient'] = forms.ModelChoiceField(
            queryset=Patient.objects.filter(owner=self.user), required=True
        )

        label = ['Pacjent', 'Wizyta', 'Opis', 'Zalecenia']
        for i, field_name in enumerate(['patient', 'appointment', 'description', 'recommendations']):
            self.fields[field_name].help_text = None
            self.fields[field_name].label = label[i]

    class Meta:
        model = MedicalHistory
        fields = ['patient', 'appointment', 'description', 'recommendations']
