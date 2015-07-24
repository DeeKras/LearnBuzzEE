# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0011_auto_20150722_1705'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='total_points',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
