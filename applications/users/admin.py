from django.contrib import admin

from applications.users.models import User, Office, Profile, UserPatient

admin.site.register(User)
admin.site.register(UserPatient)
admin.site.register(Office)
admin.site.register(Profile)