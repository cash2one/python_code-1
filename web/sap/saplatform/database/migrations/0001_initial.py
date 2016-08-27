# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DbConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('address', models.CharField(max_length=128, null=True, blank=True)),
                ('auth', models.IntegerField(null=True, blank=True)),
                ('desc', models.CharField(max_length=1024, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SQLResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sql_name', models.CharField(max_length=64, null=True, blank=True)),
                ('content', models.CharField(max_length=1024, null=True, blank=True)),
                ('exec_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('result', models.TextField(null=True, blank=True)),
                ('user', models.CharField(max_length=64, null=True, blank=True)),
            ],
        ),
    ]
