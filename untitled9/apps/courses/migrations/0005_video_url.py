# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-02-09 10:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_course_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='url',
            field=models.CharField(default='', max_length=100, verbose_name='\u89c6\u9891\u94fe\u63a5'),
        ),
    ]
