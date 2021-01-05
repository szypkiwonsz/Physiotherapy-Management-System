from datetime import datetime

from django.test import TestCase

from applications.appointments.forms import AppointmentPatientMakeForm, AppointmentOfficeUpdateForm, \
    AppointmentOfficeMakeForm, AppointmentPatientUpdateForm, ServiceForm
from applications.appointments.models import Service, Appointment
from applications.office_panel.models import Patient
from applications.users.models import User, UserOffice


class TestPatientMakeAppointmentForm(TestCase):

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
        self.service = Service.objects.create(
            office=self.appointment_office1,
            name='Konsultacja',
            duration=10
        )
        self.appointment1 = Appointment.objects.create(
            owner=self.patient1,
            office=self.appointment_office1,
            patient_email='patient@gmail.com',
            date=datetime(2012, 1, 13, 16, 00, 00),
            date_end=datetime(2012, 1, 13, 16, 30, 00),
            first_name='Kacper',
            last_name='Sawicki',
            date_selected=datetime(2012, 1, 13, 23, 51, 34),
            phone_number='000000000',
            confirmed=False,
            choice='Konsultacja'
        )

    def test_patient_make_form_valid(self):
        form = AppointmentPatientMakeForm(data={
            'date': '27.08.2020 17:00',
            'first_name': 'Kacper',
            'last_name': 'Sawicki',
            'phone_number': '000000000',
            'choice': 'Konsultacja'
        }, office=self.appointment_office1, appointment=None, date='15.12.2020 11:40', service_name='Konsultacja')
        self.assertTrue(form.is_valid())

    def test_patient_make_form_no_data(self):
        form = AppointmentPatientMakeForm(
            data={}, office=self.appointment_office1, appointment=None, date='15.12.2020 11:40', service_name='Konsultacja'
        )
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 5)

    def test_patient_make_form_wrong_first_name(self):
        form = AppointmentPatientMakeForm(data={
            'date': '27.08.2020 17:00',
            'first_name': 'Kacper_',
            'last_name': 'Sawicki',
            'phone_number': '000000000',
            'choice': 'Konsultacja'
        }, office=self.appointment_office1, appointment=None, date='15.12.2020 11:40', service_name='Konsultacja')
        self.assertFalse(form.is_valid())

    def test_patient_make_form_wrong_phone_number(self):
        form = AppointmentPatientMakeForm(data={
            'date': '06.01.2021 14:00',
            'first_name': 'Kacper',
            'last_name': 'Sawicki',
            'phone_number': '00000',
            'choice': 'Konsultacja'
        }, office=self.appointment_office1, appointment=None, date='06.01.2021 14:00', service_name='Konsultacja')
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_patient_make_form_date_taken(self):
        form = AppointmentPatientMakeForm(data={
            'date': '13.01.2012 16:00',
            'first_name': 'Kacper',
            'last_name': 'Sawicki',
            'phone_number': '000000000',
            'choice': 'Konsultacja'
        }, office=self.appointment_office1, appointment=None, date='13.01.2012 16:00', service_name='Konsultacja')
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)


class TestPatientAppointmentUpdateForm(TestCase):
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
        self.service = Service.objects.create(
            office=self.appointment_office1,
            name='Konsultacja',
            duration=10
        )
        self.appointment1 = Appointment.objects.create(
            owner=self.patient1,
            office=self.appointment_office1,
            patient_email='patient@gmail.com',
            date=datetime(2012, 1, 13, 16, 00, 00),
            date_end=datetime(2012, 1, 13, 16, 30, 00),
            first_name='Kacper',
            last_name='Sawicki',
            date_selected=datetime(2012, 1, 13, 23, 51, 34),
            phone_number='000000000',
            confirmed=False,
            choice='Konsultacja'
        )

    def test_patient_update_form_valid(self):
        form = AppointmentPatientUpdateForm(data={
            'date': '27.08.2020 17:00',
            'choice': self.service,
            'first_name': 'FirstName',
            'last_name': 'LastName',
            'phone_number': 111111111
        }, office=self.appointment_office1, appointment=2, date='15.12.2020 11:40', service_name='Konsultacja'
        )
        self.assertTrue(form.is_valid())

    def test_patient_update_form_no_data(self):
        form = AppointmentPatientUpdateForm(
            data={}, office=self.appointment_office1, appointment=2, date='15.12.2020 11:40', service_name='Konsultacja'
        )
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 5)

    def test_patient_update_form_date_taken(self):
        form = AppointmentPatientUpdateForm(data={
            'date': '13.01.2012 16:00',
            'first_name': 'Kacper',
            'last_name': 'Sawicki',
            'phone_number': '000000000',
            'choice': self.service
        }, office=self.appointment_office1, appointment=2, date='13.01.2012 16:00', service_name='Konsultacja')
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_patient_update_form_date_taken_same_appointment(self):
        form = AppointmentPatientUpdateForm(data={
            'date': '13.01.2012 16:00',
            'first_name': 'Kacper',
            'last_name': 'Sawicki',
            'phone_number': '000000000',
            'choice': self.service
        }, office=self.appointment_office1, appointment=1, date='13.01.2012 16:00', service_name='Konsultacja')
        self.assertTrue(form.is_valid())

    def test_patient_update_form_default_date(self):
        form = AppointmentPatientUpdateForm(data={
            'date': '13.01.2012 23:59',
            'first_name': 'Kacper',
            'last_name': 'Sawicki',
            'phone_number': '000000000',
            'choice': self.service
        }, office=self.appointment_office1, appointment=1, date='15.12.2020 23:59', service_name='Konsultacja')
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_patient_update_form_date_not_correct_with_office_hours(self):
        form = AppointmentPatientUpdateForm(data={
            'date': '13.01.2012 10:00',
            'first_name': 'Kacper',
            'last_name': 'Sawicki',
            'phone_number': '000000000',
            'choice': self.service
        }, office=self.appointment_office1, appointment=1, date='15.12.2020 23:59', service_name='Konsultacja')
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)


class TestOfficeAppointmentMakeForm(TestCase):

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
        self.office_patient1 = Patient.objects.create(
            owner=self.office1,
            first_name='firstname',
            last_name='lastname',
            email='patient@gmail.com',
        )
        self.service = Service.objects.create(
            office=self.appointment_office1,
            name='Konsultacja',
            duration=10
        )
        self.appointment1 = Appointment.objects.create(
            owner=self.office1,
            office=self.appointment_office1,
            patient_email='patient@gmail.com',
            date=datetime(2012, 1, 13, 16, 00, 00),
            date_end=datetime(2012, 1, 13, 16, 30, 00),
            first_name='Kacper',
            last_name='Sawicki',
            date_selected=datetime(2012, 1, 13, 23, 51, 34),
            phone_number='000000000',
            confirmed=False,
            choice='Konsultacja'
        )

    def test_office_make_form_valid(self):
        patient = Patient.objects.get(id=1)
        form = AppointmentOfficeMakeForm(data={
            'date': '27.08.2020 17:00',
            'choice': 'Konsultacja',
            'patient': patient
        }, office=self.appointment_office1, appointment=None, date='13.01.2012 16:00',
            service_name='Konsultacja')
        self.assertTrue(form.is_valid())

    def test_patient_make_form_no_data(self):
        form = AppointmentOfficeMakeForm(data={}, office=self.appointment_office1, appointment=None,
                                         date='13.01.2012 16:00', service_name='Konsultacja')
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)

    def test_patient_make_form_date_taken(self):
        form = AppointmentPatientMakeForm(data={
            'date': '13.01.2012 16:00',
            'first_name': 'Kacper',
            'last_name': 'Sawicki',
            'phone_number': '000000000',
            'choice': 'Konsultacja'
        }, office=self.appointment_office1, appointment=None, date='13.01.2012 16:00', service_name='Konsultacja')
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)


class TestOfficeUpdateAppointmentForm(TestCase):

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
            patient_email='patient@gmail.com',
            date=datetime(2012, 1, 13, 16, 00, 00),
            date_end=datetime(2012, 1, 13, 16, 30, 00),
            first_name='Kacper',
            last_name='Sawicki',
            date_selected=datetime(2012, 1, 13, 23, 51, 34),
            phone_number='000000000',
            confirmed=False,
            choice='Konsultacja'
        )

    def test_office_update_form_valid(self):
        form = AppointmentOfficeUpdateForm(data={
            'date': '27.08.2020 17:00',
            'choice': self.service
        }, office=self.appointment_office1, appointment=2, date='15.12.2020 11:40', service_name='Konsultacja'
        )
        self.assertTrue(form.is_valid())

    def test_office_update_form_no_data(self):
        form = AppointmentOfficeUpdateForm(
            data={}, office=self.appointment_office1, appointment=2, date='15.12.2020 11:40', service_name='Konsultacja'
        )
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_patient_update_form_date_taken(self):
        form = AppointmentPatientUpdateForm(data={
            'date': '13.01.2012 16:00',
            'first_name': 'Kacper',
            'last_name': 'Sawicki',
            'phone_number': '000000000',
            'choice': self.service
        }, office=self.appointment_office1, appointment=2, date='13.01.2012 16:00', service_name='Konsultacja')
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_patient_update_form_date_taken_same_appointment(self):
        form = AppointmentPatientUpdateForm(data={
            'date': '13.01.2012 16:00',
            'first_name': 'Kacper',
            'last_name': 'Sawicki',
            'phone_number': '000000000',
            'choice': self.service
        }, office=self.appointment_office1, appointment=1, date='13.01.2012 16:00', service_name='Konsultacja')
        self.assertTrue(form.is_valid())

    def test_patient_update_form_default_date(self):
        form = AppointmentPatientUpdateForm(data={
            'date': '13.01.2012 23:59',
            'first_name': 'Kacper',
            'last_name': 'Sawicki',
            'phone_number': '000000000',
            'choice': self.service
        }, office=self.appointment_office1, appointment=1, date='15.12.2020 23:59', service_name='Konsultacja')
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_patient_update_form_date_not_correct_with_office_hours(self):
        form = AppointmentPatientUpdateForm(data={
            'date': '13.01.2012 10:00',
            'first_name': 'Kacper',
            'last_name': 'Sawicki',
            'phone_number': '000000000',
            'choice': self.service
        }, office=self.appointment_office1, appointment=1, date='15.12.2020 23:59', service_name='Konsultacja')
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)


class TestServiceForm(TestCase):

    def test_service_form_valid(self):
        form = ServiceForm(data={
            'name': 'Masaż',
            'duration': '10'
        })
        self.assertTrue(form.is_valid())

    def test_service_form_invalid_duration(self):
        form = ServiceForm(data={
            'name': 'Masaż',
            'duration': '-1'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
