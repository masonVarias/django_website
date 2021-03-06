# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-15 18:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('description', models.CharField(max_length=150, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(max_length=1000)),
                ('home_page', models.URLField()),
                ('color_f', models.CharField(default='black', max_length=30)),
                ('background', models.CharField(default='white', max_length=30)),
                ('youtube', models.URLField(blank=True)),
                ('twitter', models.URLField(blank=True)),
                ('facebook', models.URLField(blank=True)),
                ('instagram', models.URLField(blank=True)),
                ('tumblr', models.URLField(blank=True)),
                ('pintrest', models.URLField(blank=True)),
                ('google_plus', models.URLField(blank=True)),
                ('twitch', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recommended', models.CharField(max_length=30)),
                ('description', models.TextField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('series_name', models.CharField(max_length=200)),
                ('watch_order', models.CharField(max_length=500)),
            ],
            options={
                'verbose_name_plural': 'series',
            },
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, default='images/fnf/fnf.jpg', upload_to='images/')),
                ('english_title', models.CharField(max_length=200)),
                ('japanese_title', models.CharField(max_length=200, null=True)),
                ('description', models.TextField(max_length=1000)),
                ('nudity', models.IntegerField(choices=[(0, 'none'), (1, 'underwear'), (2, 'cencored'), (3, 'butt'), (4, 'barbie smooth'), (5, 'outlined'), (6, 'nipple'), (7, 'full frontal')], default=0)),
                ('on_screen_intimacy', models.IntegerField(choices=[(0, 'none'), (1, 'light kissing'), (2, 'deep kissing/grope'), (3, 'sex')], default=0)),
                ('sexual_intent', models.IntegerField(choices=[(0, 'none'), (1, 'unintentional'), (2, 'mischievous'), (3, 'malicious(molestation)'), (4, 'extremley malicious(rape)')], default=0)),
                ('violence', models.IntegerField(choices=[(0, 'none'), (1, 'cartoon'), (2, 'blood'), (3, 'realistic'), (4, 'extreme')], default=0)),
                ('gore', models.IntegerField(choices=[(0, 'none'), (1, 'low'), (2, 'moderate'), (3, 'high'), (4, 'extreme')], default=0)),
                ('morbid_images', models.IntegerField(choices=[(0, 'none'), (1, 'unmarred dead'), (2, 'silhouetted dismemberment'), (3, 'dismemberment')], default=0)),
                ('feels', models.IntegerField(choices=[(0, 'none'), (1, 'low'), (2, 'moderate'), (3, 'high'), (4, 'extreme')], default=0)),
                ('profanity', models.IntegerField(choices=[(0, 'none'), (1, 'mild'), (2, 'cencored'), (3, 'uncencored')], default=0)),
                ('moral_ambiguity', models.IntegerField(choices=[(0, 'none'), (1, 'low'), (2, 'moderate'), (3, 'high'), (4, 'extreme')], default=0)),
                ('fan_service', models.IntegerField(choices=[(0, 'none'), (1, 'low'), (2, 'moderate'), (3, 'high'), (4, 'extreme')], default=0)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'ordering': ['english_title'],
            },
        ),
        migrations.CreateModel(
            name='Showlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('likes', models.IntegerField(default=0)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=30, unique=True)),
                ('description', models.CharField(max_length=150, null=True)),
            ],
            options={
                'ordering': ['tag_name'],
            },
        ),
        migrations.CreateModel(
            name='PrimaryLink',
            fields=[
                ('link_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='animeupload.Link')),
            ],
            bases=('animeupload.link',),
        ),
        migrations.CreateModel(
            name='SecondaryLink',
            fields=[
                ('link_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='animeupload.Link')),
                ('parent_link', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent_lnk', to='animeupload.PrimaryLink')),
            ],
            bases=('animeupload.link',),
        ),
        migrations.CreateModel(
            name='TVShow',
            fields=[
                ('show_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='animeupload.Show')),
                ('total_episodes', models.IntegerField()),
                ('ova', models.BooleanField(default=False)),
                ('movies', models.IntegerField(default=0)),
                ('total_seasons', models.IntegerField(default=1)),
                ('ongoing', models.BooleanField(default=False)),
            ],
            bases=('animeupload.show',),
        ),
        migrations.AddField(
            model_name='showlist',
            name='shows',
            field=models.ManyToManyField(blank=True, to='animeupload.Show'),
        ),
        migrations.AddField(
            model_name='show',
            name='genres',
            field=models.ManyToManyField(blank=True, to='animeupload.Genre'),
        ),
        migrations.AddField(
            model_name='show',
            name='series',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='animeupload.Series'),
        ),
        migrations.AddField(
            model_name='show',
            name='tags',
            field=models.ManyToManyField(blank=True, to='animeupload.Tag'),
        ),
        migrations.AddField(
            model_name='recommendation',
            name='show',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='animeupload.Show'),
        ),
        migrations.AlterUniqueTogether(
            name='showlist',
            unique_together=set([('creator', 'title')]),
        ),
    ]
