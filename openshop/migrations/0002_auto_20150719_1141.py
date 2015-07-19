# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('openshop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='idcard',
            field=models.CharField(default=datetime.datetime(2015, 7, 19, 3, 41, 50, 404000, tzinfo=utc), max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(default=datetime.datetime(2015, 7, 19, 3, 41, 58, 947000, tzinfo=utc), max_length=15),
            preserve_default=False,
        ),
    ]
