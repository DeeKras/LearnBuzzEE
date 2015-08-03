# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_auto_20150728_2306'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('upload_id', models.CharField(max_length=15)),
                ('uploaded_by', models.CharField(max_length=30)),
                ('uploaded_timestamp', models.DateTimeField(auto_now_add=True)),
                ('file_name', models.CharField(max_length=300)),
                ('amt_uploaded', models.IntegerField()),
                ('group', models.ForeignKey(to='students.Group')),
            ],
        ),
        migrations.AlterField(
            model_name='student',
            name='mathplan_type',
            field=models.CharField(blank=True, max_length=2, choices=[(b'', b'choose unit type'), (b'li', b'lines'), (b'ex', b'examples')]),
        ),
        migrations.AlterField(
            model_name='student',
            name='readingplan_type',
            field=models.CharField(blank=True, max_length=2, choices=[(b'', b'choose unit type'), (b'li', b'lines'), (b'pg', b'pages'), (b'ch', b'chapters'), (b'bk', b'books')]),
        ),
        migrations.AlterField(
            model_name='studentgainpoints',
            name='math_type',
            field=models.CharField(blank=True, max_length=2, choices=[(b'', b'choose unit type'), (b'li', b'lines'), (b'ex', b'examples')]),
        ),
        migrations.AlterField(
            model_name='studentgainpoints',
            name='reading_type',
            field=models.CharField(blank=True, max_length=2, choices=[(b'', b'choose unit type'), (b'li', b'lines'), (b'pg', b'pages'), (b'ch', b'chapters'), (b'bk', b'books')]),
        ),
        migrations.AlterField(
            model_name='studentlearningplanlog',
            name='mathplan_type',
            field=models.CharField(max_length=2, choices=[(b'', b'choose unit type'), (b'li', b'lines'), (b'ex', b'examples')]),
        ),
        migrations.AlterField(
            model_name='studentlearningplanlog',
            name='readingplan_type',
            field=models.CharField(max_length=2, choices=[(b'', b'choose unit type'), (b'li', b'lines'), (b'pg', b'pages'), (b'ch', b'chapters'), (b'bk', b'books')]),
        ),
    ]
