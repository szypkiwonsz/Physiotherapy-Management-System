from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    email = models.EmailField("Email adress", unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
