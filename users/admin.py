from django.contrib import admin

from office_panel.models import Patient
from .models import User, Office, Profile

admin.site.register(User)
admin.site.register(Patient)
admin.site.register(Office)
admin.site.register(Profile)
