from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

from applications.office_panel.models import Patient
from applications.users.models import User, Office

numeric = RegexValidator('^[0-9]*$', 'Jako numer telefonu, możesz podać jedynie cyfry.')
alphanumeric = RegexValidator('^[A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ]*$', 'Twoje imię nie może zawierać cyfr.')


# Create your models here.
class Appointment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    date = models.DateTimeField()
    name = models.CharField(max_length=120, validators=[alphanumeric])
    date_selected = models.DateTimeField(default=timezone.now)
    phone_number = models.CharField(max_length=9, validators=[numeric])
    confirmed = models.BooleanField(default=False)
    choice = models.CharField(max_length=120)

    def __str__(self):
        return str(self.owner)

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        super(Appointment, self).save(*args, **kwargs)

    class Meta:
        # Name on the admin page.
        verbose_name_plural = 'Appointments'
