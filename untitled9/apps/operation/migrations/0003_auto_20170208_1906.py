# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-02-08 19:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0002_auto_20170207_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercourse',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u63a5\u6536\u7528\u6237'),
        ),
    ]
