# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='topiccategory',
            name='fa_class',
            field=models.CharField(default=b'fa-times', max_length=64),
        ),
    ]
