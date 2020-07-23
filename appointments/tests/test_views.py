from datetime import datetime

from dateutil.tz import UTC
from django.test import TestCase, Client
from django.urls import reverse

from appointments.models import Appointment
from users.models import User, Office


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.select_office_url = reverse('appointments-select')
        self.make_appointment_url = reverse('appointments-make-appointment', args=[1])
        self.patient1 = User.objects.create_user(
            'patient', 'patient@gmail.com', 'patientpassword', is_patient=True
        )
        self.office1 = User.objects.create_user(
            'office', 'office@gmail.com', 'officepassword', is_office=True
        )
        self.appointment_office1 = Office.objects.create(
            user=self.patient1,
            name='name',
            address='address',
            city='City',
            phone_number='000000000',
            website='www.website.com'
        )

    def test_select_office_GET_not_logged_in(self):
        response = self.client.get(self.select_office_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/patient_appointment_select_office.html')

    def test_select_office_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.select_office_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointments/patient_appointment_select_office.html')

    def test_select_office_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.select_office_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/patient_appointment_select_office.html')

    def test_make_appointment_create_GET_not_logged_in(self):
        response = self.client.get(self.make_appointment_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/patient_appointment_make_form.html')

    def test_make_appointment_create_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.make_appointment_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointments/patient_appointment_make_form.html')

    def test_make_appointment_create_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.make_appointment_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/patient_appointment_make_form.html')

    def test_make_appointment_create_POST(self):
        url = reverse('appointments-make-appointment', args=[1])
        Appointment.objects.create(
            owner=self.office1,
            office=self.appointment_office1,
            date=datetime(2012, 1, 13, 16, 00, 00),
            name='name',
            date_selected=datetime(2012, 1, 13, 23, 51, 34),
            phone_number='000000000',
            confirmed=False,
            choice='Konsultacja'
        )
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.post(url, {
            'date': '17.02.1998 17:00',
            'name': 'name',
            'phone_number': '000000000',
            'choice': 'Konsultacja'
        })
        appointment2 = Appointment.objects.get(id=2)
        self.assertEquals(appointment2.date, datetime(1998, 2, 17, 17, 00, 00, tzinfo=UTC))
        self.assertEquals(appointment2.office_id, 1)
        self.assertEquals(appointment2.confirmed, False)
