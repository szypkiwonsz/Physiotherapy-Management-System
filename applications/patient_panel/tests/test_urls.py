from django.test import SimpleTestCase
from django.urls import reverse, resolve

from applications.patient_panel.views import home, offices


class TestPatientHomeUrls(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('patient_panel:home')
        self.assertEquals(resolve(url).func.view_class, home.PatientHome)


class TestPatientOfficesUrls(SimpleTestCase):

    def test_offices_list_url_resolves(self):
        url = reverse('patient_panel:offices')
        self.assertEquals(resolve(url).func.view_class, offices.OfficesListView)
