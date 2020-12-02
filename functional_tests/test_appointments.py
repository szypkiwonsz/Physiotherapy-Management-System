from datetime import datetime, timedelta
from time import sleep

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver

from applications.appointments.models import Appointment
from applications.office_panel.models import Patient
from applications.users.models import User, Office
from utils.add_zero import add_zero


class TestOfficeAppointments(StaticLiveServerTestCase):

    def setUp(self):
        self.tomorrow = datetime.today() + timedelta(1)
        self.patient1 = User.objects.create_user(
            'patient', 'patient@gmail.com', 'patientpassword', is_patient=True
        )
        self.office_user1 = User.objects.create_user(
            'office', 'office@gmail.com', 'officepassword', is_office=True
        )
        self.office1 = Office.objects.create(
            user=self.office_user1,
            name='name',
            address='address',
            city='City',
            phone_number='000000000',
            website='www.website.com'
        )
        self.appointment1 = Appointment.objects.create(
            owner=self.patient1,
            office=self.office1,
            date=self.tomorrow,
            first_name='Kacper',
            last_name='Sawicki',
            patient_email='patient@gmail.com',
            date_selected=datetime(2020, 8, 21, 17, 00, 00),
            phone_number='000000000',
            confirmed=False,
            choice='Konsultacja'
        )
        self.office_patient1 = Patient.objects.create(
            owner=self.office_user1,
            first_name='firstname',
            last_name='lastname',
            email='patient@gmail.com',
        )
        self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')

    def tearDown(self):
        self.browser.close()

    def test_appointments(self):
        self.browser.get(self.live_server_url + reverse('login'))
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[4]/div/a').click()
        appointments_text = self.browser.find_element_by_class_name('text-description').text
        self.assertEquals(
            appointments_text,
            'Wszystkie wizyty:'
        )

    def test_appointment_edit_button_redirects_to_edit_appointment(self):
        self.browser.get(self.live_server_url + reverse('login'))
        appointment_edit_url = self.live_server_url + reverse(
            'office_panel:appointments:update', args=[self.appointment1.pk]
        )
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[4]/div/a').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="replaceable-content"]/div[3]/a[1]').click()
        self.assertEquals(
            self.browser.current_url,
            appointment_edit_url
        )

    def test_appointment_delete_button_redirects_to_delete_appointment(self):
        self.browser.get(self.live_server_url + reverse('login'))
        appointment_delete_url = self.live_server_url + reverse(
            'office_panel:appointments:delete', args=[self.appointment1.pk]
        )
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[4]/div/a').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="replaceable-content"]/div[3]/a[2]').click()
        self.assertEquals(
            self.browser.current_url,
            appointment_delete_url
        )


class TestPatientAppointments(StaticLiveServerTestCase):

    def setUp(self):
        self.tomorrow = datetime.today() + timedelta(1)
        self.patient1 = User.objects.create_user(
            'patient', 'patient@gmail.com', 'patientpassword', is_patient=True
        )
        self.office_user1 = User.objects.create_user(
            'office', 'office@gmail.com', 'officepassword', is_office=True
        )
        self.office1 = Office.objects.create(
            user=self.office_user1,
            name='name',
            address='address',
            city='City',
            phone_number='000000000',
            website='www.website.com'
        )
        self.appointment1 = Appointment.objects.create(
            owner=self.patient1,
            office=self.office1,
            date=self.tomorrow,
            first_name='Kacper',
            last_name='Sawicki',
            patient_email='patient@gmail.com',
            date_selected=datetime(2020, 8, 21, 17, 00, 00),
            phone_number='000000000',
            confirmed=False,
            choice='Konsultacja'
        )
        self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')

    def tearDown(self):
        self.browser.close()

    def test_appointments(self):
        self.browser.get(self.live_server_url + reverse('login'))
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('patient@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('patientpassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('/html/body/div[3]/div/a').click()
        appointments_text = self.browser.find_element_by_class_name('text-description').text
        self.assertEquals(
            appointments_text,
            f'name, {add_zero(self.tomorrow.day)}.{add_zero(self.tomorrow.month)}.'
            f'{self.tomorrow.year}, o godz: {add_zero(self.tomorrow.hour)}:{add_zero(self.tomorrow.minute)} '
            f'- Konsultacja [Niepotwierdzona]'
        )

    def test_edit_appointment_button_redirects_to_edit_appointment(self):
        self.browser.get(self.live_server_url + reverse('login'))
        appointment_edit_url = self.live_server_url + reverse(
            'patient_panel:appointments:update', args=[self.appointment1.pk]
        )
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('patient@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('patientpassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('/html/body/div[3]/div/a').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="replaceable-content"]/div[2]/a[1]').click()
        self.assertEquals(
            self.browser.current_url,
            appointment_edit_url
        )

    def test_delete_appointment_button_redirects_to_delete_appointment(self):
        self.browser.get(self.live_server_url + reverse('login'))
        appointment_delete_url = self.live_server_url + reverse(
            'patient_panel:appointments:delete', args=[self.appointment1.pk]
        )
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('patient@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('patientpassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('/html/body/div[3]/div/a').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="replaceable-content"]/div[2]/a[2]').click()
        self.assertEquals(
            self.browser.current_url,
            appointment_delete_url
        )
