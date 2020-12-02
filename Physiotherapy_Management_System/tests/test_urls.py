from django.contrib.auth import views as auth_views
from django.test import SimpleTestCase
from django.urls import reverse, resolve

from applications.users.views import login


class TestUserUrls(SimpleTestCase):

    def test_check_user_url_resolves(self):
        url = reverse('panel')
        self.assertEquals(resolve(url).func.view_class, login.CheckUser)


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
