from django.test import TestCase

# Create your tests here.
from django.urls import reverse


class HomeTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)


class HelpTests(TestCase):
    def test_help_view_status_code(self):
        url = reverse('help')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
