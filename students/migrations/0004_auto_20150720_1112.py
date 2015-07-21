# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_auto_20150720_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='added_how',
            field=models.CharField(max_length=100),
        ),
    ]
