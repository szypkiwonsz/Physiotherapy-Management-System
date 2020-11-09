from django.test import TestCase

from applications.office_panel.forms import PatientForm


class TestPatientForm(TestCase):
    def test_make_patient_form_valid(self):
        form = PatientForm(data={
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'przykladowy_pacjent@gmail.com',
            'address': 'address',
            'pesel': '00000000000',
            'phone_number': '000000000'
        })
        self.assertTrue(form.is_valid())

    def test_make_patient_form_no_data(self):
        form = PatientForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)

    def test_make_patient_form_invalid_first_name(self):
        form = PatientForm(data={
            'first_name': 'firstname1',
            'last_name': 'lastname',
            'email': 'przykladowy_pacjent@gmail.com',
            'address': 'address',
            'pesel': '00000000000',
            'phone_number': '000000000'
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_make_patient_form_invalid_last_name(self):
        form = PatientForm(data={
            'first_name': 'firstname',
            'last_name': 'lastname1',
            'email': 'przykladowy_pacjent@gmail.com',
            'address': 'address',
            'pesel': '00000000000',
            'phone_number': '000000000'
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_make_patient_form_invalid_pesel(self):
        form = PatientForm(data={
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'przykladowy_pacjent@gmail.com',
            'address': 'address',
            'pesel': '00000',
            'phone_number': '000000000'
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_make_patient_form_invalid_phone_number(self):
        form = PatientForm(data={
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'przykladowy_pacjent@gmail.com',
            'address': 'address',
            'pesel': '00000000000',
            'phone_number': '0000'
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
