# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('openshop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='seller',
            field=models.CharField(max_length=50),
        ),
    ]
