from django.test import SimpleTestCase
from django.urls import reverse, resolve
from patient_panel.views import home, appointment, offices, medical_history


class TestPatientAppointmentUrls(SimpleTestCase):
    def test_appointment_list_url_resolves(self):
        url = reverse('patient-appointment-upcoming')
        self.assertEquals(resolve(url).func.view_class, appointment.AppointmentListView)

    def test_old_appointment_list_url_resolves(self):
        url = reverse('patient-appointment-old')
        self.assertEquals(resolve(url).func.view_class, appointment.OldAppointmentListView)

    def test_appointment_update_url_resolves(self):
        url = reverse('patient-appointment-change', args=[1])
        self.assertEquals(resolve(url).func.view_class, appointment.AppointmentUpdateView)

    def test_appointment_cancel_url_resolves(self):
        url = reverse('patient-appointment-cancel', args=[1])
        self.assertEquals(resolve(url).func.view_class, appointment.AppointmentCancelView)


class TestPatientHomeUrls(SimpleTestCase):
    def test_home_url_resolves(self):
        url = reverse('patient-home')
        self.assertEquals(resolve(url).func.view_class, home.PatientHome)


class TestPatientMedicalHistoryUrls(SimpleTestCase):
    def test_medical_history_list_url_resolves(self):
        url = reverse('patient-medical-history')
        self.assertEquals(resolve(url).func.view_class, medical_history.MedicalHistoryListView)


class TestPatientOfficesUrls(SimpleTestCase):
    def test_offices_list_url_resolves(self):
        url = reverse('patient-offices')
        self.assertEquals(resolve(url).func.view_class, offices.OfficesListView)
