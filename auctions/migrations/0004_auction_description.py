# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-12-26 13:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20171225_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='description',
            field=models.CharField(default='', max_length=1200),
        ),
    ]
