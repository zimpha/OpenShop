# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('openshop', '0002_auto_20150719_1141'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='user',
        ),
        migrations.AddField(
            model_name='order',
            name='is_complete',
            field=models.BooleanField(default=datetime.datetime(2015, 7, 19, 12, 24, 47, 34000, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='catalog',
            field=models.CharField(max_length=50),
        ),
        migrations.DeleteModel(
            name='Message',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
