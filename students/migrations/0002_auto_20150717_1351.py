# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='avatar',
            field=models.ImageField(upload_to=b'thumbpath', blank=True),
        ),
        migrations.AddField(
            model_name='student',
            name='gender',
            field=models.CharField(default='F', max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2015, 7, 17, 17, 51, 9, 94533, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
