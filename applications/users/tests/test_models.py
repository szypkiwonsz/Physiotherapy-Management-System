from PIL import Image
from django.core.exceptions import ValidationError
from django.test import TestCase

from applications.users.models import User, UserPatient, UserOffice, OfficeDay


class TestUserPatientModels(TestCase):

    def setUp(self):
        self.patient1 = User.objects.create_user(
            'patient', 'patient@gmail.com', 'patientpassword', is_patient=True
        )
        self.user_patient1 = UserPatient.objects.create(
            user=self.patient1,
            phone_number=000000000
        )

    def test_string_representation(self):
        self.assertEquals(str(self.user_patient1), self.patient1.email)


class TestOfficeModels(TestCase):

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

    def test_string_representation(self):
        self.assertEquals(str(self.appointment_office1), self.office1.email)


class TestProfileModels(TestCase):

    def setUp(self):
        self.patient1 = User.objects.create_user(
            'patient', 'patient@gmail.com', 'patientpassword', is_patient=True
        )

    def test_string_representation(self):
        self.assertEquals(str(self.patient1.profile), self.patient1.email)

    def test_change_image_resolution_on_creation(self):
        img = Image.open(self.patient1.profile.image)
        self.assertLess(img.height, 100)
        self.assertLess(img.width, 100)


class TestOfficeDayModels(TestCase):

    def setUp(self):
        self.office_user1 = User.objects.create_user(
            'office', 'office@gmail.com', 'officepassword', is_office=True
        )
        self.office1 = UserOffice.objects.create(
            user=self.office_user1,
            name='name',
            address='address',
            city='City',
            phone_number='000000000',
            website='www.website.com'
        )

    def test_save_method(self):
        OfficeDay.objects.create(
            day=0, office=self.office1, earliest_appointment_time='12:00', latest_appointment_time='18:00'
        )
        # ID=8 taken because 7 OfficeDay objects were automatically created when creating an office.
        office_day = OfficeDay.objects.get(id=8)
        self.assertEqual(office_day.day, '0')
        self.assertEqual(office_day.earliest_appointment_time, '12:00')

    def test_save_method_incorrect_data(self):
        with self.assertRaises(ValidationError):
            OfficeDay.objects.create(
                day=0, office=self.office1, earliest_appointment_time='12:00', latest_appointment_time='11:00'
            )

    def test_string_representation(self):
        pass
