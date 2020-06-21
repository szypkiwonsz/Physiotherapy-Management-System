from django.test import SimpleTestCase
from django.urls import reverse, resolve
from appointments.views import SelectOffice, MakeAppointment


class TestUrls(SimpleTestCase):
    def test_select_office_url_resolves(self):
        url = reverse('appointments-select')
        self.assertEquals(resolve(url).func.view_class, SelectOffice)

    def test_make_appointment_url_resolves(self):
        url = reverse('appointments-make-appointment', args=[1])
        self.assertEquals(resolve(url).func.view_class, MakeAppointment)
