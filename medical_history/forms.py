from django import forms
from .models import MedicalHistory


class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = ['description']
