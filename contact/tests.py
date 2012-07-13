from django.test import TestCase
from django.core.urlresolvers import reverse
from contact.models import Contact
from django.template.defaultfilters import escape, date, linebreaks
from django.template import RequestContext, Template, Context
from django.conf import settings
from django.test.client import RequestFactory
from contact.templatetags.contact_tags import edit_link
from django.db import models
from contact.management.commands.print_models import Command
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from django.test.utils import override_settings
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

    def test_edit_link(self):
        response = self.client.get(reverse('contact.views.index'))
        admin_url = reverse('admin:contact_contact_change', args=(1,))
        self.assertContains(response, admin_url)


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


class EditLinkTest(TestCase):
    def test_edit_link_tag(self):
        contact = Contact.objects.get(pk=1)
        self.assertEqual(edit_link(contact), '/admin/contact/contact/1/')

    def test_edit_link_in_context(self):
        rendered = Template(
            '{% load contact_tags %}'
            '{% edit_link object %}'
        ).render(Context({'object': Contact.objects.get(pk=1)}))

        self.assertTrue('admin/contact/contact/1/' in rendered)


class CommandTest(TestCase):
    def test_models_command(self):
        result = {}
        all_models = models.get_models()
        for model in all_models:
            result[model] = model.objects.count()
        command = Command()
        self.assertEqual(command.project_models(), result)


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
