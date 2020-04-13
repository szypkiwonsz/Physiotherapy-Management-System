from django.contrib import admin
from .models import User, Patient, Office, Profile

# Register your models here.
admin.site.register(User)
admin.site.register(Patient)
admin.site.register(Office)
admin.site.register(Profile)
