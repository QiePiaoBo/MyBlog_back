# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-08-30 02:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myBlog', '0003_auto_20190826_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='theme',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Theme_user', to='myBlog.User', unique=True),
        ),
        migrations.AlterField(
            model_name='usermood',
            name='mood_content',
            field=models.TextField(default='早晨起来拥抱太阳', null=True),
        ),
    ]
