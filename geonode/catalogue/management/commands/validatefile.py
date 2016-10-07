# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2016 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

from lxml import etree

from django.core.management.base import BaseCommand

from geonode.catalogue.validation import Validators


class Command(BaseCommand):
    help = ("Perform a validation check on one or more metadata files.")

    def add_arguments(self, parser):
        parser.add_argument('filepath', nargs='+', help="path to the metadata file")

    def handle(self, *args, **options):

        profiles = ["iso19139", "fgdc"]
        v = Validators(profiles)

        for metadata_file in options['filepath']:
            print("Checking file %s" % metadata_file)

            try:
                md = etree.parse(metadata_file)
                one_valid, all_valid, details = v.is_valid(md)
                print("   Validation results: all valid: %s - one valid: %s" % (all_valid, one_valid))
                for name, valid, errors in details:
                    print("      profile: %s valid: %s " % (name, valid))
                    for msg, line in errors:
                        print("         line %s: %s" % (line, msg))

            except etree.XMLSyntaxError as e:
                print("   Error in parsing file %s: %s" % (metadata_file, e))
                continue
            except IOError as e:
                print("   Error in reading file %s: %s" % (metadata_file, e))
                continue
