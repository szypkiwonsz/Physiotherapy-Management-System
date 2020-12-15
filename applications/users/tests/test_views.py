from django.test import TestCase, Client
from django.urls import reverse

from applications.users.models import User, UserOffice, UserPatient


class TestProfileViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.office_profile_url = reverse('users:office_profile')
        self.patient_profile_url = reverse('users:patient_profile')
        self.patient1 = User.objects.create_user(
            'patient', 'patient@gmail.com', 'patientpassword', is_patient=True
        )
        self.office1 = User.objects.create_user(
            'office', 'office@gmail.com', 'officepassword', is_office=True
        )
        self.office_user_office1 = UserOffice.objects.create(
            user=self.office1,
            name='name',
            address='address',
            city='City',
            phone_number='000000000',
            website='www.website.com'
        )
        self.patient_user_patient1 = UserPatient.objects.create(
            user=self.patient1
        )

    def test_office_profile_GET_not_logged_in(self):
        response = self.client.get(self.office_profile_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed('users/profile.html')

    def test_office_profile_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.office_profile_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed('users/profile.html')

    def test_office_profile_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.office_profile_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('users/profile.html')

    def test_office_profile_POST(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.post(self.office_profile_url, {
            'name': self.office_user_office1.name,
            'address': self.office_user_office1.address,
            'city': self.office_user_office1.city,
            'phone_number': self.office_user_office1.phone_number,
            'website': 'www.newwebsite.com',
            'email': self.office_user_office1.user.email
        })
        office_update = User.objects.get(id=2)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(user.useroffice.website, 'www.newwebsite.com')

    def test_patient_profile_GET_not_logged_in(self):
        response = self.client.get(self.patient_profile_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed('users/profile.html')

    def test_patient_profile_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.patient_profile_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('users/profile.html')

    def test_patient_profile_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.patient_profile_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed('users/profile.html')

    def test_patient_profile_POST(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.post(self.patient_profile_url, {
            'email': 'newpatientemail@gmail.com'
        })
        patient_update = User.objects.get(id=1)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(patient_update.email, 'newpatientemail@gmail.com')


class TestSignupViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('users:signup')
        self.office_signup_url = reverse('users:office_signup')
        self.patient_signup_url = reverse('users:patient_signup')

    def test_register_GET_not_logged_in(self):
        response = self.client.get(self.signup_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('users/signup.html')

    def test_register_GET_logged_as_patient(self):
        response = self.client.get(self.signup_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('users/signup.html')

    def test_register_GET_logged_as_office(self):
        response = self.client.get(self.signup_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('users/signup.html')

    def test_register_office_GET_not_logged_in(self):
        response = self.client.get(self.office_signup_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('users/signup_office.html')

    def test_register_office_GET_logged_as_patient(self):
        response = self.client.get(self.office_signup_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('users/signup_office.html')

    def test_register_office_GET_logged_as_office(self):
        response = self.client.get(self.office_signup_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('users/signup_office.html')

    def test_register_office_POST(self):
        response = self.client.post(self.office_signup_url, {
            'name': 'name',
            'address': 'address',
            'city': 'city',
            'phone_number': '000000000',
            'email': 'random_office_email@gmail.com',
            'confirm_email': 'random_office_email@gmail.com',
            'password1': 'random_password',
            'password2': 'random_password'
        })
        office_user = User.objects.get(id=1)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(office_user.email, 'random_office_email@gmail.com')
        self.assertEquals(office_user.useroffice.name, 'name')

    def test_register_patient_GET_not_logged_in(self):
        response = self.client.get(self.patient_signup_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('users/signup_patient.html')

    def test_register_patient_GET_logged_as_patient(self):
        response = self.client.get(self.patient_signup_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('users/signup_patient.html')

    def test_register_patient_GET_logged_as_office(self):
        response = self.client.get(self.patient_signup_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('users/signup_patient.html')

    def test_register_patient_POST(self):
        response = self.client.post(self.patient_signup_url, {
            'email': 'random_patient_email@gmail.com',
            'confirm_email': 'random_patient_email@gmail.com',
            'password1': 'random_password',
            'password2': 'random_password'
        })
        patient_user = User.objects.get(id=1)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(patient_user.email, 'random_patient_email@gmail.com')
