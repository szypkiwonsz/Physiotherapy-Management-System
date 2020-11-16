from django.test import SimpleTestCase, TestCase

from applications.appointments.forms import AppointmentPatientMakeForm, AppointmentOfficeUpdateForm, \
    AppointmentOfficeMakeForm
from applications.office_panel.models import Patient
from applications.users.models import User


class TestPatientMakeAppointmentForm(SimpleTestCase):
    def test_patient_make_form_valid(self):
        form = AppointmentPatientMakeForm(data={
            'date': '27.08.2020 17:00',
            'first_name': 'Kacper',
            'last_name': 'Sawicki',
            'phone_number': '000000000',
            'choice': 'Konsultacja'
        })
        self.assertTrue(form.is_valid())

    def test_patient_make_form_no_data(self):
        form = AppointmentPatientMakeForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 5)

    def test_patient_make_form_wrong_first_name(self):
        form = AppointmentPatientMakeForm(data={
            'date': '27.08.2020 17:00',
            'first_name': 'Kacper_',
            'last_name': 'Sawicki',
            'phone_number': '000000000',
            'choice': 'Konsultacja'
        })
        self.assertFalse(form.is_valid())

    def test_patient_make_form_wrong_phone_number(self):
        form = AppointmentPatientMakeForm(data={
            'date': '27.08.2020 17:00',
            'first_name': 'Kacper',
            'last_name': 'Sawicki',
            'phone_number': '00000',
            'choice': 'Konsultacja'
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)


class TestOfficeAppointmentMakeForm(TestCase):
    def setUp(self):
        self.office1 = User.objects.create_user(
            'office', 'office@gmail.com', 'officepassword', is_office=True
        )
        self.office_patient1 = Patient.objects.create(
            owner=self.office1,
            first_name='firstname',
            last_name='lastname',
            email='patient@gmail.com',
        )

    def test_office_make_form_valid(self):
        patient = Patient.objects.get(id=1)
        form = AppointmentOfficeMakeForm(data={
            'date': '27.08.2020 17:00',
            'choice': 'Konsultacja',
            'patient': patient
        }, user=self.office1)
        self.assertTrue(form.is_valid())

    def test_patient_make_form_no_data(self):
        form = AppointmentOfficeMakeForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)


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
