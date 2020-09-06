from django.contrib.auth import views as auth_views
from django.test import SimpleTestCase
from django.urls import reverse, resolve

from users.views import signup, login, profile


# class TestActivateUrls(SimpleTestCase):
#     pass


class TestProfileUrls(SimpleTestCase):
    def test_office_url_resolves(self):
        url = reverse('users:office_profile')
        self.assertEquals(resolve(url).func.view_class, profile.OfficeProfile)

    def test_patient_url_resolves(self):
        url = reverse('users:patient_profile')
        self.assertEquals(resolve(url).func.view_class, profile.PatientProfile)


class TestSignupUrls(SimpleTestCase):
    def test_register_url_resolves(self):
        url = reverse('users:signup')
        self.assertEquals(resolve(url).func.view_class, signup.Register)

    def test_register_patient_url_resolves(self):
        url = reverse('users:patient_signup')
        self.assertEquals(resolve(url).func.view_class, signup.RegisterPatient)

    def test_register_office_url_resolves(self):
        url = reverse('users:office_signup')
        self.assertEquals(resolve(url).func.view_class, signup.RegisterOffice)
