from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

from applications.users.models import User

numeric_phone_number = RegexValidator('^[0-9]*$', 'Jako numer telefonu, możesz podać jedynie cyfry.')
numeric_pesel = RegexValidator('^[0-9]*$', 'Jako pesel, możesz podać jedynie cyfry.')
alphanumeric_first_name = RegexValidator(
    '^[A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ]*$', 'Imię nie może zawierać cyfr, ani znaków specjalnych'
)
alphanumeric_last_name = RegexValidator(
    '^[A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ]*$', 'Nazwisko nie może zawierać cyfr, ani znaków specjalnych.'
)


class Patient(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patients')
    first_name = models.CharField(max_length=20, unique=False, default='', validators=[alphanumeric_first_name])
    last_name = models.CharField(max_length=40, unique=False, default='', validators=[alphanumeric_last_name])
    email = models.EmailField(unique=True, default='', error_messages={
        'unique': _('Pacjent z takim adresem email już istnieje.')
    })
    address = models.CharField(max_length=50)
    pesel = models.CharField(max_length=11, validators=[numeric_pesel])
    phone_number = models.CharField(max_length=9, validators=[numeric_phone_number])
    date_selected = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        super(Patient, self).save(*args, **kwargs)
