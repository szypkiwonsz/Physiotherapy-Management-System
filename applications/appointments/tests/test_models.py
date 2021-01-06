from datetime import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase

from applications.appointments.models import Appointment, Service
from applications.users.models import UserOffice, User


class TestAppointmentModels(TestCase):

    def setUp(self):
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
        self.service = Service.objects.create(
            office=self.appointment_office1,
            name='Konsultacja',
            duration=10
        )
        self.appointment1 = Appointment.objects.create(
            owner=self.office1,
            office=self.appointment_office1,
            date=datetime(2012, 1, 13, 16, 00, 00),
            first_name='kacper',
            last_name='sawicki',
            date_selected=datetime(2012, 1, 13, 23, 51, 34),
            phone_number='000000000',
            confirmed=False,
            service=self.service
        )

    def test_appointment_patient_name_is_capitalized_on_creation(self):
        self.assertEquals(self.appointment1.first_name, 'Kacper')
        self.assertEquals(self.appointment1.last_name, 'Sawicki')

    def test_calculate_date_end_on_creation(self):
        self.assertEquals(self.appointment1.date_end, datetime(2012, 1, 13, 16, 10))

    def test_string_representation(self):
        self.assertEquals(str(self.appointment1), '2012-01-13 16:00:00 - Kacper Sawicki')


class TestServiceModels(TestCase):

    def setUp(self):
        self.office1 = User.objects.create_user(
            'office', 'office@gmail.com', 'officepassword', is_office=True
        )
        self.service_office1 = UserOffice.objects.create(
            user=self.office1,
            name='name',
            address='address',
            city='City',
            phone_number='000000000',
            website='www.website.com'
        )
        self.service1 = Service.objects.create(
            office=self.service_office1,
            name='Masaż',
            duration=10
        )

    def test_string_representation(self):
        self.assertEqual(str(self.service1), 'Masaż')

    def test_save_method(self):
        Service.objects.create(
            office=self.service_office1,
            name='Konsultacja',
            duration=20
        )
        service = Service.objects.get(id=2)
        self.assertEqual(service.name, 'Konsultacja')

    def test_service_unique_name_per_office(self):
        with self.assertRaises(ValidationError):
            Service.objects.create(
                office=self.service_office1, name='Masaż', duration=10
            )
