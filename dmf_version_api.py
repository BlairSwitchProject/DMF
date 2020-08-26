#!/usr/bin/env python
# Author: Casey Blair
# Python 3.8.0
# This python script is used to capture the version number of a DMF controller.
# This material and information contained in this file is for general
# information purposes only. Please use at your own risk.
# Arista DMF version 7.3.0
# ''' https://arista.com
# Big_Monitoring_Fabric_7.3_REST_API_Guide_2020-06-22.pdf
# '''

import requests
import json
requests.urllib3.disable_warnings()
# The variables below are for access to the DMF controller. Eample:
# CONTROLLER = '10.1.1.1'
# USER = 'admin'
# PASSWORD = 'pa55word'

CONTROLLER = ''
USER = ''
PASSWORD = ''


class DMFAPI():
    def __init__(self, controller, username, password):
        '''inputs the ip address of the controller to create the api_root var.

        '''
        self.api_root = 'https://{0}:8443'.format(controller)
        self.username = username
        self.password = password
        self.cookies = self._authenticate()

    def _authenticate(self):
        '''uses the request module to post authentication credentials and
        Returns:
           session key for further api calls.
        '''
        url = self.api_root + '/api/v1/auth/login'
        payload = json.dumps({'user': self.username, 'password': self.password})
        auth_response = requests.post(url=url, data=payload, verify=False)
        assert auth_response.ok
        # print(auth_response)
        return auth_response.cookies['session_cookie']

    def deletesession(self):
        '''deletes the session to DMF controller

        '''
        delete_session_url = self.api_root + '/api/v1/data/controller/core/aaa/session[auth-token="{0}"]'.format(self.cookies)
        auth_data = {'cookie': "session_cookie=" + self.cookies}
        delete_session_response = requests.delete(url=delete_session_url, headers=auth_data, verify=False)
        assert delete_session_response.ok
        # print(delete_session_response)

    def version(self):
        '''uses the request module to get controller/ appliance infomation.
           api paths can be found in the api guide on Arista's web site.
        Returns:
           json output of dmf server statistics.
        '''
        version_url = self.api_root + '/api/v1/data/controller/core/version/appliance'
        auth_data = {'cookie': "session_cookie=" + self.cookies}
        version_response = requests.get(url=version_url, headers=auth_data, verify=False)
        assert version_response.ok
        network_json = version_response.json()
        return network_json


def main():
    api = DMFAPI(CONTROLLER, USER, PASSWORD)
    dmf_version = api.version()
    print(dmf_version[0]['version'])
    api.deletesession()


if __name__ == '__main__':
    main()
