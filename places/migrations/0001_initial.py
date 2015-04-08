# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import places.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('uuid', models.CharField(max_length=32, serialize=False, primary_key=True, default=places.models.uuid_generator)),
                ('status', models.CharField(choices=[('OR', 'Ordered'), ('IP', 'In Progress'), ('DO', 'Done'), ('PA', 'Payed'), ('CA', 'Cancelled')], max_length=2, default='OR')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderMenuItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('amount', models.IntegerField()),
                ('price', models.DecimalField(max_digits=6, decimal_places=2)),
                ('menuItem', models.ForeignKey(to='menus.MenuItem')),
                ('order', models.ForeignKey(to='places.Order')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('menu', models.ForeignKey(unique=True, to='menus.Menu', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('uuid', models.CharField(max_length=32, serialize=False, primary_key=True, default=places.models.uuid_generator)),
                ('table_nr', models.CharField(max_length=255, default='', blank=True)),
                ('place', models.ForeignKey(to='places.Place')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='order',
            name='menuItems',
            field=models.ManyToManyField(through='places.OrderMenuItem', to='menus.MenuItem'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='table',
            field=models.ForeignKey(to='places.Table'),
            preserve_default=True,
        ),
    ]
