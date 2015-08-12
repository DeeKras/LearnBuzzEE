# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('students', '0004_auto_20150807_1646'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guardian',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('student', models.ManyToManyField(to='students.Student')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'guardians',
            },
        ),
        migrations.RemoveField(
            model_name='parent',
            name='student',
        ),
        migrations.RemoveField(
            model_name='parent',
            name='user',
        ),
        migrations.DeleteModel(
            name='Parent',
        ),
    ]
