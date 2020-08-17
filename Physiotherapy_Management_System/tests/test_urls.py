from django.test import SimpleTestCase
from django.urls import reverse, resolve

from users.views import login


class TestUserUrls(SimpleTestCase):
    def test_check_user_url_resolves(self):
        url = reverse('panel')
        self.assertEquals(resolve(url).func.view_class, login.CheckUser)
