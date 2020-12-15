from django.test import TestCase, Client
from django.urls import reverse

from applications.office_panel.models import Patient
from applications.users.models import User, UserOffice


class TestHomeViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.office_home_url = reverse('office_panel:home')
        self.patient1 = User.objects.create_user(
            'patient', 'patient@gmail.com', 'patientpassword', is_patient=True
        )
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

    def test_office_home_GET_not_logged_in(self):
        response = self.client.get(self.office_home_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'office_panel/home.html')

    def test_office_home_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.office_home_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'office_panel/home.html')

    def test_office_home_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.office_home_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'office_panel/home.html')


class TestPatientViews(TestCase):

    def setUp(self):
        self.patient_url = reverse('office_panel:patients')
        self.create_patient_url = reverse('office_panel:patient_add')
        self.detail_patient_url = reverse('office_panel:patient_detail', args=[1])
        self.update_patient_url = reverse('office_panel:patient_update', args=[1])
        self.delete_patient_url = reverse('office_panel:patient_delete', args=[1])
        self.timetable_url = reverse('office_panel:timetable')
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
        )

    def test_patient_list_GET_not_logged_in(self):
        response = self.client.get(self.patient_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'office_panel/patient/patients.html')

    def test_patient_list_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.patient_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'office_panel/patient/patients.html')

    def test_patient_list_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.patient_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'office_panel/patient/patients.html')

    def test_patient_create_GET_not_logged_in(self):
        response = self.client.get(self.create_patient_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'office_panel/patient/patient_add_form.html')

    def test_patient_create_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.create_patient_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'office_panel/patient/patient_add_form.html')

    def test_patient_create_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.create_patient_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'office_panel/patient/patient_add_form.html')

    def test_patient_create_POST(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.post(self.create_patient_url, {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'patient2@gmail.com',
            'phone_number': '000000000'
        })
        office_patient2 = Patient.objects.get(id=2)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(office_patient2.first_name, 'Firstname')

    def test_patient_detail_GET_no_logged_in(self):
        response = self.client.get(self.detail_patient_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'office_panel/patient/patient_detail_form.html')

    def test_patient_detail_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.detail_patient_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'office_panel/patient/patient_detail_form.html')

    def test_patient_detail_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.detail_patient_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'office_panel/patient/patient_detail_form.html')

    def test_patient_update_GET_no_logged_in(self):
        response = self.client.get(self.update_patient_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'office_panel/patient/patient_update_form.html')

    def test_patient_update_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.update_patient_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'office_panel/patient/patient_update_form.html')

    def test_patient_update_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.update_patient_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'office_panel/patient/patient_update_form.html')

    def test_patient_update_POST(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.post(self.update_patient_url, {
            'first_name': self.office_patient1.first_name,
            'last_name': self.office_patient1.last_name,
            'email': 'newpatientemail@gmail.com',
            'phone_number': '000000000'
        })
        office_patient_update = Patient.objects.get(id=1)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(office_patient_update.email, 'newpatientemail@gmail.com')

    def test_patient_delete_GET_not_logged_in(self):
        response = self.client.get(self.delete_patient_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'office_panel/patient/patient_delete_confirm.html')

    def test_patient_delete_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.delete_patient_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'office_panel/patient/patient_delete_confirm.html')

    def test_patient_delete_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.delete_patient_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'office_panel/patient/patient_delete_confirm.html')

    def test_patient_delete_POST(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response_with_post = self.client.get(self.delete_patient_url)
        self.assertEquals(response_with_post.status_code, 200)
        response = self.client.post(self.delete_patient_url)
        response_with_deleted_post = self.client.get(self.delete_patient_url)
        self.assertEquals(response_with_deleted_post.status_code, 404)


class TestTimetableViews(TestCase):

    def setUp(self):
        self.timetable_url = reverse('office_panel:timetable')
        self.patient1 = User.objects.create_user(
            'patient', 'patient@gmail.com', 'patientpassword', is_patient=True
        )
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

    def test_timetable_GET_not_logged_in(self):
        response = self.client.get(self.timetable_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'office_panel/timetable/timetable.html')

    def test_timetable_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.timetable_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'office_panel/timetable/timetable.html')

    def test_timetable_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.timetable_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'office_panel/timetable/timetable.html')
