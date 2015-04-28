# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0003_auto_20150408_2227'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='place',
            options={'verbose_name': 'Plaats', 'verbose_name_plural': 'Plaatsen'},
        ),
        migrations.AlterModelOptions(
            name='table',
            options={'verbose_name': 'Tafel', 'verbose_name_plural': 'Tafels'},
        ),
    ]
