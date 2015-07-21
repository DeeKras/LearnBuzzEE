# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_auto_20150717_1351'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='added_how',
            field=models.CharField(default='default', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='added_how_detail',
            field=models.CharField(default='default', max_length=255),
            preserve_default=False,
        ),
    ]
