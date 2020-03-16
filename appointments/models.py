from django.db import models
from django.utils import timezone
from users.models import User
import random


def random_string():
    return str(random.randint(10000, 99999))


# Create your models here.
class Appointment(models.Model):
    date = models.DateTimeField()
    name = models.CharField('Enter your first name:', max_length=120)
    key = models.CharField(max_length=5, default=random_string)
    date_selected = models.DateTimeField(default=timezone.now)
    # Argument 'on_delete=models.CASCADE' - when User will be deleted, his post will be deleted too.
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)
    choice = models.CharField(max_length=120)

    def __str__(self):
        return str(self.author)

    class Meta:
        # Name on the admin page.
        verbose_name_plural = 'Appointments'


