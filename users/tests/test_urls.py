from django.contrib.auth import views as auth_views
from django.test import SimpleTestCase
from django.urls import reverse, resolve

from users.views import signup, login, profile


# class TestActivateUrls(SimpleTestCase):
#     pass


class TestLoginUrls(SimpleTestCase):
    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, login.LoginView)


class TestPasswordUrls(SimpleTestCase):
    def test_password_reset_url_resolves(self):
        url = reverse('password_reset')
        self.assertEquals(resolve(url).func.view_class, auth_views.PasswordResetView)

    def test_password_reset_done_resolves(self):
        url = reverse('password_reset_done')
        self.assertEquals(resolve(url).func.view_class, auth_views.PasswordResetDoneView)

    def test_password_reset_complete_resolves(self):
        url = reverse('password_reset_complete')
        self.assertEquals(resolve(url).func.view_class, auth_views.PasswordResetCompleteView)

    # def test_password_reset_confirm_resolves(self):
    #     pass


class TestProfileUrls(SimpleTestCase):
    def test_office_url_resolves(self):
        url = reverse('profile-office')
        self.assertEquals(resolve(url).func.view_class, profile.OfficeProfile)

    def test_patient_url_resolves(self):
        url = reverse('profile-patient')
        self.assertEquals(resolve(url).func.view_class, profile.PatientProfile)


class TestSignupUrls(SimpleTestCase):
    def test_register_url_resolves(self):
        url = reverse('signup')
        self.assertEquals(resolve(url).func.view_class, signup.Register)

    def test_register_patient_url_resolves(self):
        url = reverse('patient-signup')
        self.assertEquals(resolve(url).func.view_class, signup.RegisterPatient)

    def test_register_office_url_resolves(self):
        url = reverse('office-signup')
        self.assertEquals(resolve(url).func.view_class, signup.RegisterOffice)
