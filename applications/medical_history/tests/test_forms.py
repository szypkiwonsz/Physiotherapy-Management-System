from datetime import datetime

from django.test import TestCase

from applications.appointments.models import Appointment
from applications.medical_history.forms import MedicalHistoryForm
from applications.office_panel.models import Patient
from applications.users.models import User, Office


class TestMedicalHistoryForm(TestCase):

    def setUp(self):
        self.patient1 = User.objects.create_user(
            'patient', 'patient@gmail.com', 'patientpassword', is_patient=True
        )
        self.office1 = User.objects.create_user(
            'office', 'office@gmail.com', 'officepassword', is_office=True
        )
        self.office_patient1 = Patient.objects.create(
            owner=self.office1,
            first_name='firstname',
            last_name='lastname',
            email='patient@gmail.com',
            phone_number='000000000'
        )
        self.appointment_office1 = Office.objects.create(
            user=self.office1,
            name='name',
            address='address',
            city='City',
            phone_number='000000000',
            website='www.website.com'
        )
        self.appointment1 = Appointment.objects.create(
            owner=self.patient1,
            office=self.appointment_office1,
            date=datetime(2012, 1, 13, 16, 00, 00),
            first_name='Kacper',
            last_name='Sawicki',
            date_selected=datetime(2012, 1, 13, 23, 51, 34),
            phone_number='000000000',
            confirmed=False,
            choice='Konsultacja'
        )

    def test_medical_history_make_form_valid(self):
        form = MedicalHistoryForm(data={
            'patient': self.office_patient1.pk,
            'appointment': self.appointment1.pk,
            'description': 'random',
            'recommendations': 'random'
        }, user=self.office1)

        self.assertTrue(form.is_valid())

    def test_medical_history_make_form_no_data(self):
        form = MedicalHistoryForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)
