# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-12-28 16:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='card_expiration_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]