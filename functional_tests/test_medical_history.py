from datetime import datetime
from time import sleep

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver

from medical_history.models import MedicalHistory
from office_panel.models import Patient
from users.models import User


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
        self.medical_history1 = MedicalHistory.objects.create(
            owner=self.office_user1,
            patient=self.office_patient1,
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
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[4]/div/div[5]/a[1]').click()
        medical_history_text = self.browser.find_element_by_class_name('text-description').text
        self.assertEquals(
            medical_history_text,
            'Wszystkie historie medyczne'
        )

    def test_add_medical_history_button_redirects_to_add_medical_history(self):
        self.browser.get(self.live_server_url + reverse('login'))
        medical_history_add_url = self.live_server_url + reverse('office-make-medical-history')
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[4]/div/div[5]/a[1]').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="replaceable-content"]/div[2]/a').click()
        self.assertEquals(
            self.browser.current_url,
            medical_history_add_url
        )

    def test_medical_history_edit_button_redirects_to_edit_medical_history(self):
        self.browser.get(self.live_server_url + reverse('login'))
        medical_history_edit_url = self.live_server_url + reverse(
            'office-medical-history-change', args=[self.medical_history1.pk]
        )
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[4]/div/div[5]/a[1]').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="replaceable-content"]/div[6]/a[1]').click()
        self.assertEquals(
            self.browser.current_url,
            medical_history_edit_url
        )

    def test_medical_history_delete_button_redirects_to_delete_medical_history(self):
        self.browser.get(self.live_server_url + reverse('login'))
        medical_history_delete_url = self.live_server_url + reverse(
            'office-medical-history-delete', args=[self.medical_history1.pk]
        )
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[4]/div/div[5]/a[1]').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="replaceable-content"]/div[6]/a[2]').click()
        self.assertEquals(
            self.browser.current_url,
            medical_history_delete_url
        )

    def test_medical_history_detail_redirects_to_medical_history_detail(self):
        self.browser.get(self.live_server_url + reverse('login'))
        medical_history_detail_url = self.live_server_url + reverse(
            'office-medical-history-detail', args=[self.medical_history1.pk]
        )
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[4]/div/div[5]/a[1]').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="replaceable-content"]/a').click()
        self.assertEquals(
            self.browser.current_url,
            medical_history_detail_url
        )

    def test_patient_detail_redirects_to_patient_detail(self):
        self.browser.get(self.live_server_url + reverse('login'))
        patient_detail_url = self.live_server_url + reverse('office-patient-detail', args=[self.office_patient1.pk])
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[4]/div/div[5]/a[1]').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="replaceable-content"]/div[3]/a').click()
        self.assertEquals(
            self.browser.current_url,
            patient_detail_url
        )
