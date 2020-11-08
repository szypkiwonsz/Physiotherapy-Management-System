from datetime import datetime
from time import sleep

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver

from applications.appointments.models import Appointment
from applications.medical_history.models import MedicalHistory
from applications.office_panel.models import Patient
from applications.users.models import User, Office
from utils.add_zero import add_zero


class TestHomeNoData(StaticLiveServerTestCase):

    def setUp(self):
        self.office1 = User.objects.create_user(
            'office', 'office@gmail.com', 'officepassword', is_office=True
        )
        self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')

    def tearDown(self):
        self.browser.close()

    def test_no_patients_text(self):
        self.browser.get(self.live_server_url + reverse('login'))
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        no_offices_text = self.browser.find_element_by_class_name('form').text
        self.assertEquals(
            no_offices_text,
            'Nie masz żadnych pacjentów.\nDodaj ich tutaj'
        )

    def test_add_patient_button_redirects_to_add_patient(self):
        self.browser.get(self.live_server_url + reverse('login'))
        add_patient_button = self.live_server_url + reverse('office_panel:patient_add')
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[2]/div/a').click()
        self.assertEquals(
            self.browser.current_url,
            add_patient_button
        )

    def test_no_appointments_text(self):
        self.browser.get(self.live_server_url + reverse('login'))
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        no_appointments = self.browser.find_elements_by_class_name('form')[1].text
        self.assertEquals(
            no_appointments,
            'Nie masz umówionych żadnych wizyt.\n(tutaj pojawią się wizyty, które umówią pacjenci do twojego gabinetu.)'
        )

    def test_no_medical_histories_text(self):
        self.browser.get(self.live_server_url + reverse('login'))
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        no_medical_histories_text = self.browser.find_elements_by_class_name('form')[2].text
        self.assertEquals(
            no_medical_histories_text,
            'Nie dodałeś żadnych historii.\nDodaj je tutaj'
        )

    def test_medical_histories_make_history_button_redirects_to_make_medical_history(self):
        self.browser.get(self.live_server_url + reverse('login'))
        add_medical_history_url = self.live_server_url + reverse('office_panel:medical_history:make')
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[4]/div/a').click()
        self.assertEquals(
            self.browser.current_url,
            add_medical_history_url
        )


class TestHome(StaticLiveServerTestCase):

    def setUp(self):
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
        self.office_patient1 = Patient.objects.create(
            owner=self.office_user1,
            first_name='firstname',
            last_name='lastname',
            email='patient@gmail.com',
        )
        self.appointment1 = Appointment.objects.create(
            owner=self.patient1,
            office=self.office1,
            date=datetime(datetime.today().year, datetime.today().month, datetime.today().day + 1),
            name='Kacper',
            date_selected=datetime(2020, 8, 21, 17, 00, 00),
            phone_number='000000000',
            confirmed=False,
            choice='Konsultacja'
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

    def test_patients(self):
        self.browser.get(self.live_server_url + reverse('login'))
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        patient_text = self.browser.find_element_by_class_name('text-description').text
        self.assertEquals(
            patient_text,
            'Firstname Lastname, patient@gmail.com'
        )

    def test_patient_detail_button_redirects_to_patient_detail(self):
        self.browser.get(self.live_server_url + reverse('login'))
        patient_detail_url = self.live_server_url + reverse(
            'office_panel:patient_detail', args=[self.office_patient1.pk]
        )
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[2]/div/div[1]/a').click()
        self.assertEquals(
            self.browser.current_url,
            patient_detail_url
        )

    def test_patients_all_button_redirects_to_patients_list(self):
        self.browser.get(self.live_server_url + reverse('login'))
        all_patients_url = self.live_server_url + reverse('office_panel:patients')
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[2]/div/div[3]/a[1]').click()
        self.assertEquals(
            self.browser.current_url,
            all_patients_url
        )

    def test_patient_edit_button_redirects_to_edit_patient(self):
        self.browser.get(self.live_server_url + reverse('login'))
        edit_patient_url = self.live_server_url + reverse('office_panel:patient_update', args=[self.office_patient1.pk])
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[2]/div/div[2]/a[1]').click()
        self.assertEquals(
            self.browser.current_url,
            edit_patient_url
        )

    def test_patient_delete_button_redirects_to_confirm_delete(self):
        self.browser.get(self.live_server_url + reverse('login'))
        delete_patient_url = self.live_server_url + reverse(
            'office_panel:patient_delete', args=[self.office_patient1.pk]
        )
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[2]/div/div[2]/a[2]').click()
        self.assertEquals(
            self.browser.current_url,
            delete_patient_url
        )

    def test_patients_add_button_redirects_to_patient_add(self):
        self.browser.get(self.live_server_url + reverse('login'))
        add_patient_url = self.live_server_url + reverse('office_panel:patient_add')
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[2]/div/div[3]/a[2]').click()
        self.assertEquals(
            self.browser.current_url,
            add_patient_url
        )

    def test_appointments(self):
        self.browser.get(self.live_server_url + reverse('login'))
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        appointment_text = self.browser.find_elements_by_class_name('text-description')[1].text
        self.assertEquals(
            appointment_text,
            f'patient@gmail.com, {add_zero(datetime.today().day + 1)}.'
            f'{add_zero(datetime.today().month)}.{datetime.today().year}, o godz: 00:00 - Konsultacja\n'
            f'[Niepotwierdzona]'
        )

    def test_appointments_all_button_redirects_to_all_appointments(self):
        self.browser.get(self.live_server_url + reverse('login'))
        all_appointments_url = self.live_server_url + reverse('office_panel:appointments:list')
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[3]/div/a').click()
        self.assertEquals(
            self.browser.current_url,
            all_appointments_url
        )

    def test_appointment_edit_button_redirects_to_edit_appointment(self):
        self.browser.get(self.live_server_url + reverse('login'))
        edit_appointment_url = self.live_server_url + reverse(
            'office_panel:appointments:update', args=[self.appointment1.pk]
        )
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[3]/div/div[2]/a[1]').click()
        self.assertEquals(
            self.browser.current_url,
            edit_appointment_url
        )

    def test_appointment_delete_button_redirects_to_confirm_delete(self):
        self.browser.get(self.live_server_url + reverse('login'))
        delete_appointment_url = self.live_server_url + reverse(
            'office_panel:appointments:delete', args=[self.appointment1.pk]
        )
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[3]/div/div[2]/a[2]').click()
        self.assertEquals(
            self.browser.current_url,
            delete_appointment_url
        )

    def test_medical_histories(self):
        self.browser.get(self.live_server_url + reverse('login'))
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        medical_history_text = self.browser.find_elements_by_class_name('form')[-1].text
        self.assertEquals(
            medical_history_text,
            'Ostatnio dodane historie:\nHistoria medyczna - 21.08.2020, 17:00\nPacjent: Firstname Lastname\nOpis:\n'
            'description\nZalecenia:\nrecommendations\nEdytuj Usuń\nPokaż wszystkie historie Dodaj'
        )

    def test_medical_history_detail_button_redirect_to_history_detail(self):
        self.browser.get(self.live_server_url + reverse('login'))
        medical_history_detail_url = self.live_server_url + reverse(
            'office_panel:medical_history:detail', args=[self.medical_history1.pk]
        )
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[4]/div/a[1]').click()
        self.assertEquals(
            self.browser.current_url,
            medical_history_detail_url
        )

    def test_medical_history_patient_detail_button_redirect_to_patient_detail(self):
        self.browser.get(self.live_server_url + reverse('login'))
        patient_detail_url = self.live_server_url + reverse(
            'office_panel:patient_detail', args=[self.office_patient1.pk]
        )
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[4]/div/div[1]/a').click()
        self.assertEquals(
            self.browser.current_url,
            patient_detail_url
        )

    def test_medical_histories_all_button_redirects_to_all_histories(self):
        self.browser.get(self.live_server_url + reverse('login'))
        all_medical_histories_url = self.live_server_url + reverse('office_panel:medical_history:list')
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[4]/div/div[5]/a[1]').click()
        self.assertEquals(
            self.browser.current_url,
            all_medical_histories_url
        )

    def test_medical_history_edit_button_redirects_to_edit_history(self):
        self.browser.get(self.live_server_url + reverse('login'))
        medical_history_change_url = self.live_server_url + reverse(
            'office_panel:medical_history:update', args=[self.medical_history1.pk]
        )
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[4]/div/div[4]/a[1]').click()
        self.assertEquals(
            self.browser.current_url,
            medical_history_change_url
        )

    def test_medical_history_delete_button_redirects_to_delete_history(self):
        self.browser.get(self.live_server_url + reverse('login'))
        delete_medical_history_url = self.live_server_url + reverse(
            'office_panel:medical_history:delete', args=[self.medical_history1.pk]
        )
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[4]/div/div[4]/a[2]').click()
        self.assertEquals(
            self.browser.current_url,
            delete_medical_history_url
        )

    def test_medical_history_add_button_redirects_to_add_medical_history(self):
        self.browser.get(self.live_server_url + reverse('login'))
        make_medical_history_url = self.live_server_url + reverse('office_panel:medical_history:make')
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[4]/div/div[5]/a[2]').click()
        self.assertEquals(
            self.browser.current_url,
            make_medical_history_url
        )


class TestPatientsNoData(StaticLiveServerTestCase):

    def setUp(self):
        self.office_user1 = User.objects.create_user(
            'office', 'office@gmail.com', 'officepassword', is_office=True
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

    def test_patients(self):
        self.browser.get(self.live_server_url + reverse('login'))
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        patient_text = self.browser.find_element_by_class_name('text-description').text
        self.assertEquals(
            patient_text,
            'Firstname Lastname, patient@gmail.com'
        )

    def test_patients_add_patient_button_redirect_to_add_patient(self):
        self.browser.get(self.live_server_url + reverse('login'))
        add_patient_url = self.live_server_url + reverse('office_panel:patient_add')
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[2]/div/div[3]/a[1]').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="replaceable-content"]/div[2]/a').click()
        self.assertEquals(
            self.browser.current_url,
            add_patient_url
        )

    def test_patient_detail_button_redirects_to_patient_detail(self):
        self.browser.get(self.live_server_url + reverse('login'))
        patient_detail_url = self.live_server_url + reverse(
            'office_panel:patient_detail', args=[self.office_patient1.pk]
        )
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[2]/div/div[3]/a[1]').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('/html/body/div/div[2]/div[2]/div[2]/div[3]/a').click()
        self.assertEquals(
            self.browser.current_url,
            patient_detail_url
        )

    def test_patient_edit_button_redirects_to_patient_edit(self):
        self.browser.get(self.live_server_url + reverse('login'))
        patient_edit_url = self.live_server_url + reverse('office_panel:patient_update', args=[self.office_patient1.pk])
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[2]/div/div[3]/a[1]').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="replaceable-content"]/div[4]/a[1]').click()
        self.assertEquals(
            self.browser.current_url,
            patient_edit_url
        )

    def test_patient_delete_button_redirects_to_patient_delete(self):
        self.browser.get(self.live_server_url + reverse('login'))
        patient_delete_url = self.live_server_url + reverse(
            'office_panel:patient_delete', args=[self.office_patient1.pk]
        )
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[2]/div/div[3]/a[1]').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="replaceable-content"]/div[4]/a[2]').click()
        self.assertEquals(
            self.browser.current_url,
            patient_delete_url
        )


class TestPatients(StaticLiveServerTestCase):

    def setUp(self):
        self.office_user1 = User.objects.create_user(
            'office', 'office@gmail.com', 'officepassword', is_office=True
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

    def test_patients(self):
        self.browser.get(self.live_server_url + reverse('login'))
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/div[3]/a[1]').click()
        patients_text = self.browser.find_element_by_class_name('text-description').text
        self.assertEquals(
            patients_text,
            'Wszyscy pacjenci:'
        )

    def test_add_patient_button_redirects_to_add_patient(self):
        self.browser.get(self.live_server_url + reverse('login'))
        patient_add_url = self.live_server_url + reverse('office_panel:patient_add')
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/div[3]/a[1]').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="replaceable-content"]/div[2]/a').click()
        self.assertEquals(
            self.browser.current_url,
            patient_add_url
        )

    def test_patient_detail_redirects_to_patient_detail(self):
        self.browser.get(self.live_server_url + reverse('login'))
        patient_edit_url = self.live_server_url + reverse('office_panel:patient_detail', args=[self.office_patient1.pk])
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/div[3]/a[1]').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="replaceable-content"]/div[3]/a').click()
        self.assertEquals(
            self.browser.current_url,
            patient_edit_url
        )

    def test_edit_patient_button_redirects_to_edit_patient(self):
        self.browser.get(self.live_server_url + reverse('login'))
        patient_edit_url = self.live_server_url + reverse('office_panel:patient_update', args=[self.office_patient1.pk])
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/div[3]/a[1]').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="replaceable-content"]/div[4]/a[1]').click()
        self.assertEquals(
            self.browser.current_url,
            patient_edit_url
        )

    def test_delete_patient_button_redirects_to_delete_patient(self):
        self.browser.get(self.live_server_url + reverse('login'))
        patient_delete_url = self.live_server_url + reverse(
            'office_panel:patient_delete', args=[self.office_patient1.pk]
        )
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/div[3]/a[1]').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="replaceable-content"]/div[4]/a[2]').click()
        self.assertEquals(
            self.browser.current_url,
            patient_delete_url
        )
