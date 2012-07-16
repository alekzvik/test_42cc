from django.db import models


CHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)


class RequestEntry(models.Model):
    path = models.TextField()
    method = models.CharField(max_length=200)
    query = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    priority = models.SmallIntegerField(default=1, choices=CHOICES)

    def __unicode__(self):
        return u"%s %s%s" % (self.method.upper(), self.path, self.query)

    class Meta():
        ordering = ["-priority", "timestamp"]
