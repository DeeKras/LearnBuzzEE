# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0013_studentlearningplanlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='currentplan_id',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='studentgainpoints',
            name='plan_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentlearningplanlog',
            name='plan_id',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
    ]
