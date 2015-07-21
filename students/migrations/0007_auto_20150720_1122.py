# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0006_auto_20150720_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='readingplan_per',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='readingplan_points',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
