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
            name='Bank',
            fields=[
                ('card_number', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('password', models.CharField(max_length=20)),
                ('balance', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('pic', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('catalog', models.CharField(max_length=50)),
                ('publisher', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('seller', models.CharField(max_length=100)),
                ('order_time', models.DateTimeField()),
                ('is_set', models.BooleanField()),
                ('is_paid', models.BooleanField()),
                ('is_complete', models.BooleanField()),
                ('box_id', models.IntegerField(blank=True)),
                ('comment', models.TextField(blank=True)),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('buyer', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(to='openshop.Item')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('idcard', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=15)),
                ('nfc', models.CharField(max_length=20)),
                ('cards', models.OneToOneField(to='openshop.Bank')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
    ]
