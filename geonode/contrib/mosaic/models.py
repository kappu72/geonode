# -*- coding: utf-8 -*-

from django.conf import settings

from django.db import models
from django.utils.translation import ugettext_lazy as _

from geonode.layers.models import Layer, cov_exts


TIME_REGEX = (
    ('[0-9]{8}', _('YYYYMMDD')),
    ('[0-9]{8}T[0-9]{6}', _("YYYYMMDD'T'hhmmss")),
    ('[0-9]{8}T[0-9]{6}Z', _("YYYYMMDD'T'hhmmss'Z'")),
)


class Mosaic(Layer):

    """
    Mosaic (inherits Layer fields)
    """

    has_time = models.BooleanField(default=False)
    has_elevation = models.BooleanField(default=False)

    time_regex = models.CharField(max_length=128, null=True, choices=TIME_REGEX)
    elevation_regex = models.CharField(max_length=128, null=True)

    @property
    def display_type(self):
        return "Mosaic"

    @property
    def service_type(self):
        return "WCS"

    @property
    def ows_url(self):
        return settings.OGC_SERVER['default']['PUBLIC_LOCATION'] + "wms"

    def get_base_file(self):
        """Get  geotiff file for this layer.
        For mosaics, this function need some specific constraints
        since we have a set of related files
        """

        # If there was no upload_session return None
        if self.upload_session is None:
            return None, None

        base_exts = [x.replace('.', '') for x in cov_exts]
        base_files = self.upload_session.layerfile_set.filter(
            name__in=base_exts)
        base_files_count = base_files.count()

        # If there are no files in the upload_session return None
        if base_files_count == 0:
            return None, None

        msg = 'There should only be one main file (.shp or .geotiff), found %s' % base_files_count
        assert base_files_count == 1, msg

        # we need to check, for shapefile, if column names are valid
        list_col = None

        # no error, let's return the base files
        return base_files.get(), list_col
