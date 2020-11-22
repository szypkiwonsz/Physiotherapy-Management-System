from datetime import datetime

from django.test import TestCase, Client
from django.urls import reverse

from applications.appointments.models import Appointment
from applications.office_panel.models import Patient
from applications.users.models import User, Office


class TestOfficeAppointmentViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.appointment_list_url = reverse('office_panel:appointments:list')
        self.make_appointment_url = reverse('office_panel:appointments:make', args=[2])
        self.update_appointment_url = reverse('office_panel:appointments:update', args=[1])
        self.delete_appointment_url = reverse('office_panel:appointments:delete', args=[1])
        self.patient1 = User.objects.create_user(
            'patient', 'patient@gmail.com', 'patientpassword', is_patient=True
        )
        self.office1 = User.objects.create_user(
            'office', 'office@gmail.com', 'officepassword', is_office=True
        )
        self.office_patient1 = Patient.objects.create(
            owner=self.office1,
            first_name='firstname',
            last_name='lastname',
            email='patient@gmail.com',
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
            patient_email='patient@gmail.com',
            date=datetime(2012, 1, 13, 16, 00, 00),
            first_name='Kacper',
            last_name='Sawicki',
            date_selected=datetime(2012, 1, 13, 23, 51, 34),
            phone_number='000000000',
            confirmed=False,
            choice='Konsultacja'
        )

    def test_appointment_list_GET_not_logged_in(self):
        response = self.client.get(self.appointment_list_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/office_appointments.html')

    def test_appointment_list_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.appointment_list_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/office_appointments.html')

    def test_appointment_list_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.appointment_list_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointments/office/appointments.html')

    def test_appointment_update_GET_not_logged_in(self):
        response = self.client.get(self.update_appointment_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/office/appointment_update_form.html')

    def test_appointment_update_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.update_appointment_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/office_appointment_update_form.html')

    def test_appointment_update_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.update_appointment_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointments/office/appointment_update_form.html')

    def test_appointment_update_POST(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.post(self.update_appointment_url, {
            'date': '17.02.2020 17:00',
            'confirmed': True
        })
        appointment_update = Appointment.objects.get(id=1)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(appointment_update.confirmed, True)

    def test_appointment_delete_GET_not_logged_in(self):
        response = self.client.get(self.delete_appointment_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/office/appointment_delete_confirm.html')

    def test_appointment_delete_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.delete_appointment_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/office/appointment_delete_confirm.html')

    def test_appointment_delete_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.delete_appointment_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointments/office/appointment_delete_confirm.html')

    def test_appointment_delete_POST(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response_with_post = self.client.get(self.delete_appointment_url)
        self.assertEquals(response_with_post.status_code, 200)
        response = self.client.post(self.delete_appointment_url)
        response_with_deleted_post = self.client.get(self.update_appointment_url)
        self.assertEquals(response_with_deleted_post.status_code, 404)

    def test_make_appointment_create_GET_not_logged_in(self):
        response = self.client.get(self.make_appointment_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/office_panel/appointment_make_form.html')

    def test_make_appointment_create_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.make_appointment_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/office_panel/appointment_make_form.html')

    """How to test with request.GET -> appointments.views.office (line 122)"""
    # def test_make_appointment_create_GET_logged_as_office(self):
    #     self.client.login(username='office@gmail.com', password='officepassword')
    #     response = self.client.get(self.make_appointment_url)
    #
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'appointments/office_panel/appointment_make_form.html')
    #
    # def test_make_appointment_create_POST(self):
    #     self.client.login(username='office@gmail.com', password='officepassword')
    #     response = self.client.post(self.make_appointment_url, {
    #         'choice': 'Konsultacja',
    #         'patient': self.office_patient1,
    #     })
    #     appointment2 = Appointment.objects.get(id=3)
    #     self.assertEquals(appointment2.date, datetime(1998, 2, 17, 17, 00, 00))
    #     self.assertEquals(appointment2.office_id, 2)
    #     self.assertEquals(appointment2.confirmed, False)
    #     self.assertEquals(appointment2.first_name, 'firstname')


class TestPatientAppointmentViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.select_office_url = reverse('patient_panel:appointments:select')
        self.make_appointment_url = reverse('patient_panel:appointments:make', args=[2])
        self.upcoming_appointments_list_url = reverse('patient_panel:appointments:upcoming')
        self.old_appointments_list_url = reverse('patient_panel:appointments:old')
        self.update_appointment_url = reverse('patient_panel:appointments:update', args=[1])
        self.delete_appointment_url = reverse('patient_panel:appointments:delete', args=[1])
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
            patient_email='patient@gmail.com',
            date=datetime(2012, 1, 13, 16, 00, 00),
            first_name='Kacper',
            last_name='Sawicki',
            date_selected=datetime(2012, 1, 13, 23, 51, 34),
            phone_number='000000000',
            confirmed=False,
            choice='Konsultacja'
        )
        self.appointment2 = Appointment.objects.create(
            owner=self.patient1,
            office=self.appointment_office1,
            patient_email='patient@gmail.com',
            date=datetime(2018, 1, 13, 16, 00, 00),
            first_name='Kacper',
            last_name='Sawicki',
            date_selected=datetime(2018, 1, 13, 23, 51, 34),
            phone_number='000000000',
            confirmed=False,
            choice='Konsultacja'
        )

    def test_select_office_GET_not_logged_in(self):
        response = self.client.get(self.select_office_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/patient/appointment_select_office.html')

    def test_select_office_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.select_office_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointments/patient/appointment_select_office.html')

    def test_select_office_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.select_office_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/patient/appointment_select_office.html')

    def test_make_appointment_create_GET_not_logged_in(self):
        response = self.client.get(self.make_appointment_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/patient/appointment_make_form.html')

    def test_make_appointment_create_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.make_appointment_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointments/patient/appointment_make_form.html')

    def test_make_appointment_create_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.make_appointment_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/patient/appointment_make_form.html')

    def test_make_appointment_create_POST(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.post(self.make_appointment_url, {
            'date': '17.02.1998 17:00',
            'first_name': self.appointment1.first_name,
            'last_name': self.appointment1.last_name,
            'phone_number': '000000000',
            'choice': 'Konsultacja'
        })
        appointment2 = Appointment.objects.get(id=3)
        self.assertEquals(appointment2.date, datetime(1998, 2, 17, 17, 00, 00))
        self.assertEquals(appointment2.office_id, 2)
        self.assertEquals(appointment2.confirmed, False)

    def test_make_appointment_create_too_early_time_POST(self):
        # the default earliest time is: 11:00
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.post(self.make_appointment_url, {
            'date': '17.02.1998 08:00',
            'first_name': self.appointment1.first_name,
            'last_name': self.appointment1.last_name,
            'phone_number': '000000000',
            'choice': 'Konsultacja'
        })
        with self.assertRaises(Appointment.DoesNotExist):
            Appointment.objects.get(id=3)

    def test_make_appointment_create_too_late_time_POST(self):
        # the default latest time is 18:00
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.post(self.make_appointment_url, {
            'date': '17.02.1998 22:00',
            'first_name': self.appointment1.first_name,
            'last_name': self.appointment1.last_name,
            'phone_number': '000000000',
            'choice': 'Konsultacja'
        })
        with self.assertRaises(Appointment.DoesNotExist):
            Appointment.objects.get(id=3)

    def test_make_appointment_create_date_taken_POST(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.post(self.make_appointment_url, {
            'date': '13.01.2012 16:00',
            'first_name': self.appointment1.first_name,
            'last_name': self.appointment1.last_name,
            'phone_number': '000000000',
            'choice': 'Konsultacja'
        })
        with self.assertRaises(Appointment.DoesNotExist):
            Appointment.objects.get(id=3)

    def test_upcoming_appointment_list_GET_not_logged_in(self):
        response = self.client.get(self.upcoming_appointments_list_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/patient/appointments_upcoming.html')

    def test_upcoming_appointment_list_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.upcoming_appointments_list_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointments/patient/appointments_upcoming.html')

    def test_upcoming_appointment_list_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.upcoming_appointments_list_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/patient/appointments_upcoming.html')

    def test_old_appointment_list_GET_not_logged_in(self):
        response = self.client.get(self.old_appointments_list_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/patient/appointments_old.html')

    def test_old_appointment_list_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.old_appointments_list_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointments/patient/appointments_old.html')

    def test_old_appointment_list_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.old_appointments_list_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/patient/appointments_old.html')

    def test_update_appointment_GET_not_logged_in(self):
        response = self.client.get(self.update_appointment_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/patient/appointment_update_form.html')

    def test_update_appointment_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.update_appointment_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointments/patient/appointment_update_form.html')

    def test_update_appointment_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.update_appointment_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/patient/appointment_update_form.html')

    def test_update_appointment_POST(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.post(self.update_appointment_url, {
            'date': '17.02.2020 17:00',
            'first_name': self.appointment1.first_name,
            'last_name': self.appointment1.last_name,
            'phone_number': '111111111',
            'choice': self.appointment1.choice
        })
        appointment_update = Appointment.objects.get(id=1)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(appointment_update.confirmed, False)
        self.assertEquals(appointment_update.phone_number, '111111111')

    def test_update_appointment_date_taken_POST(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.post(self.update_appointment_url, {
            'date': '13.01.2018 16:00',
            'first_name': self.appointment1.first_name,
            'last_name': self.appointment1.last_name,
            'phone_number': '111111111',
            'choice': self.appointment1.choice
        })
        appointment_update = Appointment.objects.get(id=1)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(appointment_update.confirmed, False)
        self.assertEquals(appointment_update.phone_number, '000000000')

    def test_delete_appointment_GET_not_logged_in(self):
        response = self.client.get(self.delete_appointment_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/patient/appointment_cancel_confirm.html')

    def test_delete_appointment_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.delete_appointment_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointments/patient/appointment_cancel_confirm.html')

    def test_delete_appointment_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.delete_appointment_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/patient/appointment_cancel_confirm.html')

    def test_delete_appointment_POST(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response_with_post = self.client.get(self.delete_appointment_url)
        self.assertEquals(response_with_post.status_code, 200)
        response = self.client.post(self.delete_appointment_url)
        response_with_deleted_post = self.client.get(self.update_appointment_url)
        self.assertEquals(response_with_deleted_post.status_code, 404)
