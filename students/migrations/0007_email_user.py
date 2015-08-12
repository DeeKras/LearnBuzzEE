# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('students', '0006_remove_email_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='user',
            field=models.ForeignKey(related_name='emailuser', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
