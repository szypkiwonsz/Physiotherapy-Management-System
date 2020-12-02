from datetime import datetime, timedelta
from time import sleep

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException

from applications.appointments.models import Appointment
from applications.medical_history.models import MedicalHistory
from applications.office_panel.models import Patient
from applications.users.models import User, Office
from utils.add_zero import add_zero


class TestNavigationBar(StaticLiveServerTestCase):

    def setUp(self):
        self.patient1 = User.objects.create_user(
            'patient', 'patient@gmail.com', 'patientpassword', is_patient=True
        )
        self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')

    def tearDown(self):
        self.browser.close()

    def test_appointment_panel_upcoming_button_redirects_to_upcoming_appointments(self):
        self.browser.get(self.live_server_url + reverse('login'))
        upcoming_appointments_url = self.live_server_url + reverse('patient_panel:appointments:upcoming')
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('patient@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('patientpassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        try:
            self.browser.find_element_by_xpath('//*[@id="navbarDropdownMenuLink"]').click()
            sleep(0.5)
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[1]/li[2]/div/a[1]').click()
        except ElementNotInteractableException:
            # Mobile version
            self.browser.find_element_by_xpath('/html/body/nav/button').click()
            sleep(0.5)
            self.browser.find_element_by_xpath('//*[@id="navbarDropdownMenuLink"]').click()
            sleep(0.5)
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[1]/li[2]/div/a[1]').click()
        self.assertEquals(
            self.browser.current_url,
            upcoming_appointments_url
        )

    def test_appointment_panel_make_button_redirects_to_select_office(self):
        self.browser.get(self.live_server_url + reverse('login'))
        select_office_url = self.live_server_url + reverse('patient_panel:appointments:select')
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('patient@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('patientpassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        try:
            self.browser.find_element_by_xpath('//*[@id="navbarDropdownMenuLink"]').click()
            sleep(0.5)
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[1]/li[2]/div/a[2]').click()
        except ElementNotInteractableException:
            # Mobile version
            self.browser.find_element_by_xpath('/html/body/nav/button').click()
            sleep(0.5)
            self.browser.find_element_by_xpath('//*[@id="navbarDropdownMenuLink"]').click()
            sleep(0.5)
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[1]/li[2]/div/a[2]').click()
        self.assertEquals(
            self.browser.current_url,
            select_office_url
        )

    def test_appointment_panel_old_button_redirects_to_old_appointments(self):
        self.browser.get(self.live_server_url + reverse('login'))
        old_appointments_url = self.live_server_url + reverse('patient_panel:appointments:old')
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('patient@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('patientpassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        try:
            self.browser.find_element_by_xpath('//*[@id="navbarDropdownMenuLink"]').click()
            sleep(0.5)
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[1]/li[2]/div/a[3]').click()
        except ElementNotInteractableException:
            # Mobile version
            self.browser.find_element_by_xpath('/html/body/nav/button').click()
            sleep(0.5)
            self.browser.find_element_by_xpath('//*[@id="navbarDropdownMenuLink"]').click()
            sleep(0.5)
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[1]/li[2]/div/a[3]').click()
        self.assertEquals(
            self.browser.current_url,
            old_appointments_url
        )


class TestHomeNoData(StaticLiveServerTestCase):

    def setUp(self):
        self.patient1 = User.objects.create_user(
            'patient', 'patient@gmail.com', 'patientpassword', is_patient=True
        )
        self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')

    def tearDown(self):
        self.browser.close()

    def test_no_offices_text(self):
        self.browser.get(self.live_server_url + reverse('login'))
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('patient@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('patientpassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        no_offices_text = self.browser.find_element_by_class_name('form').text
        self.assertEquals(
            no_offices_text,
            'Nie jesteś zarejestrowany w żadnym gabinecie.\n(gabinet musi dodać Cię do swojej bazy)\nUmów się na '
            'wizytę'
        )

    def test_office_make_appointment_button_redirects_to_select_office(self):
        self.browser.get(self.live_server_url + reverse('login'))
        select_office_url = self.live_server_url + reverse('patient_panel:appointments:select')
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('patient@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('patientpassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('/html/body/div[2]/div/a').click()
        self.assertEquals(
            self.browser.current_url,
            select_office_url
        )

    def test_no_appointments_text(self):
        self.browser.get(self.live_server_url + reverse('login'))
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('patient@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('patientpassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        no_appointments = self.browser.find_elements_by_class_name('form')[1].text
        self.assertEquals(
            no_appointments,
            'Nie masz umówionych żadnych wizyt.\n(kliknij przycisk poniżej i umów swoją pierwszą wizytę.)\nUmów się na '
            'wizytę'
        )

    def test_appointments_make_appointment_button_redirects_to_select_office(self):
        self.browser.get(self.live_server_url + reverse('login'))
        select_office_url = self.live_server_url + reverse('patient_panel:appointments:select')
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('patient@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('patientpassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('/html/body/div[3]/div/a').click()
        self.assertEquals(
            self.browser.current_url,
            select_office_url
        )

    def test_no_medical_histories_text(self):
        self.browser.get(self.live_server_url + reverse('login'))
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('patient@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('patientpassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        no_medical_histories_text = self.browser.find_elements_by_class_name('form')[2].text
        self.assertEquals(
            no_medical_histories_text,
            'Nie masz żadnych historii medycznych.\n(żaden gabinet nie dodał twojej historii medycznej.)\nUmów się na '
            'wizytę'
        )

    def test_medical_histories_make_appointment_button_redirects_to_select_office(self):
        self.browser.get(self.live_server_url + reverse('login'))
        select_office_url = self.live_server_url + reverse('patient_panel:appointments:select')
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('patient@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('patientpassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('/html/body/div[4]/div/a').click()
        self.assertEquals(
            self.browser.current_url,
            select_office_url
        )


class TestHome(StaticLiveServerTestCase):

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
        self.office_patient1 = Patient.objects.create(
            owner=self.office_user1,
            first_name='firstname',
            last_name='lastname',
            email='patient@gmail.com',
        )
        self.appointment1 = Appointment.objects.create(
            owner=self.patient1,
            office=self.office1,
            patient_email='patient@gmail.com',
            date=self.tomorrow,
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
            description='description',
            recommendations='recommendations',
            date_selected=datetime(2020, 8, 21, 17, 00, 00),
        )
        self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')

    def tearDown(self):
        self.browser.close()

    def test_offices(self):
        self.browser.get(self.live_server_url + reverse('login'))
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('patient@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('patientpassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        office_name = self.browser.find_element_by_class_name('form').text
        self.assertEquals(
            office_name,
            'Gabinety do których zostałeś ostatnio przypisany:\n(wyświetlone są tylko te w których odbyłeś już wizytę)'
            '\nname\nPokaż wszystkie gabinety'
        )

    def test_show_all_offices_button_redirects_to_offices(self):
        self.browser.get(self.live_server_url + reverse('login'))
        all_offices_url = self.live_server_url + reverse('patient_panel:offices')
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('patient@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('patientpassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('/html/body/div[2]/div/a').click()
        self.assertEquals(
            self.browser.current_url,
            all_offices_url
        )

    def test_appointments(self):
        self.browser.get(self.live_server_url + reverse('login'))
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('patient@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('patientpassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        appointment_text = self.browser.find_element_by_class_name('text-description').text
        self.assertEquals(
            appointment_text,
            f'name, {add_zero(self.tomorrow.day)}.{add_zero(self.tomorrow.month)}.'
            f'{self.tomorrow.year}, o godz: {add_zero(self.tomorrow.hour)}:{add_zero(self.tomorrow.minute)} '
            f'- Konsultacja [Niepotwierdzona]'
        )

    def test_show_all_upcoming_button_redirects_to_upcoming_appointments(self):
        self.browser.get(self.live_server_url + reverse('login'))
        upcoming_appointments_url = self.live_server_url + reverse('patient_panel:appointments:upcoming')
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('patient@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('patientpassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('/html/body/div[3]/div/a').click()
        self.assertEquals(
            self.browser.current_url,
            upcoming_appointments_url
        )

    def test_edit_appointment_button_redirects_to_update_appointment(self):
        self.browser.get(self.live_server_url + reverse('login'))
        update_appointment_url = self.live_server_url + reverse(
            'patient_panel:appointments:update', args=[self.appointment1.pk]
        )
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('patient@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('patientpassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/a[1]').click()
        self.assertEquals(
            self.browser.current_url,
            update_appointment_url
        )

    def test_delete_appointment_button_redirects_to_confirm_delete(self):
        self.browser.get(self.live_server_url + reverse('login'))
        cancel_appointment_url = self.live_server_url + reverse(
            'patient_panel:appointments:delete', args=[self.appointment1.pk]
        )
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('patient@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('patientpassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/a[2]').click()
        self.assertEquals(
            self.browser.current_url,
            cancel_appointment_url
        )

    def test_medical_histories(self):
        self.browser.get(self.live_server_url + reverse('login'))
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('patient@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('patientpassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        office_name = self.browser.find_elements_by_class_name('form')[-1].text
        self.assertEquals(
            office_name,
            'Twoje historie medyczne:\nname\nData dodania: 21.08.2020, o godz: 17:00\nOpis:\ndescription\nZalecenia:\n'
            'recommendations\nPokaż wszystkie wizyty'
        )

    def test_show_all_medical_histories_button_redirects_to_medical_histories(self):
        self.browser.get(self.live_server_url + reverse('login'))
        medical_histories_url = self.live_server_url + reverse('patient_panel:medical_history:list')
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('patient@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('patientpassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('/html/body/div[4]/div/a').click()
        self.assertEquals(
            self.browser.current_url,
            medical_histories_url
        )
