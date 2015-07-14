# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from datetime import timedelta
from uuid import uuid4

from django.test import TestCase
from django.conf import settings
from django.contrib.auth import get_user_model
from guardian.shortcuts import get_anonymous_user

from itertools import cycle

from geonode.base.models import TopicCategory
from geonode.layers.models import Layer
from geonode.maps.models import Map, MapLayer

from geonode.base.populate_test_data import create_models
from geonode.layers.populate_layers_data import create_layer_data

from .models import Mosaic


logger = logging.getLogger("geonode.mosaic.test")

if 'geonode.geoserver' in settings.INSTALLED_APPS:
    logger.error("Disconnecting GeoServer signals")

    from django.db.models import signals
    from geonode.geoserver.signals import geoserver_pre_save_maplayer
    from geonode.geoserver.signals import geoserver_post_save_map
    from geonode.geoserver.signals import geoserver_pre_save
    from geonode.geoserver.signals import geoserver_post_save
    signals.pre_save.disconnect(geoserver_pre_save_maplayer, sender=MapLayer)
    signals.post_save.disconnect(geoserver_post_save_map, sender=Map)
    signals.pre_save.disconnect(geoserver_pre_save, sender=Layer)
    signals.post_save.disconnect(geoserver_post_save, sender=Layer)

class MosaicTest(TestCase):

    """Tests geonode.layers app/module
    """

    #fixtures = ['bobby']

    def setUp(self):
        self.user = 'admin'
        self.passwd = 'admin'
        create_models(type='layer')
        create_layer_data()
        self.anonymous_user = get_anonymous_user()

    def test_model(self):

        lcount0 = Layer.objects.count()
        logger.error("Existing layers %s", lcount0)

        for layer in Layer.objects.all():
            logger.error("Layer %r", layer)

        biota = TopicCategory.objects.get(identifier='biota')
        location = TopicCategory.objects.get(identifier='location')

        users = get_user_model().objects.all()

        layer_data = [
            ('Mosaic 00', 'Mosaic 00 abs', 'mosaic00', 'geonode:mosaic00', [0, 5, 0, 5],
                '00010101', ('populartag',), location),
            ('Mosaic 01', 'Mosaic 01 abs', 'mosaic01', 'geonode:mosaic01', [0, 6, 0, 6],
                '00010101', ('populartag',), biota),
            ('Mosaic 99', 'Mosaic 99 abs', 'mosaic99', 'geonode:mosaic99', [0, 9, 0, 9],
                '00010101', ('populartag',), biota),
            ]

        for ld, owner in zip(layer_data, cycle(users)):
            title, abstract, name, typename, (bbox_x0, bbox_x1, bbox_y0, bbox_y1), dt, kws, category = ld
            year, month, day = map(int, (dt[:4], dt[4:6], dt[6:]))
            start = datetime(year, month, day)
            end = start + timedelta(days=365)
            l = Mosaic(title=title,
                          abstract=abstract,
                          name=name,
                          typename=typename,
                          bbox_x0=bbox_x0,
                          bbox_x1=bbox_x1,
                          bbox_y0=bbox_y0,
                          bbox_y1=bbox_y1,
                          uuid=str(uuid4()),
                          owner=owner,
                          temporal_extent_start=start,
                          temporal_extent_end=end,
                          date=start,
                          storeType='mosaic',
                          category=category,

                          has_time=True,
                          has_elevation=False,
                          time_regex='yyyymmdd',
                          elevation_regex=None,
                      )
            l.save()
            logger.error("Stored mosaic: %r", l)
            for kw in kws:
                l.keywords.add(kw)
                l.save()

        lcount1 = Layer.objects.count()
        logger.error("Total layers %s", lcount1)
        logger.error("Total mosaics %s", Mosaic.objects.count())

        # check that new mosaics are counted as layers
        self.assertEqual(lcount1, lcount0 + 3)
        self.assertEqual(Mosaic.objects.count(), 3)

        # some sample queries
        for mosaic in Mosaic.objects.all():
            logger.error("Mosaic id: %s, name:%s, typename:%s", mosaic.id, mosaic.name, mosaic.typename)

        self.assertEqual(Mosaic.objects.filter(name="mosaic00").count(), 1)
        self.assertEqual(Mosaic.objects.filter(name__startswith="mosaic0").count(), 2)
        self.assertEqual(Mosaic.objects.filter(name__startswith="mosaic").count(), 3)






