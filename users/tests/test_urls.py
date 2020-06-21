from django.test import SimpleTestCase
from django.urls import reverse, resolve
from users.views import signup, login, activate_account, password, profile


# class TestActivateAccountUrls(SimpleTestCase):
#     def test_activate_account_url_resolves(self):
#         url = reverse('activate')
#         self.assertEquals(resolve(url).func.view_class, activate_account.activate())


class TestLoginUrls(SimpleTestCase):
    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, login.LoginView)

# ''' TOKEN!!! '''
# class TestPasswordUrls(SimpleTestCase):
#     def test_new_password_confirm_url_resolves(self):
#         url = reverse('password_reset_confirm')
#         self.assertEquals(resolve(url).func.view_class, password.NewPasswordResetConfirmView)


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
