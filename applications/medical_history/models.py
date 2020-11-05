from django.db import models
from django.utils import timezone

from applications.appointments.models import Appointment
from applications.office_panel.models import Patient
from applications.users.models import User


# Create your models here.
class MedicalHistory(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True)
    description = models.TextField()
    recommendations = models.TextField()
    date_selected = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.patient.first_name} {self.patient.last_name}'

    class Meta:
        verbose_name_plural = 'Medical Histories'
