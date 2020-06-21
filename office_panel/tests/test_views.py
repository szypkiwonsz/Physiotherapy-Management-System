from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from medical_history.models import MedicalHistory
from users.models import User, Patient


class TestMedicalHistoryViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.medical_history_url = reverse('office-medical-history')
        self.make_medical_history_url = reverse('office-make-medical-history')
        self.detail_medical_history_url = reverse('office-medical-history-detail', args=[1])
        # self.update_medical_history_url = reverse('office_panel:office-medical-history-change', args=[1])
        # self.delete_medical_history_url = reverse('office_panel:office-medical-history-delete', args=[1])
        self.patient1 = User.objects.create_user(
            'patient', 'patient@gmail.com', 'patientpassword', is_patient=True
        )
        self.patient1.save()
        self.office1 = User.objects.create_user(
            'office', 'office@gmail.com', 'officepassword', is_office=True
        )
        self.office1.save()
        self.office_patient1 = Patient.objects.create(
            owner=self.office1,
            first_name='firstname',
            last_name='lastname',
            email='patient@gmail.com'
        )
        self.office_patient1.save()
        self.medical_history1 = MedicalHistory.objects.create(
            owner=self.office1,
            patient=self.office_patient1,
            description='description',
            recommendations='recommendations',
            date_selected=timezone.now(),
        )
        self.medical_history1.save()

    def test_medical_history_list_GET_no_logged_in(self):
        response = self.client.get(self.medical_history_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'office_panel/office_medical_history.html')

    def test_medical_history_list_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.medical_history_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'office_panel/office_medical_history.html')

    def test_medical_history_list_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.medical_history_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'office_panel/office_medical_history.html')

    def test_make_medical_history_create_GET_no_logged_in(self):
        response = self.client.get(self.make_medical_history_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'medical_history/medical_history_detail_form.html')

    def test_make_medical_history_create_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.make_medical_history_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'medical_history/medical_history_detail_form.html')

    def test_make_medical_history_create_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.make_medical_history_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'medical_history/medical_history_detail_form.html')

    # def test_make_medical_history_create_POST(self):
    #     url = reverse('office-make-medical-history')
    #     self.client.login(username='office@gmail.com', password='officepassword')
    #     response = self.client.post(url, {
    #         'patient': Patient.objects.get(pk=1),
    #         'description': 'description',
    #         'recommendations': 'recommendations'
    #     })
    #     print(response)
    #     medical_history2 = MedicalHistory.objects.get(id=2)
    #     self.assertEquals(medical_history2.description, 'description')

    def test_medical_history_detail_GET_no_logged_in(self):
        response = self.client.get(self.detail_medical_history_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'medical_history/medical_history_detail_form.html')

    def test_medical_history_detail_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.detail_medical_history_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'medical_history/medical_history_detail_form.html')

    def test_medical_history_detail_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.detail_medical_history_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'medical_history/medical_history_detail_form.html')
