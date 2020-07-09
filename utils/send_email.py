from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from users.tokens import account_activation_token
from utils.date_time import DateTime


def appointment_confirmation_office(patient_name, date, office_email):
    subject = 'Fizjo-System - Nowa Wizyta'
    message = f'\nPacjent {patient_name} umówił wizytę w twoim gabinecie na godzinę {DateTime.add_zero(date.hour)}:' \
              f'{DateTime.add_zero(date.minute)} dnia {DateTime.add_zero(date.day)}.{DateTime.add_zero(date.month)}.' \
              f'{DateTime.add_zero(date.year)}.\n\n' \
              'Potwierdź wizytę pacjenta logując się do panelu swojego gabinetu.\n\n' \
              'Fizjo-System'
    email = EmailMessage(subject, message, to=[office_email])
    email.send()


def appointment_confirmation_patient(patient_name, office_name, date, patient_email):
    subject = 'Fizjo-System - Umówiono Wizytę'
    message = f'\nWitaj {patient_name},\n\n' \
              f'Twoja wizyta umówiona na godzinę {DateTime.add_zero(date.hour)}:' \
              f'{DateTime.add_zero(date.minute)} dnia {DateTime.add_zero(date.day)}.{DateTime.add_zero(date.month)}.' \
              f'{DateTime.add_zero(date.year)} w gabinecie {office_name} oczekuje na potwierdzenie.\n' \
              f'Potwierdzenie wizyty ze strony gabinetu otrzymasz w kolejnym mailu.\n\n' \
              'Jeśli chcesz odwołać wizytę, skorzystaj z opcji odwołaj znajdującej się w panelu pacjenta.\n\n' \
              'Fizjo-System'
    email = EmailMessage(subject, message, to=[patient_email])
    email.send()


def activation_email(user, current_site, user_email):
    subject = 'Fizjo-System - Aktywacja Konta'
    message = render_to_string('users/activate_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    email = EmailMessage(
        subject, message, to=[user_email]
    )
    email.send()
