# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-13 23:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('animeupload', '0014_auto_20160813_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='description',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='tag_relation',
            name='show_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='animeupload.Show'),
        ),
        migrations.AlterField(
            model_name='tag_relation',
            name='tag_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='animeupload.Tag'),
        ),
    ]
