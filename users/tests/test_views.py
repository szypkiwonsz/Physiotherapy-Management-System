from django.test import TestCase, Client
from django.urls import reverse

from users.models import User, Office, UserPatient


# class TestActivateViews(TestCase):
#     pass


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


class TestPasswordViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.password_reset_url = reverse('password_reset')
        self.password_reset_done_url = reverse('password_reset_done')
        self.password_reset_complete_url = reverse('password_reset_complete')

    def test_password_reset_url_GET(self):
        response = self.client.get(self.password_reset_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('registration/password_reset_form.html')

    # def test_password_reset_confirm_url_GET(self):
    #     pass

    def test_password_reset_done_url_GET(self):
        response = self.client.get(self.password_reset_done_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('registration/password_reset_dont.html')

    def test_password_reset_complete_url_GET(self):
        response = self.client.get(self.password_reset_complete_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('registration/password_reset_complete.html')


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
        url = reverse('profile-office')
        response = self.client.post(url, {
            'name': self.office_user_office1.name,
            'address': self.office_user_office1.address,
            'city': self.office_user_office1.city,
            'phone_number': self.office_user_office1.phone_number,
            'website': 'www.newwebsite.com',
            'email': self.office_user_office1.user.email
        })
        office_update = User.objects.get(id=2)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(office_update.office.website, 'www.newwebsite.com')

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
        url = reverse('profile-patient')
        response = self.client.post(url, {
            'email': 'newpatientemail@gmail.com'
        })
        patient_update = User.objects.get(id=1)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(patient_update.email, 'newpatientemail@gmail.com')


class TestSignupViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.office_signup_url = reverse('office-signup')
        self.patient_signup_url = reverse('patient-signup')

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
        url = reverse('office-signup')
        response = self.client.post(url, {
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
        self.assertEquals(office_user.office.name, 'name')

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
        url = reverse('patient-signup')
        response = self.client.post(url, {
            'email': 'random_patient_email@gmail.com',
            'confirm_email': 'random_patient_email@gmail.com',
            'password1': 'random_password',
            'password2': 'random_password'
        })
        patient_user = User.objects.get(id=1)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(patient_user.email, 'random_patient_email@gmail.com')
