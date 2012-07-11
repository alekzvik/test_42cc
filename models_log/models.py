from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

ACTION_CHOICES = (
    ('C', 'create'),
    ('U', 'update'),
    ('D', 'delete'),
)


class ModelLog(models.Model):
    model_name = models.CharField(max_length=200)
    action = models.CharField(max_length=1, choices=ACTION_CHOICES)
    changed_pk = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'timestamp'

    @classmethod
    def log(cls, action, instance):
        if not isinstance(instance, cls):
            name = "%s.%s" % (instance._meta.app_label,
                              instance._meta.module_name)
            pk = instance.pk if isinstance(instance.pk, (int, long)) else 0
            log_entry = cls(model_name=name, action=action, changed_pk=pk)
            log_entry.save()


@receiver(post_save)
def save_handler(sender, instance, created, **kwargs):
    if created:
        ModelLog.log('create', instance)
    else:
        ModelLog.log('update', instance)


@receiver(post_delete)
def delete_handler(sender, instance, **kwargs):
    ModelLog.log('delete', instance)
