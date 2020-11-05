from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _
from easy_thumbnails.fields import ThumbnailerImageField


class User(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_office = models.BooleanField(default=False)

    username = models.CharField(max_length=40, unique=False, default='')
    email = models.EmailField(unique=True, error_messages={
        'unique': _("Użytkownik z takim adresem email już istnieje.")
    })

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class UserPatient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=9)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name_plural = 'UserPatient'


class Office(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=9)
    website = models.CharField(max_length=20)

    def __str__(self):
        return self.user.email


class Profile(models.Model):
    CROP_SETTINGS = {'size': (100, 100), 'crop': 'smart'}

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = ThumbnailerImageField(default='default.jpg', upload_to='profile_pics', resize_source=CROP_SETTINGS)

    def __str__(self):
        return self.user.email

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #
    #     img = Image.open(self.image.path)
    #
    #     if img.height > 100 or img.width > 100:
    #         output_size = (100, 100)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)
    #         img.close()
