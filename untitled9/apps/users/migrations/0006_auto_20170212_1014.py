# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-02-12 10:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20170212_0950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='birthday',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='\u751f\u65e5'),
        ),
    ]
