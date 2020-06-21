from django.test import TestCase, Client
from django.urls import reverse


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        self.help_url = reverse('help')
        self.offices_url = reverse('offices')

    def test_home_GET(self):
        response = self.client.get(self.home_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home_page/home.html')

    def test_help_GET(self):
        response = self.client.get(self.help_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home_page/help.html')

    def test_offices_GET(self):
        response = self.client.get(self.offices_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home_page/offices.html')
