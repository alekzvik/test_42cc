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
        self.assertContains(response, 'href="/requests/"')

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


class PriorityTest(TestCase):
    def setUp(self):
        RequestEntry.objects.all().delete()

    def tearDown(self):
        RequestEntry.objects.all().delete()

    def test_default_priority(self):
        self.client.get('/')
        entry = RequestEntry.objects.get(pk=1)
        self.assertEqual(entry.priority, 1)

    def test_priority_ordering(self):
        for i in range(20):
            self.client.get('/')
        self.client.get('/edit/')
        entry = RequestEntry.objects.latest('timestamp')
        entry.priority = 5
        entry.save()
        response = self.client.get(reverse('requests_view'))
        self.assertContains(response, '/edit/')
