# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-02-08 20:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_course_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='tag',
            field=models.CharField(default='', max_length=50, verbose_name='\u8bfe\u7a0b\u6807\u7b7e'),
        ),
    ]
