# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_auto_20150720_1112'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name_plural': 'students'},
        ),
        migrations.AlterField(
            model_name='student',
            name='mathplan_per',
            field=models.PositiveIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='mathplan_points',
            field=models.PositiveIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='readingplan_per',
            field=models.PositiveIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='readingplan_points',
            field=models.PositiveIntegerField(blank=True),
        ),
    ]
