# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0007_auto_20150720_1122'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=30)),
                ('content', models.TextField()),
                ('student', models.ForeignKey(to='students.Student')),
            ],
            options={
                'verbose_name_plural': 'student logs',
            },
        ),
        migrations.AlterModelOptions(
            name='parent',
            options={'verbose_name_plural': 'parents'},
        ),
    ]
