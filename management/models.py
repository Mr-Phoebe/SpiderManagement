from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class MyUser(models.Model):
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=16)

    def __str__(self):
        return self.user.username


class Task(models.Model):
    user = models.ForeignKey(MyUser, related_name='task')
    url = models.CharField(max_length=512, null=True)
    name = models.CharField(max_length=128)
    content = models.CharField(max_length=128, null=True)
    hasfile = models.BooleanField(default=False)
    method = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class META:
        ordering = ['name']
