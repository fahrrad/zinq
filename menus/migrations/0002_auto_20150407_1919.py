# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0001_initial'),
        ('places', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='place',
            field=models.ForeignKey(to='places.Place'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set([('name', 'place')]),
        ),
    ]
