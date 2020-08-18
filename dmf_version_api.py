import requests
import json
requests.urllib3.disable_warnings()

CONTROLLER = '10.11.1.170'
USER = 'admin'
PASSWORD = 'xxx'


class DMFAPI():
    def __init__(self, server, username, password):
        self.api_root = 'https://{0}:8443'.format(server)
        self.username = username
        self.password = password
        self.cookies = self._authenticate()

    def _authenticate(self):
        rs = requests.Session()
        url = self.api_root + '/api/v1/auth/login'
        payload = json.dumps({'user': self.username, 'password': self.password})
        auth_response = rs.post(url=url, data=payload, verify=False)
        assert auth_response.ok
        return rs.cookies['session_cookie']
        #print(auth_response)

    def _deletesession(self):
        delete_session_url = self.api_root + '/api/v1/data/controller/core/aaa/session[auth-token="{0}"]'.format(self.cookies)
        auth_data = {'cookie': "session_cookie=" + self.cookies}
        delete_session_response = requests.delete(url=delete_session_url, headers=auth_data, verify=False)
        assert delete_session_response.ok
        #print(delete_session_response)

    def _version(self):
        version_url = self.api_root + '/api/v1/data/controller/core/version/appliance'
        auth_data = {'cookie': "session_cookie=" + self.cookies}
        version_response = requests.get(url=version_url, headers=auth_data, verify=False)
        assert version_response.ok
        network_json = version_response.json()
        return network_json


def main():
    api = DMFAPI(CONTROLLER, USER, PASSWORD)
    api._authenticate()
    dmf_version = api._version()
    print(dmf_version[0]['version'])
    api._deletesession()

if __name__ == '__main__':
    main()
