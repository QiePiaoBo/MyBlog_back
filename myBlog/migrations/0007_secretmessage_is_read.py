# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-09-22 13:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myBlog', '0006_usermood_mood_secret'),
    ]

    operations = [
        migrations.AddField(
            model_name='secretmessage',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
