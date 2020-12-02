from django.test import TestCase
from django.utils import timezone

from applications.medical_history.models import MedicalHistory
from applications.office_panel.models import Patient
from applications.users.models import User


class TestMedicalHistoryModels(TestCase):

    def setUp(self):
        self.office1 = User.objects.create_user(
            'office', 'office@gmail.com', 'officepassword', is_office=True
        )
        self.office_patient1 = Patient.objects.create(
            owner=self.office1,
            first_name='firstname',
            last_name='lastname',
            email='patient@gmail.com'
        )
        self.medical_history1 = MedicalHistory.objects.create(
            owner=self.office1,
            patient=self.office_patient1,
            description='description',
            recommendations='recommendations',
            date_selected=timezone.now()
        )

    def test_string_representation(self):
        self.assertEquals(
            str(self.medical_history1), f'{self.office_patient1.first_name} {self.office_patient1.last_name}'
        )
