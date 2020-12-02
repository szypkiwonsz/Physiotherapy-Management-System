from django.db import models
from django.utils import timezone

from applications.users.models import User
from utils.regex_validators import alphanumeric_first_name, alphanumeric_last_name, numeric_pesel, numeric_phone_number


class Patient(models.Model):
    """Patient model for the office."""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patients')
    first_name = models.CharField(max_length=20, default='', validators=[alphanumeric_first_name()])
    last_name = models.CharField(max_length=40, default='', validators=[alphanumeric_last_name()])
    email = models.EmailField()
    address = models.CharField(max_length=50)
    pesel = models.CharField(max_length=11, validators=[numeric_pesel()])
    phone_number = models.CharField(max_length=9, validators=[numeric_phone_number()])
    date_selected = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        super(Patient, self).save(*args, **kwargs)
