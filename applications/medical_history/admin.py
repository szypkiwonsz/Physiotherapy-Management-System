from django.contrib import admin

# Register your models here.
from applications.medical_history.models import MedicalHistory

admin.site.register(MedicalHistory)
