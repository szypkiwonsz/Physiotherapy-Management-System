from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_office = models.BooleanField(default=False)

    username = models.CharField(max_length=40, unique=False, default='')
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Patient(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patients')
    first_name = models.CharField(max_length=20, unique=False, default='')
    last_name = models.CharField(max_length=40, unique=False, default='')
    email = models.EmailField(unique=True, default='')

    def __str__(self):
        return self.first_name + " " + self.last_name


class Office(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=50)
    patients = models.ManyToManyField(Patient)
