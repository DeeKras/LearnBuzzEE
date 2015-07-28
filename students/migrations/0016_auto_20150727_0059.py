# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0015_auto_20150726_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='sent_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 27, 4, 59, 10, 493249, tzinfo=utc), blank=True),
            preserve_default=False,
        ),
    ]
