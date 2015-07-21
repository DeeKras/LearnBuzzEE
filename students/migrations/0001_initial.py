# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(max_length=30)),
                ('lastname', models.CharField(max_length=30)),
                ('group', models.CharField(max_length=1, choices=[(b'A', b'Group A'), (b'B', b'Group B'), (b'C', b'Group C'), (b'D', b'Group D')])),
                ('math_points', models.IntegerField(default=0)),
                ('reading_points', models.PositiveIntegerField(default=0)),
                ('mathplan_points', models.PositiveIntegerField()),
                ('mathplan_per', models.PositiveIntegerField()),
                ('mathplan_type', models.CharField(max_length=2, choices=[(b'li', b'lines'), (b'ex', b'examples')])),
                ('readingplan_points', models.PositiveIntegerField()),
                ('readingplan_per', models.PositiveIntegerField()),
                ('readingplan_type', models.CharField(max_length=2, choices=[(b'li', b'lines'), (b'pg', b'pages'), (b'ch', b'chapters'), (b'bk', b'books')])),
            ],
        ),
        migrations.AddField(
            model_name='parent',
            name='student',
            field=models.ManyToManyField(to='students.Student'),
        ),
        migrations.AddField(
            model_name='parent',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
