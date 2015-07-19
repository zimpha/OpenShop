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
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('pic', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(max_digits=5, decimal_places=2)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order_time', models.DateTimeField()),
                ('is_set', models.BooleanField()),
                ('is_buy', models.BooleanField()),
                ('box_id', models.IntegerField()),
                ('comment', models.TextField()),
                ('buyer', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(to='openshop.Item')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='catalog',
            field=models.ForeignKey(to='openshop.Tag'),
        ),
        migrations.AddField(
            model_name='item',
            name='publisher',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
