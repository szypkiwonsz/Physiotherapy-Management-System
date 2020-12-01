from django.core.exceptions import ValidationError
from django.test import TestCase

from applications.office_panel.models import Patient
from applications.users.models import User


class TestOfficePanelModels(TestCase):

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

    def test_patient_name_is_capitalized_on_creation(self):
        self.assertEquals(self.office_patient1.first_name, 'Firstname')
        self.assertEquals(self.office_patient1.last_name, 'Lastname')

    def test_string_representation(self):
        self.assertEquals(
            str(self.office_patient1), f'{self.office_patient1.first_name} {self.office_patient1.last_name}'
        )

    def test_save_method(self):
        Patient.objects.create(
            owner=self.office1,
            first_name='firstname',
            last_name='lastname',
            email='new_patient_email@gmail.com',
        )
        # ID=2 taken because first Patient was created in setUp method
        patient = Patient.objects.get(id=2)
        self.assertEqual(patient.email, 'new_patient_email@gmail.com')
