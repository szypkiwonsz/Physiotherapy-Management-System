from django.test import TestCase, Client
from django.urls import reverse

from users.models import User


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
        self.assertTemplateNotUsed(response, 'patient_panel/home.html')

    def test_home_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.home_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'patient_panel/home.html')

    def test_home_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.home_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'patient_panel/home.html')


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
        self.assertTemplateNotUsed(response, 'patient_panel/offices.html')

    def test_offices_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.patient_offices_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'patient_panel/offices.html')

    def test_offices_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.patient_offices_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'patient_panel/offices.html')
