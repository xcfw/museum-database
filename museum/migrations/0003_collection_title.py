# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-24 04:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museum', '0002_auto_20170123_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='title',
            field=models.CharField(default=' ', max_length=140),
        ),
    ]
