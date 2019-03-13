# Octoprint REST API support
#
# Copyright (C) 2019  Stanislav Kljuhhin <stanislav.kljuhhin@me.com>
#
# This file may be distributed under the terms of the GNU GPLv3 license.
import requests


DEFAULT_HOST = 'http://localhost:80'
GET_FILES = '/api/files'

class Octoprint:
    def __init__(self, config):
        self.api_key = config.get('api_key')
        self.host = config.get('host', DEFAULT_HOST)
        self._headers = {'X-Api-Key': self.api_key}
        self.gcode = config.get_printer().lookup_object('gcode')
        self.gcode.register_command('OCTOPRINT', self.cmd_OCTOPRINT)

    def list_files(self):
        r = requests.get(self.host + GET_FILES, headers=self._headers)
        if r.status_code != 200:
            return
        for file in r.json().get('files', []):
            yield file['display'], file['refs']['resource']

    def _print_file(self, resource):
        json = {'command': 'select', 'print': True}
        r = requests.post(resource, headers=self._headers, json=json)

    def cmd_OCTOPRINT(self, params):
        print_file = params.get('PRINT_FILE')
        if print_file is None:
            self.gcode.respond_info('Required parameter missing.')
            return
        self._print_file(print_file)
        self.gcode.respond_info('Printing %s' % print_file)


def load_config(config):
    return Octoprint(config)