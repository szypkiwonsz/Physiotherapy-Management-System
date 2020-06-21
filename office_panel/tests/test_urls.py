from django.test import SimpleTestCase
from django.urls import reverse, resolve
from office_panel.views import home, patient, appointment, medical_history


class TestOfficeAppointmentUrls(SimpleTestCase):
    def test_appointment_list_url_resolves(self):
        url = reverse('office-appointments')
        self.assertEquals(resolve(url).func.view_class, appointment.AppointmentListView)

    def test_appointment_change_url_resolves(self):
        url = reverse('office-appointment-change', args=[1])
        self.assertEquals(resolve(url).func.view_class, appointment.AppointmentUpdateView)

    def test_appointment_delete_url_resolves(self):
        url = reverse('office-appointment-delete', args=[1])
        self.assertEquals(resolve(url).func.view_class, appointment.AppointmentDeleteView)


class TestOfficeHomeUrls(SimpleTestCase):
    def test_patient_list_url_resolves(self):
        url = reverse('office-home')
        self.assertEquals(resolve(url).func.view_class, home.OfficePanelView)


class TestOfficeMedicalHistoryUrls(SimpleTestCase):
    def test_medical_history_list_url_resolves(self):
        url = reverse('office-medical-history')
        self.assertEquals(resolve(url).func.view_class, medical_history.MedicalHistoryListView)


class TestOfficePatientUrls(SimpleTestCase):
    def test_patient_list_url_resolves(self):
        url = reverse('office-patients')
        self.assertEquals(resolve(url).func.view_class, patient.PatientListView)

    def test_patient_create_url_resolves(self):
        url = reverse('office-patient-add')
        self.assertEquals(resolve(url).func.view_class, patient.PatientCreateView)

    def test_patient_detail_url_resolves(self):
        url = reverse('office-patient-detail', args=[1])
        self.assertEquals(resolve(url).func.view_class, patient.PatientDetailView)

    def test_patient_update_url_resolves(self):
        url = reverse('office-patient-change', args=[1])
        self.assertEquals(resolve(url).func.view_class, patient.PatientUpdateView)

    def test_patient_delete_url_resolves(self):
        url = reverse('office-patient-delete-confirm', args=[1])
        self.assertEquals(resolve(url).func.view_class, patient.PatientDeleteView)
