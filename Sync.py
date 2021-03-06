#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import json
import base64
import os


class Sync(object):
    """
    Sync connection wrapper.

    :param server_url:
    :param username:
    :param password:
    """
    def __init__(self, server_url, username, password):
        self.server_url = server_url
        self.username = username
        self.password = password
        self.headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic ' + str(base64.b64encode(
                (self.username + ':' + self.password).encode('utf-8')
            ), encoding='utf-8')
        }

    def pull(self):
        """
        Read the base64 encoded data from the sync server.
        :return:
        """
        request = requests.post(self.server_url + "ajax/read.php",
                                data="",
                                headers=self.headers,
                                verify=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'certificate.pem'))
        if request.status_code == requests.codes.ok:
            received_data = json.loads(request.text)
            if 'result' in received_data:
                return received_data['result']
            else:
                return ''
        else:
            return ''

    def push(self, data):
        """
        Push data to the server. This overwrites data living there. Please pull and merge first.
        :param data:
        :return:
        """
        request = requests.post(self.server_url + "ajax/write.php",
                                data={'data': data},
                                headers=self.headers,
                                verify=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'certificate.pem'))
        if request.status_code == requests.codes.ok:
            return True
        else:
            return False
