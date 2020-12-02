from celery import shared_task
from django.core.mail import EmailMessage


@shared_task
def appointment_confirmation_email_office(patient_name, date, time, office_email):
    """
    Celery task that sends an email confirming the visit to the office.
    :param patient_name: <str> -> patient first name
    :param date: <str> -> date of appointment
    :param time: <str> -> hour time of appointment
    :param office_email: <str> -> office email
    """
    subject = 'Fizjo-System - Nowa Wizyta'
    message = f'\nPacjent {patient_name} umówił wizytę w twoim gabinecie na godzinę {time} dnia {date}.\n\n' \
              'Potwierdź wizytę pacjenta logując się do panelu swojego gabinetu.\n\n' \
              'Fizjo-System'
    email = EmailMessage(subject, message, to=[office_email])
    email.send()


@shared_task
def appointment_confirmation_email_patient(patient_name, office_name, date, time, patient_email):
    """
    Celery task that sends an email confirming the visit to the patient.
    :param patient_name: <str> -> patient first name
    :param office_name: <str> -> name of the office
    :param date: <str> -> date of appointment
    :param time: <str> -> hour time of appointment
    :param patient_email: <str> -> patient email
    """
    subject = 'Fizjo-System - Umówiono Wizytę'
    message = f'\nWitaj {patient_name},\n\n' \
              f'Twoja wizyta umówiona na godzinę {time} dnia {date} w gabinecie {office_name} ' \
              f'oczekuje na potwierdzenie.\n' \
              f'Potwierdzenie wizyty ze strony gabinetu otrzymasz w kolejnym mailu.\n\n' \
              'Jeśli chcesz odwołać wizytę, skorzystaj z opcji odwołaj znajdującej się w panelu pacjenta.\n\n' \
              'Fizjo-System'
    email = EmailMessage(subject, message, to=[patient_email])
    email.send()
