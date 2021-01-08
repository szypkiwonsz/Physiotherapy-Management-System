from django.test import SimpleTestCase
from django.urls import reverse, resolve

from applications.office_panel.views import home, patient


class TestOfficeHomeUrls(SimpleTestCase):

    def test_patient_list_url_resolves(self):
        url = reverse('office_panel:home')
        self.assertEquals(resolve(url).func.view_class, home.OfficePanelView)


class TestOfficePatientUrls(SimpleTestCase):

    def test_patient_list_url_resolves(self):
        url = reverse('office_panel:patients')
        self.assertEquals(resolve(url).func.view_class, patient.PatientListView)

    def test_patient_create_url_resolves(self):
        url = reverse('office_panel:patient_add')
        self.assertEquals(resolve(url).func.view_class, patient.PatientCreateView)

    def test_patient_detail_url_resolves(self):
        url = reverse('office_panel:patient_detail', args=[1])
        self.assertEquals(resolve(url).func.view_class, patient.PatientDetailView)

    def test_patient_update_url_resolves(self):
        url = reverse('office_panel:patient_update', args=[1])
        self.assertEquals(resolve(url).func.view_class, patient.PatientUpdateView)

    def test_patient_delete_url_resolves(self):
        url = reverse('office_panel:patient_delete', args=[1])
        self.assertEquals(resolve(url).func.view_class, patient.PatientDeleteView)
