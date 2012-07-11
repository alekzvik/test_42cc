from django.test import TestCase
from django.db import models
from models_log.models import ModelLog


class TestModel(models.Model):
    number = models.IntegerField()


class ModelLogTest(TestCase):
    def setUp(self):
        TestModel.objects.create(number=0)

    def test_create(self):
        item = ModelLog.objects.latest()
        self.assertEqual(item.model_name, 'models_log.testmodel')
        self.assertEqual(item.action, 'create')
        self.assertEqual(item.changed_pk, 1)

    def test_update(self):
        count = ModelLog.objects.count()
        data = TestModel.objects.get(pk=1)
        data.number = 1
        data.save()
        self.assertEqual(ModelLog.objects.count(), count + 1)
        item = ModelLog.objects.latest()
        self.assertEqual(item.model_name, 'models_log.testmodel')
        self.assertEqual(item.action, 'update')
        self.assertEqual(item.changed_pk, 1)

    def test_delete(self):
        count = ModelLog.objects.count()
        data = TestModel.objects.get(pk=1)
        data.delete()
        self.assertEqual(ModelLog.objects.count(), count + 1)
        item = ModelLog.objects.latest()
        self.assertEqual(item.model_name, 'models_log.testmodel')
        self.assertEqual(item.action, 'delete')
        self.assertEqual(item.changed_pk, 1)
