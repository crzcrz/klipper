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
        self.__headers = {'X-Api-Key': self.api_key}


    def list_files(self):
        r = requests.get(self.host + GET_FILES, headers=self.__headers)
        if r.status_code != 200:
            return
        for file in r.json().get('files', []):
            yield file['display'], file['refs']['resource']


def load_config(config):
    return Octoprint(config)