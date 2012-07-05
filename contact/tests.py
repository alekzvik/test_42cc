"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class ContactTest(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.client = Client()

    def test_contact(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)

        used_templates = [template.name for template in response.templates]
        self.assertEqual(used_templates, ['index.html', 'base.html'])

        self.assertContains(response, 'Vykalyuk', status_code=200)

        bad_response = self.client.get('/something')
        self.assertEqual(bad_response.status_code, 404)
        self.assertTemplateUsed(bad_response, '404.html')
