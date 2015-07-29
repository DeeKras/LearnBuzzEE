# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='email',
            options={'verbose_name_plural': 'emails'},
        ),
        migrations.AlterModelOptions(
            name='studentgainpoints',
            options={'verbose_name_plural': 'Student.GainPoints'},
        ),
        migrations.AlterModelOptions(
            name='studentlearningplanlog',
            options={'verbose_name_plural': 'StudentLearningPlanLogs'},
        ),
    ]
