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
# Note: most of this code has been taken from https://github.com/ckan/ckanext-spatial
#       which is distributed under the AGPL 3.0
#########################################################################

import os
import logging
from lxml import etree

log = logging.getLogger(__name__)


class BaseValidator(object):
    '''Base class for a validator.'''
    name = None
    title = None

    @classmethod
    def is_valid(cls, xml):
        '''
        Runs the validation on the supplied XML etree.
        Returns a tuple, the first value is a boolean indicating
        whether the validation passed or not. The second is a list of tuples,
        each containing the error message and the error line.

        Returns tuple:
          (is_valid, [(error_message_string, error_line_number)])
        '''
        raise NotImplementedError


class XsdValidator(BaseValidator):
    '''Base class for validators that use an XSD schema.'''

    @classmethod
    def _is_valid(cls, xml, xsd_filepath, xsd_name):
        '''Returns whether or not an XML file is valid according to
        an XSD. Returns a tuple, the first value is a boolean indicating
        whether the validation passed or not. The second is a list of tuples,
        each containing the error message and the error line.

        Params:
          xml - etree of the XML to be validated
          xsd_filepath - full path to the XSD file
          xsd_name - string describing the XSD

        Returns:
          (is_valid, [(error_message_string, error_line_number)])
        '''
        xsd = etree.parse(xsd_filepath)
        schema = etree.XMLSchema(xsd)
        try:
            schema.assertValid(xml)
        except etree.DocumentInvalid:
            log.info('Validation errors found using schema {0}'.format(xsd_name))
            errors = []
            for error in schema.error_log:
                errors.append((error.message, error.line))
            errors.insert
            return False, errors
        return True, []


class ISO19139Schema(XsdValidator):
    name = 'iso19139'
    title = 'ISO19139 XSD Schema'

    @classmethod
    def is_valid(cls, xml):
        xsd_path = 'xml/iso19139'
        gmx_xsd_filepath = os.path.join(os.path.dirname(__file__),
                                        xsd_path, 'gmx/gmx.xsd')
        xsd_name = 'Dataset schema (gmx.xsd)'
        is_valid, errors = cls._is_valid(xml, gmx_xsd_filepath, xsd_name)
        if not is_valid:
            # TODO: not sure if we need this one, keeping for backwards compatibility
            errors.insert(0, ('{0} Validation Error'.format(xsd_name), None))
        return is_valid, errors


class FGDCSchema(XsdValidator):
    '''
    XSD based validation for FGDC metadata documents.

    Uses XSD schema from the Federal Geographic Data Comittee:

    http://www.fgdc.gov/schemas/metadata/

    '''

    name = 'fgdc'
    title = 'FGDC XSD Schema'

    @classmethod
    def is_valid(cls, xml):
        xsd_path = 'xml/fgdc'

        xsd_filepath = os.path.join(os.path.dirname(__file__),
                                    xsd_path, 'fgdc-std-001-1998.xsd')
        return cls._is_valid(xml, xsd_filepath, 'FGDC Schema (fgdc-std-001-1998.xsd)')

all_validators = (ISO19139Schema, FGDCSchema)


class Validators(object):
    '''
    Validates XML against one or more profiles (i.e. validators).
    '''
    def __init__(self, profiles=["iso19139", "fgdc"]):
        self.profiles = profiles

        self.validators = {}  # name: class
        for validator_class in all_validators:
            self.validators[validator_class.name] = validator_class

    def add_validator(self, validator_class):
            self.validators[validator_class.name] = validator_class

    def is_valid(self, xml):
        '''Returns whether or not an XML file is valid.
        Returns a tuple,
        - the first value is a boolean indicating whether the validation passed
          at least for one validator,
        - the second value is a boolean reporting if the validation passed
          for all the requested validators (you may want to use a XSD schema and
          a set of schematron rules for instance)
        - the third value is a list reporting the validation details: for each
          validator you get:
          - the validator name
          - a boolean indicating if the validation has passed with the validator
          - an optional list of validation errors in a tuple (message, line)

        Params:
          xml - etree of the XML to be validated

        Returns:
          (is_one_valid, is_all_valid, [ profile name, is valid, [(error_message_string, error_line_number)]])
        '''

        is_all_valid = True
        is_one_valid = False
        profile_list = []

        log.debug('Starting validation against profile(s) %s' % ','.join(self.profiles))
        for name in self.profiles:
            validator = self.validators[name]
            is_valid, error_message_list = validator.is_valid(xml)

            is_all_valid = is_all_valid and is_valid
            is_one_valid = is_one_valid or is_valid

            profile_list.append((name, is_valid, error_message_list))
            if not is_valid:
                log.info('Validating against "%s" profile failed' % validator.title)
                log.debug('%r', error_message_list)
            else:
                log.debug('Validated against "%s"', validator.title)

        return is_one_valid, is_all_valid, profile_list
