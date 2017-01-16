# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_auto_20170110_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='bbox_x0',
            field=models.DecimalField(null=True, max_digits=19, decimal_places=10, blank=True),
        ),
        migrations.AddField(
            model_name='region',
            name='bbox_x1',
            field=models.DecimalField(null=True, max_digits=19, decimal_places=10, blank=True),
        ),
        migrations.AddField(
            model_name='region',
            name='bbox_y0',
            field=models.DecimalField(null=True, max_digits=19, decimal_places=10, blank=True),
        ),
        migrations.AddField(
            model_name='region',
            name='bbox_y1',
            field=models.DecimalField(null=True, max_digits=19, decimal_places=10, blank=True),
        ),
        migrations.AddField(
            model_name='region',
            name='srid',
            field=models.CharField(default=b'EPSG:4326', max_length=255),
        ),
    ]
