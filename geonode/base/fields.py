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

from django import forms
from django.conf import settings

from geonode.base.models import Thesaurus
from geonode.base.models import ThesaurusKeyword
from geonode.base.models import ThesaurusKeywordLabel

class CategoryChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return '<span class="has-popover" data-container="body" data-toggle="popover" data-placement="top" ' \
               'data-content="' + obj.description + '" trigger="hover">' \
               '<div class="fa-stack fa-1g">' \
               '<i class="fa fa-square-o fa-stack-2x"></i>' \
               '<i class="fa '+obj.fa_class+' fa-stack-1x"></i></div>' \
               '&nbsp;' + obj.gn_description + '</span>'


class MultiThesauriField(forms.MultiValueField):
    def __init__(self, label=None, required=True, help_text=None, widget=None):
        
        fields_list = []
        for el in settings.THESAURI:
            choices_list = []
            thesaurus_name = el['name'];
            t = Thesaurus.objects.get(identifier=thesaurus_name)
            for tk in t.thesaurus.all():
                tkl = tk.keyword.filter(lang='en')
                choices_list.append((tkl[0].id, tkl[0].label))
            fields_list.append(forms.MultipleChoiceField(choices = tuple(choices_list)))
        
        fields = tuple(fields_list)
        
        super(MultiThesauriField, self).__init__(fields, required, widget, label)
        
    def compress(selfself, data_list):
        if data_list:
            print "**************** FIELD ************************" + str(data_list[0]);
            #return '%s,%s,%s' % (data_list[0], data_list[1], data_list[2])
            return '%s' % (data_list[0])
        return None