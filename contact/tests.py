from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from contact.models import Contact
from django.template.defaultfilters import escape, date, linebreaks


class ContactTest(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.client = Client()

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
