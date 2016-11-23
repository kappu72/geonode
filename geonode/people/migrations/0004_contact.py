# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0003_auto_20160824_0245'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position_name', models.CharField(max_length=255, null=True, verbose_name='position name')),
                ('role', models.CharField(max_length=255, null=True, verbose_name='role')),
                ('organization_name', models.CharField(max_length=255, null=True, verbose_name='organization name')),
                ('email_address', models.EmailField(max_length=254, verbose_name='email address')),
            ],
        ),
    ]
