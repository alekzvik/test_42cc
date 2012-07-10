from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    birth_date = models.DateField()
    email = models.EmailField()
    jabber = models.CharField(max_length=200)
    skype = models.CharField(max_length=200)
    bio = models.TextField()
    other_contacts = models.TextField()
    photo = models.ImageField(upload_to='photos', blank=True, null=True)
