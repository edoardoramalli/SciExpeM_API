from enum import Enum
import requests
import json
import sys
from SciExpeM_API.Utility import settings


class HTTP_TYPE(Enum):
    GET = 0
    POST = 1


class RequestAPI:
    def __init__(self, address: str,
                 params: dict, mode: HTTP_TYPE,
                 ip: str = None, port: int = None, content_type: str = 'application/json',
                 secure: bool = None, token: str = None, verify: bool = None):

        ip = settings.IP if not ip else ip
        port = settings.PORT if not port else port
        secure = settings.SECURE if not secure else secure
        token = settings.TOKEN if not token else token
        verify = settings.VERIFY if not verify else verify

        self.headers = {}
        if token:
            self.headers['Authorization'] = 'Token ' + token
        self.headers['Content-Type'] = content_type
        # self.headers['Accept'] = '*/*'

        if secure:
            init = "https://"
        else:
            init = "http://"
        url = init + ip + ":" + str(port) + "/" + address
        try:
            if mode == HTTP_TYPE.GET:
                self.requests = requests.get(url, headers=self.headers, json=params, verify=verify)
            elif mode == HTTP_TYPE.POST:
                self.requests = requests.post(url, headers=self.headers, json=params, verify=verify)
            self.status_code = self.requests.status_code
            self.requests.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(str(e))
            print("HTTP ERROR {} -> {}".format(self.status_code, json.loads(self.requests.text)), file=sys.stderr)
        except (
        requests.exceptions.Timeout, requests.exceptions.TooManyRedirects, requests.exceptions.RequestException):
            self.status_code = 0
            print('CONNECTION ERROR. Try later.', file=sys.stderr)
