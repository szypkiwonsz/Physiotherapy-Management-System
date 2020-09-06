from django.test import SimpleTestCase

from appointments.forms import AppointmentPatientMakeForm, AppointmentOfficeUpdateForm


class TestPatientMakeAppointmentForm(SimpleTestCase):
    def test_patient_make_form_valid(self):
        form = AppointmentPatientMakeForm(data={
            'date': '27.08.2020 17:00',
            'name': 'Name',
            'phone_number': '000000000',
            'choice': 'Konsultacja'
        })
        self.assertTrue(form.is_valid())

    def test_patient_make_form_no_data(self):
        form = AppointmentPatientMakeForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)

    def test_patient_make_form_wrong_name(self):
        form = AppointmentPatientMakeForm(data={
            'date': '27.08.2020 17:00',
            'name': 'Name1',
            'phone_number': '000000000',
            'choice': 'Konsultacja'
        })
        self.assertFalse(form.is_valid())

    def test_patient_make_form_wrong_phone_number(self):
        form = AppointmentPatientMakeForm(data={
            'date': '27.08.2020 17:00',
            'name': 'name',
            'phone_number': '00000',
            'choice': 'Konsultacja'
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)


class TestOfficeUpdateAppointmentForm(SimpleTestCase):
    def test_office_update_form_valid(self):
        form = AppointmentOfficeUpdateForm(data={
            'date': '27.08.2020 17:00',
        })
        self.assertTrue(form.is_valid())

    def test_office_update_form_no_data(self):
        form = AppointmentOfficeUpdateForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
