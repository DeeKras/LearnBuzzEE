# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0010_auto_20150721_1820'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='math_remaining',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='student',
            name='reading_remaining',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='student',
            name='mathplan_per',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='mathplan_points',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='mathplan_type',
            field=models.CharField(blank=True, max_length=2, choices=[(b'li', b'lines'), (b'ex', b'examples')]),
        ),
        migrations.AlterField(
            model_name='student',
            name='readingplan_per',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='readingplan_points',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='readingplan_type',
            field=models.CharField(blank=True, max_length=2, choices=[(b'li', b'lines'), (b'pg', b'pages'), (b'ch', b'chapters'), (b'bk', b'books')]),
        ),
    ]
