# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-12-28 21:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auction_email_sent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='picture',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
