from django.db import models
from users.models import User, Patient
from appointments.models import Appointment


# Create your models here.
class MedicalHistory(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    description = models.TextField()
    recommendations = models.TextField()
