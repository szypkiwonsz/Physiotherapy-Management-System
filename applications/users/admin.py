from django.contrib import admin

from applications.appointments.models import Service
from applications.users.models import User, Profile, UserPatient, OfficeDay, UserOffice

admin.site.register(User)
admin.site.register(UserPatient)
admin.site.register(UserOffice)
admin.site.register(Profile)
admin.site.register(OfficeDay)
