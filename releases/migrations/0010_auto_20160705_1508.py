# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-05 22:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('releases', '0009_binary_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='binary',
            name='status',
            field=models.CharField(default='new', max_length=20),
        ),
    ]