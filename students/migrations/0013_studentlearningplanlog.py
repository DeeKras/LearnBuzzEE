# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0012_student_total_points'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentLearningPlanLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=30)),
                ('mathplan_points', models.PositiveIntegerField(null=True, blank=True)),
                ('mathplan_per', models.PositiveIntegerField(null=True, blank=True)),
                ('mathplan_type', models.CharField(max_length=2)),
                ('readingplan_points', models.PositiveIntegerField(null=True, blank=True)),
                ('readingplan_per', models.PositiveIntegerField(null=True, blank=True)),
                ('readingplan_type', models.CharField(max_length=2)),
                ('student', models.ForeignKey(to='students.Student')),
            ],
        ),
    ]
