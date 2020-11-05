from django.test import SimpleTestCase
from django.urls import reverse, resolve

from applications.medical_history.views import office, patient


class TestOfficeMedicalHistoryUrls(SimpleTestCase):
    def test_medical_history_list_url_resolves(self):
        url = reverse('office_panel:medical_history:list')
        self.assertEquals(resolve(url).func.view_class, office.MedicalHistoryListView)

    def test_medical_history_add_url_resolves(self):
        url = reverse('office_panel:medical_history:make')
        self.assertEquals(resolve(url).func.view_class, office.MakeMedicalHistory)

    def test_medical_history_detail_url_resolves(self):
        url = reverse('office_panel:medical_history:detail', args=[1])
        self.assertEquals(resolve(url).func.view_class, office.MedicalHistoryDetailView)

    def test_medical_history_update_url_resolves(self):
        url = reverse('office_panel:medical_history:update', args=[1])
        self.assertEquals(resolve(url).func.view_class, office.MedicalHistoryUpdateView)

    def test_medical_history_delete_url_resolves(self):
        url = reverse('office_panel:medical_history:delete', args=[1])
        self.assertEquals(resolve(url).func.view_class, office.MedicalHistoryDeleteView)


class TestPatientMedicalHistoryUrls(SimpleTestCase):
    def test_medical_history_list_url_resolves(self):
        url = reverse('patient_panel:medical_history:list')
        self.assertEquals(resolve(url).func.view_class, patient.MedicalHistoryListView)
