from django.db import models
from users.models import User


# Create your models here.
class MedicalHistory(models.Model):
    description = models.TextField()
