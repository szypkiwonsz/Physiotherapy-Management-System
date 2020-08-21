from time import sleep

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException


class TestHomePageNotLoggedIn(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')

    def tearDown(self):
        self.browser.close()

    def test_panel_button_redirects_to_panel(self):
        self.browser.get(self.live_server_url)
        add_url = self.live_server_url + reverse('login')
        try:
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[1]/li[2]/a').click()
        except ElementNotInteractableException:
            # Mobile version
            self.browser.find_element_by_xpath('/html/body/nav/button').click()
            sleep(0.2)
            self.browser.find_element_by_xpath('//*[@id="basicExampleNav"]/ul[1]/li[2]/a').click()
        self.assertEquals(
            self.browser.current_url,
            add_url
        )
