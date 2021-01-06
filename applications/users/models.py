import calendar

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext as _
from easy_thumbnails.fields import ThumbnailerImageField

from applications.users.utils import get_days_of_week, get_hours_in_day


class User(AbstractUser):
    """User model with the possibility of registration as an office or patient."""
    is_patient = models.BooleanField(default=False)
    is_office = models.BooleanField(default=False)

    username = models.CharField(max_length=40, unique=False, default='')
    email = models.EmailField(unique=True, error_messages={
        'unique': _("Użytkownik z takim adresem email już istnieje.")
    })

    # replacing username by email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class UserPatient(models.Model):
    """Patient model that can be assigned to a user"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=9)

    def __str__(self):
        return self.user.email


class UserOffice(models.Model):
    """Office model that can be assigned to a user"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=9)
    website = models.CharField(max_length=20)
    appointment_time_interval = models.PositiveIntegerField(
        default=20, validators=[MinValueValidator(10), MaxValueValidator(60)]
    )

    def __str__(self):
        return self.user.email

    class Meta:
        # name on the admin page
        verbose_name_plural = 'User offices'


class OfficeDay(models.Model):
    """A model to determine the times of making an appointment in the office for a given day."""
    DAY_CHOICES = get_days_of_week()
    HOUR_CHOICES = get_hours_in_day()

    office = models.ForeignKey(UserOffice, on_delete=models.CASCADE, related_name='office_days')
    day = models.CharField(max_length=1, choices=DAY_CHOICES)
    earliest_appointment_time = models.CharField(max_length=5, choices=HOUR_CHOICES, default='11:00')
    latest_appointment_time = models.CharField(max_length=5, choices=HOUR_CHOICES, default='18:00')

    def save(self, *args, **kwargs):
        self.validate_hours()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.office.name} - {calendar.day_name[int(self.day)]}'

    def validate_hours(self):
        if self.earliest_appointment_time > self.latest_appointment_time:
            raise ValidationError(
                'The closing hour must be greater than the opening hour.',
                params={'opening_hour': self.earliest_appointment_time, 'closing_hour': self.latest_appointment_time}
            )


class Profile(models.Model):
    """User profile model."""
    CROP_SETTINGS = {'size': (100, 100), 'crop': 'smart'}

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = ThumbnailerImageField(default='default.jpg', upload_to='profile_pics', resize_source=CROP_SETTINGS)

    def __str__(self):
        return self.user.email
