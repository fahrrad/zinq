# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0002_auto_20150408_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='menuItems',
            field=models.ManyToManyField(to='menus.MenuItem', through='places.OrderMenuItem'),
            preserve_default=True,
        ),
    ]
