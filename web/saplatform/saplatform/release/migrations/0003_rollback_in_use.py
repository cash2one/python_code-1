# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('release', '0002_auto_20160226_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='rollback',
            name='in_use',
            field=models.BooleanField(default=False),
        ),
    ]
