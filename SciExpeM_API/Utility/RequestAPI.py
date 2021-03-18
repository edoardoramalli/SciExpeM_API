from enum import Enum
import requests
import json
import sys


class HTTP_TYPE(Enum):
    GET = 0
    POST = 1


class RequestAPI:
    def __init__(self, ip: str, port: int, address: str,
                 params: dict, mode: HTTP_TYPE,
                 secure: bool, token: str = None):
        self.ip = ip
        self.port = port
        self.params = params
        self.token = token
        self.mode = mode
        self.headers = {"Authorization": "Token " + token, "Content-Type": "application/json"} if token else None
        if secure:
            init = "https://"
        else:
            init = "http://"
        url = init + ip + ":" + str(port) + "/" + address
        try:
            if mode == HTTP_TYPE.GET:
                self.requests = requests.get(url, headers=self.headers, json=self.params)
            elif mode == HTTP_TYPE.POST:
                self.requests = requests.post(url, headers=self.headers, json=self.params)
            self.status_code = self.requests.status_code
            self.requests.raise_for_status()
        except requests.exceptions.HTTPError:
            print("HTTP ERROR {} -> {}".format(self.status_code, json.loads(self.requests.text)), file=sys.stderr)
        except (requests.exceptions.Timeout, requests.exceptions.TooManyRedirects, requests.exceptions.RequestException):
            self.status_code = 0
            print('CONNECTION ERROR. Try later.', file=sys.stderr)

    #     self.transfer_attribute()
    #
    # def transfer_attribute(self):
    #     list_attribute = [x for x in dir(self.requests) if "__" not in x]
    #     for attribute in list_attribute:
    #         setattr(self, attribute, getattr(self.requests, attribute))