from datetime import datetime

from django.test import TestCase

from applications.appointments.models import Appointment
from applications.users.models import Office, User


class TestAppointmentModels(TestCase):

    def setUp(self):
        self.patient1 = User.objects.create_user(
            'patient', 'patient@gmail.com', 'patientpassword', is_patient=True
        )
        self.office1 = User.objects.create_user(
            'office', 'office@gmail.com', 'officepassword', is_office=True
        )
        self.appointment_office1 = UserOffice.objects.create(
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
            first_name='kacper',
            last_name='sawicki',
            date_selected=datetime(2012, 1, 13, 23, 51, 34),
            phone_number='000000000',
            confirmed=False,
            choice='Konsultacja'
        )

    def test_appointment_patient_name_is_capitalized_on_creation(self):
        self.assertEquals(self.appointment1.first_name, 'Kacper')
        self.assertEquals(self.appointment1.last_name, 'Sawicki')

    def test_string_representation(self):
        self.assertEquals(str(self.appointment1), self.patient1.email)
