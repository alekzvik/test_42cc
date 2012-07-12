from django.test import TestCase
from django.core.urlresolvers import reverse
from contact.models import Contact
from django.template.defaultfilters import escape, date, linebreaks
from django.template import RequestContext
from django.conf import settings
from django.test.client import RequestFactory
from django.test import LiveServerTestCase
from selenium import webdriver
import time


class ContactTest(TestCase):
    fixtures = ['initial_data.json']

    def test_contact(self):
        response = self.client.get(reverse('contact.views.index'))

        self.assertEqual(response.status_code, 200)

        data = Contact.objects.get()
        self.assertContains(response, data.name)
        self.assertContains(response, data.last_name)
        self.assertContains(response, date(data.birth_date))
        self.assertContains(response, data.email)
        self.assertContains(response, data.skype)
        self.assertContains(response, data.jabber)
        self.assertContains(response, linebreaks(escape(data.bio)))
        self.assertContains(response, linebreaks(escape(data.other_contacts)))


class BadResponseTest(TestCase):
    def test_404(self):
        bad_response = self.client.get('/something')
        self.assertEqual(bad_response.status_code, 404)
        self.assertTemplateUsed(bad_response, '404.html')


class SettingsContextProcessorTest(TestCase):
    def test_context_processor(self):
        f = RequestFactory()
        c = RequestContext(f.request())
        self.assertTrue(c.get('settings') is settings)


class ContactEditTest(TestCase):
    def tearDown(self):
        self.client.logout()

    def test_login(self):
        response = self.client.get(reverse('contact_edit'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('contact_edit'))
        self.assertEqual(response.status_code, 200)

    def test_form_get(self):
        data = Contact.objects.get()
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('contact_edit'))

        self.assertContains(response, data.name)
        self.assertContains(response, data.last_name)
        self.assertContains(response, data.birth_date)
        self.assertContains(response, data.email)
        self.assertContains(response, data.skype)
        self.assertContains(response, data.jabber)
        self.assertContains(response, escape(data.bio))
        self.assertContains(response, escape(data.other_contacts))

    def test_form_post(self):
        data = dict()
        data['name'] = 'Robin'
        data['last_name'] = 'Poulsen'
        data['birth_date'] = '1983-01-05'
        data['email'] = 'rpoulsen@gmail.com'
        data['jabber'] = 'rpoulsen@gmail.com'
        data['skype'] = 'rpoulsen'
        data['bio'] = "I'm a sweden django guru."
        data['other_contacts'] = "My facebook: facebook.com/rpoulsen"

        self.client.login(username='admin', password='admin')
        response = self.client.post(reverse('contact_edit'), data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Contact.objects.count(), 1)

        self.assertContains(response, data['name'])
        self.assertContains(response, data['last_name'])
        self.assertContains(response, date(data['birth_date']))
        self.assertContains(response, data['email'])
        self.assertContains(response, data['jabber'])
        self.assertContains(response, data['skype'])
        self.assertContains(response, escape(data['bio']))
        self.assertContains(response, data['other_contacts'])


class AjaxSimpleTest(TestCase):
    def test_ajax_form(self):
        data = dict()
        data['name'] = 'Robin'
        data['last_name'] = 'Poulsen'
        data['birth_date'] = '1983-01-05'
        data['email'] = 'rpoulsen@gmail.com'
        data['jabber'] = 'rpoulsen@gmail.com'
        data['skype'] = 'rpoulsen'
        data['bio'] = "I'm a sweden django guru."
        data['other_contacts'] = "My facebook: facebook.com/rpoulsen"
        self.client.login(username='admin', password='admin')
        self.client.post(reverse('contact_edit'), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(Contact.objects.count(), 1)

        contact = Contact.objects.get(pk=1)
        for key, value in data.items():
            if key != 'birth_date':
                self.assertEqual(getattr(contact, key), value)


class AjaxSeleniumTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        settings.DEBUG = True
        cls.driver = webdriver.Firefox()
        super(AjaxSeleniumTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(AjaxSeleniumTest, cls).tearDownClass()
        cls.driver.quit()
        settings.DEBUG = False

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
        time.sleep(1)
