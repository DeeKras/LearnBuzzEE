# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0009_studentgainpoints'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentgainpoints',
            name='math_amt',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='studentgainpoints',
            name='reading_amt',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
    ]
