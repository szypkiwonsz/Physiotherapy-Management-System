from django.db import models
from django.utils import timezone

from users.models import User


class Patient(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patients')
    first_name = models.CharField(max_length=20, unique=False, default='')
    last_name = models.CharField(max_length=40, unique=False, default='')
    email = models.EmailField(unique=True, default='')
    address = models.CharField(max_length=50)
    pesel = models.CharField(max_length=11)
    phone_number = models.CharField(max_length=9)
    date_selected = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        super(Patient, self).save(*args, **kwargs)
