# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-21 05:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('animeupload', '0018_auto_20160820_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag_relation',
            name='show',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='animeupload.Show'),
        ),
    ]
