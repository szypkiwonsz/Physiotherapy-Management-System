from time import sleep

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException

from users.models import User


class TestHomePageNotLoggedIn(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')

    def tearDown(self):
        self.browser.close()

    def test_panel_button_redirects_to_login(self):
        self.browser.get(self.live_server_url)
        login_url = self.live_server_url + reverse('login')
        try:
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[1]/li[2]/a').click()
        except ElementNotInteractableException:
            # Mobile version
            self.browser.find_element_by_xpath('/html/body/nav/button').click()
            sleep(0.2)
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[1]/li[2]/a').click()
        self.assertEquals(
            self.browser.current_url,
            login_url
        )

    def test_offices_button_redirects_to_offices(self):
        self.browser.get(self.live_server_url)
        offices_url = self.live_server_url + reverse('offices')
        try:
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[1]/li[3]/a').click()
        except ElementNotInteractableException:
            # Mobile version
            self.browser.find_element_by_xpath('/html/body/nav/button').click()
            sleep(0.2)
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[1]/li[3]/a').click()
        self.assertEquals(
            self.browser.current_url,
            offices_url
        )

    def test_help_button_redirects_to_help(self):
        self.browser.get(self.live_server_url)
        help_url = self.live_server_url + reverse('help')
        try:
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[1]/li[4]/a').click()
        except ElementNotInteractableException:
            # Mobile version
            self.browser.find_element_by_xpath('/html/body/nav/button').click()
            sleep(0.2)
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[1]/li[4]/a').click()
        self.assertEquals(
            self.browser.current_url,
            help_url
        )

    def test_login_button_redirects_to_login(self):
        self.browser.get(self.live_server_url)
        login_url = self.live_server_url + reverse('login')
        try:
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[2]/li[1]/a').click()
        except ElementNotInteractableException:
            # Mobile version
            self.browser.find_element_by_xpath('/html/body/nav/button').click()
            sleep(0.2)
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[2]/li[1]/a').click()
        self.assertEquals(
            self.browser.current_url,
            login_url
        )

    def test_register_button_redirects_to_signup_choice(self):
        self.browser.get(self.live_server_url)
        signup_url = self.live_server_url + reverse('signup')
        try:
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[2]/li[2]/a').click()
        except ElementNotInteractableException:
            # Mobile version
            self.browser.find_element_by_xpath('/html/body/nav/button').click()
            sleep(0.2)
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[2]/li[2]/a').click()
        self.assertEquals(
            self.browser.current_url,
            signup_url
        )


class TestHomePageLoggedAsPatient(StaticLiveServerTestCase):

    def setUp(self):
        self.patient1 = User.objects.create_user(
            'patient', 'patient@gmail.com', 'patientpassword', is_patient=True
        )
        self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')

    def tearDown(self):
        self.browser.close()

    def test_panel_button_redirects_to_panel(self):
        self.browser.get(self.live_server_url + reverse('login'))
        panel_patient_url = self.live_server_url + reverse('patient-home')
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('patient@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('patientpassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        self.browser.get(self.live_server_url + reverse('home'))
        try:
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[1]/li[2]/a').click()
        except ElementNotInteractableException:
            # Mobile version
            self.browser.find_element_by_xpath('/html/body/nav/button').click()
            sleep(0.2)
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[1]/li[2]/a').click()
        self.assertEquals(
            self.browser.current_url,
            panel_patient_url
        )

    def test_offices_button_redirects_to_offices(self):
        self.browser.get(self.live_server_url + reverse('login'))
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('patient@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('patientpassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        self.browser.get(self.live_server_url + reverse('home'))
        offices_url = self.live_server_url + reverse('offices')
        try:
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[1]/li[3]/a').click()
        except ElementNotInteractableException:
            # Mobile version
            self.browser.find_element_by_xpath('/html/body/nav/button').click()
            sleep(0.2)
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[1]/li[3]/a').click()
        self.assertEquals(
            self.browser.current_url,
            offices_url
        )

    def test_help_button_redirects_to_help(self):
        self.browser.get(self.live_server_url + reverse('login'))
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('patient@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('patientpassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        self.browser.get(self.live_server_url + reverse('home'))
        help_url = self.live_server_url + reverse('help')
        try:
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[1]/li[4]/a').click()
        except ElementNotInteractableException:
            # Mobile version
            self.browser.find_element_by_xpath('/html/body/nav/button').click()
            sleep(0.2)
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[1]/li[4]/a').click()
        self.assertEquals(
            self.browser.current_url,
            help_url
        )

    def test_profile_button_redirects_to_profile(self):
        self.browser.get(self.live_server_url + reverse('login'))
        profile_patient_url = self.live_server_url + reverse('profile-patient')
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('patient@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('patientpassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        self.browser.get(self.live_server_url + reverse('home'))
        try:
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[2]/li[1]/a').click()
        except ElementNotInteractableException:
            # Mobile version
            self.browser.find_element_by_xpath('/html/body/nav/button').click()
            sleep(0.2)
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[2]/li[1]/a').click()
        self.assertEquals(
            self.browser.current_url,
            profile_patient_url
        )

    def test_logout_button_redirects_to_logout(self):
        self.browser.get(self.live_server_url + reverse('login'))
        logout_url = self.live_server_url + reverse('logout')
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('patient@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('patientpassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        self.browser.get(self.live_server_url + reverse('home'))
        try:
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[2]/li[2]/a').click()
        except ElementNotInteractableException:
            # Mobile version
            self.browser.find_element_by_xpath('/html/body/nav/button').click()
            sleep(0.2)
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[2]/li[2]/a').click()
        self.assertEquals(
            self.browser.current_url,
            logout_url
        )


class TestHomePageLoggedAsOffice(StaticLiveServerTestCase):

    def setUp(self):
        self.patient1 = User.objects.create_user(
            'office', 'office@gmail.com', 'officepassword', is_office=True
        )
        self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')

    def tearDown(self):
        self.browser.close()

    def test_panel_button_redirects_to_panel(self):
        self.browser.get(self.live_server_url + reverse('login'))
        panel_office_url = self.live_server_url + reverse('office-home')
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        self.browser.get(self.live_server_url + reverse('home'))
        try:
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[1]/li[2]/a').click()
        except ElementNotInteractableException:
            # Mobile version
            self.browser.find_element_by_xpath('/html/body/nav/button').click()
            sleep(0.2)
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[1]/li[2]/a').click()
        self.assertEquals(
            self.browser.current_url,
            panel_office_url
        )

    def test_offices_button_redirects_to_offices(self):
        self.browser.get(self.live_server_url + reverse('login'))
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        self.browser.get(self.live_server_url + reverse('home'))
        offices_url = self.live_server_url + reverse('offices')
        try:
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[1]/li[3]/a').click()
        except ElementNotInteractableException:
            # Mobile version
            self.browser.find_element_by_xpath('/html/body/nav/button').click()
            sleep(0.2)
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[1]/li[3]/a').click()
        self.assertEquals(
            self.browser.current_url,
            offices_url
        )

    def test_help_button_redirects_to_help(self):
        self.browser.get(self.live_server_url + reverse('login'))
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        self.browser.get(self.live_server_url + reverse('home'))
        help_url = self.live_server_url + reverse('help')
        try:
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[1]/li[4]/a').click()
        except ElementNotInteractableException:
            # Mobile version
            self.browser.find_element_by_xpath('/html/body/nav/button').click()
            sleep(0.2)
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[1]/li[4]/a').click()
        self.assertEquals(
            self.browser.current_url,
            help_url
        )

    def test_profile_button_redirects_to_profile(self):
        self.browser.get(self.live_server_url + reverse('login'))
        profile_office_url = self.live_server_url + reverse('profile-office')
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        self.browser.get(self.live_server_url + reverse('home'))
        try:
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[2]/li[1]/a').click()
        except ElementNotInteractableException:
            # Mobile version
            self.browser.find_element_by_xpath('/html/body/nav/button').click()
            sleep(0.2)
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[2]/li[1]/a').click()
        self.assertEquals(
            self.browser.current_url,
            profile_office_url
        )

    def test_logout_button_redirects_to_logout(self):
        self.browser.get(self.live_server_url + reverse('login'))
        logout_url = self.live_server_url + reverse('logout')
        self.browser.find_element_by_xpath('//*[@id="id_username"]').send_keys('office@gmail.com')
        self.browser.find_element_by_xpath('//*[@id="id_password"]').send_keys('officepassword')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/form/button').click()
        self.browser.get(self.live_server_url + reverse('home'))
        try:
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[2]/li[2]/a').click()
        except ElementNotInteractableException:
            # Mobile version
            self.browser.find_element_by_xpath('/html/body/nav/button').click()
            sleep(0.2)
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[2]/li[2]/a').click()
        self.assertEquals(
            self.browser.current_url,
            logout_url
        )
