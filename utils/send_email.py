from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from users.tokens import account_activation_token
from utils.date_time import DateTime


def appointment_confirmation_office(office_name, name, date, office_email):
    subject = 'Appointment - {}'.format(office_name)
    message = '{} was appointed for {}:{} on day {}.{}.{}. ' \
              'Confirm the visit in the admin panel.'.format(name, DateTime.add_zero(date.hour),
                                                             DateTime.add_zero(date.minute),
                                                             DateTime.add_zero(date.day),
                                                             DateTime.add_zero(date.month),
                                                             DateTime.add_zero(date.year))
    email = EmailMessage(subject, message, to=[office_email])
    email.send()


def appointment_confirmation_patient(date, patient_email):
    subject = 'Your appointments on fizjo-med has been correctly arranged'
    message = f'You have been correctly arranged to visit for {DateTime.add_zero(date.hour)}:' \
        f'{DateTime.add_zero(date.minute)} on day {DateTime.add_zero(date.day)}.' \
        f'{DateTime.add_zero(date.month)}.{DateTime.add_zero(date.year)}. ' \
        'If you want to cancel your visit, use the form on our website.'
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
    to_email = user_email
    email = EmailMessage(
        subject, message, to=[to_email]
    )
    email.send()
