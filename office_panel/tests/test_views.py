from datetime import datetime

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from appointments.models import Appointment
from medical_history.models import MedicalHistory
from office_panel.models import Patient
from users.models import User, Office


class TestAppointmentViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.appointment_list_url = reverse('office-appointments')
        self.update_appointment_url = reverse('office-appointment-change', args=[1])
        self.delete_appointment_url = reverse('office-appointment-delete', args=[1])
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
        url = reverse('office-appointment-change', args=[1])
        response = self.client.post(url, {
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

    def test_medical_history_delete_POST(self):
        url = reverse('office-appointment-delete', args=[1])
        self.client.login(username='office@gmail.com', password='officepassword')
        response_with_post = self.client.get(self.delete_appointment_url)
        self.assertEquals(response_with_post.status_code, 200)
        response = self.client.post(url)
        response_with_deleted_post = self.client.get(self.update_appointment_url)
        self.assertEquals(response_with_deleted_post.status_code, 404)


class TestHomeViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.office_home_url = reverse('office-home')
        self.patient1 = User.objects.create_user(
            'patient', 'patient@gmail.com', 'patientpassword', is_patient=True
        )
        self.office1 = User.objects.create_user(
            'office', 'office@gmail.com', 'officepassword', is_office=True
        )

    def test_office_home_GET_not_logged_in(self):
        response = self.client.get(self.office_home_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'office_panel/office_home.html')

    def test_office_home_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.office_home_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'office_panel/office_home.html')

    def test_office_home_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.office_home_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'office_panel/office_home.html')


class TestMedicalHistoryViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.medical_history_url = reverse('office-medical-history')
        self.make_medical_history_url = reverse('office-make-medical-history')
        self.detail_medical_history_url = reverse('office-medical-history-detail', args=[1])
        self.update_medical_history_url = reverse('office-medical-history-change', args=[1])
        self.delete_medical_history_url = reverse('office-medical-history-delete', args=[1])
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
            email='patient@gmail.com'
        )
        self.medical_history1 = MedicalHistory.objects.create(
            owner=self.office1,
            patient=self.office_patient1,
            description='description',
            recommendations='recommendations',
            date_selected=timezone.now(),
        )

    def test_medical_history_list_GET_not_logged_in(self):
        response = self.client.get(self.medical_history_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'office_panel/office_medical_history.html')

    def test_medical_history_list_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.medical_history_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'office_panel/office_medical_history.html')

    def test_medical_history_list_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.medical_history_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'office_panel/office_medical_history.html')

    def test_make_medical_history_create_GET_not_logged_in(self):
        response = self.client.get(self.make_medical_history_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'medical_history/medical_history_detail_form.html')

    def test_make_medical_history_create_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.make_medical_history_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'medical_history/medical_history_detail_form.html')

    def test_make_medical_history_create_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.make_medical_history_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'medical_history/medical_history_detail_form.html')

    def test_make_medical_history_create_POST(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        url = reverse('office-make-medical-history')
        response = self.client.post(url, {
            'patient': Patient.objects.get(id=1).pk,
            'description': 'description',
            'recommendations': 'recommendations'
        })
        medical_history2 = MedicalHistory.objects.get(id=2)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(medical_history2.description, 'description')

    def test_medical_history_detail_GET_not_logged_in(self):
        response = self.client.get(self.detail_medical_history_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'medical_history/medical_history_detail_form.html')

    def test_medical_history_detail_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.detail_medical_history_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'medical_history/medical_history_detail_form.html')

    def test_medical_history_detail_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.detail_medical_history_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'medical_history/medical_history_detail_form.html')

    def test_medical_history_update_GET_not_logged_in(self):
        response = self.client.get(self.update_medical_history_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'medical_history/medical_history_update_form.html')

    def test_medical_history_update_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.update_medical_history_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'medical_history/medical_history_update_form.html')

    def test_medical_history_update_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.update_medical_history_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'medical_history/medical_history_update_form.html')

    def test_medical_history_update_POST(self):
        url = reverse('office-medical-history-change', args=[1])
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.post(url, {
            'patient': self.medical_history1.patient.pk,
            'description': self.medical_history1.description,
            'recommendations': 'newrecommendations'
        })
        medical_history_update = MedicalHistory.objects.get(id=1)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(medical_history_update.recommendations, 'newrecommendations')

    def test_medical_history_delete_GET_not_logged_in(self):
        response = self.client.get(self.delete_medical_history_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'medical_history/medical_history_delete_confirm.html')

    def test_medical_history_delete_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.delete_medical_history_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'medical_history/medical_history_delete_confirm.html')

    def test_medical_history_delete_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.delete_medical_history_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'medical_history/medical_history_delete_confirm.html')

    def test_medical_history_delete_POST(self):
        url = reverse('office-medical-history-delete', args=[1])
        self.client.login(username='office@gmail.com', password='officepassword')
        response_with_post = self.client.get(self.detail_medical_history_url)
        self.assertEquals(response_with_post.status_code, 200)
        response = self.client.post(url)
        response_with_deleted_post = self.client.get(self.detail_medical_history_url)
        self.assertEquals(response_with_deleted_post.status_code, 404)


class TestPatientViews(TestCase):

    def setUp(self):
        self.patient_url = reverse('office-patients')
        self.create_patient_url = reverse('office-patient-add')
        self.detail_patient_url = reverse('office-patient-detail', args=[1])
        self.update_patient_url = reverse('office-patient-change', args=[1])
        self.delete_patient_url = reverse('office-patient-delete-confirm', args=[1])
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

    def test_patient_list_GET_not_logged_in(self):
        response = self.client.get(self.patient_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'office_panel/office_patients.html')

    def test_patient_list_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.patient_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'office_panel/office_patients.html')

    def test_patient_list_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.patient_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'office_panel/office_patients.html')

    def test_patient_create_GET_not_logged_in(self):
        response = self.client.get(self.create_patient_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'office_panel/patient_add_form.html')

    def test_patient_create_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.create_patient_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'office_panel/patient_add_form.html')

    def test_patient_create_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.create_patient_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'office_panel/patient_add_form.html')

    def test_patient_create_POST(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        url = reverse('office-patient-add')
        response = self.client.post(url, {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'patient2@gmail.com'
        })
        office_patient2 = Patient.objects.get(id=2)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(office_patient2.first_name, 'Firstname')

    def test_patient_detail_GET_no_logged_in(self):
        response = self.client.get(self.detail_patient_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'office_panel/patient_detail_form.html')

    def test_patient_detail_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.detail_patient_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'office_panel/patient_detail_form.html')

    def test_patient_detail_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.detail_patient_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'office_panel/patient_detail_form.html')

    def test_patient_update_GET_no_logged_in(self):
        response = self.client.get(self.update_patient_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'office_panel/patient_update_form.html')

    def test_patient_update_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.update_patient_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'office_panel/patient_update_form.html')

    def test_patient_update_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.update_patient_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'office_panel/patient_update_form.html')

    def test_patient_update_POST(self):
        url = reverse('office-patient-change', args=[1])
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.post(url, {
            'first_name': self.office_patient1.first_name,
            'last_name': self.office_patient1.last_name,
            'email': 'newpatientemail@gmail.com'
        })
        office_patient_update = Patient.objects.get(id=1)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(office_patient_update.email, 'newpatientemail@gmail.com')

    def test_patient_delete_GET_not_logged_in(self):
        response = self.client.get(self.delete_patient_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'office_panel/patient_delete_confirm.html')

    def test_patient_delete_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.delete_patient_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'office_panel/patient_delete_confirm.html')

    def test_patient_delete_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.delete_patient_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'office_panel/patient_delete_confirm.html')

    def test_patient_delete_POST(self):
        url = reverse('office-patient-delete-confirm', args=[1])
        self.client.login(username='office@gmail.com', password='officepassword')
        response_with_post = self.client.get(self.delete_patient_url)
        self.assertEquals(response_with_post.status_code, 200)
        response = self.client.post(url)
        response_with_deleted_post = self.client.get(self.delete_patient_url)
        self.assertEquals(response_with_deleted_post.status_code, 404)
