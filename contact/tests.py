from django.test import TestCase
from django.core.urlresolvers import reverse
from contact.models import Contact
from django.template.defaultfilters import escape, date, linebreaks
from django.template import RequestContext
from django.conf import settings
from django.test.client import RequestFactory


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
        self.assertContains(response, date(data.birth_date))
        self.assertContains(response, data.email)
        self.assertContains(response, data.skype)
        self.assertContains(response, data.jabber)
        self.assertContains(response, linebreaks(escape(data.bio)))
        self.assertContains(response, linebreaks(escape(data.other_contacts)))

    def test_form_post(self):
        data = dict()
        data['name'] = 'Robin'
        data['last_name'] = 'Poulsen'
        data['birth_date'] = '1983-01-05'
        data['email'] = 'rpoulsen@gmail.com'
        data['jabber'] = 'rpoulsen@gmail.com'
        data['skype'] = 'rpoulsen'
        data['bio'] = "I'm a sweden django guru."
        data['other_contact'] = "My facebook: facebook.com/rpoulsen"

        self.client.login(username='admin', password='admin')
        response = self.client.post(reverse('contact_edit'), data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Contact.objects.count(), 1)

        for item in data.values():
            self.assertContains(self.response, item)

