# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0008_auto_20150721_0935'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentGainPoints',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=30)),
                ('math_source', models.TextField(blank=True)),
                ('math_source_details', models.TextField(blank=True)),
                ('math_amt', models.PositiveIntegerField(blank=True)),
                ('math_type', models.CharField(blank=True, max_length=2, choices=[(b'li', b'lines'), (b'ex', b'examples')])),
                ('reading_source', models.TextField(blank=True)),
                ('reading_source_details', models.TextField(blank=True)),
                ('reading_amt', models.PositiveIntegerField(blank=True)),
                ('reading_type', models.CharField(blank=True, max_length=2, choices=[(b'li', b'lines'), (b'pg', b'pages'), (b'ch', b'chapters'), (b'bk', b'books')])),
                ('student', models.ForeignKey(to='students.Student')),
            ],
        ),
    ]
