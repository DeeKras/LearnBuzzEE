# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0016_auto_20150727_0059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='sent_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
