# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-12-17 21:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20171212_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountant',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.User'),
        ),
        migrations.AlterField(
            model_name='customer_support',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.User'),
        ),
        migrations.AlterField(
            model_name='seller',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.User'),
        ),
    ]
