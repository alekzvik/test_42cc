from django.db import models


class RequestEntry(models.Model):
    path = models.TextField()
    method = models.CharField(max_length=200)
    query = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
