# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import geonode.people.models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0006_merge'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='profile',
            managers=[
                ('objects', geonode.people.models.ProfileUserManager()),
            ],
        ),
    ]
