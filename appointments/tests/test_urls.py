from django.test import SimpleTestCase
from django.urls import reverse, resolve
from appointments.views import patient, office


class TestPatientAppointmentsUrls(SimpleTestCase):
    def test_select_office_url_resolves(self):
        url = reverse('appointments-select')
        self.assertEquals(resolve(url).func.view_class, patient.SelectOffice)

    def test_make_appointment_url_resolves(self):
        url = reverse('appointments-make-appointment', args=[1])
        self.assertEquals(resolve(url).func.view_class, patient.MakeAppointment)

    def test_appointment_list_url_resolves(self):
        url = reverse('patient-appointment-upcoming')
        self.assertEquals(resolve(url).func.view_class, patient.AppointmentListView)

    def test_old_appointment_list_url_resolves(self):
        url = reverse('patient-appointment-old')
        self.assertEquals(resolve(url).func.view_class, patient.OldAppointmentListView)

    def test_appointment_update_url_resolves(self):
        url = reverse('patient-appointment-change', args=[1])
        self.assertEquals(resolve(url).func.view_class, patient.AppointmentUpdateView)

    def test_appointment_cancel_url_resolves(self):
        url = reverse('patient-appointment-cancel', args=[1])
        self.assertEquals(resolve(url).func.view_class, patient.AppointmentCancelView)


class TestOfficeAppointmentUrls(SimpleTestCase):
    def test_appointment_list_url_resolves(self):
        url = reverse('office-appointments')
        self.assertEquals(resolve(url).func.view_class, office.AppointmentListView)

    def test_appointment_change_url_resolves(self):
        url = reverse('office-appointment-change', args=[1])
        self.assertEquals(resolve(url).func.view_class, office.AppointmentUpdateView)

    def test_appointment_delete_url_resolves(self):
        url = reverse('office-appointment-delete', args=[1])
        self.assertEquals(resolve(url).func.view_class, office.AppointmentDeleteView)
