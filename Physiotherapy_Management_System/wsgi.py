"""
WSGI config for css project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

from Physiotherapy_Management_System import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Physiotherapy_Management_System.settings')

application = get_wsgi_application()
if not settings.DEBUG:
    application = WhiteNoise(application)
