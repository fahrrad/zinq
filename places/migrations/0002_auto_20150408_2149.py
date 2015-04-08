# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='menuItems',
            field=models.ManyToManyField(related_name='order_for_menu_items', through='places.OrderMenuItem', to='menus.MenuItem'),
            preserve_default=True,
        ),
    ]
