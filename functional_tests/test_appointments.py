from datetime import datetime, timedelta
from time import sleep

from dateutil.relativedelta import relativedelta
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver

from applications.appointments.models import Appointment, Service
from applications.office_panel.models import Patient
from applications.users.models import User, UserOffice
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
        self.office1 = UserOffice.objects.create(
            user=self.office_user1,
            name='name',
            address='address',
            city='City',
            phone_number='000000000',
            website='www.website.com'
        )
        self.service = Service.objects.create(
            office=self.office1,
            name='Konsultacja',
            duration=10
        )
        self.appointment1 = Appointment.objects.create(
            owner=self.patient1,
            office=self.office1,
            date=self.tomorrow,
            date_end=self.tomorrow + timedelta(minutes=20),
            first_name='Kacper',
            last_name='Sawicki',
            patient_email='patient@gmail.com',
            date_selected=datetime(2020, 8, 21, 17, 00, 00),
            phone_number='000000000',
            confirmed=False,
            service=self.service
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
        self.office1 = UserOffice.objects.create(
            user=self.office_user1,
            name='name',
            address='address',
            city='City',
            phone_number='000000000',
            website='www.website.com'
        )
        self.service = Service.objects.create(
            office=self.office1,
            name='Konsultacja',
            duration=10
        )
        self.appointment1 = Appointment.objects.create(
            owner=self.patient1,
            office=self.office1,
            date=self.tomorrow,
            date_end=self.tomorrow + timedelta(minutes=20),
            first_name='Kacper',
            last_name='Sawicki',
            patient_email='patient@gmail.com',
            date_selected=datetime(2020, 8, 21, 17, 00, 00),
            phone_number='000000000',
            confirmed=False,
            service=self.service
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


class TestOfficeTimetable(StaticLiveServerTestCase):

    def setUp(self):
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
        self.patient1 = User.objects.create_user(
            'patient', 'patient@gmail.com', 'patientpassword', is_patient=True
        )
        self.service = Service.objects.create(
            office=self.office1,
            name='Konsultacja',
            duration=10
        )
        self.appointment1 = Appointment.objects.create(
            owner=self.patient1,
            office=self.office1,
            patient_email='patient@gmail.com',
            date=datetime(datetime.today().year, datetime.today().month, 2),
            date_end=datetime(datetime.today().year, datetime.today().month, 2) + timedelta(minutes=20),
            first_name='Kacper',
            last_name='Sawicki',
            date_selected=datetime(2020, 8, 21, 17, 00, 00),
            phone_number='000000000',
            confirmed=False,
            service=self.service
        )
        self.service = Service.objects.create(
            office=self.office1,
            name='Masaż',
            duration=10
        )
        self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')
        self.now = datetime.now()

    def test_timetable(self):
        self.browser.get(self.live_server_url + reverse('login'))
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[3]/div/a').click()
        timetable_date = self.browser.find_element_by_class_name('font-weight-bold').text
        self.assertEquals(
            timetable_date,
            f'{add_zero(self.now.month)}.{self.now.year}'
        )

    def test_timetable_previous_month_button_show_previous_month(self):
        self.remove_month_date = self.now - relativedelta(months=1)
        self.browser.get(self.live_server_url + reverse('login'))
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[3]/div/a').click()
        self.browser.find_element_by_xpath('//*[@id="service"]/option[2]').click()
        sleep(2)
        self.browser.find_element_by_xpath('//*[@id="date-select-down"]').click()
        sleep(2)
        timetable_date = self.browser.find_element_by_class_name('font-weight-bold').text
        self.assertEquals(
            timetable_date,
            f'{add_zero(self.remove_month_date.month)}.{self.remove_month_date.year}'
        )

    def test_timetable_next_month_button_show_next_month(self):
        self.add_month_date = self.now + relativedelta(months=1)
        self.browser.get(self.live_server_url + reverse('login'))
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[3]/div/a').click()
        self.browser.find_element_by_xpath('//*[@id="service"]/option[2]').click()
        sleep(2)
        self.browser.find_element_by_xpath('//*[@id="date-select-up"]').click()
        sleep(2)
        timetable_date = self.browser.find_element_by_class_name('font-weight-bold').text
        self.assertEquals(
            timetable_date,
            f'{add_zero(self.add_month_date.month)}.{self.add_month_date.year}'
        )


class TestPatientTimetable(StaticLiveServerTestCase):

    def setUp(self):
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
        self.patient1 = User.objects.create_user(
            'patient', 'patient@gmail.com', 'patientpassword', is_patient=True
        )
        self.service = Service.objects.create(
            office=self.office1,
            name='Konsultacja',
            duration=10
        )
        self.appointment1 = Appointment.objects.create(
            owner=self.patient1,
            office=self.office1,
            patient_email='patient@gmail.com',
            date=datetime(datetime.today().year, datetime.today().month, 2),
            date_end=datetime(datetime.today().year, datetime.today().month, 2) + timedelta(minutes=20),
            first_name='Kacper',
            last_name='Sawicki',
            date_selected=datetime(2020, 8, 21, 17, 00, 00),
            phone_number='000000000',
            confirmed=False,
            service=self.service
        )
        self.service = Service.objects.create(
            office=self.office1,
            name='Masaż',
            duration=10
        )
        self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')
        self.now = datetime.now()

    def test_timetable(self):
        self.browser.get(self.live_server_url + reverse('login'))
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('patient@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('patientpassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('/html/body/div[4]/div/a').click()
        self.browser.find_element_by_xpath('/html/body/div[2]/div/a/div').click()
        timetable_date = self.browser.find_element_by_class_name('font-weight-bold').text
        self.assertEquals(
            timetable_date,
            f'{add_zero(self.now.month)}.{self.now.year}'
        )

    def test_timetable_previous_month_button_show_previous_month(self):
        self.remove_month_date = self.now - relativedelta(months=1)
        self.browser.get(self.live_server_url + reverse('login'))
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('patient@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('patientpassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('/html/body/div[4]/div/a').click()
        self.browser.find_element_by_xpath('/html/body/div[2]/div/a/div').click()
        self.browser.find_element_by_xpath('//*[@id="service"]/option[2]').click()
        sleep(2)
        self.browser.find_element_by_xpath('//*[@id="date-select-down"]').click()
        sleep(2)
        timetable_date = self.browser.find_element_by_class_name('font-weight-bold').text
        self.assertEquals(
            timetable_date,
            f'{add_zero(self.remove_month_date.month)}.{self.remove_month_date.year}'
        )

    def test_timetable_next_month_button_show_next_month(self):
        self.add_month_date = self.now + relativedelta(months=1)
        self.browser.get(self.live_server_url + reverse('login'))
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('patient@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('patientpassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('/html/body/div[4]/div/a').click()
        self.browser.find_element_by_xpath('/html/body/div[2]/div/a/div').click()
        self.browser.find_element_by_xpath('//*[@id="service"]/option[2]').click()
        sleep(2)
        self.browser.find_element_by_xpath('//*[@id="date-select-up"]').click()
        sleep(2)
        timetable_date = self.browser.find_element_by_class_name('font-weight-bold').text
        self.assertEquals(
            timetable_date,
            f'{add_zero(self.add_month_date.month)}.{self.add_month_date.year}'
        )


class TestServices(StaticLiveServerTestCase):

    def setUp(self):
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
        self.service = Service.objects.create(
            office=self.office1,
            name='Konsultacja',
            duration=10
        )
        self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')

    def tearDown(self):
        self.browser.close()

    def test_services(self):
        self.browser.get(self.live_server_url + reverse('login'))
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="sidebar-wrapper"]/div/a[6]').click()
        service_text = self.browser.find_element_by_class_name('text-description').text
        self.assertEquals(
            service_text,
            'Usługi oferowane przez twój gabinet:'
        )

    def test_add_service_button_redirects_to_add_service(self):
        self.browser.get(self.live_server_url + reverse('login'))
        service_add_url = self.live_server_url + reverse('office_panel:appointments:service_add')
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="sidebar-wrapper"]/div/a[6]').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[2]/div/div[2]/a').click()
        self.assertEquals(
            self.browser.current_url,
            service_add_url
        )

    def service_edit_button_redirects_to_edit_service(self):
        self.browser.get(self.live_server_url + reverse('login'))
        service_edit_url = self.live_server_url + reverse(
            'office_panel:appointments:service_edit', args=[self.service.pk]
        )
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="sidebar-wrapper"]/div/a[6]').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[2]/div/div[4]/a[1]').click()
        self.assertEquals(
            self.browser.current_url,
            service_edit_url
        )

    def test_service_delete_button_redirects_to_delete_service(self):
        self.browser.get(self.live_server_url + reverse('login'))
        service_delete_url = self.live_server_url + reverse(
            'office_panel:appointments:service_delete', args=[self.service.pk]
        )
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="sidebar-wrapper"]/div/a[6]').click()
        sleep(0.5)
        self.browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[2]/div/div[4]/a[2]').click()
        self.assertEquals(
            self.browser.current_url,
            service_delete_url
        )
