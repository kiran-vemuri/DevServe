# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 20:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('releases', '0003_auto_20160628_2000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='binary',
            name='path',
            field=models.CharField(default='/tmp', max_length=500),
        ),
        migrations.AlterField(
            model_name='product',
            name='path',
            field=models.CharField(default='/tmp', max_length=500),
        ),
    ]
