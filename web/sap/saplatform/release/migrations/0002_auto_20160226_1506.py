# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('release', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project', models.CharField(max_length=64, null=True, blank=True)),
                ('branch', models.CharField(max_length=64, null=True, blank=True)),
                ('hash', models.CharField(max_length=16, null=True, blank=True)),
                ('test_id', models.CharField(max_length=16, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='RollBack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project', models.CharField(max_length=64, null=True, blank=True)),
                ('branch', models.CharField(max_length=64, null=True, blank=True)),
                ('hash', models.CharField(max_length=16, null=True, blank=True)),
                ('time', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='releaserecord',
            name='environment',
        ),
        migrations.RemoveField(
            model_name='releaserecord',
            name='no_version',
        ),
        migrations.AddField(
            model_name='releaserecord',
            name='branch',
            field=models.CharField(max_length=64, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='releaserecord',
            name='hash',
            field=models.CharField(max_length=16, null=True, blank=True),
        ),
    ]
