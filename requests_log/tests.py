from django.test import TestCase
from requests_log.models import RequestEntry
from django.core.urlresolvers import reverse


class NoLogsTest(TestCase):
    def test_nologs(self):
        logs = RequestEntry.objects.all()
        self.assertEqual(logs.count(), 0)


class LinkTest(TestCase):
    def test_link(self):
        response = self.client.get(reverse('contact.views.index'))
        self.assertContains(response, 'href="/requests"')

    def tearDown(self):
        RequestEntry.objects.all().delete()


class LogsTest(TestCase):
    TRIES = 20

    def test_log(self):
        for i in range(self.TRIES):
            self.client.get(reverse('contact.views.index'))
        logs = RequestEntry.objects.all()
        self.assertEqual(logs.count(), 20)

    def tearDown(self):
        RequestEntry.objects.all().delete()


class ViewTest(TestCase):
    def test_view(self):
        response = self.client.get(reverse('requests_view'))
        self.assertContains(response, 'GET')
        self.assertContains(response, '/requests')

    def tearDown(self):
        RequestEntry.objects.all().delete()
