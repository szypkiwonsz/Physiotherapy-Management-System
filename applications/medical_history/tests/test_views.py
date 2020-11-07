from datetime import datetime

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from applications.medical_history.models import MedicalHistory
from applications.office_panel.models import Patient
from applications.users.models import User, Office
from applications.appointments.models import Appointment


class TestOfficeMedicalHistoryViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.medical_history_url = reverse('office_panel:medical_history:list')
        self.make_medical_history_url = reverse('office_panel:medical_history:make')
        self.detail_medical_history_url = reverse('office_panel:medical_history:detail', args=[1])
        self.update_medical_history_url = reverse('office_panel:medical_history:update', args=[1])
        self.delete_medical_history_url = reverse('office_panel:medical_history:delete', args=[1])
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

    def test_medical_history_list_GET_not_logged_in(self):
        response = self.client.get(self.medical_history_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'medical_history/office/medical_history.html')

    def test_medical_history_list_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.medical_history_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'medical_history/office/medical_history.html')

    def test_medical_history_list_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.medical_history_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'medical_history/office/medical_history.html')

    def test_make_medical_history_create_GET_not_logged_in(self):
        response = self.client.get(self.make_medical_history_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'medical_history/office/medical_history_detail_form.html')

    def test_make_medical_history_create_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.make_medical_history_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'medical_history/office/medical_history_detail_form.html')

    def test_make_medical_history_create_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.make_medical_history_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'medical_history/office/medical_history_detail_form.html')

    def test_make_medical_history_create_POST(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.post(self.make_medical_history_url, {
            'patient': self.office_patient1.pk,
            'appointment': self.appointment1.pk,
            'description': 'description',
            'recommendations': 'recommendations'
        })
        medical_history2 = MedicalHistory.objects.get(id=2)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(medical_history2.description, 'description')

    def test_medical_history_detail_GET_not_logged_in(self):
        response = self.client.get(self.detail_medical_history_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'medical_history/office/medical_history_detail_form.html')

    def test_medical_history_detail_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.detail_medical_history_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'medical_history/office/medical_history_detail_form.html')

    def test_medical_history_detail_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.detail_medical_history_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'medical_history/office/medical_history_detail_form.html')

    def test_medical_history_update_GET_not_logged_in(self):
        response = self.client.get(self.update_medical_history_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'medical_history/office/medical_history_update_form.html')

    def test_medical_history_update_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.update_medical_history_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'medical_history/office/medical_history_update_form.html')

    def test_medical_history_update_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.update_medical_history_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'medical_history/office/medical_history_update_form.html')

    def test_medical_history_update_POST(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.post(self.update_medical_history_url, {
            'patient': self.medical_history1.patient.pk,
            'appointment': self.appointment1.pk,
            'description': self.medical_history1.description,
            'recommendations': 'newrecommendations'
        })
        medical_history_update = MedicalHistory.objects.get(id=1)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(medical_history_update.recommendations, 'newrecommendations')

    def test_medical_history_delete_GET_not_logged_in(self):
        response = self.client.get(self.delete_medical_history_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'medical_history/office/medical_history_delete_confirm.html')

    def test_medical_history_delete_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.delete_medical_history_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'medical_history/office/medical_history_delete_confirm.html')

    def test_medical_history_delete_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.delete_medical_history_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'medical_history/office/medical_history_delete_confirm.html')

    def test_medical_history_delete_POST(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response_with_post = self.client.get(self.detail_medical_history_url)
        self.assertEquals(response_with_post.status_code, 200)
        response = self.client.post(self.delete_medical_history_url)
        response_with_deleted_post = self.client.get(self.detail_medical_history_url)
        self.assertEquals(response_with_deleted_post.status_code, 404)


class TestPatientMedicalHistoryViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.medical_history_url = reverse('patient_panel:medical_history:list')
        self.patient1 = User.objects.create_user(
            'patient', 'patient@gmail.com', 'patientpassword', is_patient=True
        )
        self.office1 = User.objects.create_user(
            'office', 'office@gmail.com', 'officepassword', is_office=True
        )

    def test_medical_history_GET_not_logged_in(self):
        response = self.client.get(self.medical_history_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'medical_history/patient/medical_history.html')

    def test_medical_history_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.medical_history_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'medical_history/patient/medical_history.html')

    def test_medical_history_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.medical_history_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'medical_history/patient/medical_history.html')
