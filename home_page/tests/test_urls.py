from django.test import SimpleTestCase
from django.urls import reverse, resolve
from home_page.views import HomeView, HelpView, OfficesView


class TestUrls(SimpleTestCase):
    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func.view_class, HomeView)

    def test_help_url_resolves(self):
        url = reverse('help')
        self.assertEquals(resolve(url).func.view_class, HelpView)

    def test_offices_url_resolves(self):
        url = reverse('offices')
        self.assertEquals(resolve(url).func.view_class, OfficesView)
