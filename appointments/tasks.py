from django.core.mail import EmailMessage
from celery import shared_task
from utils.date_time import DateTime


@shared_task
def appointment_confirmation_office(patient_name, date, time, office_email):
    hour = time[0]
    minute = time[1]
    day = date[2]
    month = date[1]
    year = date[0]
    subject = 'Fizjo-System - Nowa Wizyta'
    message = f'\nPacjent {patient_name} umówił wizytę w twoim gabinecie na godzinę {hour}:' \
              f'{minute} dnia {day}.{month}.' \
              f'{year}.\n\n' \
              'Potwierdź wizytę pacjenta logując się do panelu swojego gabinetu.\n\n' \
              'Fizjo-System'
    email = EmailMessage(subject, message, to=[office_email])
    email.send()


@shared_task
def appointment_confirmation_patient(patient_name, office_name, date, time, patient_email):
    hour = time[0]
    minute = time[1]
    day = date[2]
    month = date[1]
    year = date[0]
    subject = 'Fizjo-System - Umówiono Wizytę'
    message = f'\nWitaj {patient_name},\n\n' \
              f'Twoja wizyta umówiona na godzinę {hour}:' \
              f'{minute} dnia {day}.{DateTime.add_zero(month)}.' \
              f'{year} w gabinecie {office_name} oczekuje na potwierdzenie.\n' \
              f'Potwierdzenie wizyty ze strony gabinetu otrzymasz w kolejnym mailu.\n\n' \
              'Jeśli chcesz odwołać wizytę, skorzystaj z opcji odwołaj znajdującej się w panelu pacjenta.\n\n' \
              'Fizjo-System'
    email = EmailMessage(subject, message, to=[patient_email])
    email.send()
