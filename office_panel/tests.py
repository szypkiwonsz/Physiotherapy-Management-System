from django.urls import reverse
from django.test import TestCase


# Create your tests here.
class OfficeHomeTests(TestCase):
    def test_office_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
