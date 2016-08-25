# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-21 19:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('animeupload', '0019_auto_20160820_2252'),
    ]

    operations = [
        migrations.CreateModel(
            name='recommendation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recommendment', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=300)),
                ('show_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='animeupload.Show', unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='tag_relation',
            name='show',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='animeupload.Show'),
        ),
    ]