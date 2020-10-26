from celery import shared_task
from django.core.mail import EmailMessage


@shared_task
def appointment_confirmation_email_office(patient_name, date, time, office_email):
    date = '.'.join(date)
    time = ':'.join(time[:2])
    subject = 'Fizjo-System - Nowa Wizyta'
    message = f'\nPacjent {patient_name} umówił wizytę w twoim gabinecie na godzinę {time} dnia {date}.\n\n' \
              'Potwierdź wizytę pacjenta logując się do panelu swojego gabinetu.\n\n' \
              'Fizjo-System'
    email = EmailMessage(subject, message, to=[office_email])
    email.send()


@shared_task
def appointment_confirmation_email_patient(patient_name, office_name, date, time, patient_email):
    date = '.'.join(date)
    time = ':'.join(time[:2])
    subject = 'Fizjo-System - Umówiono Wizytę'
    message = f'\nWitaj {patient_name},\n\n' \
              f'Twoja wizyta umówiona na godzinę {time} dnia {date} w gabinecie {office_name} ' \
              f'oczekuje na potwierdzenie.\n' \
              f'Potwierdzenie wizyty ze strony gabinetu otrzymasz w kolejnym mailu.\n\n' \
              'Jeśli chcesz odwołać wizytę, skorzystaj z opcji odwołaj znajdującej się w panelu pacjenta.\n\n' \
              'Fizjo-System'
    email = EmailMessage(subject, message, to=[patient_email])
    email.send()
