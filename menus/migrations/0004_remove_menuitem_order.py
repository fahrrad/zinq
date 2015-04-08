# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0003_menuitem_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuitem',
            name='order',
        ),
    ]
