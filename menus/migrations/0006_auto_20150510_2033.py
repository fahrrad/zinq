# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0005_auto_20150422_2013'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menuitem',
            options={'verbose_name': 'Product', 'verbose_name_plural': 'Producten', 'ordering': ['position']},
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='position',
            field=models.PositiveSmallIntegerField(verbose_name='Position'),
            preserve_default=True,
        ),
    ]
