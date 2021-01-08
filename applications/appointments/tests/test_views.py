from datetime import datetime

from django.test import TestCase, Client
from django.urls import reverse

from applications.appointments.models import Appointment, Service
from applications.office_panel.models import Patient
from applications.users.models import User, UserOffice


class TestOfficeAppointmentViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.appointment_list_url = reverse('office_panel:appointments:list')
        self.make_appointment_url = reverse('office_panel:appointments:make', args=[2, '15.12.2020 11:40', 'Masaż'])
        self.update_appointment_url = reverse('office_panel:appointments:update', args=[1])
        self.delete_appointment_url = reverse('office_panel:appointments:delete', args=[1])
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
            first_name='Kacper',
            last_name='Sawicki',
            date_selected=datetime(2012, 1, 13, 23, 51, 34),
            phone_number='000000000',
            confirmed=False,
            service=self.service
        )

    def test_appointment_list_GET_not_logged_in(self):
        response = self.client.get(self.appointment_list_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/office_appointments.html')

    def test_appointment_list_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.appointment_list_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/office_appointments.html')

    def test_appointment_list_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.appointment_list_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointments/office/appointments.html')

    def test_appointment_update_GET_not_logged_in(self):
        response = self.client.get(self.update_appointment_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/office/appointment_update_form.html')

    def test_appointment_update_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.update_appointment_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/office_appointment_update_form.html')

    def test_appointment_update_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.update_appointment_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointments/office/appointment_update_form.html')

    def test_appointment_update_POST(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.post(self.update_appointment_url, {
            'date': '06.01.2021 15:00',
            'confirmed': True,
            'service': self.service.pk
        })
        appointment_update = Appointment.objects.get(id=1)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(appointment_update.confirmed, True)

    def test_appointment_delete_GET_not_logged_in(self):
        response = self.client.get(self.delete_appointment_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/office/appointment_delete_confirm.html')

    def test_appointment_delete_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.delete_appointment_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/office/appointment_delete_confirm.html')

    def test_appointment_delete_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.delete_appointment_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointments/office/appointment_delete_confirm.html')

    def test_appointment_delete_POST(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response_with_post = self.client.get(self.delete_appointment_url)
        self.assertEquals(response_with_post.status_code, 200)
        response = self.client.post(self.delete_appointment_url)
        response_with_deleted_post = self.client.get(self.update_appointment_url)
        self.assertEquals(response_with_deleted_post.status_code, 404)

    def test_make_appointment_create_GET_not_logged_in(self):
        response = self.client.get(self.make_appointment_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/office_panel/appointment_make_form.html')

    def test_make_appointment_create_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.make_appointment_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/office_panel/appointment_make_form.html')


class TestPatientAppointmentViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.select_office_url = reverse('patient_panel:appointments:select')
        self.make_appointment_url = reverse(
            'patient_panel:appointments:make', args=[2, f'{str(datetime.now().strftime("%d.%m.%Y"))} '
                                                        f'11:00', 'Konsultacja']
        )
        self.upcoming_appointments_list_url = reverse('patient_panel:appointments:upcoming')
        self.old_appointments_list_url = reverse('patient_panel:appointments:old')
        self.update_appointment_url = reverse('patient_panel:appointments:update', args=[1])
        self.delete_appointment_url = reverse('patient_panel:appointments:delete', args=[1])
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
            first_name='Kacper',
            last_name='Sawicki',
            date_selected=datetime(2012, 1, 13, 23, 51, 34),
            phone_number='000000000',
            confirmed=False,
            service=self.service
        )
        self.appointment2 = Appointment.objects.create(
            owner=self.patient1,
            office=self.appointment_office1,
            patient_email='patient@gmail.com',
            date=datetime(2018, 1, 13, 16, 00, 00),
            first_name='Kacper',
            last_name='Sawicki',
            date_selected=datetime(2018, 1, 13, 23, 51, 34),
            phone_number='000000000',
            confirmed=False,
            service=self.service
        )

    def test_select_office_GET_not_logged_in(self):
        response = self.client.get(self.select_office_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/patient/appointment_select_office.html')

    def test_select_office_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.select_office_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointments/patient/appointment_select_office.html')

    def test_select_office_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.select_office_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/patient/appointment_select_office.html')

    def test_make_appointment_create_GET_not_logged_in(self):
        response = self.client.get(self.make_appointment_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/patient/appointment_make_form.html')

    def test_make_appointment_create_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.make_appointment_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointments/patient/appointment_make_form.html')

    def test_make_appointment_create_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.make_appointment_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/patient/appointment_make_form.html')

    def test_make_appointment_create_POST(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.post(self.make_appointment_url, {
            'date': str(datetime.now().strftime('%d.%m.%Y') + ' 11:00'),
            'first_name': self.appointment1.first_name,
            'last_name': self.appointment1.last_name,
            'phone_number': '000000001',
            'service': self.service.pk
        })
        appointment2 = Appointment.objects.get(id=3)
        self.assertEquals(
            appointment2.date, datetime.strptime(str(datetime.now().strftime('%d.%m.%Y') + ' 11:00'), '%d.%m.%Y %H:%M'))
        self.assertEquals(appointment2.office_id, 2)
        self.assertEquals(appointment2.confirmed, False)

    def test_make_appointment_create_too_early_time_POST(self):
        # the default earliest time is: 11:00
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.post(self.make_appointment_url, {
            'date': '25.12.2020 11:00',
            'first_name': self.appointment1.first_name,
            'last_name': self.appointment1.last_name,
            'phone_number': '000000000',
        })
        with self.assertRaises(Appointment.DoesNotExist):
            Appointment.objects.get(id=3)

    def test_make_appointment_create_too_late_time_POST(self):
        # the default latest time is 18:00
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.post(self.make_appointment_url, {
            'first_name': self.appointment1.first_name,
            'last_name': self.appointment1.last_name,
            'phone_number': '000000000'
        })
        with self.assertRaises(Appointment.DoesNotExist):
            Appointment.objects.get(id=3)

    def test_make_appointment_create_date_taken_POST(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.post(self.make_appointment_url, {
            'date': '13.01.2012 16:00',
            'first_name': self.appointment1.first_name,
            'last_name': self.appointment1.last_name,
            'phone_number': '000000000',
            'service': 'Konsultacja'
        })
        with self.assertRaises(Appointment.DoesNotExist):
            Appointment.objects.get(id=3)

    def test_upcoming_appointment_list_GET_not_logged_in(self):
        response = self.client.get(self.upcoming_appointments_list_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/patient/appointments_upcoming.html')

    def test_upcoming_appointment_list_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.upcoming_appointments_list_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointments/patient/appointments_upcoming.html')

    def test_upcoming_appointment_list_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.upcoming_appointments_list_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/patient/appointments_upcoming.html')

    def test_old_appointment_list_GET_not_logged_in(self):
        response = self.client.get(self.old_appointments_list_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/patient/appointments_old.html')

    def test_old_appointment_list_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.old_appointments_list_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointments/patient/appointments_old.html')

    def test_old_appointment_list_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.old_appointments_list_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/patient/appointments_old.html')

    def test_update_appointment_GET_not_logged_in(self):
        response = self.client.get(self.update_appointment_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/patient/appointment_update_form.html')

    def test_update_appointment_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.update_appointment_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointments/patient/appointment_update_form.html')

    def test_update_appointment_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.update_appointment_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/patient/appointment_update_form.html')

    def test_update_appointment_POST(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.post(self.update_appointment_url, {
            'date': '17.12.2020 17:00',
            'first_name': self.appointment1.first_name,
            'last_name': self.appointment1.last_name,
            'phone_number': '111111111',
            'service': self.service.pk
        })
        appointment_update = Appointment.objects.get(id=1)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(appointment_update.confirmed, False)
        self.assertEquals(appointment_update.phone_number, '111111111')

    def test_update_appointment_date_taken_POST(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.post(self.update_appointment_url, {
            'date': '13.01.2018 16:00',
            'first_name': self.appointment1.first_name,
            'last_name': self.appointment1.last_name,
            'phone_number': '111111111',
            'service': self.service
        })
        appointment_update = Appointment.objects.get(id=1)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(appointment_update.confirmed, False)
        self.assertEquals(appointment_update.phone_number, '000000000')

    def test_delete_appointment_GET_not_logged_in(self):
        response = self.client.get(self.delete_appointment_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/patient/appointment_cancel_confirm.html')

    def test_delete_appointment_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.delete_appointment_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointments/patient/appointment_cancel_confirm.html')

    def test_delete_appointment_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.delete_appointment_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/patient/appointment_cancel_confirm.html')

    def test_delete_appointment_POST(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.post(self.delete_appointment_url)
        self.assertEquals(response.status_code, 302)
        response_with_deleted_post = self.client.get(self.update_appointment_url)
        self.assertEquals(response_with_deleted_post.status_code, 404)


class TestOfficeTimetableViews(TestCase):

    def setUp(self):
        self.timetable_url = reverse('office_panel:appointments:timetable')
        self.patient1 = User.objects.create_user(
            'patient', 'patient@gmail.com', 'patientpassword', is_patient=True
        )
        self.office1 = User.objects.create_user(
            'office', 'office@gmail.com', 'officepassword', is_office=True
        )
        self.timetable_office1 = UserOffice.objects.create(
            user=self.office1,
            name='name',
            address='address',
            city='City',
            phone_number='000000000',
            website='www.website.com'
        )

    def test_timetable_GET_not_logged_in(self):
        response = self.client.get(self.timetable_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/timetable.html')

    def test_timetable_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.timetable_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/timetable.html')

    def test_timetable_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.timetable_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointments/timetable.html')


class TestPatientTimetableViews(TestCase):

    def setUp(self):
        self.timetable_url = reverse('patient_panel:appointments:timetable', args=[1])
        self.patient1 = User.objects.create_user(
            'patient', 'patient@gmail.com', 'patientpassword', is_patient=True
        )
        self.office1 = User.objects.create_user(
            'office', 'office@gmail.com', 'officepassword', is_office=True
        )
        self.timetable_office1 = UserOffice.objects.create(
            user=self.office1,
            name='name',
            address='address',
            city='City',
            phone_number='000000000',
            website='www.website.com'
        )

    def test_timetable_GET_not_logged_in(self):
        response = self.client.get(self.timetable_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/timetable.html')

    def test_timetable_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.timetable_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointments/timetable.html')

    def test_timetable_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.timetable_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/timetable.html')


class TestServiceViews(TestCase):

    def setUp(self):
        self.add_service_url = reverse('office_panel:appointments:service_add')
        self.delete_service_url = reverse('office_panel:appointments:service_delete', args=[1])
        self.edit_service_url = reverse('office_panel:appointments:service_edit', args=[1])
        self.list_service_url = reverse('office_panel:appointments:service_list')
        self.patient1 = User.objects.create_user(
            'patient', 'patient@gmail.com', 'patientpassword', is_patient=True
        )
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
            name='Konsultacja',
            duration=10
        )

    def test_add_service_GET_not_logged_in(self):
        response = self.client.get(self.add_service_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/office/service_add_form.html')

    def test_add_service_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.add_service_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/office/service_add_form.html')

    def test_add_service_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.add_service_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointments/office/service_add_form.html')

    def test_add_service_POST(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.post(self.add_service_url, {
            'name': 'Masaż',
            'duration': '10'
        })
        service_added = Service.objects.get(id=2)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(service_added.name, 'Masaż')
        self.assertEquals(service_added.duration, 10)

    def test_delete_service_GET_not_logged_in(self):
        response = self.client.get(self.delete_service_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/office/service_delete_confirm.html')

    def test_delete_service_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.delete_service_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/office/service_delete_confirm.html')

    def test_delete_service_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.delete_service_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointments/office/service_delete_confirm.html')

    def test_delete_service_POST(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.post(self.delete_service_url)
        self.assertEquals(response.status_code, 302)
        response_with_deleted_service = self.client.get(self.delete_service_url)
        self.assertEquals(response_with_deleted_service.status_code, 404)

    def test_edit_service_GET_not_logged_in(self):
        response = self.client.get(self.edit_service_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/office/service_update_form.html')

    def test_edit_service_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.edit_service_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/office/service_update_form.html')

    def test_edit_service_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.edit_service_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointments/office/service_update_form.html')

    def test_edit_service_POST(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.post(self.edit_service_url, {
            'name': 'Zabieg',
            'duration': '10'
        })
        self.assertEquals(response.status_code, 302)
        service_edited = Service.objects.get(id=1)
        self.assertEquals(service_edited.name, 'Zabieg')

    def test_list_service_GET_not_logged_in(self):
        response = self.client.get(self.list_service_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/office/services.html')

    def test_list_service_GET_logged_as_patient(self):
        self.client.login(username='patient@gmail.com', password='patientpassword')
        response = self.client.get(self.list_service_url)

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'appointments/office/services.html')

    def test_list_service_GET_logged_as_office(self):
        self.client.login(username='office@gmail.com', password='officepassword')
        response = self.client.get(self.list_service_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointments/office/services.html')
