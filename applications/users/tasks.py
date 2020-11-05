from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from applications.users.tokens import account_activation_token
from applications.users.models import User


@shared_task
def activation_email(user_id, domain, user_email):
    subject = 'Fizjo-System - Aktywacja Konta'
    user = User.objects.get(pk=user_id)
    message = render_to_string('users/activate_email.html', {
        'user': user,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user_id)),
        'token': account_activation_token.make_token(user),
    })
    email = EmailMessage(
        subject, message, to=[user_email]
    )
    email.send()
