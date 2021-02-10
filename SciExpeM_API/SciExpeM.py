import requests
from enum import Enum

class HTTP_TYPE(Enum):
    GET = 0
    POST = 1


class RequestAPI:
    def __init__(self, ip: str, port: int, address: str, params: dict, token: str, mode: HTTP_TYPE, secure: bool):
        self.ip = ip
        self.port = port
        self.params = params
        self.token = token
        self.mode = mode
        self.headers = {"Authorization": "Token " + token}
        if secure:
            init = "https://"
        else:
            init = "http://"
        url = init + ip + ":" + str(port) + "/" + address

        if mode == HTTP_TYPE.GET:
            self.requests = requests.get(url, headers=self.headers, params=self.params)
        elif mode == HTTP_TYPE.POST:
            self.requests = requests.post(url, headers=self.headers, data=self.params)

        self.transfer_attribute()

    def transfer_attribute(self):
        list_attribute = [x for x in dir(self.requests) if "__" not in x]
        for attribute in list_attribute:
            setattr(self, attribute, getattr(self.requests, attribute))

class SciExpeM:

    def __init__(self, ip, port, token, secure):
        self.ip = ip
        self.port = port
        self.token = token
        self.secure = secure

        self.Experiment = {}
        self.ChemModel = {}
        self.CommonProperty = {}
        self.CurveMatchingResult = {}
        self.DataColumn = {}
        self.Execution = {}
        self.ExecutionColumn = {}
        self.FilePaper = {}
        self.InitialSpecie = {}

    def filter(self, model_name, *args, **kwargs):

        params = {'model': 'Experiment', 'query': 'cerca'}

        address = 'ExperimentManager/API/filterDataBase'

        request = RequestAPI(ip=self.ip,
                             port=self.port,
                             address=address,
                             token=self.token,
                             mode=HTTP_TYPE.POST,
                             secure=self.secure,
                             params=params)

        print(request.requests.status_code, request.requests.text)


a = SciExpeM(ip='127.0.0.1',
              port=8080,
              secure=False,
              token='f8fa855a5ff8ac3653528a989afdb6ea1d5096eb')



a.filter(12)