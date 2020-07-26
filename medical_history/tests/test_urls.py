from django.test import SimpleTestCase
from django.urls import reverse, resolve

from medical_history.views import office, patient


class TestOfficeMedicalHistoryUrls(SimpleTestCase):
    def test_medical_history_list_url_resolves(self):
        url = reverse('office-medical-history')
        self.assertEquals(resolve(url).func.view_class, office.MedicalHistoryListView)

    def test_medical_history_add_url_resolves(self):
        url = reverse('office-make-medical-history')
        self.assertEquals(resolve(url).func.view_class, office.MakeMedicalHistory)

    def test_medical_history_detail_url_resolves(self):
        url = reverse('office-medical-history-detail', args=[1])
        self.assertEquals(resolve(url).func.view_class, office.MedicalHistoryDetailView)

    def test_medical_history_update_url_resolves(self):
        url = reverse('office-medical-history-change', args=[1])
        self.assertEquals(resolve(url).func.view_class, office.MedicalHistoryUpdateView)

    def test_medical_history_delete_url_resolves(self):
        url = reverse('office-medical-history-delete', args=[1])
        self.assertEquals(resolve(url).func.view_class, office.MedicalHistoryDeleteView)


class TestPatientMedicalHistoryUrls(SimpleTestCase):
    def test_medical_history_list_url_resolves(self):
        url = reverse('patient-medical-history')
        self.assertEquals(resolve(url).func.view_class, patient.MedicalHistoryListView)
