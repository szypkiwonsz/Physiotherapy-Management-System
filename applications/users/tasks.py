from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from applications.users.models import User
from applications.users.tokens import account_activation_token


@shared_task
def send_activation_email(user_id, domain, user_email):
    """
    A celery task that sends an email with an activation link after registering a user.
    :param user_id: <int> -> id of user registered
    :param domain: <str> -> domain
    :param user_email: <string> -> Registered user's email
    :return: None
    """
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
