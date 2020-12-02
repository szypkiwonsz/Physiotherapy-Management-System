from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver

from applications.users.models import User


class TestLogin(StaticLiveServerTestCase):

    def setUp(self):
        self.patient1 = User.objects.create_user(
            'patient', 'patient@gmail.com', 'patientpassword', is_patient=True
        )
        self.office1 = User.objects.create_user(
            'office', 'office@gmail.com', 'officepassword', is_office=True
        )
        self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')

    def tearDown(self):
        self.browser.close()

    def test_no_account_button_redirects_to_signup(self):
        self.browser.get(self.live_server_url + reverse('login'))
        signup_url = self.live_server_url + reverse('users:signup')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/small[1]/a').click()
        self.assertEquals(
            self.browser.current_url,
            signup_url
        )

    def test_forgot_password_button_redirects_to_password_reset(self):
        self.browser.get(self.live_server_url + reverse('login'))
        password_reset_url = self.live_server_url + reverse('password_reset')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/small[2]/a').click()
        self.assertEquals(
            self.browser.current_url,
            password_reset_url
        )

    def test_password_reset_redirects_to_password_reset_done(self):
        self.browser.get(self.live_server_url + reverse('password_reset'))
        password_reset_done_url = self.live_server_url + reverse('password_reset_done')
        self.browser.find_element_by_xpath('//*[@id="id_email"]').send_keys('random@gmail.com')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        self.assertEquals(
            self.browser.current_url,
            password_reset_done_url
        )

    def test_login_as_patient_redirects_to_patient_panel(self):
        self.browser.get(self.live_server_url + reverse('login'))
        panel_patient_url = self.live_server_url + reverse('patient_panel:home')
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('patient@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('patientpassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        self.assertEquals(
            self.browser.current_url,
            panel_patient_url
        )

    def test_login_as_office_redirects_to_office_panel(self):
        self.browser.get(self.live_server_url + reverse('login'))
        panel_office_url = self.live_server_url + reverse('office_panel:home')
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        self.assertEquals(
            self.browser.current_url,
            panel_office_url
        )


class TestRegister(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')

    def tearDown(self):
        self.browser.close()

    def test_register_patient_redirects_to_signup_patient(self):
        self.browser.get(self.live_server_url + reverse('users:signup'))
        signup_patient_url = self.live_server_url + reverse('users:patient_signup')
        self.browser.find_element_by_xpath('//*[@id="image-patient"]').click()
        self.assertEquals(
            self.browser.current_url,
            signup_patient_url
        )

    def test_register_office_redirects_to_signup_office(self):
        self.browser.get(self.live_server_url + reverse('users:signup'))
        signup_office_url = self.live_server_url + reverse('users:office_signup')
        self.browser.find_element_by_xpath('//*[@id="image-office"]').click()
        self.assertEquals(
            self.browser.current_url,
            signup_office_url
        )

    def test_signup_patient_redirects_to_login(self):
        self.browser.get(self.live_server_url + reverse('users:patient_signup'))
        login_url = self.live_server_url + reverse('login')
        self.browser.find_element_by_xpath('//*[@id="id_email"]').send_keys('randompatient@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_confirm_email"]').send_keys('randompatient@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password1"]').send_keys('szypkiwonsz')
        self.browser.find_element_by_xpath('//*[@id="id_password2"]').send_keys('szypkiwonsz')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        self.assertEquals(
            self.browser.current_url,
            login_url
        )

    def test_signup_office_redirects_to_login(self):
        self.browser.get(self.live_server_url + reverse('users:office_signup'))
        login_url = self.live_server_url + reverse('login')
        self.browser.find_element_by_xpath('//*[@id="id_name"]').send_keys('Fizjo-Test')
        self.browser.find_element_by_xpath('//*[@id="id_address"]').send_keys('Random')
        self.browser.find_element_by_xpath('//*[@id="id_city"]').send_keys('Random')
        self.browser.find_element_by_xpath('//*[@id="id_phone_number"]').send_keys('000000000')
        self.browser.find_element_by_xpath('//*[@id="id_email"]').send_keys('randomoffice@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_confirm_email"]').send_keys('randomoffice@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password1"]').send_keys('szypkiwonsz')
        self.browser.find_element_by_xpath('//*[@id="id_password2"]').send_keys('szypkiwonsz')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        self.assertEquals(
            self.browser.current_url,
            login_url
        )

    def test_signup_have_account_button_redirect_to_login(self):
        self.browser.get(self.live_server_url + reverse('users:signup'))
        login_url = self.live_server_url + reverse('login')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/div[3]/small/a').click()
        self.assertEquals(
            self.browser.current_url,
            login_url
        )

    def test_signup_patient_have_account_button_redirect_to_login(self):
        self.browser.get(self.live_server_url + reverse('users:patient_signup'))
        login_url = self.live_server_url + reverse('login')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/div/small/a').click()
        self.assertEquals(
            self.browser.current_url,
            login_url
        )

    def test_signup_office_have_account_button_redirect_to_login(self):
        self.browser.get(self.live_server_url + reverse('users:office_signup'))
        login_url = self.live_server_url + reverse('login')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/div/small/a').click()
        self.assertEquals(
            self.browser.current_url,
            login_url
        )
