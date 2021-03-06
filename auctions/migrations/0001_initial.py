# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-12-25 14:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=240)),
                ('starting_bid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('ending_at', models.DateTimeField()),
                ('live', models.BooleanField(default=False)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='')),
                ('seller', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='users.Seller')),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bid_at', models.DateTimeField(auto_now_add=True)),
                ('auction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.Auction')),
                ('bidder', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='users.User')),
            ],
        ),
    ]
