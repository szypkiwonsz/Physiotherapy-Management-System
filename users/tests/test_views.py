from django.test import TestCase, Client
from django.urls import reverse

from users.models import User


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
        pass

    def test_login_POST_as_patient(self):
        pass
