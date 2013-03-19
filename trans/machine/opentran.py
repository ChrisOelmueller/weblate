# -*- coding: utf-8 -*-
#
# Copyright © 2012 - 2013 Michal Čihař <michal@cihar.com>
#
# This file is part of Weblate <http://weblate.org/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from trans.machine.base import MachineTranslation
import urllib


class OpenTranTranslation(MachineTranslation):
    '''
    Open-Tran machine translation support.
    '''
    name = 'open-tran'
    verbose = 'Open-Tran'

    def download_languages(self):
        return self.json_req('http://open-tran.eu/json/supported')

    def format_match(self, match):
        '''
        Reformats match to (translation, quality) tuple.
        '''
        return (
            match['text'],
            100 - (match['value'] - 1) * 20,
        )

    def download_translations(self, language, text):
        '''
        Downloads and processes translations.
        '''
        response = self.json_req(
            'http://en.%s.open-tran.eu/json/suggest/%s' % (
                language, urllib.quote(text)
            )
        )

        return [self.format_match(match) for match in response if match['value'] <= 4]