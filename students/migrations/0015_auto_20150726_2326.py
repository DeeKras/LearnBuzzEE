# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0014_auto_20150723_2232'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email_from', models.CharField(max_length=250)),
                ('email_to', models.EmailField(max_length=254)),
                ('email_cc', models.EmailField(max_length=254, blank=True)),
                ('email_subject', models.CharField(max_length=250)),
                ('email_body', models.TextField()),
                ('status', models.CharField(default=b'draft', max_length=25)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=30)),
                ('sent_date', models.DateTimeField(null=True)),
                ('student', models.ForeignKey(to='students.Student')),
            ],
        ),
        migrations.AlterField(
            model_name='studentlearningplanlog',
            name='mathplan_type',
            field=models.CharField(max_length=2, choices=[(b'li', b'lines'), (b'ex', b'examples')]),
        ),
        migrations.AlterField(
            model_name='studentlearningplanlog',
            name='readingplan_type',
            field=models.CharField(max_length=2, choices=[(b'li', b'lines'), (b'pg', b'pages'), (b'ch', b'chapters'), (b'bk', b'books')]),
        ),
    ]
