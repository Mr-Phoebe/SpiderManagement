# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-03-23 14:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('management', '0005_task_taskfile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskfile',
            name='task',
        ),
        migrations.AddField(
            model_name='task',
            name='hasfile',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='TaskFile',
        ),
    ]
