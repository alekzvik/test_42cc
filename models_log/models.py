from django.db import models, DatabaseError
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

ACTION_CHOICES = (
    ('C', 'create'),
    ('U', 'update'),
    ('D', 'delete'),
)


class ModelLog(models.Model):
    # model_name = models.CharField(max_length=200)
    action = models.CharField(max_length=1, choices=ACTION_CHOICES)
    changed_pk = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType)
    content_object = generic.GenericForeignKey('content_type', 'changed_pk')

    class Meta:
        get_latest_by = 'timestamp'

    # @classmethod
    # def log(cls, action, instance):
    #     if not isinstance(instance, cls):
    #         name = "%s.%s" % (instance._meta.app_label,
    #                           instance._meta.module_name)
    #         pk = instance.pk if isinstance(instance.pk, (int, long)) else 0
    #         log_entry = cls(model_name=name, action=action, changed_pk=pk)
    #         log_entry.save()


def log(action, sender, instance):
    content_type = ContentType.objects.get_for_model(sender)
    if content_type != ContentType.objects.get_for_model(ModelLog):
        try:
            pk = instance.pk if isinstance(instance.pk, (long, int)) else 0
            ModelLog.objects.create(
                action=action,
                content_type=content_type,
                changed_pk=pk,
            )
        except DatabaseError, e:
            print e


@receiver(post_save)
def save_handler(sender, instance, created, **kwargs):
    if created:
        log('create', sender, instance)
    else:
        log('update', sender, instance)


@receiver(post_delete)
def delete_handler(sender, instance, **kwargs):
    log('delete', sender, instance)
