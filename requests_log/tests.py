"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
# from django.test.client import Client
from requests_log.models import RequestEntry


class NoLogsTest(TestCase):
    def test_nologs(self):
        logs = RequestEntry.objects.all()
        self.assertEqual(logs.count(), 0)


class LinkTest(TestCase):
    def test_link(self):
        response = self.client.get('/')
        self.assertContains(response, 'href="/requests"')

    def tearDown(self):
        RequestEntry.objects.all().delete()


class LogsTest(TestCase):
    TRIES = 20

    def test_log(self):
        for i in range(self.TRIES):
            self.client.get('/')
        logs = RequestEntry.objects.all()
        self.assertEqual(logs.count(), 20)

    def tearDown(self):
        RequestEntry.objects.all().delete()


class Test(TestCase):
    def test_view(self):
        response = self.client.get('/requests')
        self.assertContains(response, 'GET')
        self.assertContains(response, '/requests')
