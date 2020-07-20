from django.test import TestCase, Client
from django.urls import reverse

from users.models import User, Profile, Office


class TestLoginViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.panel_url = reverse('panel')
        self.login_url = reverse('login')
        self.patient1 = User.objects.create_user(
            'patient', 'patient@gmail.com', 'patientpassword', is_patient=True
        )
        self.office1 = User.objects.create_user(
            'office', 'office@gmail.com', 'officepassword', is_office=True
        )

    def test_check_user_GET_not_logged_in(self):
        response = self.client.get(self.panel_url)

        self.assertEquals(response.status_code, 302)

    def test_check_user_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.panel_url)

        self.assertEquals(response.status_code, 302)

    def test_check_user_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.panel_url)

        self.assertEquals(response.status_code, 302)

    def test_login_GET(self):
        response = self.client.get(self.login_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('users/login.html')

    def test_login_POST_as_office(self):
        url = reverse('login')
        response = self.client.post(url, {
            'username': 'office@gmail.com',
            'password': 'officepassword'
        })
        self.assertEquals(response.status_code, 302)

    def test_login_POST_as_patient(self):
        url = reverse('login')
        response = self.client.post(url, {
            'username': 'patient@gmail.com',
            'password': 'patientpassword'
        })
        self.assertEquals(response.status_code, 302)

    def test_login_POST_wrong(self):
        url = reverse('login')
        response = self.client.post(url, {
            'username': 'wrong_email@gmail.com',
            'password': 'wrong_password'
        })
        self.assertEquals(response.status_code, 200)


class TestProfileViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.office_profile_url = reverse('profile-office')
        self.patient_profile_url = reverse('profile-patient')
        self.patient1 = User.objects.create_user(
            'patient', 'patient@gmail.com', 'patientpassword', is_patient=True
        )
        self.office1 = User.objects.create_user(
            'office', 'office@gmail.com', 'officepassword', is_office=True
        )
        self.office_user_office1 = Office.objects.create(
            user=self.office1,
            name='name',
            address='address',
            city='City',
            phone_number='000000000',
            website='www.website.com'
        )

    def test_office_profile_GET_not_logged_in(self):
        response = self.client.get(self.office_profile_url)

        self.assertEquals(response.status_code, 302)

    def test_office_profile_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.office_profile_url)

        self.assertEquals(response.status_code, 302)

    def test_office_profile_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.office_profile_url)

        self.assertEquals(response.status_code, 200)
