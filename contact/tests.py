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
        r = RequestContext(f.request())
        for k, v in settings.__dict__.items():
            self.assertIn(v, r['settings'])
