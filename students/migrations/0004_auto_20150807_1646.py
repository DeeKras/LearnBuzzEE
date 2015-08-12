# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_student_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='educator',
            name='added_how',
            field=models.CharField(default='playing', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='educator',
            name='added_how_detail',
            field=models.CharField(default='playing', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='educator',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2015, 8, 7, 20, 46, 39, 581215, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
