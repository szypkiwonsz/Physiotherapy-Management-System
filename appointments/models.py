import random

from django.db import models
from django.utils import timezone

from office_panel.models import Patient
from users.models import User, Office


def random_string():
    return str(random.randint(10000, 99999))


# Create your models here.
class Appointment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    date = models.DateTimeField()
    name = models.CharField('Enter your first name:', max_length=120)
    date_selected = models.DateTimeField(default=timezone.now)
    phone_number = models.CharField(max_length=9)
    # Argument 'on_delete=models.CASCADE' - when User will be deleted, his post will be deleted too.
    confirmed = models.BooleanField(default=False)
    choice = models.CharField(max_length=120)

    def __str__(self):
        return str(self.owner)

    class Meta:
        # Name on the admin page.
        verbose_name_plural = 'Appointments'
