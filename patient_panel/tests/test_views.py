from datetime import datetime

from django.test import TestCase, Client
from django.urls import reverse

from appointments.models import Appointment
from users.models import User, Office


class TestAppointmentViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.upcoming_appointments_list_url = reverse('patient-appointment-upcoming')
        self.old_appointments_list_url = reverse('patient-appointment-old')
        self.update_appointment_url = reverse('patient-appointment-change', args=[1])
        self.delete_appointment_url = reverse('patient-appointment-cancel', args=[1])
        self.patient1 = User.objects.create_user(
            'patient', 'patient@gmail.com', 'patientpassword', is_patient=True
        )
        self.office1 = User.objects.create_user(
            'office', 'office@gmail.com', 'officepassword', is_office=True
        )
        self.appointment_office1 = Office.objects.create(
            user=self.office1,
            name='name',
            address='address',
            city='City',
            phone_number='000000000',
            website='www.website.com'
        )
        self.appointment1 = Appointment.objects.create(
            owner=self.patient1,
            office=self.appointment_office1,
            date=datetime(2012, 1, 13, 16, 00, 00),
            name='name',
            date_selected=datetime(2012, 1, 13, 23, 51, 34),
            phone_number='000000000',
            confirmed=False,
            choice='Konsultacja'
        )

    def test_upcoming_appointment_list_GET_not_logged_in(self):
        response = self.client.get(self.upcoming_appointments_list_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'patient_panel/appointments_upcoming.html')

    def test_upcoming_appointment_list_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.upcoming_appointments_list_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'patient_panel/appointments_upcoming.html')

    def test_upcoming_appointment_list_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.upcoming_appointments_list_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'patient_panel/appointments_upcoming.html')

    def test_old_appointment_list_GET_not_logged_in(self):
        response = self.client.get(self.old_appointments_list_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'patient_panel/appointments_old.html')

    def test_old_appointment_list_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.old_appointments_list_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'patient_panel/appointments_old.html')

    def test_old_appointment_list_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.old_appointments_list_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'patient_panel/appointments_old.html')

    def test_update_appointment_GET_not_logged_in(self):
        response = self.client.get(self.update_appointment_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'patient_panel/appointment_update_form.html')

    def test_update_appointment_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.update_appointment_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'patient_panel/appointment_update_form.html')

    def test_update_appointment_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.update_appointment_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'patient_panel/appointment_update_form.html')

    def test_update_appointment_POST(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        url = reverse('patient-appointment-change', args=[1])
        response = self.client.post(url, {
            'date': '17.02.2020 17:00',
            'name': self.appointment1.name,
            'phone_number': '111111111',
            'choice': self.appointment1.choice
        })
        appointment_update = Appointment.objects.get(id=1)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(appointment_update.confirmed, False)
        self.assertEquals(appointment_update.phone_number, '111111111')

    def test_delete_appointment_GET_not_logged_in(self):
        response = self.client.get(self.delete_appointment_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'patient_panel/appointment_cancel_confirm.html')

    def test_delete_appointment_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.delete_appointment_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'patient_panel/appointment_cancel_confirm.html')

    def test_delete_appointment_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.delete_appointment_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'patient_panel/appointment_cancel_confirm.html')

    def test_delete_appointment_POST(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        url = reverse('patient-appointment-cancel', args=[1])
        response_with_post = self.client.get(self.delete_appointment_url)
        self.assertEquals(response_with_post.status_code, 200)
        response = self.client.post(url)
        response_with_deleted_post = self.client.get(self.update_appointment_url)
        self.assertEquals(response_with_deleted_post.status_code, 404)


class TestHomeViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.home_url = reverse('patient-home')
        self.patient1 = User.objects.create_user(
            'patient', 'patient@gmail.com', 'patientpassword', is_patient=True
        )
        self.office1 = User.objects.create_user(
            'office', 'office@gmail.com', 'officepassword', is_office=True
        )

    def test_home_GET_not_logged_in(self):
        response = self.client.get(self.home_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'patient_panel/patient_home.html')

    def test_home_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.home_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'patient_panel/patient_home.html')

    def test_home_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.home_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'patient_panel/patient_home.html')


class TestMedicalHistoryViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.medical_history_url = reverse('patient-medical-history')
        self.patient1 = User.objects.create_user(
            'patient', 'patient@gmail.com', 'patientpassword', is_patient=True
        )
        self.office1 = User.objects.create_user(
            'office', 'office@gmail.com', 'officepassword', is_office=True
        )

    def test_medical_history_GET_not_logged_in(self):
        response = self.client.get(self.medical_history_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'patient_panel/patient_medical_history.html')

    def test_medical_history_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.medical_history_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'patient_panel/patient_medical_history.html')

    def test_medical_history_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.medical_history_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'patient_panel/patient_medical_history.html')


class TestOfficesViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.patient_offices_url = reverse('patient-offices')
        self.patient1 = User.objects.create_user(
            'patient', 'patient@gmail.com', 'patientpassword', is_patient=True
        )
        self.office1 = User.objects.create_user(
            'office', 'office@gmail.com', 'officepassword', is_office=True
        )

    def test_offices_GET_not_logged_in(self):
        response = self.client.get(self.patient_offices_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'patient_panel/patient_office.html')

    def test_offices_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.patient_offices_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'patient_panel/patient_office.html')

    def test_offices_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.patient_offices_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'patient_panel/patient_office.html')
