# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-01 16:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tweets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='nickname',
            field=models.CharField(max_length=32, unique=True),
        ),
    ]
