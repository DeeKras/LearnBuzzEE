# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_auto_20150812_0926'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='email',
            name='student',
        ),
    ]
