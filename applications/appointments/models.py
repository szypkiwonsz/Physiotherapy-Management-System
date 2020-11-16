from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

from applications.office_panel.models import Patient
from applications.users.models import User, Office

numeric = RegexValidator('^[0-9]*$', 'Jako numer telefonu, możesz podać jedynie cyfry.')
alphanumeric_first_name = RegexValidator(
    '^[A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ]*$', 'Imię nie może zawierać cyfr, ani znaków specjalnych'
)
alphanumeric_last_name = RegexValidator(
    '^[A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ]*$', 'Nazwisko nie może zawierać cyfr, ani znaków specjalnych.'
)


# Create your models here.
class Appointment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    patient_email = models.EmailField()
    first_name = models.CharField(max_length=20, unique=False, default='', validators=[alphanumeric_first_name])
    last_name = models.CharField(max_length=40, unique=False, default='', validators=[alphanumeric_last_name])
    date = models.DateTimeField()
    date_selected = models.DateTimeField(default=timezone.now)
    phone_number = models.CharField(max_length=9, validators=[numeric])
    confirmed = models.BooleanField(default=False)
    choice = models.CharField(max_length=120)

    def __str__(self):
        return str(self.owner)

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        super(Appointment, self).save(*args, **kwargs)

    class Meta:
        # Name on the admin page.
        verbose_name_plural = 'Appointments'
