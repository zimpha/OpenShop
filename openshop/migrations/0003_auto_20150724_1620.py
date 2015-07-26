# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('openshop', '0002_auto_20150724_1001'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='nfc_buyer',
            field=models.CharField(default=datetime.datetime(2015, 7, 24, 8, 20, 20, 119000, tzinfo=utc), max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='nfc_seller',
            field=models.CharField(default=datetime.datetime(2015, 7, 24, 8, 20, 25, 922000, tzinfo=utc), max_length=20),
            preserve_default=False,
        ),
    ]
