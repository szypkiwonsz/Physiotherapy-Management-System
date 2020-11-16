from django.test import SimpleTestCase
from django.urls import reverse, resolve
from applications.appointments.views import patient, office


class TestPatientAppointmentsUrls(SimpleTestCase):
    def test_select_office_url_resolves(self):
        url = reverse('patient_panel:appointments:select')
        self.assertEquals(resolve(url).func.view_class, patient.SelectOffice)

    def test_make_appointment_url_resolves(self):
        url = reverse('patient_panel:appointments:make', args=[1])
        self.assertEquals(resolve(url).func.view_class, patient.MakeAppointment)

    def test_appointment_list_url_resolves(self):
        url = reverse('patient_panel:appointments:upcoming')
        self.assertEquals(resolve(url).func.view_class, patient.AppointmentListView)

    def test_old_appointment_list_url_resolves(self):
        url = reverse('patient_panel:appointments:old')
        self.assertEquals(resolve(url).func.view_class, patient.OldAppointmentListView)

    def test_appointment_update_url_resolves(self):
        url = reverse('patient_panel:appointments:update', args=[1])
        self.assertEquals(resolve(url).func.view_class, patient.AppointmentUpdateView)

    def test_appointment_cancel_url_resolves(self):
        url = reverse('patient_panel:appointments:delete', args=[1])
        self.assertEquals(resolve(url).func.view_class, patient.AppointmentCancelView)


class TestOfficeAppointmentUrls(SimpleTestCase):
    def test_appointment_list_url_resolves(self):
        url = reverse('office_panel:appointments:list')
        self.assertEquals(resolve(url).func.view_class, office.AppointmentListView)

    def test_appointment_change_url_resolves(self):
        url = reverse('office_panel:appointments:update', args=[1])
        self.assertEquals(resolve(url).func.view_class, office.AppointmentUpdateView)

    def test_appointment_delete_url_resolves(self):
        url = reverse('office_panel:appointments:delete', args=[1])
        self.assertEquals(resolve(url).func.view_class, office.AppointmentDeleteView)

    def test_appointment_make_url_resolves(self):
        url = reverse('office_panel:appointments:make', args=[1])
        self.assertEquals(resolve(url).func.view_class, office.MakeAppointment)
