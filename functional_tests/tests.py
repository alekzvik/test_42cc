# from django.conf import settings
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from django.test.utils import override_settings
import time


@override_settings(DEBUG=True)
class AjaxSeleniumTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = WebDriver()
        super(AjaxSeleniumTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(AjaxSeleniumTest, cls).tearDownClass()
        cls.driver.quit()

    def test_ajax_form_selenium(self):
        driver = self.driver
        driver.get(self.live_server_url + "/edit/")
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("admin")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("admin")
        driver.find_element_by_id("login_form").submit()
        driver.find_element_by_id("id_email").clear()
        driver.find_element_by_id("id_email").send_keys("")
        driver.find_element_by_id("id_sendbutton").click()
        self.assertFalse(driver.find_element_by_id("id_sendbutton").is_enabled())
        time.sleep(1)
        driver.find_element_by_id("id_email").clear()
        driver.find_element_by_id("id_email").send_keys("test")
        driver.find_element_by_id("id_sendbutton").click()
        self.assertFalse(driver.find_element_by_id("id_sendbutton").is_enabled())
        time.sleep(1)
        driver.find_element_by_id("id_email").clear()
        driver.find_element_by_id("id_email").send_keys("test@example.com")
        driver.find_element_by_id("id_sendbutton").click()
        self.assertFalse(driver.find_element_by_id("id_sendbutton").is_enabled())
