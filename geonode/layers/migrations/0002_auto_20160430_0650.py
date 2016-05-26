# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('layers', '0001_initial'),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='layer',
            name='service',
            field=models.ForeignKey(related_name='layer_set', blank=True, to='services.Service', null=True),
        ),
        migrations.AddField(
            model_name='layer',
            name='styles',
            field=models.ManyToManyField(related_name='LayerStyles', to='layers.Style'),
        ),
        migrations.AddField(
            model_name='layer',
            name='upload_session',
            field=models.ForeignKey(blank=True, to='layers.UploadSession', null=True),
        ),
        migrations.AddField(
            model_name='attribute',
            name='layer',
            field=models.ForeignKey(related_name='attribute_set', to='layers.Layer'),
        ),
    ]
