from datetime import datetime
from time import sleep

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver

from applications.appointments.models import Appointment
from applications.medical_history.models import MedicalHistory
from applications.office_panel.models import Patient
from applications.users.models import User, Office


class TestOfficeMedicalHistory(StaticLiveServerTestCase):

    def setUp(self):
        self.patient1 = User.objects.create_user(
            'patient', 'patient@gmail.com', 'patientpassword', is_patient=True
        )
        self.office_user1 = User.objects.create_user(
            'office', 'office@gmail.com', 'officepassword', is_office=True
        )
        self.office_patient1 = Patient.objects.create(
            owner=self.office_user1,
            first_name='firstname',
            last_name='lastname',
            email='patient@gmail.com',
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
            patient_email='patient@gmail.com',
            date=datetime(datetime.today().year, datetime.today().month, 2),
            first_name='Kacper',
            last_name='Sawicki',
            date_selected=datetime(2020, 8, 21, 17, 00, 00),
            phone_number='000000000',
            confirmed=False,
            choice='Konsultacja'
        )
        self.medical_history1 = MedicalHistory.objects.create(
            owner=self.office_user1,
            patient=self.office_patient1,
            appointment=self.appointment1,
            description='description',
            recommendations='recommendations',
            date_selected=datetime(2020, 8, 21, 17, 00, 00),
        )
        self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')

    def tearDown(self):
        self.browser.close()

    def test_medical_histories(self):
        self.browser.get(self.live_server_url + reverse('login'))
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[5]/div/div[6]/a[1]').click()
        medical_history_text = self.browser.find_element_by_class_name('text-description').text
        self.assertEquals(
            medical_history_text,
            'Wszystkie historie medyczne'
        )

    def test_add_medical_history_button_redirects_to_add_medical_history(self):
        self.browser.get(self.live_server_url + reverse('login'))
        medical_history_add_url = self.live_server_url + reverse('office_panel:medical_history:make')
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[5]/div/div[6]/a[1]').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="replaceable-content"]/div[2]/a').click()
        self.assertEquals(
            self.browser.current_url,
            medical_history_add_url
        )

    def test_medical_history_edit_button_redirects_to_edit_medical_history(self):
        self.browser.get(self.live_server_url + reverse('login'))
        medical_history_edit_url = self.live_server_url + reverse(
            'office_panel:medical_history:update', args=[self.medical_history1.pk]
        )
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[5]/div/div[6]/a[1]').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="replaceable-content"]/div[7]/a[1]').click()
        self.assertEquals(
            self.browser.current_url,
            medical_history_edit_url
        )

    def test_medical_history_delete_button_redirects_to_delete_medical_history(self):
        self.browser.get(self.live_server_url + reverse('login'))
        medical_history_delete_url = self.live_server_url + reverse(
            'office_panel:medical_history:delete', args=[self.medical_history1.pk]
        )
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[5]/div/div[6]/a[1]').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="replaceable-content"]/div[7]/a[2]').click()
        self.assertEquals(
            self.browser.current_url,
            medical_history_delete_url
        )

    def test_medical_history_detail_redirects_to_medical_history_detail(self):
        self.browser.get(self.live_server_url + reverse('login'))
        medical_history_detail_url = self.live_server_url + reverse(
            'office_panel:medical_history:detail', args=[self.medical_history1.pk]
        )
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[5]/div/div[6]/a[1]').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="replaceable-content"]/a').click()
        self.assertEquals(
            self.browser.current_url,
            medical_history_detail_url
        )

    def test_patient_detail_redirects_to_patient_detail(self):
        self.browser.get(self.live_server_url + reverse('login'))
        patient_detail_url = self.live_server_url + reverse(
            'office_panel:patient_detail', args=[self.office_patient1.pk]
        )
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[5]/div/div[6]/a[1]').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="replaceable-content"]/div[3]/a').click()
        self.assertEquals(
            self.browser.current_url,
            patient_detail_url
        )
