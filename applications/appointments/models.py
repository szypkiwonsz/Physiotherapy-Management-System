import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from applications.office_panel.models import Patient
from applications.users.models import User, UserOffice
from utils.regex_validators import alphanumeric_first_name, numeric_phone_number, alphanumeric_last_name


# Create your models here.
class Appointment(models.Model):
    """Appointment model for the office."""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='services', blank=True, null=True)
    office = models.ForeignKey(UserOffice, on_delete=models.CASCADE)
    patient_email = models.EmailField()
    first_name = models.CharField(max_length=20, unique=False, default='', validators=[alphanumeric_first_name()])
    last_name = models.CharField(max_length=40, unique=False, default='', validators=[alphanumeric_last_name()])
    date = models.DateTimeField()
    date_end = models.DateTimeField()
    date_selected = models.DateTimeField(default=timezone.now)
    phone_number = models.CharField(max_length=9, validators=[numeric_phone_number()])
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.date} - {self.first_name} {self.last_name}'

    def calculate_date_end(self):
        self.date_end = self.date + datetime.timedelta(minutes=int(self.service.duration))

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        self.calculate_date_end()
        super(Appointment, self).save(*args, **kwargs)

    class Meta:
        # name on the admin page
        verbose_name_plural = 'Appointments'


class Service(models.Model):
    """Service model for the office."""
    office = models.ForeignKey(UserOffice, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    duration = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.name}'

    def validate_unique(self, exclude=None):
        """Validate uniqueness service name per office."""
        qs = Service.objects.filter(office=self.office_id)
        if qs.filter(name=self.name).exists():
            raise ValidationError('Nazwa usługi musi być unikalna dla gabinetu.')

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(Service, self).save(*args, **kwargs)
