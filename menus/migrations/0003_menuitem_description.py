# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0002_auto_20150407_1919'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='description',
            field=models.CharField(null=True, blank=True, max_length=1024),
            preserve_default=True,
        ),
    ]
