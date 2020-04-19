from django import forms
from .models import MedicalHistory


class MedicalHistoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(MedicalHistoryForm, self).__init__(*args, **kwargs)

        label = ['Pacjent', 'Wizyta', 'Opis', 'Zalecenia']
        for i, field_name in enumerate(['patient', 'appointment', 'description', 'recommendations']):
            self.fields[field_name].help_text = None
            self.fields[field_name].label = label[i]

    class Meta:
        model = MedicalHistory
        fields = ['patient', 'appointment', 'description', 'recommendations']
