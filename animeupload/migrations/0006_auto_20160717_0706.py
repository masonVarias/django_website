# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-17 14:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('animeupload', '0005_auto_20160716_1327'),
    ]

    operations = [
        migrations.RenameField(
            model_name='show',
            old_name='os_intimacy',
            new_name='on_screen_intimacy',
        ),
    ]