from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class MyUser(models.Model):
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=16)
    permission = models.IntegerField(default=1)

    def __unicode__(self):
        return self.user.username


class Book(models.Model):
    name = models.CharField(max_length=128)
    price = models.FloatField()
    author = models.CharField(max_length=128)
    publish_date = models.DateField()
    category = models.CharField(max_length=128)

    class META:
        ordering = ['name']

    def __unicode__(self):
        return self.name



