from PIL import Image
from django.test import TestCase

from users.models import User, UserPatient, Office


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
        self.appointment_office1 = Office.objects.create(
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
