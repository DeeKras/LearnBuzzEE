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
            name='Educator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('called', models.CharField(max_length=100)),
                ('email_from', models.CharField(max_length=100)),
                ('email_signature', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'educators',
            },
        ),
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
                ('sent_date', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('groupname', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'groups',
            },
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name_plural': 'parents',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(max_length=30)),
                ('lastname', models.CharField(max_length=30)),
                ('gender', models.CharField(max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('avatar', models.ImageField(upload_to=b'thumbpath', blank=True)),
                ('start_date', models.DateField(auto_now_add=True)),
                ('added_how', models.CharField(max_length=100)),
                ('added_how_detail', models.CharField(max_length=255)),
                ('total_points', models.PositiveIntegerField(default=0)),
                ('math_points', models.IntegerField(default=0)),
                ('math_remaining', models.IntegerField(default=0)),
                ('reading_points', models.PositiveIntegerField(default=0)),
                ('reading_remaining', models.IntegerField(default=0)),
                ('currentplan_id', models.PositiveIntegerField(default=0)),
                ('mathplan_points', models.PositiveIntegerField(null=True, blank=True)),
                ('mathplan_per', models.PositiveIntegerField(null=True, blank=True)),
                ('mathplan_type', models.CharField(blank=True, max_length=2, choices=[(b'li', b'lines'), (b'ex', b'examples')])),
                ('readingplan_points', models.PositiveIntegerField(null=True, blank=True)),
                ('readingplan_per', models.PositiveIntegerField(null=True, blank=True)),
                ('readingplan_type', models.CharField(blank=True, max_length=2, choices=[(b'li', b'lines'), (b'pg', b'pages'), (b'ch', b'chapters'), (b'bk', b'books')])),
                ('group', models.ForeignKey(to='students.Group')),
            ],
            options={
                'verbose_name_plural': 'students',
            },
        ),
        migrations.CreateModel(
            name='StudentGainPoints',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=30)),
                ('plan_id', models.PositiveIntegerField()),
                ('math_source', models.TextField(blank=True)),
                ('math_source_details', models.TextField(blank=True)),
                ('math_amt', models.PositiveIntegerField(null=True, blank=True)),
                ('math_type', models.CharField(blank=True, max_length=2, choices=[(b'li', b'lines'), (b'ex', b'examples')])),
                ('reading_source', models.TextField(blank=True)),
                ('reading_source_details', models.TextField(blank=True)),
                ('reading_amt', models.PositiveIntegerField(null=True, blank=True)),
                ('reading_type', models.CharField(blank=True, max_length=2, choices=[(b'li', b'lines'), (b'pg', b'pages'), (b'ch', b'chapters'), (b'bk', b'books')])),
                ('student', models.ForeignKey(to='students.Student')),
            ],
        ),
        migrations.CreateModel(
            name='StudentLearningPlanLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=30)),
                ('plan_id', models.PositiveIntegerField(null=True, blank=True)),
                ('mathplan_points', models.PositiveIntegerField(null=True, blank=True)),
                ('mathplan_per', models.PositiveIntegerField(null=True, blank=True)),
                ('mathplan_type', models.CharField(max_length=2, choices=[(b'li', b'lines'), (b'ex', b'examples')])),
                ('readingplan_points', models.PositiveIntegerField(null=True, blank=True)),
                ('readingplan_per', models.PositiveIntegerField(null=True, blank=True)),
                ('readingplan_type', models.CharField(max_length=2, choices=[(b'li', b'lines'), (b'pg', b'pages'), (b'ch', b'chapters'), (b'bk', b'books')])),
                ('student', models.ForeignKey(to='students.Student')),
            ],
        ),
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
        migrations.AddField(
            model_name='email',
            name='student',
            field=models.ForeignKey(to='students.Student'),
        ),
        migrations.AddField(
            model_name='educator',
            name='group',
            field=models.ManyToManyField(to='students.Group'),
        ),
    ]
