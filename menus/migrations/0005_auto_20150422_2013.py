# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0004_auto_20150420_2208'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menuitem',
            options={'verbose_name': 'Product', 'verbose_name_plural': 'Producten', 'ordering': ['category', 'position']},
        ),
        migrations.AddField(
            model_name='menuitem',
            name='position',
            field=models.PositiveSmallIntegerField(verbose_name='Position', default=0),
            preserve_default=True,
        ),
    ]
