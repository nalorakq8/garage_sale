# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-12-29 17:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20171229_0011'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='payed',
            field=models.BooleanField(default=False),
        ),
    ]
