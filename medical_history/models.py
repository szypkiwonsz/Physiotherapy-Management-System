from django.db import models
from django.utils import timezone

from appointments.models import Appointment
from office_panel.models import Patient
from users.models import User


# Create your models here.
class MedicalHistory(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True)
    description = models.TextField()
    recommendations = models.TextField()
    date_selected = models.DateTimeField(default=timezone.now)
