from django.db.models.signals import post_save
from django.dispatch import receiver

from applications.users.models import Profile, Office, OfficeDay
from applications.users.models import User


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=Office)
def create_office_day(sender, instance, created, **kwargs):
    if created:
        OfficeDay.objects.create(office=instance, day=0)
        OfficeDay.objects.create(office=instance, day=1)
        OfficeDay.objects.create(office=instance, day=2)
        OfficeDay.objects.create(office=instance, day=3)
        OfficeDay.objects.create(office=instance, day=4)
        OfficeDay.objects.create(office=instance, day=5)
        OfficeDay.objects.create(office=instance, day=6)
