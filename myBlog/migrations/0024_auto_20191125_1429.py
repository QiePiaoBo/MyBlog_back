# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-11-25 06:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myBlog', '0023_blogtype_icon'),
    ]

    operations = [
        migrations.RenameField(
            model_name='systemnotice',
            old_name='send_group_id',
            new_name='send_group',
        ),
        migrations.RenameField(
            model_name='systemnotice',
            old_name='send_id',
            new_name='send_user',
        ),
    ]
